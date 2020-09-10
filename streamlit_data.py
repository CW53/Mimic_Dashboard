import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from streamlit_folium import folium_static
import folium
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from datetime import date
from folium.plugins import MarkerCluster



# 9/9/20: All that is left to do is fix labels on pie charts, fix date range slider, add legend to map, display total # of incidents; hook up selection boxxes to change map, table, display total

st.beta_set_page_config(page_title="None",page_icon="None",layout="wide", initial_sidebar_state="auto")

#Title
st.title("SVU: Victim Based Crimes!")
df = pd.read_csv('https://data.baltimorecity.gov/resource/wsfq-mvij.csv')

#replace NaNs, create fresh dataframe
df = df.fillna(0)

# explanation for this project
st.text("This is a project where I attempted to mimic the PowerBI Dashboard called")
st.text("BPD Part 1 Victim Based Crime. I decided to use streamlit because")
st.text("it looked fun and it was new to me. Unfortunately, streamlit does not have layout grids")
st.text("yet and I wasn't able to mimic everything: see lack of display box highlighting")
st.text("total incidents and a two prong date range slider.")
st.text("Original dashboard can be found here: https://app.powerbigov.us/view?r=eyJrIjoiNTM0NTQwMjctZmIwOC00M2JkLTkzNzAtNmExM2U2MzU2NzRlIiwidCI6IjMxMmNiMTI2LWM2YWUtNGZjMi04MDBkLTMxOGU2NzljZTZjNyJ9")
st.text("In summation, it's not perfect, it still has areas that need improvement")
st.text("which will come as streamlit continues to grow and update.")
#hide raw data from view, click to unhide
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

## Layout: select hours slider, below that a map and below the map will be more stats via visuals or a layout of charts

#Add date frame to sidebar
add_slider = st.sidebar.slider("Choose a date range", value=date(2020, 9, 5), format="MM/DD/YYYY")


# In body of the page
st.subheader("Hours in the day for crime")
st.text("See how the data changes hour by hour")
hour_to_filter = st.slider('crimetime', 0, 23, 12)


### Create colors for each marker/condition
conditions = [
    (df['description'] == 'LARCENY'),
    (df['description'] == 'COMMON ASSAULT'),
    (df['description'] == 'BULGLARY'),
    (df['description'] == 'LARCENY FROM AUTO'),
    (df['description'] == 'AGGRAVATED ASSAULT'),
    (df['description'] == 'AUTO THEFT'),
    (df['description'] == 'ROBBERY - STREET'),
    (df['description'] == 'ROBBERY - COMMERCIAL'),
    (df['description'] == 'ROBBERY - RESIDENCE'),
    (df['description'] == 'ROBBERY - CARJACKING'),
    (df['description'] == 'SHOOTING'),
    (df['description'] == 'HOMICIDE'),
    (df['description'] == 'RAPE'),
    (df['description'] == 'ARSON')
    ]

# create a list of the values we want to assign for each condition
values = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'lightblue', 'lightgreen', 'gray']

# create a new column and use np.select to assign values to it using our lists as arguments
df['color_code'] = np.select(conditions, values)

m = folium.Map(location=[39.3248, -76.6024], zoom_start = 11)

for h in range(0,len(df)):
  folium.Marker([df.iloc[h]['latitude'], df.iloc[h]['longitude']], popup=df.iloc[h]['description'], tooltip=df.iloc[h]['neighborhood'], icon=folium.Icon(df.iloc[h]['color_code'])).add_to(m)

# Add legend for color code of crime type
st.write(pd.DataFrame({
    'Type': ['Larceny', 'Common Assault', 'Burglary', 'Larceny from Auto', 'Aggravated Assault', 'Auto Theft', 'Robbery - Street','Robbery - Commercial', 'Robbery - Residence', 'Robbery - Carjacking', 'Shooting', 'Homicide', 'Rape', 'Arson'],
    'Color Code': ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'lightblue', 'lightgreen', 'gray']
}))
folium_static(m)



# Split into days, months, years to match the table below the map I am mimicking
df['year'] = df['crimedate'].str.split('-').str[0]
df['month'] =df['crimedate'].str.split('-').str[-2]

# Table of breakdown based on zoom
map_table = df.filter(['crimecode', 'year', 'month', 'description', 'district', 'premise', 'weapon'])
st.dataframe(map_table)
# change format of month from 12 to December: Unsuccesful



## thanks for the tutorial: https://towardsdatascience.com/explore-any-data-with-a-custom-interactive-web-app-data-science-with-sports-410644ac742

# Pie chart of districts 
import plotly.express as px



Labels = ['NorthEast', 'SouthEast', 'Central', 'Southern', 'Northern', 'SouthWest', 'NorthWest', 'Eastern', 'Western', 'Unknown' ]
Data_points = [46413, 43838, 35849, 34925, 34275, 32327, 30717, 27116, 24865, 612]
st.subheader("Recorded Incidents by District")
fig = px.pie(values=Data_points, names=Labels,
             title='Recorded Incidents by District')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)


# Pie chart of crime type
Type = ['Larceny', 'Common Assault', 'Burglary', 'Larceny from Auto', 'Aggravated Assault', 'Auto Theft', 'Robbery - Street', 'Robbery - Commercial', 'Shooting', 'Robbery - Residence', 'Robbery - Carjacking', 'Homicide', 'Rape', 'Arson']
Ct_pt = [69326, 51932, 44282, 40752, 34440, 27250, 21805, 5470, 4215, 3259, 2754, 2073, 2048, 1331]
fig1 = px.pie(names=Type, values=Ct_pt, title='Total Incidents by Type')
fig1.update_traces(textposition='inside', textinfo='percent')
st.subheader("Total Incidents by Type")
st.plotly_chart(fig1)

# DONE # Selection boxxes based on 'District, Neighborhood, Weapon, description 
# # add sidebar choices. 

add_selectbox = st.sidebar.selectbox('Which district do you want to explore?', df['district'].unique())
add_selectbox = st.sidebar.selectbox('Which neighborhood do you want to learn more about?', df['neighborhood'].unique())
add_selectbox = st.sidebar.selectbox('What type of weapon was used?', df['weapon'].unique())
add_selectbox = st.sidebar.selectbox ('What type of crime was committed?', df['description'].unique())







## Make a version of this:https://app.powerbigov.us/view?r=eyJrIjoiNTM0NTQwMjctZmIwOC00M2JkLTkzNzAtNmExM2U2MzU2NzRlIiwidCI6IjMxMmNiMTI2LWM2YWUtNGZjMi04MDBkLTMxOGU2NzljZTZjNyJ9
## Streamlit reference: https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets


