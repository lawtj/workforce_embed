import streamlit as st
import pandas as pd
import numpy as np
import folium
import geopandas as gpd
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_extras.row import row 
from nav import insert_nav
import os
from dotenv import load_dotenv


st.set_page_config(page_title='CANESCA', page_icon=':earth_americas:', layout='wide', initial_sidebar_state='collapsed')

@st.cache_data
def read_country():
    country = gpd.read_file('data/can_country.geojson')
    return country

@st.cache_data
def read_states():
    states = gpd.read_file('data/can_states.geojson')
    return states

@st.cache_data
def read_csv():
    can = pd.read_csv('data/canesca.csv')
    return can

country = read_country()
states = read_states()
can = read_csv()

def canescamap():
    country = read_country()
    states = read_states()
    can = read_csv()

    m = folium.Map(location=[-10, 30], zoom_start=4.5)

    attr = 'Tiles Courtesy of Stadia'
    if os.path.exists(".streamlit/secrets.toml"):
        tiles = 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png?api_key='+st.secrets['stadiamaps']
    else:
        load_dotenv()
        tiles = 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png?api_key='+os.environ.get('stadiamaps')

    tile_layer = folium.TileLayer(
    tiles=tiles,
    attr=attr,
    name='Jawg Light',
    overlay=False,
    control=False,
    opacity=0.5

    ).add_to(m)

    countries = folium.GeoJson(country, name='countries',
                               style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 2, 'fillOpacity': 0.00, "dashArray": "5, 5"},
                               ).add_to(m)

    boundaries = folium.GeoJson(states, name='boundaries',
                                style_function=lambda x: {'fillColor': 'blue', 'color': 'purple', 'weight': 0, 'fillOpacity': 0.05,},
                                highlight_function=lambda x: {'weight': 1, 'fillOpacity': 0.1},
                                tooltip=folium.features.GeoJsonTooltip(fields=['admin','name'], aliases=['Country: ', 'District: '])
                                ).add_to(m)
        

    marker_cluster = MarkerCluster().add_to(m)

    for i in can['Longitude'].unique():
        if pd.notnull(i):
            folium.Marker(location=[can[can['Longitude'] == i]['Latitude'].values[0], i], 
                          tooltip=folium.Tooltip('<strong>'+str(can[can['Longitude']==i]['PRIMARY_ORGANISATION'].values[0])+'</strong>: <p>'+str(can[can['Longitude']==i]['Number_of_Anaesthesiologists'].values[0])+' anaesthesiologist(s)'),
                          ).add_to(marker_cluster)
    return m


#######################################################################################
st_folium(canescamap(),use_container_width=True, returned_objects=[])
