import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen 
import json
from copy import deepcopy

import plotly.io as pio


st.title("Swiss Renewable Energy Data Exploration")
st.header("A comparison of cantons and energy sources")

url = "https://open-power-system-data.org"
st.write("data source:", url)


@st.cache_data
def load_data(path):
     df = pd.read_csv(path)
     return df
df_ch = load_data(path = "data/renewable_power_plants_CH.csv")
df_ch = deepcopy(df_ch) #for security

if st.checkbox("Show DataFrame"):
     st.subheader("This is my dataset:")
     st.dataframe(data=df_ch)

df_ch["date"] = pd.to_datetime(df_ch["commissioning_date"])
df_ch_sources = df_ch.groupby(["energy_source_level_2", "date"])["production"].sum().reset_index()
df_ch_sources.rename(columns={"energy_source_level_2": "Source"}, inplace=True)
renewable_sources = df_ch["energy_source_level_2"].unique()

p_fig = px.histogram(df_ch_sources, 
                   x="date", 
                   y="production", 
                   color="Source",  # Group by source
                   barmode="stack"  # "group" for side-by-side bars
)
p_fig.update_layout(
    plot_bgcolor="white",
    xaxis_title="Commissioning Date",
    yaxis=dict(title="Production Capacity", title_font=dict(size=16)),
    hovermode="x unified",
    title=dict(text="New Renewables Commissioned in Switzerland", font=dict(size=24))
)
p_fig.update_traces(hovertemplate="<b>Date:</b> %{x}<br>" +
                                "<b>Production:</b> %{y} MW<br>")
st.plotly_chart(p_fig)

import json

# Load GeoJSON file
with open("data/georef-switzerland-kanton.geojson") as f:
    cantons = json.load(f)

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais', 
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich', 
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève', 
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz', 
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

df_ch['canton_name'] = df_ch['canton'].map(cantons_dict)

df_ch_grouped = df_ch.groupby(["canton_name"])["production"].sum().reset_index()

m_fig = px.choropleth_map(df_ch_grouped, geojson=cantons, locations='canton_name', color='production', featureidkey="properties.kan_name",
                           color_continuous_scale="Viridis",
                           range_color=(0, 500000),
                           map_style="carto-positron",
                           zoom=7, center = {"lat": 46.8182, "lon": 8.2275},
                           opacity=0.5,
                           labels={'production':'Renewable Energy Production', 'canton_name': "Canton"}
                          )
m_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

df_ch_capacity = df_ch.groupby(["canton_name"])["electrical_capacity"].sum().reset_index()

m_fig2 = px.choropleth_map(df_ch_capacity, geojson=cantons, locations='canton_name', color='electrical_capacity', featureidkey="properties.kan_name",
                           color_continuous_scale="Viridis",
                           range_color=(0, 200),
                           map_style="carto-positron",
                           zoom=7, center = {"lat": 46.8182, "lon": 8.2275},
                           opacity=0.5,
                           labels={'production':'Renewable Energy Electrical Capacity', 'canton_name': "Canton"}
                          )
m_fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



left_column, right_column = st.columns(2)
plot_types = ["Production", "Electrical Capacity"]
plot_type = left_column.selectbox("Choose which plot", plot_types)

if plot_type == "Production":
    st.plotly_chart(m_fig)
else:
    st.plotly_chart(m_fig2)

