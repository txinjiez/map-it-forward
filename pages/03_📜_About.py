import streamlit as st

st.set_page_config(
     page_title="ELRO Gameboard",
     page_icon="🎲",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "# Weekly games. Answer questions and compete against other grades"
     }
)

with open('./database/about.txt', 'r') as f:
    about = f.read()
    st.markdown(about)