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

# side bar
st.sidebar.title('Third-party inventory')
page = st.sidebar.radio('Go to', ['Grassland and crops monitoring', 'Crop cover duration', 'Hedgerows monitoring'])

st.title('Third party data for intensive farming monitoring (IFM)')

# grassland & crop monitoring
if page == 'Grassland and crops monitoring':
    st.header('Grassland and crops monitoring')
    # description
    st.subheader('Description')
    st.write('Intensive agriculture is responsible for disrupting local ecosystems and coastal waters, and the '
             'environmental consequences of its practices are well-established. The bay of Saint-Brieuc has become a '
             'focal point for environmental concerns, primarily due to the proliferation of algal blooms. These blooms '
             'caused by intensive agricultural activities, pose serious threats to marine ecosystems, water quality '
             'and public health. There is a need to understand the relationship between intensive farming practices '
             'and their ecological repercussions. Knowledge of crop types will also make it possible to model the '
             'quantities of inputs (NPK fertilisers, pesticides, etc.) that are spread on the soil and therefore the '
             'excesses found in rivers and the sea. ')

    # legislation
    st.subheader('Legislation on grasslands')
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)

    # CLMS limitations
    st.subheader('Limitation of CLMS for IFM')
    st.write('To accurately capture agricultural changes, an annual update of flows is necessary to understand the '
             'agricultural context. Current Copernicus services do not allow for sufficiently precise tracking of '
             'agricultural territory evolution, despite its crucial impact on local ecosystems, due to several factors:')
    lst = ['Copernicus Services like CLC, CZ, RZ, UA are not designed to identify specific crops, they provide '
           'general information about land cover for agricultural surfaces. ',
           'The update frequency of Copernicus Land Monitoring Services is not high enough (an annual update would '
           'be necessary to map crop rotations). ',
           'Production methodologies may evolve, especially for grasslands and SWF, making it difficult to compare '
           'products and thus characterize change. ']
    s = ''
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)

    # kermap solution
    st.subheader('Third-party product')
    st.write('Kermap provides an annual crop classification based on analysis of time series of Copernicus Sentinel-2 '
             'imagery. It relies on a Deep Learning approach and utilizes LPIS (Land Parcel Identification System) '
             'data from across Europe for calibration and validation. It is generated according to two temporalities: ')
    lst = ['The "In-Season" detection aims to identify crops in place during the season and provide monthly mapping of '
           'crops almost in real-time. ',
           'The "Full-Season" detection aims to accurately identify the predominant crop throughout the cropping year. '
           'In France, this classification provides information on crops one year prior to the LPIS publication and '
           'is spatially comprehensive ']
    s = ''
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)

    # load agri stats
    agri_df = read_dataframe('data/dataframes/agri_stats.csv').astype({
        'Crop': 'string',
        '2017 (%)': 'float',
        '2018 (%)': 'float',
        '2019 (%)': 'float',
        '2021 (%)': 'float',
        '2022 (%)': 'float',
        '2023 (%)': 'float'
    })

    # crop identification map : user selector
    years = [2017, 2018, 2019, 2021, 2022, 2023]
    images = {
        2017: 'data/images/third_party/crop_id_2017.png',
        2018: 'data/images/third_party/crop_id_2018.png',
        2019: 'data/images/third_party/crop_id_2019.png',
        2021: 'data/images/third_party/crop_id_2021.png',
        2022: 'data/images/third_party/crop_id_2022.png',
        2023: 'data/images/third_party/crop_id_2023.png'
    }
    selected_year = st.selectbox("Crop identification map : select a year", years)
    st.image(images[selected_year], caption=f"Map for {selected_year}", use_column_width=True)
    agri_df = agri_df.sort_values(f'{selected_year} (%)', ascending=False)
    st.write(alt.Chart(agri_df).mark_bar().encode(
        x=alt.X('Crop', sort=None),
        y=f'{selected_year} (%)'
    ))

    st.write('The algorithm detects up to 22 types of crops over the european territory, including: wheat, corn, barley, '
             'rapeseed, soybeans, and in addition to major crops, it enables mapping of the distribution of pastures '
             'and fallow land and allows monitoring annual changes. ')
    st.write('The pixel-based crop classification allows to monitor internal crop and grasslands changes both at '
             'parcel and regional levels. The table below shows the evolution of crop rotation every year. The most '
             'common crops of the region are wheat and corn, grass and fallow lands represent a third of surfaces in '
             'the region of Saint-Brieuc. ')
    st.write('The methodology has been designed to be scalable. So the annual crop classification is available all '
             'over the European Union every year.')
    st.write('To access to the european crop identification, click here : https://agri.kermap.com/')

    # conclusion
    st.subheader('Conclusion')
    st.write('Monitoring grasslands and crop practices is crucial for understanding the ecological impacts of '
             'intensive farming activities. The current limitations of services like CLMS, which provide data at a '
             'cadence of 3-5 years and at a broad classification level, are insufficient for accurately assessing '
             'these impacts. To effectively quantify and understand the effects of intensive farming, there is a need '
             'to increase both the frequency (from multi-year to annual or in-season) and the precision (from broad '
             'categories to specific crops like wheat and corn) of monitoring efforts.')
    st.write('While Copernicus Sentinel-2 data provides the necessary foundation for such monitoring, the data alone'
             ' is not sufficient without enhanced services. The third-party (Kermap) crop detection product offers a '
             'scalable solution, enabling monitoring at the parcel level with the capability to extend this approach '
             'across Europe. This increased precision and frequency will significantly improve our ability to monitor '
             'and manage agricultural practices, leading to better-informed decisions for sustainable farming and '
             'ecological preservation. ')

