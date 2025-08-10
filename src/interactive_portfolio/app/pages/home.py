from __future__ import annotations

import streamlit as st

from interactive_portfolio import __version__

st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

st.title("Interactive Portfolio")
st.caption(f"Version {__version__}")

tabs = st.tabs(["Overview"])

with tabs[0]:
    pass
