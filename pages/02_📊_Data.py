import pandas as pd
import streamlit as st


# Page Configuration
st.set_page_config(
     page_title="Map It Forward",
     page_icon="📍",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Show where you want community imporvemnts!"
     }
)

st.title("🚧     SITE UNDER CONSTRUCTION       🏗️")


# Load data
submissions = pd.read_csv("database/submissions.csv")

st.table(submissions)