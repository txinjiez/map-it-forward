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
st.sidebar.info(f'If you find a bug, please report it [here.](https://github.com/orgs/ELROSTEM/discussions/1)')

# Logo
logo = Image.open('image/logo.jpg')
st.image(logo, width=300)

st.title('Map It Forward')
st.markdown("## Show where you want community imporvemnts!")

if st.checkbox("Check my location"):
    loc = stjs.get_geolocation()
    st.write(f"Your coordinates are {loc}")

# center on Liberty Bell, add marker
m = folium.Map(location=[40.730610, -73.935242], zoom_start=12)
folium.Marker(
    [40.730610, -73.935242], popup="Location", tooltip="Location"
).add_to(m)

st_folium(m, width=725, returned_objects=[])

df = pd.read_csv("database/submissions.csv")
# Create a form to submit a submission
with st.form("Add submission", clear_on_submit=True):
    name = st.text_input("Name")
    description = st.text_area("Description")
    submit_button = st.form_submit_button("Submit")
if submit_button:

    df.loc[len(df)] = [date.today().strftime("%m/%d/%Y"), name, description]
    df.to_csv("database/submissions.csv", index=False)
    
    st.success("Submission submitted!")
    sleep(1)
    st.experimental_rerun()
        