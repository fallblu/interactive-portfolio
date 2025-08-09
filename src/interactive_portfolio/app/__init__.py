"""
interactive_portfolio.app
Conventions for Streamlit pages:

- Each page module (e.g., Home.py, Projects.py) should define:
    PAGE_TITLE: str      # optional, for display
    PAGE_ICON: str       # optional, emoji or icon text
    render() -> None     # required: writes to the Streamlit UI

These conventions make it easy to list or auto-discover pages later.
"""

from typing import Protocol


class RenderFn(Protocol):
    def __call__(self) -> None: ...


__all__ = ["RenderFn"]
