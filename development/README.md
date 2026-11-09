# Maintainer helpers

These Python utilities are retained for development and are not part of the
installable directory package in `plugins/motivs`. They are not fetched or run by
the distributed skill. Do not copy them back into that package without reviewing
Anthropic's publisher/file policy and updating the package checks.

- `scaffold_studio.py`: generates an initial automation module and manifest.
- `check_platform_adapter.py`: imports reviewed automation code to check the
  backend adapter; running it executes that module in the chosen environment.
- `intelligence_kernels.py`: build-time calculation references requiring NumPy
  and pandas, not an importable dependency of hosted automation versions.

Use only reviewed code and synthetic data for development. Protected customer
examples stay in Motivs. The distributed skill authors its self-contained notebook
from the contract and uses Motivs MCP for isolated validation and feedback.
