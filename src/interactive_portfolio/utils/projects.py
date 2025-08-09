# src/interactive_portfolio/utils/projects.py
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache
from typing import NamedTuple

# Try to access the package search path for portfolio_projects
try:
    from portfolio_projects import __path__ as PROJECTS_PATH  # type: ignore[attr-defined]

    _HAS_PROJECTS = True
except Exception:
    PROJECTS_PATH = []  # type: ignore[assignment]
    _HAS_PROJECTS = False


import importlib
import pkgutil


class ProjectEntry(NamedTuple):
    package: str
    info: object
    render: Callable[[], None]


class SkippedEntry(NamedTuple):
    package: str
    error: Exception


def has_projects() -> bool:
    """Return True if the portfolio_projects package is importable."""
    return _HAS_PROJECTS


def _load_project(pkg: str) -> ProjectEntry:
    """
    Import meta.PROJECT and render.render() from a project package and return a ProjectEntry.
    Raises if the project is malformed.
    """
    meta = importlib.import_module(f"{pkg}.meta")
    render_mod = importlib.import_module(f"{pkg}.render")

    project_info = getattr(meta, "PROJECT", None)
    if project_info is None:
        raise AttributeError(f"{pkg}.meta must define a PROJECT object")

    render_fn = getattr(render_mod, "render", None)
    if not callable(render_fn):
        raise AttributeError(f"{pkg}.render must define a callable render()")

    return ProjectEntry(package=pkg, info=project_info, render=render_fn)


@lru_cache(maxsize=1)
def _discover_impl() -> tuple[tuple[ProjectEntry, ...], tuple[SkippedEntry, ...]]:
    """
    Cached discovery. Returns tuples of (valid, skipped).
    Using a cache avoids repeated imports on every Streamlit rerun.
    """
    if not _HAS_PROJECTS:
        return tuple(), tuple()

    valid: list[ProjectEntry] = []
    skipped: list[SkippedEntry] = []

    for mod in pkgutil.iter_modules(PROJECTS_PATH):
        pkg = f"portfolio_projects.{mod.name}"
        try:
            valid.append(_load_project(pkg))
        except Exception as e:
            skipped.append(SkippedEntry(package=pkg, error=e))
    return tuple(valid), tuple(skipped)


def discover_projects() -> tuple[list[ProjectEntry], list[SkippedEntry]]:
    """Public, list-based wrapper around the cached implementation."""
    v, s = _discover_impl()
    return list(v), list(s)


def refresh_projects_cache() -> None:
    """Clear the discovery cache. Call after adding/removing projects."""
    _discover_impl.cache_clear()  # type: ignore[attr-defined]
