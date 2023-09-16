import pandas as pd
import streamlit as st

import folium
from streamlit_folium import st_folium
from streamlit_echarts import JsCode, st_echarts

# Chart helper functions
# Renders a pie chart (modified from https://echarts.streamlit.app/)
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

st.title("🚧 Submission Data 🏗️")

# Load data
submissions = pd.read_csv("database/submissions.csv")

# Map Location
m = folium.Map(location=[40.712772, -74.006058], zoom_start=12)

for index,row in submissions.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]], tooltip=row["category"],
        popup=(row["recommendation"] + '<br>Severity=' + str(row["severity"])), 
    ).add_to(m)

st_folium(m, width=725, returned_objects=[])

# Dataframe
st.dataframe(submissions)

# Gets a dictionary of all of the items in a column and their counts
def get_project_dict(column, isCompletedOption):
    columnSeries = submissions.loc[0:, column]
    columnDict = dict()
    for i in range(len(columnSeries.tolist())):
        elem = columnSeries.tolist()[i]
        if column == "address": 
            elem = columnSeries.tolist()[i].split(", ")[-5]
        # Only add to dictionary if the project is what the user wants to see
        if isCompletedOption == 'All projects':
            columnDict[elem] = columnDict.get(elem, 0) + 1
        elif isCompletedOption == 'Incomplete projects only':
            if submissions.loc[i, "status"] == 'Incomplete':
                columnDict[elem] = columnDict.get(elem, 0) + 1
        elif isCompletedOption == 'Completed projects only':
            if submissions.loc[i, "status"] == 'Completed':
                columnDict[elem] = columnDict.get(elem, 0) + 1
    return columnDict

# Pie charts
isCompletedOption = st.selectbox(
    'What projects do you want to see?',
    ('All projects', 'Incomplete projects only', 'Completed projects only'))

render_pie("Counties", get_project_dict("address", isCompletedOption))
render_pie("Severity", get_project_dict("severity", isCompletedOption))


