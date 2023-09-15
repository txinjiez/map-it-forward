import pandas as pd
import streamlit as st

import folium
from streamlit_folium import st_folium
from streamlit_echarts import JsCode, st_echarts

# Chart helper functions
def render_pie(title, data):
    dataList = []
    minValue, maxValue = 0, 0
    for key in data:
        dataList.append({"value": data[key], "name": key})
        if data[key] < minValue: minValue = data[key]
        if data[key] > maxValue: maxValue = data[key]
    pie_options = {
        "backgroundColor": "#2c343c",
        "title": {
            "text": title,
            "left": "center",
            "top": 20,
            "textStyle": {"color": "#ccc"},
        },
        "tooltip": {"trigger": "item", "formatter": "{b} : {c} ({d}%)"},
        "visualMap": {
            "show": False,
            "min": minValue,
            "max": maxValue+1,
            "inRange": {"colorLightness": [0, 1]},
        },
        "series": [
            {
                "name": "Source of interview",
                "type": "pie",
                "radius": "55%",
                "center": ["50%", "50%"],
                "data": dataList,
                "roseType": "radius",
                "label": {"color": "rgba(255, 255, 255, 0.3)"},
                "labelLine": {
                    "lineStyle": {"color": "rgba(255, 255, 255, 0.3)"},
                    "smooth": 0.2,
                    "length": 10,
                    "length2": 20,
                },
                "itemStyle": {
                    "color": "#c23531",
                    "shadowBlur": 200,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                },
                "animationType": "scale",
                "animationEasing": "elasticOut",
            }
        ],
    }
    st_echarts(options=pie_options)

# Page configuration
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

# Pie chart of counties
address = submissions.loc[0:, "address"]
countyDict = dict()
for elem in address.tolist():
    county = elem.split(", ")[-5]
    countyDict[county] = countyDict.get(county, 0) + 1
render_pie("Counties", countyDict)

st.dataframe(submissions)

# Map Location
m = folium.Map(location=[40.712772, -74.006058], zoom_start=12)

for index,row in submissions.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]], popup=row["recommendation"], tooltip=row["category"]
    ).add_to(m)

st_folium(m, width=725, returned_objects=[])