# crop cover duration
if page == 'Crop cover duration':
    st.header('Crop cover duration')
    st.subheader('Description')
    st.write('European regulatory framework (Nitrates Directive) was adopted in 1991 with two objectives:  ')
    lst = ['To reduce water pollution from nitrates and eutrophication stemming from agricultural activities. ',
           'To prevent the spread of these pollutants']
    s = ''
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)

    st.write('In the context of the Saint-Brieuc region, it helps prevent the influx of pollutants into protected '
             'areas. ')
    st.write('The use of cover crops is essential for preserving and enhancing ecosystem services. These cover crops '
             'are plants grown between main crops and play a crucial role in soil protection, biodiversity '
             'preservation, and biogeochemical cycle regulation. They act as nitrate traps, capturing excess'
             ' nitrogen in the soil and thus reducing nitrate leaching into groundwater and watercourses. '
             'Within the framework of the Nitrates Directive, which aims to reduce nitrate pollution and prevent '
             'eutrophication. ')
    st.write('Quantifying the duration of crop cover is crucial for assessing the effectiveness of plots in reducing '
             'nitrate levels in soils and groundwater. The length of time a plot is covered by crops can have a '
             'significant impact on its ability to retain nitrates and prevent them from contaminating the '
             'environment. The longer the parcel is covered, the less it is exposed to erosion, and the more it '
             'contributes to environmental preservation. ')

    st.subheader('Cover duration with the Copernicus program’s data ')
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">Introduce S2 data in a dedicated section</p>', unsafe_allow_html=True)
    st.write('Optical data from the Sentinel-2 satellites of the Copernicus program can be used to calculate the crop '
             'cover duration. Freely available to the public, they carry a multispectral instrument (MSI) with 13 '
             'spectral bands, including bands specifically designed for vegetation monitoring. These bands are crucial '
             'for NDVI calculation. Sentinel-2 data also have high radiometric accuracy, essential for reliable NDVI '
             'calculations.')
    st.image('data/images/third_party/s2_bands_10m.png', caption='Sentinel-2 10 m spatial resolution bands: B2 (490 nm), '
                                                     'B3 (560 nm), B4 (665 nm) and B8 (842 nm)')
    st.image('data/images/third_party/s2_bands_20m.png', caption='Sentinel-2 20 m spatial resolution bands: B5 (705 nm), '
                                                     'B6 (740 nm), B7 (783 nm), B8a (865 nm), B11 (1610 nm) and '
                                                     'B12 (2190 nm)')
    st.image('data/images/third_party/s2_bands_20m.png', caption='Sentinel-2 60 m spatial resolution bands: B1 (443 nm), '
                                                     'B9 (940 nm) and B10 (1375 nm)')

    st.write('As crop cover duration computation is based on Sentinel-2 imagery with a 5-day revisit period, there '
             'is a need for daily interpolation to determine the number of days. During periods of heavy cloud cover, '
             'particularly in winter, which lengthens the interpolation period. Clear images may be unavailable for '
             'several weeks or months. This situation heightens uncertainty regarding crop development, especially '
             'critical during winter when monitoring cropping practices such as intermediate crops and tillage events '
             'is essential. ')

    st.write('Daily data would offer up-to-date information on crop development, allowing for real-time monitoring '
             'of changes in vegetation cover, growth patterns, and health status. With daily data, it would be '
             'possible to accurately track the evolution of crops by increasing the number of '
             'clear observations during very cloudy periods, reducing uncertainties associated with interpolating data '
             'over longer periods and providing a more precise knowledge of crop dynamics.')

