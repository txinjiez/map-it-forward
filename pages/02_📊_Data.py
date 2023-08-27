import pandas as pd
import streamlit as st

import folium
from streamlit_folium import st_folium

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



# Map Location
m = folium.Map(location=[40.712772, -74.006058], zoom_start=12)

for index,row in submissions.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]], popup=row["category"], tooltip=row["severity"]
    ).add_to(m)


st_folium(m, width=725, returned_objects=[])