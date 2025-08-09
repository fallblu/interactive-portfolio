"""
interactive_portfolio
- Exposes __version__ for display and diagnostics
- Provides a package-level logger `log` (no global logging config)
- (Optional) re-exports a few settings for convenience
"""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

# Package version (fallback when not installed in editable mode)
try:
    __version__ = version("interactive-portfolio")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Library logging best practice: add a NullHandler so importing doesn't configure logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# Optional: convenience re-exports. Keep this cheap and resilient.
try:
    from .settings import ASSETS_DIR, STUDY_DIR  # noqa: F401
except Exception:
    # Don't crash imports during partial setups or tooling runs
    pass

__all__ = ["__version__", "log", "ASSETS_DIR", "STUDY_DIR"]
