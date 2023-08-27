####################################################################################################
# Author: Ryan Zhang
# Description: Main file for the project
# Date: 2023
####################################################################################################

from datetime import date
from time import sleep

import pandas as pd
import streamlit as st

import streamlit_js_eval as stjs

import folium
from streamlit_folium import st_folium
from PIL import Image

st.set_page_config(
     page_title="Map It Forward",
     page_icon="📍",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Show where you want community imporvemnts!"
     }
)

#Bug report system
st.sidebar.info(f'If you find a bug, please report it [here.](https://github.com/Rhyzhang/map-it-forward/issues)')

# Logo
logo = Image.open('image/logo.jpg')
st.image(logo, width=300)

st.title('Map It Forward')
st.markdown("## Show where you want community imporvemnts!")

# Get Location
loc = stjs.get_geolocation()
# st.write(f"Your coordinates are {loc}")
lat = loc["coords"]["latitude"]
lon = loc["coords"]["longitude"]

# Map Location
m = folium.Map(location=[lat, lon], zoom_start=12)
folium.Marker(
    [lat, lon], popup="Location", tooltip="Your Current Location"
).add_to(m)

st_folium(m, width=725, returned_objects=[])



# Get submissions
df = pd.read_csv("database/submissions.csv")
# Create a form to submit a submission
with st.form("Add submission", clear_on_submit=True):
    today_date = date.today().strftime("%m/%d/%Y")
    age = st.number_input("Age", min_value=0, max_value=100, value=0)
    category = st.multiselect("Category", ["Roads", "Parks", "Schools", "Housing", "Other"])
    address = st.text_input("Address")
    reccomendation = st.text_area("Reccomendation")
    severity = st.slider("Severity", min_value=0, max_value=10, value=0)
    description = st.text_area("Description")
    
    submit_button = st.form_submit_button("Submit")
if submit_button:

    df.loc[len(df)] = [today_date, age, category, lat, lon, address, reccomendation, severity, description]
    df.to_csv("database/submissions.csv", index=False)
    
    st.success("Submission submitted!")
    sleep(1)
    st.experimental_rerun()
        