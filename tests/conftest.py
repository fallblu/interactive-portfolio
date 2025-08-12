# tests/conftest.py
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch  # use directly at session scope


def _project_root() -> Path:
    # repo root: tests/ -> project/
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def _test_env(tmp_path_factory: pytest.TempPathFactory):
    """
    Session-wide test environment:
      - Add 'src/' to sys.path so the package imports without an editable install.
      - Provide a temp assets dir so settings.ASSETS_DIR validation passes.
      - Provide a fallback app version when the package isn't installed.
      - Silence Streamlit usage telemetry.
    """
    mp = MonkeyPatch()  # manual monkeypatch for session scope

    root = _project_root()
    src = root / "src"
    sys.path.insert(0, str(src))

    assets_dir = tmp_path_factory.mktemp("assets")
    mp.setenv("IP_ROOT", str(root))
    mp.setenv("IP_ASSETS_DIR", str(assets_dir))
    mp.setenv("APP_VERSION", os.getenv("APP_VERSION", "dev"))
    mp.setenv("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

    try:
        yield
    finally:
        mp.undo()  # clean up env/path changes
