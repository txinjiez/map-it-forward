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
from geopy.geocoders import Nominatim

import folium
from streamlit_folium import st_folium
from PIL import Image

def get_pos(lat, lng):
    return lat, lng

st.set_page_config(
     page_title="Map It Forward",
     page_icon="📍",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "Show where you want community improvements!"
     }
)

#Bug report system
st.sidebar.info(f'If you find a bug, please report it [here.](https://github.com/Rhyzhang/map-it-forward/issues)')

# Logo
logo = Image.open('image/logonm.PNG')
st.image(logonm)

st.title('Map It Forward')
st.markdown("## a participatory community mapping tool")
st.markdown("pin where you want community improvements!")

# Load data
submissions = pd.read_csv("database/submissions.csv")

# Select Postion Map
with st.expander("Select Postion on Map"):
    if 'pos' not in st.session_state:
        st.session_state.pos = None
    m = folium.Map(location=[40.712772, -74.006058], zoom_start=10, min_zoom=10, min_lat = 40.3, max_lat = 40.98, min_lon = -73.5, max_lon = -74.4, max_bounds = True)
    m.add_child(folium.LatLngPopup())
    map = st_folium(m, height=350, width=700)

    data = None
    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
    if data is not None:
        st.session_state.pos = data
        st.info("Your location is: " + str(st.session_state.pos))

# Initial Map
map_container = st.empty()
with map_container:
    m = folium.Map(location=[40.712772, -74.006058], zoom_start=10, min_zoom=10, min_lat = 40.3, max_lat = 40.98, min_lon = -73.5, max_lon = -74.4, max_bounds = True)
    for index,row in submissions.iterrows():
        folium.Marker(
            [row["lat"], row["lon"]], popup=row["recommendation"], tooltip=row["category"]
        ).add_to(m)
    st_folium(m, height=350, width=725, returned_objects=[])
# If user has selected a location, show it on the map
if st.session_state.pos is not None:
    lat, lon = st.session_state.pos
    with map_container:
        m = folium.Map(location=[40.712772, -74.006058], zoom_start=10, min_zoom=10, min_lat = 40.3, max_lat = 40.98, min_lon = -73.5, max_lon = -74.4, max_bounds = True)
        folium.Marker(
            [st.session_state.pos[0], st.session_state.pos[1]], popup="Location", tooltip="Your Current Location"
        ).add_to(m)
        st_folium(m, height=350, width=725, returned_objects=[])

# Auto get Location if User wants
loc = False
geolocator = Nominatim(user_agent="community-service")
if st.button("Check my location automatically", help="Need trouble shooting? Go to about page: ..."):
    loc = stjs.get_geolocation()
    sleep(1)
    st.info("The accuracy is: " + str(loc["coords"]["accuracy"]))
    lat = loc["coords"]["latitude"]
    lon = loc["coords"]["longitude"]

    with map_container:
        m = folium.Map(location=[lat, lon], zoom_start=12, min_zoom=10, min_lat = 40.3, max_lat = 40.98, min_lon = -73.5, max_lon = -74.4, max_bounds = True)
        folium.Marker(
            [lat, lon], popup="Location", tooltip="Your Current Location"
        ).add_to(m)
        map = st_folium(m, height=350, width=725, returned_objects=[])

# Get submissions
df = pd.read_csv("database/submissions.csv")
# Create a form to submit a submission
with st.form("Add submission", clear_on_submit=True):
    today_date = date.today().strftime("%m/%d/%Y")
    age = st.number_input("Age", min_value=0, max_value=100, value=0)
    category = st.multiselect("Category", ["Roads", "Parks", "Schools", "Housing", "Other"])
    
    if loc or st.session_state.pos is not None:
        # Automatically fill in the location and address
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%f", value=float(lat))
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%f", value=float(lon))
        location = geolocator.reverse(f"{lat}, {lon}")
        address = st.text_input("Address", value=location.address)
    else:
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%f", value=0.0)
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%f", value=0.0)
        address = st.text_input("Address")

    reccomendation = st.text_area("Reccomendation")
    severity = st.slider("Severity", min_value=0, max_value=10, value=0)
    description = st.text_area("Description")


    if st.form_submit_button("Submit"):
        # Check if all fields are filled out
        if age == 0.0 or category == [] or lat == 0.0 or lon == 0.0 or not address or not reccomendation or severity == 0 or not description:
            st.error("Please fill out all fields!")
        else:
            df.loc[len(df)] = [today_date, age, category, lat, lon, address, reccomendation, severity, description]
            df.to_csv("database/submissions.csv", index=False)
            
            st.success("Submission submitted!")
            sleep(1)
            st.experimental_rerun()







# def get_pos(lat, lng):
#     return lat, lng

# m = folium.Map(location=[40.712772, -74.006058], zoom_start=12)
# m.add_child(folium.LatLngPopup())

# map = st_folium(m, height=350, width=700)

# data = None
# if map.get("last_clicked"):
#     data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
    

# if data is not None:
#     folium.Marker(
#         [data[0], data[1]], popup="hi", tooltip="Your Current Location"
#     ).add_to(m)
#     st_folium(m, width=725, returned_objects=[])
#     st.write(data) # Writes to the app
#     print(data) # Writes to terminal

