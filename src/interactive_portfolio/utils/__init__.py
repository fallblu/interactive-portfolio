from __future__ import annotations

import logging
from typing import Final

"""
Shared utilities for the Streamlit app (formatting, links, small helpers).

Guidelines:
- Keep this file lightweight; avoid importing heavy libs or submodules here.
- Put helpers in focused modules (e.g., formatting.py, io.py) and import them
  explicitly where needed instead of re-exporting from this package.
"""

log: Final[logging.Logger] = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ["log"]
