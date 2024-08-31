import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium

def map_bv():
    bv_geom = gpd.read_file('data/geometries/bv_sb-4326.fgb', engine='pyogrio')
    bv_geom['DateCreationOH'] = bv_geom['DateCreationOH'].astype('string')
    bv_geom = bv_geom.rename(columns={'ida': 'BV Ref'})
    bv_geom = bv_geom.to_json()
    bv_style = {'fillColor': '#C0C0C0', 'color': '#696969'}
    folium.GeoJson(bv_geom,
                   style_function=lambda x: bv_style,
                   popup=folium.GeoJsonPopup(
                       fields=['BV Ref', 'area_km2'],
                       aliases=['BV Ref : ', 'Area (km²) : ']
                   )).add_to(study_map)

# 1. context
st.title('Context')
st.write('This pilot demonstrator aims to demonstrate an integrated approach to monitoring biodiversity in the Bay of '
         'Saint-Brieuc, Brittany, France. The region faces significant environmental challenges due to intensive '
         'agriculture and livestock farming, which lead to excessive nitrogen emissions. These emissions negatively '
         'impact wetlands, Natura2000 protected areas, and coastal ecosystems, causing issues like large algae blooms. '
         'The project explores Earth Observation (EO) technology to monitor the effects of intensive farming on these '
         'ecosystems and assess the effectiveness of current Copernicus Land Monitoring Services (CLMS) and new EO '
         'sensors in supporting biodiversity and ecosystem protection.')

# 2. study area
st.title('Study area')
st.write('The study area includes NATURA 2000 sites, part of an EU ecological network aimed at conserving wildlife and '
         'natural habitats. It focuses on the Bay of Saint-Brieuc in northern Brittany, France, which was designated '
         'as a "Natural Reserve" in April 1998. The bay, located between the Bréhat archipelago and Cap Fréhel, covers '
         'about 800 km², including the Yffiniac and Morieux coves. The study area also encompasses the surrounding '
         'catchment areas, totaling 1,225 km².')

# map study area
# init study map
study_map = folium.Map(location=[48.589098, -2.432541],
                       zoom_start=9,
                       attr='© OpenStreetMap contributors')

# map catchment basin
bv_map = map_bv()

# N2K sites map
n2k_style = {'fillColor': '#87CEFA', 'color': '#1E90FF'}
n2k_geom = gpd.read_file('data/geometries/n2000_sb-4326.fgb').to_json()
folium.GeoJson(n2k_geom,
               style_function=lambda x:n2k_style,
               popup=folium.GeoJsonPopup(
                   fields=['SITECODE', 'SITENAME', 'SITETYPE'],
                   aliases=['Site code : ', 'Site name : ', 'Site Type : ']
               )).add_to(study_map)

#folium.LayerControl().add_to(study_map)
# display
sm = st_folium(study_map, width=900, height=600)

st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>',
            unsafe_allow_html=True)