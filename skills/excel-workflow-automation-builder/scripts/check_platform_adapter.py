#!/usr/bin/env python3
"""Check a staged automation the way Motivs checks it on upload.

The platform imports automation.py and calls run_automation. It does not open the file
as a notebook, so a platform-rendered automation is a module with an optional maintainer
view, not a Marimo notebook. This script runs that same check locally, in a subprocess,
so an import-time failure is reported rather than inherited.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

BRIDGE = """
import importlib.util
import inspect
import sys
from pathlib import Path

notebook_path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("motivs_platform_check", notebook_path)
if spec is None or spec.loader is None:
    raise SystemExit(f"Could not import automation module: {notebook_path}")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
adapter = getattr(module, "run_automation", None)
if adapter is None or not callable(adapter):
    raise SystemExit("Missing callable run_automation(input_paths, output_dir, parameters).")
names = list(inspect.signature(adapter).parameters)
required = ["input_paths", "output_dir", "parameters"]
if names[: len(required)] != required:
    raise SystemExit(
        "run_automation must accept "
        f"({', '.join(required)}); this one accepts ({', '.join(names)})."
    )
print("platform adapter check passed")
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", help="Path to the staged automation.py")
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Seconds to allow for the import (default 120)",
    )
    arguments = parser.parse_args()

    notebook_path = Path(arguments.notebook).resolve()
    if not notebook_path.is_file():
        print(f"No automation source at {notebook_path}", file=sys.stderr)
        return 2

    try:
        completed = subprocess.run(
            [sys.executable, "-c", BRIDGE, str(notebook_path)],
            cwd=str(notebook_path.parent),
            text=True,
            capture_output=True,
            timeout=arguments.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(
            f"The automation did not finish importing within {arguments.timeout}s. "
            "Move work out of import time and into run_automation.",
            file=sys.stderr,
        )
        return 1

    output = (completed.stdout + completed.stderr).strip()
    print(output or "no output")
    return 0 if completed.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
