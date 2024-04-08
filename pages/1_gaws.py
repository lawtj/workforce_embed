import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import Search, GroupedLayerControl
import pandas as pd
import geopandas as gpd
import branca.colormap as cm
from streamlit_extras.row import row 
from nav import insert_nav


st.set_page_config(layout="wide", page_title='Global Surgery and Anesthesia Workforce Maps', page_icon='🌍', initial_sidebar_state='collapsed')

import branca.colormap as cm


CENTER_START = [44.653024159812, 15.732421875000002]
ZOOM_START = 4

if "center" not in st.session_state:
    st.session_state["center"] = CENTER_START
if "zoom" not in st.session_state:
    st.session_state["zoom"] = 4


attr = 'Tiles Courtesy of Jawg Maps'
tiles = 'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png'

@st.cache_data
def read_gdf():
    gdf = gpd.read_file('data/geodf.geojson')
    gdf = gdf[['NAME', 'geometry', 'totalpap', 'totalnpap', 'physicians2015', 'totalpap_cap', 'physicians2015_cap', 'Country_x','population','nurses2015', 'nurses2015_cap', 'totalnpap_cap']]
    return gdf

gdf = pd.DataFrame(read_gdf())

def createmap(gdf):
    gdf['totalpap'] = gdf['totalpap'].fillna('No data')
    gdf['totalpap_cap'] = gdf['totalpap_cap'].fillna('No data')
    gdf['physicians2015_cap'] = gdf['physicians2015_cap'].fillna('No data')
    
    m = folium.Map(tiles=None, zoom_start=3, location=CENTER_START, world_copy_jump=False)
    step = cm.StepColormap(
    ["#d73027", "#fc8d59", '#fee090', '#ffffbf', '#e0f3f8', '#91bfdb', '#4575b4',], vmin=-1, vmax=25, index=[0, 1, 3, 5, 10, 15,20], caption="step"
)
    step.caption = 'PAP density per 100,000 population'
    
    tile_layer = folium.TileLayer(
        tiles=tiles,
        attr=attr,
        name='Jawg Light',
        overlay=False,
        control=False,

    ).add_to(m)
    def style_function(x):
        if x['properties']['totalpap_cap'] != 'No data':
            return {'fillColor': step(x['properties']['totalpap_cap']), 'color': 'black', 'weight': 1, 'fillOpacity': 0.7}
        else:
            return {'color': 'black', 'weight': 1, 'fillOpacity': 0.4}


    papgeo= folium.GeoJson(gdf, show=True,
                    # style_function=lambda x: {'color': 'black', 'fillColor': step(x['properties']['totalpap_cap']), 'weight': 1, 'fillOpacity': 0.7},
                    style_function=style_function,
                    tooltip=folium.GeoJsonTooltip(fields=['NAME', 'totalpap','totalpap_cap'], aliases=['Country: ', 'Total PAPs', 'Total PAP density: '], localize=True),
                    name='PAP Capacity',
                    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.5}, overlay=False
    ).add_to(m)

    m.add_child(step)

    statesearch = Search(
    layer=papgeo,
    geom_type="Polygon",
    placeholder="Search for a country",
    collapsed=False,
    search_label="NAME",
    weight=3,
).add_to(m)
          
    return m

def createmap2016(gdf):
    gdf['physicians2015_cap'] = gdf['physicians2015_cap'].fillna(-1)
    gdf['physicians2015'] = gdf['physicians2015'].fillna(-1)
    m = folium.Map(tiles=None, zoom_start=3, location=CENTER_START, world_copy_jump=False)
    
    tile_layer = folium.TileLayer(
        tiles=tiles,
        attr=attr,
        name='Jawg Light',
        overlay=False,
        control=False,

    ).add_to(m)

    step = cm.StepColormap(
    ["#7e757f", "#d73027", "#fc8d59", '#fee090', '#ffffbf', '#e0f3f8', '#91bfdb', '#4575b4',], vmin=-1, vmax=25, index=[-1, 0, 1, 3, 5, 10, 15,20], caption="step"
)
    step.caption = 'PAP density per 100,000 population'

    papgeo= folium.GeoJson(gdf, show=True,
                    style_function=lambda x: {'color': 'black', 'fillColor': step(x['properties']['physicians2015_cap']), 'weight': 1, 'fillOpacity': 0.7},
                    tooltip=folium.GeoJsonTooltip(fields=['NAME', 'physicians2015','physicians2015_cap'], aliases=['Country: ', 'Total PAPs (2015)', 'Total PAP density (2015): '], localize=True),
                    name='PAP Capacity (2015)',
                    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.5}, overlay=False
    ).add_to(m)

    m.add_child(step)

    statesearch = Search(
    layer=papgeo,
    geom_type="Polygon",
    placeholder="Search for a country",
    collapsed=False,
    search_label="NAME",
    weight=3,
    ).add_to(m)

    return m

