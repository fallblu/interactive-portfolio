from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Interactive Portfolio", page_icon="📈", layout="wide")

# Guard for older Streamlit versions
if not hasattr(st, "navigation") or not hasattr(st, "Page"):
    st.error("This Streamlit version lacks st.navigation/st.Page. Please upgrade Streamlit.")
    st.stop()

BASE_DIR = Path(__file__).resolve().parent  # .../src/interactive_portfolio/app
PAGES_DIR = BASE_DIR / "pages"  # .../src/interactive_portfolio/app/pages


def page(filename: str, title: str, icon: str):
    path = PAGES_DIR / filename
    if not path.exists():
        # Helpful message if the path is wrong
        st.exception(FileNotFoundError(f"Expected page at: {path}"))
        st.stop()
    return st.Page(str(path), title=title, icon=icon)


home_page = page("home.py", title="Home", icon="🏠")
ts_plotter_page = page("time_series_plotter.py", title="Time Series Plotter", icon="📈")

pages = [home_page, ts_plotter_page]

pg = st.navigation(pages)
pg.run()
