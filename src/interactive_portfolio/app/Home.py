# src/interactive_portfolio/app/Home.py
from __future__ import annotations

import streamlit as st

from interactive_portfolio import __version__
from interactive_portfolio.utils.projects import (
    discover_projects,
    has_projects,
    refresh_projects_cache,  # optional, for a "Refresh" button
)

st.set_page_config(page_title="Interactive Portfolio – Home", page_icon="🏠", layout="centered")

st.title("Interactive Portfolio")
st.caption(f"Version {__version__}")

tabs = st.tabs(["Overview", "Projects"])

# Discover once for metrics & the Projects tab
if has_projects():
    VALID_PROJECTS, SKIPPED_PROJECTS = discover_projects()
else:
    VALID_PROJECTS, SKIPPED_PROJECTS = [], []

with tabs[0]:
    # ... your overview content ...
    pass
    # (rest unchanged)

with tabs[1]:
    st.subheader("Projects")

    if not has_projects():
        st.info(
            "No project package found. Create `src/portfolio_projects/__init__.py` and add a project."
        )
        st.stop()

    if st.button("Refresh project list"):
        refresh_projects_cache()
        st.rerun()

    if not VALID_PROJECTS:
        st.info("No valid projects yet. Add a folder under `src/portfolio_projects/`.")
    else:
        labels = []
        mapping = {}
        for entry in VALID_PROJECTS:
            info = entry.info
            title = getattr(info, "title", None) or entry.package.rsplit(".", 1)[-1]
            labels.append(title)
            mapping[title] = entry

        choice = st.selectbox("Choose a project", labels)
        selected = mapping[choice]

        summary = getattr(selected.info, "summary", "No summary provided.")
        st.write(summary)

        tech = getattr(selected.info, "tech", None)
        if isinstance(tech, list | tuple) and tech:
            st.caption("Tech: " + ", ".join(map(str, tech)))

        st.divider()
        st.write("### Demo")
        selected.render()

    if SKIPPED_PROJECTS:
        with st.expander("Skipped projects"):
            for e in SKIPPED_PROJECTS:
                st.code(f"{e.package}: {e.error}")