def createnpapmap(gdf):
    min_value = gdf['totalnpap_cap'].min()
    max_value = gdf['totalnpap_cap'].max()
    linear = cm.linear.YlGn_09.scale(min_value, max_value)
    linear.caption = 'NPAP density per 100,000 population'
    gdf['totalnpap'] = gdf['totalnpap'].fillna('No data')
    gdf['totalnpap_cap'] = gdf['totalnpap_cap'].fillna('No data')
    gdf['nurses2015_cap'] = gdf['nurses2015_cap'].fillna('No data')
    
    m = folium.Map(tiles=None, zoom_start=3, location=CENTER_START, world_copy_jump=False)
    
    tile_layer = folium.TileLayer(
        tiles=tiles,
        attr=attr,
        name='Jawg Light',
        overlay=False,
        control=False,

    ).add_to(m)

    def style_function(x):
        if x['properties']['totalnpap_cap'] != 'No data':
            return {'fillColor': linear(x['properties']['totalnpap_cap']), 'color': 'black', 'weight': 1, 'fillOpacity': 0.7}
        else:
            return {'color': 'black', 'weight': 1, 'fillOpacity': 0.1}

    npapgeo= folium.GeoJson(gdf, show=True,
                    # style_function=lambda x: {'color': 'black', 'fillColor': linear(x['properties']['totalnpap_cap']), 'weight': 1, 'fillOpacity': 0.7},
                    style_function=style_function,
                    tooltip=folium.GeoJsonTooltip(fields=['NAME', 'totalnpap','totalnpap_cap'], aliases=['Country: ', 'Total NPAPs', 'Total NPAP density: '], localize=True),
                    name='NPAP Capacity',
                    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.5}, overlay=False
    ).add_to(m)

    statesearch = Search(
    layer=npapgeo,
    geom_type="Polygon",
    placeholder="Search for a country",
    collapsed=False,
    search_label="NAME",
    weight=3,
    ).add_to(m)

    m.add_child(linear)
    return m



if 'mapoption' not in st.session_state:
    st.session_state['mapoption'] = 'Physician Anesthesia Providers (PAP)'

def mapdescription(mapoption):
    if mapoption == 'Physician Anesthesia Providers (PAP)':
        return 'This map shows the number of Physician Anesthesia Providers (PAPs) per 100,000 population. Data is derived from the Global Anesthesia Workforce Survey [published](https://journals.lww.com/anesthesia-analgesia/fulltext/9900/the_global_anesthesia_workforce_survey__updates.788.aspx) in 2024. \n\n Law, Tyler J., Michael S. Lipnick, Wayne Morriss, Adrian W. Gelb,  et al. 2024. “The Global Anesthesia Workforce Survey: Updates and Trends in the Anesthesia Workforce.” Anesthesia & Analgesia, March, 10.1213/ANE.0000000000006836.'
    elif mapoption == 'PAP (2016)':
        return 'This map shows the number of Physician Anesthesia Providers (PAPs) per 100,000 population, taken from data [published](https://pubmed.ncbi.nlm.nih.gov/28753173/) in 2016 as part of the WFSA Global Anesthesia Workforce Survey. \n\n Kempthorne, Peter, Wayne W. Morriss, Jannicke Mellin-Olsen, and Julian Gore-Booth. 2017. “The WFSA Global Anesthesia Workforce Survey.” Anesthesia and Analgesia 125 (3): 981–90.'
    elif mapoption == 'Nonphysician Anesthesia Providers':
        return 'This map shows the number of Non-physician Anesthesia Providers (NPAP) per 100,000 population. It is also taken from the Global Anesthesia Workforce Survey [published](https://journals.lww.com/anesthesia-analgesia/fulltext/9900/the_global_anesthesia_workforce_survey__updates.788.aspx) in 2024. It includes both Nurse Anesthetists and other cadres of anesthesia provider who are not physicians. \n\n Law, Tyler J., Michael S. Lipnick, Wayne Morriss, Adrian W. Gelb,  et al. 2024. “The Global Anesthesia Workforce Survey: Updates and Trends in the Anesthesia Workforce.” Anesthesia & Analgesia, March, 10.1213/ANE.0000000000006836.'

