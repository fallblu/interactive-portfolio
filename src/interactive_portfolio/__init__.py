from __future__ import annotations

import logging
import os
from importlib.metadata import PackageNotFoundError, version


def _resolve_version() -> str:
    # Try common distribution names, then an env override, then a safe default
    for dist in ("interactive-portfolio", "interactive_portfolio"):
        try:
            return version(dist)
        except PackageNotFoundError:
            pass
    return os.getenv("APP_VERSION", "dev")


__version__ = _resolve_version()

# Library logging best practice: do not configure logging on import
log = logging.getLogger("interactive_portfolio")
log.addHandler(logging.NullHandler())

# Keep the public surface minimal; avoid re-exporting settings to prevent side effects
__all__ = ["__version__", "log"]
