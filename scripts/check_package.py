"""Check the source package without executing its automation helpers."""

import json
from pathlib import Path
import re
import struct
import subprocess
import sys


def check(root):
    repository = root.resolve()
    root = repository / 'plugins/motivs'
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z",
         "--", "plugins/motivs"],
        cwd=repository, check=True, capture_output=True,
    )
    names = sorted({str(Path(name).relative_to('plugins/motivs'))
                    for name in result.stdout.decode().split("\0") if name})
    require(bool(names), "installable plugin folder is empty")
    require(not (repository / '.claude-plugin/plugin.json').exists(),
            "root must be a marketplace, not a second installable plugin")
    require(not any((root / name).exists() for name in (
        'scripts', '.github', 'PUBLISHING.md', 'development',
    )), "maintainer tooling must stay outside the installed plugin")
    require(len(names) <= 512, "source package exceeds 512 files")
    seen = set()
    total_size = 0
    reserved = {"con", "prn", "aux", "nul"}
    reserved.update(f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10))
    images = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico'}
    text_types = {'.md', '.txt', '.json', '.yml', '.yaml'}
    package_configs = {
        'package.json', 'package-lock.json', 'npm-shrinkwrap.json',
        'pnpm-workspace.yaml', 'pnpm-lock.yaml', 'yarn.lock', 'bun.lock',
        'bun.lockb', 'uv.toml', 'uv.lock', 'pyproject.toml', 'requirements.txt',
        '.npmrc', '.yarnrc', '.yarnrc.yml',
    }
    for name in names:
        path = root / name
        suffix = path.suffix.lower()
        folded = name.casefold()
        require(folded not in seen, f"case-insensitive path collision: {name}")
        seen.add(folded)
        require(not path.is_symlink(), f"symlink is not distributable: {name}")
        require(path.is_file(), f"missing or non-regular file: {name}")
        require(path.resolve().is_relative_to(root), f"path escapes package: {name}")
        require(not any(part.startswith('.env') or part in {
            '.DS_Store', '__MACOSX', 'node_modules', '__pycache__', '.venv',
        } for part in path.relative_to(root).parts), f"unwanted package file: {name}")
        require(not any(part.split('.')[0].casefold() in reserved
                        for part in Path(name).parts), f"reserved path: {name}")
        require(suffix in images | text_types
                or name in {'LICENSE', '.gitignore'}, f"unexpected package file: {name}")
        require(path.name.lower() not in package_configs, f"package-manager configuration: {name}")
        if not path.is_file() or path.is_symlink():
            continue
        require(not path.stat().st_mode & 0o111, f"executable file mode: {name}")
        size = path.stat().st_size
        total_size += size
        require(size < (5 * 1024 * 1024 if suffix in images else 256 * 1024),
                f"file exceeds preflight size limit: {name}")
        raw = path.read_bytes()
        require(not raw.startswith(b'#!'), f"shebang in package file: {name}")
        if suffix in images:
            signatures = {
                '.png': raw.startswith(b'\x89PNG\r\n\x1a\n'),
                '.jpg': raw.startswith(b'\xff\xd8\xff') and raw.endswith(b'\xff\xd9'),
                '.jpeg': raw.startswith(b'\xff\xd8\xff') and raw.endswith(b'\xff\xd9'),
                '.gif': raw.startswith((b'GIF87a', b'GIF89a')),
                '.webp': raw.startswith(b'RIFF') and raw[8:12] == b'WEBP',
                '.ico': raw.startswith(b'\x00\x00\x01\x00'),
            }
            require(signatures[suffix], f"image content does not match type: {name}")
        else:
            require(b'\0' not in raw, f"NUL bytes in text: {name}")
            try:
                raw.decode('utf-8')
            except UnicodeDecodeError:
                errors.append(f"non-UTF-8 text: {name}")
            require(not raw.startswith((b'\x7fELF', b'MZ', b'\xcf\xfa\xed\xfe')),
                    f"program signature in text file: {name}")
    require(total_size < 50 * 1024 * 1024, "source package exceeds 50 MiB")

    manifest = json.loads((root / '.claude-plugin/plugin.json').read_text())
    marketplace = json.loads((repository / '.claude-plugin/marketplace.json').read_text())
    mcp = json.loads((root / '.mcp.json').read_text())
    require(manifest['name'] == marketplace['name'] == 'motivs', "plugin identity changed")
    require(marketplace['plugins'] == [{'name': 'motivs', 'source': './plugins/motivs'}],
            "marketplace must point to the isolated plugin folder")
    require(manifest['displayName'] == 'Motivs', "product display name changed")
    require(manifest['author']['name'] == marketplace['owner']['name'] == 'MOTIVS OÜ',
            "publisher identity changed")
    require(re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), "invalid release version")
    require(manifest['skills'] == './skills/' and manifest['mcpServers'] == './.mcp.json',
            "unexpected component paths")
    require(mcp == {'mcpServers': {'motivs': {
        'type': 'http', 'url': 'https://mcp.motivs.ai/mcp',
    }}}, "MCP must contain only the production OAuth endpoint, no embedded credentials")
    require(not any(key in manifest for key in ('hooks', 'commands', 'agents', 'lspServers')),
            "new executable components require an explicit preflight review")
    for key in ('icon', 'skills', 'mcpServers'):
        path = root / manifest[key]
        require(path.exists() and path.resolve().is_relative_to(root), f"invalid {key} path")
    icon = (root / manifest['icon']).read_bytes()
    require(icon[:8] == b'\x89PNG\r\n\x1a\n' and icon[12:16] == b'IHDR', "icon must be PNG")
    if len(icon) >= 29:
        width, height, depth, color = struct.unpack('>IIBB', icon[16:26])
        require(width == height == 512 and depth == 8 and color in (2, 6),
                "expected 512px, 8-bit RGB/RGBA icon")
    else:
        errors.append("truncated icon")

    readme = (root / 'README.md').read_text()
    prose = re.sub(r'```.*?```', '', readme, flags=re.S)
    require(len(prose.split()) >= 40, "README needs at least 40 words outside code blocks")
    require(f"**{manifest['version']}**" in readme, "README release version is stale")
    require(f"**{manifest['version']}**" in (repository / 'README.md').read_text(),
            "repository README release version is stale")
    require(f"## {manifest['version']} - " in (root / 'CHANGELOG.md').read_text(),
            "release missing from changelog")
    require(bool((root / 'LICENSE').read_text().strip()), "license missing")
    require((root / 'LICENSE').read_bytes() == (repository / 'LICENSE').read_bytes(),
            "installed license differs from repository license")
    skill_dir = root / 'skills/excel-workflow-automation-builder'
    skill = (skill_dir / 'SKILL.md').read_text()
    require(skill.startswith('---\nname: excel-workflow-automation-builder\n'),
            "unexpected skill identity or frontmatter")
    for rel in set(re.findall(r'`((?:references|scripts)/[^`\s]+\.(?:md|py))`', skill)):
        require((skill_dir / rel).is_file(), f"missing skill dependency: {rel}")
    for path in skill_dir.rglob('*.md'):
        body = path.read_text()
        require(not any(name in body for name in (
            'scaffold_studio.py', 'check_platform_adapter.py', 'intelligence_kernels.py',
            'development/helpers',
        )), f"installed skill depends on an omitted helper: {path.relative_to(root)}")
    require('Do not download, reconstruct, or execute omitted helper scripts' in skill,
            "instruction-only execution boundary missing")
    collaboration = (skill_dir / 'references/collaboration-and-versions.md').read_text()
    for concept in ('access.can_manage', 'access.can_pin', 'workspace Owner',
                    'parent_version_id', 'contract_revision_id', 'pinned_version_id',
                    'protected inputs or outputs', '`stopped` is terminal'):
        require(concept in collaboration, f"missing collaboration guard: {concept}")
    require('Never include an account email' in collaboration, "profile privacy guard missing")
    require('only the current automation owner can change its working pin' not in collaboration,
            "working pin guidance excludes workspace Owner")
    if errors:
        raise ValueError('\n'.join(errors))
    print(f"package checks passed: {manifest['version']}, {len(names)} files, {total_size} bytes")


if __name__ == '__main__':
    try:
        check(Path(__file__).resolve().parents[1])
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"package checks failed: {error}", file=sys.stderr)
        sys.exit(1)
