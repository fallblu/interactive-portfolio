# tests/test_smoke.py
from __future__ import annotations

import ast
import importlib
import re
from pathlib import Path

PKG = "interactive_portfolio"


def test_package_imports():
    assert importlib.import_module(PKG) is not None


def test_version_resolves():
    mod = importlib.import_module(PKG)
    ver = getattr(mod, "__version__", "")
    # Accept "dev" during local runs, or a SemVer-ish string
    assert isinstance(ver, str) and ver
    assert ver == "dev" or re.match(r"^\d+\.\d+\.\d+(?:[.-][0-9A-Za-z]+)?$", ver)


def test_page_files_exist_and_parse():
    # Adjust if you rename/move pages
    root = Path(__file__).resolve().parents[1]  # repo root
    pages = [
        root / "src" / "interactive_portfolio" / "app" / "pages" / "home.py",
        root / "src" / "interactive_portfolio" / "app" / "pages" / "time_series_plotter.py",
    ]
    for p in pages:
        assert p.exists(), f"Missing page file: {p}"
        source = p.read_text(encoding="utf-8")
        # Parse to ensure syntax validity without executing Streamlit code
        ast.parse(source, filename=str(p))