################ Layout ################

map = createmap(read_gdf())
pap2016 = createmap2016(read_gdf())
npapmap = createnpapmap(read_gdf())


mapdict = {'Physician Anesthesia Providers (PAP)': map, 'PAP (2016)':pap2016, 'Nonphysician Anesthesia Providers': npapmap}


header = st.empty()

left, right = st.columns(2)
with left:
    slot_population = st.empty()
    slot_paps = st.empty()
    slot_papdensity = st.empty()
    slot_paps2015 = st.empty()
    slot_papdensity2015 = st.empty()
with right:
    slot_npaps = st.empty()
    slot_npapdensity = st.empty()
    slot_npaps2015 = st.empty()
    slot_npapdensity2015 = st.empty()


def writestats(message, col, slot):
    # if out['last_active_drawing']['properties'][col] is not None:
    if isinstance(out['last_active_drawing']['properties'][col], float) or isinstance(out['last_active_drawing']['properties'][col], int):
        slot.write(message+ str(round(out['last_active_drawing']['properties'][col],2)))
    else:
        slot.write(message+ 'Data not available')

# st_folium(m, width=1200, height=800, center=st.session_state['center'], returned_objects=[])
out = st_folium(mapdict[st.session_state['mapoption']], center=st.session_state['center'], returned_objects=['last_active_drawing','last_clicked','bounds'], use_container_width=True, height=750,)
st.subheader('Global Data Table')
st.dataframe(gdf[gdf['Country_x'].notnull()][['Country_x', 'totalpap', 'totalpap_cap', 'physicians2015','physicians2015_cap', 'totalnpap', 'totalnpap_cap', 'nurses2015', 'nurses2015_cap', 'population']],
        column_config={
            'Country_x': st.column_config.Column('Country'),
            'totalpap': st.column_config.Column('Total PAPs'),
            'totalpap_cap': st.column_config.Column('Total PAP density'),
            'physicians2015': st.column_config.Column('PAPs (2015)'),
            'physicians2015_cap': st.column_config.Column('PAP density (2015)'),
            'totalnpap': st.column_config.Column('Total NPAPs'),
            'totalnpap_cap': st.column_config.Column('Total NPAP density'),
            'nurses2015': st.column_config.Column('NPAPs (2015)'),
            'nurses2015_cap': st.column_config.Column('NPAP density (2015)'),
            'population': st.column_config.Column('Population')
        }, use_container_width=True)

st.selectbox('Select Map', ['Physician Anesthesia Providers (PAP)', 'PAP (2016)','Nonphysician Anesthesia Providers'], key='mapoption')
if out['last_active_drawing'] is None:
    header.write('Please select a country to view statistics.')
else:
    header.subheader(out['last_active_drawing']['properties']['NAME'])
    if isinstance(out['last_active_drawing']['properties']['population'], float) or isinstance(out['last_active_drawing']['properties']['population'], int):
        slot_population.write('**Population**: '+ str(round(out['last_active_drawing']['properties']['population']/10,1))+ ' million')
    else:
        slot_population.write('**Population**: '+ 'Data not available')
    writestats('**Total PAPs**: ', 'totalpap', slot_paps)
    writestats('**Total PAP density**: ', 'totalpap_cap', slot_papdensity)
    writestats('**PAP 2015**: ', 'physicians2015', slot_paps2015)
    writestats('**PAP density (2015)**: ', 'physicians2015_cap', slot_papdensity2015)
    writestats('**Total NPAPs**: ', 'totalnpap', slot_npaps)
    writestats('**Total NPAPs (2015)**: ', 'nurses2015', slot_npaps2015)
    writestats('**NPAP density**: ', 'totalnpap_cap', slot_npapdensity)
    writestats('**NPAP density (2015)**: ', 'nurses2015_cap', slot_npapdensity2015)
st.divider()
st.caption(mapdescription(st.session_state['mapoption']))



