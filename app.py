import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen 
import json
from copy import deepcopy

import plotly.io as pio
#pio.renderers.default = 'colab'   # try changing this in case your plots aren't shown

#df= pd.read_csv("data/raw/mpg.csv")


st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("data source", url)

#"This works too:", url

#st.table(data=df)

if st.checkbox("Show DataFrame"):
     st.subheader("This is my dataset:")
     st.dataframe(data=df)
    

#use if you have a lot of data
@st.cache_data
def load_data(path):
     df = pd.read_csv(path)
     return df
df_mpg = load_data(path = "data/raw/mpg.csv")
df_mpg = deepcopy(df_mpg) #for security
left_column, right_column = st.columns(2)
show_means = right_column.radio(
     label="Show Class Means", options =["Yes", "No"]
)
years = ["All"] + sorted(pd.unique(df_mpg["year"]))
year = left_column.selectbox("Choose a year", years, index = 0)

if year == "All":
     df_year = df_mpg
else:
     df_year = df_mpg[df_mpg["year"] == year]
class_means = df_mpg.groupby("class").mean(numeric_only=True)

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

#matplotlib
fig, ax = plt.subplots(figsize = (10,8))
if show_means == "Yes":
    ax.scatter(class_means["displ"], class_means["hwy"], color="red")
ax.scatter(df_year['displ'], df_year['hwy'], alpha = 0.7)
ax.set_title("Engine Size vs highway Fuel Mileage")
ax.set_label("Displacement (Liters)")
ax.set_ylabel("MPG")

#in ploty

p_fig = px.scatter(df_year, x="displ", y="hwy", opacity=0.5,
                   range_x=[1,8], range_y=[10,50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                    title= "Engine Size vs. Highway Fuel Mileage")
if show_means =="Yes":
     p_fig.add_trace(go.Scatter(x=class_means['displ'], y = class_means['hwy'],
                                 mode = "markers",
                                 marker = dict(color="red")))
     p_fig.update_layout(showlegend=False)
p_fig.update_layout(title_font_size=22)


if plot_type == "Matplotlib":
    st.pyplot(fig)
else:
    st.plotly_chart(p_fig)

#Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()

ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']

st.map(ds_geo)
