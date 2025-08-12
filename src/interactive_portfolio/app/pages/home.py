from __future__ import annotations

import os

import streamlit as st

# Prefer getting version from the installed package, but fall back gracefully
try:
    from interactive_portfolio import __version__ as VERSION  # works when package is importable
except Exception:
    try:
        from importlib.metadata import version

        VERSION = version("interactive_portfolio")
    except Exception:
        VERSION = "dev"


def render_home() -> None:
    st.title("Interactive Portfolio")
    st.caption(f"Version {VERSION}")

    # Keep it simple until you actually need multiple tabs
    with st.container():
        # Example: quick links, status, or empty state
        st.write("Welcome! Select a page from the navigation to get started.")

        # Optional: small dev-only banner (toggle with IP_DEBUG=1)
        if os.getenv("IP_DEBUG") == "1":
            st.info("Development mode is ON (IP_DEBUG=1).")

        # Optional: a quick session reset helper
        # if st.button("Reset session"):
        #     st.session_state.clear()
        #     st.rerun()


if __name__ == "__main__":
    render_home()
