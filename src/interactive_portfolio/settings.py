from __future__ import annotations

import os
from pathlib import Path
from typing import Final


def _find_project_root(start: Path) -> Path:
    """
    Discover the project root by walking upward until we hit an anchor file.
    Falls back to two levels up (your original behavior) if none are found.
    """
    for parent in (start,) + tuple(start.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    return start.parents[2]


_THIS_FILE = Path(__file__).resolve()
_DEFAULT_ROOT = _find_project_root(_THIS_FILE)

# Allow overrides in different environments (Cloud, Docker, etc.)
ROOT: Final[Path] = Path(os.getenv("IP_ROOT", str(_DEFAULT_ROOT)))
ASSETS_DIR: Final[Path] = Path(os.getenv("IP_ASSETS_DIR", str(ROOT / "assets")))


def require_dir(path: Path, name: str) -> Path:
    """Validate that a directory exists, with a helpful error if not."""
    if not path.exists():
        raise FileNotFoundError(
            f"{name} directory not found at {path}. "
            f"Set IP_{name.upper()}_DIR or IP_ROOT environment variable, or create the directory."
        )
    return path


# Validate at import time (comment out if you prefer lazy validation)
require_dir(ASSETS_DIR, "assets")


def asset_path(*parts: str | os.PathLike[str]) -> Path:
    """Build a path inside the assets directory."""
    return ASSETS_DIR.joinpath(*map(str, parts))
