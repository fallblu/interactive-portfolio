"""
Shared utilities for the Streamlit app (formatting, links, small helpers).
Put *lightweight* functions here and import within pages as needed.
"""

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ["log"]  # expand as you add helpers and want to re-export them
