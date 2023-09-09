import streamlit as st

st.set_page_config(
     page_title="Map It Foward",
     page_icon="📍",
     initial_sidebar_state="expanded",
     menu_items={
         
          'About': "Participatory community mapping"
     }
)

with open('./database/about.txt', 'r') as f:
    about = f.read()
    st.markdown(about)
     # Logo
logo = Image.open('image/miflogo.PNG')
st.image(logo, width=300)

st.title('Map It Forward')
st.markdown("participatory community mapping")
