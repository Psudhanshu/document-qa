import streamlit as st
page1 = st.Page("lab1.py", title="Lab1")
page2 = st.Page("lab2.py", title="Lab2")

pg = st.navigation([page1,page2])
st.set_page_config(page_title="all Labs")
pg.run()