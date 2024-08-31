import os
import glob
import altair as alt
import pandas as pd
import geopandas as gpd
import pandas as pd
import json
from pyogrio import read_dataframe
import streamlit as st
from streamlit_folium import folium_static
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
#from modules.nav import Navbar
import leafmap.foliumap as leafmap
from datetime import datetime


# 4. Algal bloom detection
# ------------------------

def show_s2_ts(year):
    st.image(f'data/images/algaes/s2_ts_{year}.png', caption='Sentinel-2 time series')

    # graphics
    # cloud 2023
    cloud_df = read_dataframe(f'data/dataframes/cloud_stats_{year}_df.csv')
    cloud_df['date'] = pd.to_datetime(cloud_df['date'])
    cloud_df['perc_cloud'] = cloud_df['perc_cloud'].astype(float)
    cloud_df['perc_cloud_norm'] = cloud_df['perc_cloud_norm'].astype(float)

    # let the user select cloud percentage
    selected_perc = st.slider('Select a percentage of clouds', min_value=0, max_value=100, value=100)
    cloud23_df_filtered = cloud_df[cloud_df['perc_cloud'] <= selected_perc]
    num_points = len(cloud23_df_filtered)

    # set colors
    colors = ['g' if val <= selected_perc else 'gray' for val in cloud_df['perc_cloud']]
    st.write(f'Number of images available : **{num_points}**')

    # plot
    fig, ax = plt.subplots()
    ax.scatter(cloud_df['date'], cloud_df['perc_cloud'], color=colors)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    ax.set_xlabel('Date')
    ax.set_ylabel('Cloud / cloud shadow cover (%)')
    ax.set_title(f'Cloud / cloud shadow cover < {selected_perc}%')
    ax.grid(True)
    g = plt.Line2D([0], [0], marker='o', color='w', label=f'< {selected_perc}%', markerfacecolor='g',
                   markersize=10)
    G = plt.Line2D([0], [0], marker='o', color='w', label=f'≥ {selected_perc}%', markerfacecolor='gray',
                   markersize=10)
    ax.legend(handles=[g, G], loc='lower left')
    st.pyplot(fig)


st.title('Algal bloom detection')
st.subheader('Description')
st.write('The intensive farming context of the region of Saint-Brieuc lead to nutrient runoff, contributing to the '
         'formation of algal blooms in the bay which is the outlet for all the contaminated waters. These blooms, '
         'characterized by the rapid proliferation of algae, pose significant threats to biodiversity by depleting '
         'oxygen levels in the water and disrupting aquatic ecosystems. The rotting of the algaes that stagnate also '
         'leads to significant air pollution with hydrogen sulphide, which threaten wildlife and passer-by. ')
st.image('data/images/algaes/algaes_detection.png', caption='Algaes proliferation detected over Saint-Brieuc bay’s beaches '
                                                     'with S2 satellite (composite S2 image and ground photos) ')

# image gallery
algaes_l = ['data/images/algaes/algaes1.png',
            'data/images/algaes/algaes2.png',
            'data/images/algaes/algaes3.png',
            'data/images/algaes/algaes4.png']

col1, col2, col3, col4 = st.columns(4)
for i, im in enumerate(algaes_l):
    with eval(f'col{i % 3 + 1}'):
        st.image(im, use_column_width='auto')



# init study map
study_map = folium.Map(location=[48.589098, -2.432541],
                       zoom_start=9,
                       attr='© OpenStreetMap contributors')

# map catchment basin
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

# map roi
roi = read_dataframe('data/geometries/roi.fgb').to_json()
#folium.Map(roi).add_to(study_map)
folium.GeoJson(roi).add_to(study_map)

sm = st_folium(study_map, width=900, height=600)

# s2 for algal bloom detection
st.subheader('Copernicus data for algal blooms monitoring')
st.write('Copernicus Sentinel-2 imagery can be used to detect algal blooms. By analysing spectral signatures, it is '
         'possible to identify areas experiencing abnormal levels of chlorophyll, indicative of algal presence. '
         'However, one major challenge in utilizing Sentinel-2 imagery for algal bloom detection is the intermittent '
         'availability of data due to cloud cover, making some images unusable for analysis. This limitation '
         'impedes timely monitoring and early detection of algal blooms, particularly during critical stages of their '
         'development. Furthermore, detecting algal blooms in coastal areas, such as the bay, is more effective during '
         'low tide when the water is shallow and the algae are more visible. This underscores the importance '
         'of having high-cadence data, potentially daily, to enable early detection and timely intervention. ')
# gif
#st.image('data/gif/rgb_png_2023.gif', caption='RGB Sentinel-2 time series from january to december 2023.')

# plot s2 time series
selected_year = st.selectbox("Select a year : ", ['2023'])
st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">Add 2022</p>',
            unsafe_allow_html=True)
show_s2_ts(selected_year)

st.write('The analysis of the time series from 2023 highlights several critical insights regarding the '
         'limitations of Copernicus Sentinel-2 capabilities in monitoring environmental phenomena such as algal '
         'blooms. The graphic above represents the percentage of clouds and cloud shadows '
         'present in each image throughout the time series. It shows the lack of clear data despite a 5 days revisit '
         'time. As the figure shows, 2023 has been particularly challenging due to the high prevalence of cloudy '
         'conditions. In fact, it wasn’t until mid-July that the first image with less than 20% cloud and cloud shadow '
         'cover was available. This delay severely impacts the ability to monitor early-stage algal blooms. Moreover, '
         'on the few clear images that are available, some show high tide conditions, further complicating the '
         'detection process. ')