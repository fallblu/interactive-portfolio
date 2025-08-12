import streamlit as st

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
time_series_plotter_page = st.Page(
    "pages/time_series_plotter.py", title="Time Series Plotter", icon="📈"
)
test_page = st.Page("pages/test_page.py", title="Test Page", icon="❓")

pg = st.navigation([home_page, time_series_plotter_page, test_page])

pg.run()