# hedgerows
if page == 'Hedgerows monitoring':
    st.header('Hedgerows monitoring')
    # description
    st.subheader('Description')
    st.write('Tree hedges play a crucial role in the agricultural landscape by acting as natural barriers that reduce '
             'soil erosion, prevent nutrient-rich topsoil from being washed away into waterways, and combat wind '
             'erosion. This reduction in erosion is essential for preventing the leaching of nutrient-rich soil into '
             'adjacent waterways, a major factor in the proliferation of algal blooms. By enhancing soil stability and '
             'promoting water filtration, tree hedges serve as effective filters, reducing the runoff of nutrients '
             'into rivers and streams.')
    st.write('In addition to their role in erosion control, tree hedges support biodiversity by providing habitats for '
             'a variety of species, contributing to the ecological stability and resilience of agricultural systems. '
             'Hedgerows also function as biological corridors, facilitating the exchange of insect populations as well '
             'as other vertebrate and invertebrate animals.')
    st.write('Finally, monitoring tree hedges is a key strategy for maintaining sustainable agriculture and protecting '
             'both water and soil quality.')
    st.image('data/images/third_party/hedgerows_es.png', caption='Ecosystem services prodived by hedgerows.')

    # regulations
    st.subheader('Regulations on clearing hedges')
    st.write('Hedgerows are central to the "Hedgerow Pact," which seeks to halt the destruction and degradation of '
             'hedgerows that has been ongoing since the 1950s. France loses 20,000 km of hedgerows each year, with the '
             'current total standing at 750,000 km. The Pact, with a budget of €110 million, aims to preserve '
             'biodiversity by increasing the number of hedgerows by 50,000 km by 2030. However, in certain cases, '
             'hedgerows can be removed, but their removal is subject to specific regulations and administrative '
             'procedures.')
    st.write('The Rural Code, Town Planning Code, Environment Code, Heritage Code, Public Health Code, local decrees, '
             'and rules relating to European aid under the Common Agricultural Policy (CAP) all govern the maintenance '
             'and felling of hedgerows. These regulations may not all apply simultaneously but can overlap depending '
             "on the farm's location or its proximity to protected areas.")
    st.write('For farmers receiving CAP aid, the permanent removal of a hedge or part of a hedge is prohibited. '
             'A prior declaration to the Direction départementale des territoires et de la mer (DDTM) is required. '
             'The Order of 14 March 2023 on Good Agricultural and Environmental Conditions (GAEC) stipulates that '
             'permanent hedge removal is authorized in specific cases.')

    # knews on hedges
    st.subheader('Pressure on hedges continues')
    st.write('In Brittany, hedgerows continue to experience a significant decline, with the rate of loss accelerating '
             'over the past decade. Each year, approximately 23,500 km of hedgerows disappear in France, with 70% '
             'already wiped out since the land consolidation of the 1950s. Unfortunately, this trend shows no signs of '
             'reversing: "The disappearance and degradation of hedgerows are inevitable consequences of changes in the '
             'agricultural model," and "Undeclared levelings would be the biggest clearances."')
    st.write('Although hedgerows are theoretically protected, in practice, there are few obstacles to their removal. '
             'Penalties are rare, and enforcement of regulations is challenging. Moreover, following recent farm '
             'protests, the government has announced its intention to relax the standards regulating hedgerows.')
    st.write('“Destroy step by step to avoid being caught”. Another way to turn away from Good Agricultural and '
             'Environmental Conditions (BCAE 8) is to cut down the hedges step by step. Smaller trees are cut the '
             'first year, then others the next year, and so on. ‘It is a gradual erosion of trees practiced in order '
             'to get around the BCAE regulation.')

    # mapping hedges
    st.subheader('Mapping and observation of hedges and SWF')
    st.write('The SWF product provided by the Copernicus program has limitations in monitoring '
             'hedgerow trees, with both temporal and spatial resolutions needing improvement. Currently available for '
             '2015 and 2018, it lacks the frequency required for effective monitoring and management, especially in '
             'dynamic agricultural landscapes where annual updates are essential to capture changes in hedgerow '
             'extent. The 5-meter resolution is insufficient for detecting very small hedges or trees, which often '
             'require meter or sub-meter resolution for accurate mapping.')
    st.image('data/images/third_party/swf_tphp.png')
    st.write('The third-party methodology used to map hedgerows precisely leverages deep learning and very high resolution (VHR) '
             'imagery. Training and validation data were sourced from annotated samples, allowing '
             'the model to generalize effectively across different regions. A neural network was trained on these '
             'datasets, enabling accurate hedge detection at scale. Initially applied to the entire French territory, '
             'the method was then extended to cities worldwide, demonstrating its adaptability and scalability. The '
             'results show high accuracy in hedge detection, making this approach suitable for large-scale '
             'environmental monitoring, urban planning, and conservation efforts globally.')

    st.subheader('Conclusion')
    st.write('Hedgerows that are of major importance in preventing intensive farming activities and protecting '
             'ecosystems, have been shrinking for decades in the Britany region. Despite european regulations, '
             'farmers have found ways to get around BCAE regulation and keep cutting trees. The current SWF product is not a '
             'good option to monitor hedges as it is not updated frequently enough and the resolution is too coarse. '
             'If the S2 temporal cadence is sufficient to detect such cuts, the spatial resolution is too coarse to '
             'identify trees. Meter or sub-meter resolution is needed to detect the degradations and quantify the '
             'loss. Other satellites like Pleiades would be a good alternative to map changes of hedgerows, especially '
             'since Pleiades proposes tri-stereo acquisitions which would improve hedgerows detection.')