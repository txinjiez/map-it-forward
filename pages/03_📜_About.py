import streamlit as st

with open('./database/about.txt', 'r') as f:
    about = f.read()
    st.markdown(about)

# Logo
logo = Image.open('image/miflogo.PNG')
st.image(logo, width=300)

st.title('Map It Forward')
st.markdown("participatory community mapping")
