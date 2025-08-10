import streamlit as st

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
test_page = st.Page("pages/test_page.py", title="Test Page", icon="❓")

pg = st.navigation([home_page, test_page])

pg.run()
