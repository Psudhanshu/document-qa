import streamlit as st
page1 = st.Page("lab1.py", title="Lab1")
# page2 = st.Page("HW2.py", title="Lab2")
page2 = st.Page("HW2.py",title="Lab2")
page3 = st.Page("Lab3.py",title="Lab3")
page4 = st.Page("Lab4.py",title="Lab4")
page5 = st.Page("Lab5.py", title="Lab5")
pg = st.navigation([page1,page2,page3,page4,page5])
st.set_page_config(page_title="all Labs")
pg.run()


