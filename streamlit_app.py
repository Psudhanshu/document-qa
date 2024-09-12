import streamlit as st
page1 = st.Page("lab1.py", title="Lab1")
# page2 = st.Page("HW2.py", title="Lab2")
page2 = st.Page("HW2.py",title="Lab2")
page3 = st.Page("Lab3.py",title="Lab3")
pg = st.navigation([page1,page2,page3])
st.set_page_config(page_title="all Labs")
pg.run()

