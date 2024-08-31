import os
import glob
import streamlit as st
from pyogrio import read_dataframe

# side bar
st.sidebar.title('CLMS inventory')
page = st.sidebar.radio('Go to', ['Corine Land Cover', 'Costal Zones', 'Riparian Zones', 'Urban Atlas',
                                  'Imperviousness', 'Small Woody Features', 'Grassland', 'Tree Cover Change Mask',
                                  'Water and Wetness'])

# title
st.title('CLMS data for intensive farming monitoring (IFM)')

# clc
if page == 'Corine Land Cover':
    st.header('Corine land cover (CLC)')
    # description
    st.write('Corine Land Cover is a biophysical land cover / land use European database. This project, launched '
            'in 1985, is managed by the European Environment Agency (EEA) and covers 39 states. The first CORINE '
            'Land Cover (CLC) has been produced in 1990 and updates have been produced in 2000, 2006, 2012, and 2018.'
            'The inventory contains 44 land cover classes. The product has a Minimum Mapping Unit (MMU) of 25 hectares '
             '(ha) for areal phenomena and a minimum width of 100 m for linear phenomena. The time series are '
             'complemented by change layers every 6 years, which highlight changes in land cover with a MMU of 5 ha.')
    st.write('The CLC nomenclature is organized on three levels. The first level (five items) indicates the major '
             'categories of land cover. The second level composed of 15 items and the third level composed of 44 items')

    # clc map
    st.subheader('CLC map')
    # display clc map according to year selected by the user (status + change)
    years = ['1990', '2000', '2006', '2012', '2018']
    y = st.selectbox("Select a year : ", options=years)
    st.image(f'data/images/clms/clc_{y}.png', caption=f"CLC map ({y})", use_column_width=True)
    if y != '1990':
        change_map = glob.glob(f'data/images/clms/clc_change_map*{y[-2:]}.png')[0]
        change_table = glob.glob(f'data/images/clms/clc_change_table*{y[-2:]}.png')[0]
        d1 = os.path.basename(change_map).split("_")[-1][0:2]
        if d1 == '90':
            d1 = '1990'
        else:
            d1 = f'20{d1}'
        d2 = f'20{os.path.basename(change_map).split("_")[-1][3:5]}'
        st.subheader(f'CLC change map {d1} - {d2}')
        st.image(change_map, caption=f"CLC change map ({d1} - {d2})", use_column_width=True)
        st.subheader(f'CLC change table {d1} - {d2}')
        st.image(change_table, caption=f"CLC change table ({d1} - {d2})", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    st.write('The Corine Land Cover product provides highly relevant information on the major trends that have '
             'occurred in the 11 watersheds area, with greater precision on the flow of artificial development and '
             'forest management. There is some information on agriculture between 1990-2000 and 2000-2006, and a '
             'little less between 2006-2012, no agricultural changes have been identified between 2012 and 2018.  '
             'These agricultural land cover changes concern internal conversions from annual crops to grassland and '
             'vice versa and other agricultural conversion.  We can therefore note that the areas of change in '
             'internal agricultural conversions between grassland and annual crops seem a little coarse, as the '
             'thresholds for changes in Corine land cover only include areas greater than or equal to 5 hectares, '
             'which represents large areas. Finally, we note that agricultural conversions are no longer identified '
             'between 2012 and 2018. ')

# cz
if page == 'Costal Zones':
    st.header('Costal zones (CZ)')
    # decription
    st.write('The coastal Zones product provides detailed land cover and land use information for 71 thematic land '
             'cover classes for all European coastal territory to a landward distance of 10 km with total area '
             'mapped of approximatively 730,000km². The product has a six-year update cycle and is now available '
             'for the 2012 and 2018 reference years with the 2012-2018 change layer. The dataset has a Minimum Mapping '
             'Unit (MMU) of 0.5 ha and a Minimum Mapping Width (MMW) of 10 m and is available as vector data. ')

    # cz map
    st.subheader('CZ map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year : ", options=years)
    st.image(f'data/images/clms/cz_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('CZ change map 2012 - 2018')
    st.image(f'data/images/clms/cz_change_12-18.png', caption=f"CZ change map (2012-2018)", use_column_width=True)
    st.subheader('CZ change table 2012 - 2018')
    st.image(f'data/images/clms/cz_change_table_12-18.png', caption=f"CZ change table (2012-2018)", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    st.write('The change table shows the surface area of land cover / land use changes between 2012 and 2018 in the '
             'coastal zones, reveals two main flows.  A flow relating to urban dynamics (shown in red color in Table '
             '5) and a flow relating to changes in forest cover (in green color). Despite the fact that the surface '
             'thresholds of this CZ database are much smaller than those of Corine land cover (MMU = 0.5 ha instead '
             'of 5 ha for CLC changes), the flow representing agricultural changes and conversions (in yellow) is '
             'weakly represented, only a few hectares of changes have been identified.')

# rz
if page == 'Riparian Zones':
    st.header('Riparian zones (RZ)')
    # description
    st.write('The RZ data provides detailed land cover and land use information for 55 thematic classes in a '
             'variable buffer zone of selected rivers across Europe for the 2012 and 2018 reference year. The dataset '
             'has a Minimum Mapping Unit (MMU) of 0.5 ha and a Minimum Mapping Width (MMW) of 10 m and is available '
             'as vector data. It is updated every six years, and currently consists of three layers—a land cover/land '
             'use layer for 2012 and 2018 and a change layer for 2012-2018. ')

    # rz map
    st.subheader('RZ map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year :", options=years)
    st.image(f'data/images/clms/rz_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('RZ change map 2012 - 2018')
    st.image(f'data/images/clms/rz_change_12-18.png', caption=f"RZ change map (2012-2018)", use_column_width=True)
    st.subheader('RZ change table 2012 - 2018')
    st.image(f'data/images/clms/rz_change_table_12-18.png', caption=f"RZ change table (2012-2018)", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    st.write('The land cover changes observed mainly represent the flow of artificialization and the other flow '
             'categories essentially corresponding to the conversion of mining extraction into grassy area. There is '
             'not any flow representing agricultural rotations between grassland systems and annual crops.')
    st.write('Buffer strips located along watercourses protect soils from erosion risks, improve their structure and '
             'contribute to the protection of running water by limiting the risks of diffuse pollution. In general, '
             'they favor crop auxiliaries and biodiversity. It is therefore important to know the type of crops and '
             'their change over time within the riparian zone and to determine the proportion of grassed areas & '
             'annual crops (corn/ wheat/ cabbage ...). ')

# ua
if page == 'Urban Atlas':
    st.header('Urban Atlas (UA)')
    # description
    st.write('The Urban Atlas data provides land cover and land use data with the integrated population '
             'estimates in 788 Functional Urban Areas (FUA) with more than 50,000 inhabitants in EEA39 countries for '
             'the 2018, 2012 and 2006 reference year. The dataset maps land cover and land use for 17 urban classes '
             'with the Minimum Mapping Unit (MMU) of 0.25 ha and for 10 rural classes with the MMU of 1 ha and is '
             'available as vector data and updated every 6 years. Urban Atlas data are available for the 2006, 2012 '
             'and 2018 reference years including the two change products for 2006-2012 and 2012-2018. Only reference '
             'year 2012 and 2018 are available for the Functional Urban Area (FUA) of Saint-Brieuc city.  ')

    # ua map
    st.subheader('UA map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year: ", options=years)
    st.image(f'data/images/clms/ua_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('UA change map 2012 - 2018')
    st.image(f'data/images/clms/ua_change_12-18.png', caption=f"UA change map (2012-2018)", use_column_width=True)
    st.subheader('UA change table 2012 - 2018')
    st.image(f'data/images/clms/ua_change_table_12-18.png', caption=f"UA change table (2012-2018)", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    st.write('The Urban Atlas products allows users to access detailed land cover and land use maps for several '
             'functional urban areas across Europe, in addition to street tree maps, height measurements building '
             'blocks and population estimates. These products provide relevant information on urban expansions over '
             'agricultural and natural areas, industrial lands, roadways, mining extensions. In fact, all the '
             'biophysical elements concerning the artificialization of land. The purpose of this database therefore '
             'does not concern changes relating to the agricultural domain or natural spaces.')

# imp
if page == 'Imperviousness':
    st.header('Imperviousness')
    # description
    st.write('Impermeable surfaces such as roads and buildings prevent rainwater from infiltrating the ground, '
             'leading to increased runoff, flooding and reduced groundwater recharge.  According to Copernicus, '
             'Imperviousness products detect the spatial distribution and evolution over time of artificially sealed '
             'areas at continental level. The main products are Imperviousness Density, which provides data on '
             'imperviousness density in a range from 0 to 100% (for dates 2006, 2009, 2012, 2015, 2018), and maps of '
             'classified changes at variable resolution (10, 20, 100m). These data are available in raster format and '
             'updated every 3 years.')

    # imp map
    st.subheader('Imperviousness map')
    # display clc map according to year selected by the user (status + change)
    years = ['2006', '2009', '2012', '2015', '2018']
    y = st.selectbox("Select a year: ", options=years)
    st.image(f'data/images/clms/imp_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    if y != '2006':
        change_map = glob.glob(f'data/images/clms/imp_change*{y[-2:]}.png')[0]
        d1 = f'20{os.path.basename(change_map).split("_")[-1][0:2]}'
        d2 = f'20{os.path.basename(change_map).split("_")[-1][3:5]}'
        st.subheader(f'Imperviousness change map {d1} - {d2}')
        st.image(change_map, caption=f"Imperviousness change map ({d1} - {d2})", use_column_width=True)

    # wip
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)

# swf
if page == 'Small Woody Features':
    st.header('Small Woody Fetures (SWF)')
    # description
    st.write('The Copernicus service Small Woody Features product provides data on woody features ≤ 30 m wide and '
             '≥ 30 m long, as well as patchy structures from 200 m² to 5,000 m² in area, with a spatial resolution '
             'of 5m. These data, available for 2015 and 2018, cover the EEA38 and the UK, providing a tool for '
             'understanding landscapes, assessing biodiversity and carbon sequestration, supporting sustainable land '
             'management and mitigating climate change. Small woody formations can also help to regulate water cycles '
             'and prevent soil erosion, functions that are particularly important in agricultural areas where soil '
             'health is extremely important. ')

    # swf map
    st.subheader('SWF map')
    # display clc map according to year selected by the user (status)
    years = ['2015', '2018']
    y = st.selectbox("Select a year: ", options=years)
    st.image(f'data/images/clms/swf_{y}.png', caption=f"SWF map ({y})", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    st.image(f'data/images/clms/swf_change_table_15-18.png', caption=f"SWF change table (2015 - 2018)", use_column_width=True)
    # wip
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">Ajouter fond Nimbo</p>', unsafe_allow_html=True)

    # swf omissions / commissions
    gl_select = st.selectbox("Zoom on SWF data", options=['SWF 2015', 'SWF 2018', 'SWF 2015 commissions', 'SWF 2015 omissions'])
    if gl_select == 'SWF 2015':
        st.image('data/images/clms/swf_2015-zoom.png')
    elif gl_select == 'SWF 2018':
        st.image('data/images/clms/swf_2018-zoom.png')
    elif gl_select == 'SWF 2015 commissions':
        st.image('data/images/clms/swf_com_2015.png')
    else:
        st.image('data/images/clms/swf_om_2015.png')

    st.write('The SWF 2015 and SWF 2018 databases are not comparable and provide independent data. Therefore, it is '
             'not possible to monitor real changes in SWF cover, such as the destruction of hedgerows or the '
             'restoration of linear features. Observations carried out on a small sample in Saint Brieuc, in catchment '
             'area No. 2 and near the village of Hénon, reveal significant differences between the two reference '
             'datasets. Both 2015 and 2018 still have omissions of SWFs, particularly hedges. Additionally, some '
             'features that were present and mapped in 2015 are no longer mapped in 2018, even though they still '
             'exist. Improvements are noticeable in the 2018 database compared to 2015, with false SWFs mapped in 2015 '
             'being removed in 2018, and real SWFs that were omitted in 2015 now being correctly mapped in 2018. '
             'However, the SWF gains between 2015 and 2018 include erroneous changes due to a methodological '
             'improvement applied. In 2015, isolated elements (with a surface area of over 1,500 m²) that improved '
             'connectivity were classified as additional woody feature (AWF) values, whereas in 2020, they are '
             'integrated into other small woody features.')
    st.write('The identification of SWFs, including hedges and small patches of woodland, must be very precise and '
             'exhaustive if we are to monitor their evolution in space and time. The 5-meter resolution proposed by '
             'Copernicus products seems sufficient at the regional level, especially for carbon stock or biomass '
             'estimation. Unfortunately, there are still far too many SWFs omitted from the maps, and monitoring '
             'actual changes (hedgerow removal and/or restoration) certainly requires more accurate data. Annual '
             'monitoring of SWFs could be a better way to assess changes, especially as hedgerows are gradually '
             'destroyed by felling the trees that make up the hedge, until both the slope and the hedge have '
             'disappeared completely.')

# grassland
if page == 'Grassland':
    st.header('Grassland')
    # description
    st.write('The High-Resolution Layer Grassland is a pan-European binary product that provides a '
             'grassland/non-grassland mask, with triennial updates for 2015 and 2018. Its spatial resolution was '
             '20 meters in 2015 and improved to 10 meters in 2018. Annual updates are planned from 2024 onward. '
             'Additionally, a change detection layer for 2015–2018 is available to help distinguish real changes '
             'from false changes caused by the difference in resolution between the two products.')
    st.subheader('Grassland map')
    # display clc map according to year selected by the user (status + change)
    years = ['2015', '2018']
    y = st.selectbox("Select a year:", options=years)
    st.image(f'data/images/clms/grass_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('Grassland change map')
    st.image('data/images/clms/grass_change_15-18.png', caption=f"Grassland change map (2015-2018)", use_column_width=True)
    st.write('The maps show the grassland areas in 2015 and 2018 by catchment area. It is notable that the grassland '
             'areas in 2018 are significantly larger than in 2015, in some cases more than double. However, these '
             'differences observed between the two dates do not reflect real changes.')

    # analysis
    st.subheader('Analysis')
    grass_select = st.selectbox('Zoom on : ', options=['Grassland layer (2015)', 'Grassland change layer (2015-2018)'])
    if grass_select == 'Grassland layer (2015)':
        st.image('data/images/clms/grass_2015-zoom.png', caption='Zoom on grassland map (2015)')
    if grass_select == 'Grassland change layer (2015-2018)':
        st.image('data/images/clms/grass_change_15-18-zoom.png', caption='Zoom on grassland change map (2015-2018)')

    # barplot grassland change 2015-2018
    grass_change_15_18 = read_dataframe('data/dataframes/grass_change_table_15-18.csv')
    grass_change_15_18['Catchment area'] = grass_change_15_18['Catchment area'].astype('int')
    grass_change_15_18['2015'] = grass_change_15_18['2015'].astype('float')
    grass_change_15_18['2018'] = grass_change_15_18['2018'].astype('float')
    st.bar_chart(grass_change_15_18,
                 x='Catchment area',
                 y=['2015', '2018'],
                 y_label='Surface (ha)',
                 stack=False)

    st.write('The graphic above shows the grassland areas in 2015 and 2018 by catchment area. We note areas of '
             'grassland in 2018 are significantly larger than 2015 (sometimes more than double). These differences '
             'observed between the two dates do not correspond to real changes. ')

    st.subheader('Analysis')
    st.write('The 2015 and 2018 Grassland layers are not directly comparable, as they were produced using different '
             'methodologies and surface thresholds. Therefore, the changes indicated in the change layer reflect '
             'methodological differences rather than actual land cover changes between annual crops and grassland. '
             'Even though the identification of grasslands in 2018 appears reliable, we are still far from '
             'having accurate and relevant information on conversions from grassland to annual crops. This is a key '
             'indicator from an environmental, biodiversity, and pollution assessment perspective.')

# tccm
if page == 'Tree Cover Change Mask':
    st.header('Tree Cover Change Mask (TCCM)')
    st.write('This data provides pan-European information at a spatial resolution of 20 meters on changes across '
             'four thematic classes: unchanged areas with no tree cover, new tree cover, loss of tree cover, and '
             'unchanged areas with tree cover. These changes are tracked between the 2012/2015 and 2015/2018 reference '
             'years.')
    st.subheader('TCCM map')
    # display tccm map according to year selected by the user (change)
    years = ['2012-2015', '2015-2018']
    y = st.selectbox("Select a year:", options=years).replace('20', '')
    st.image(f'data/images/clms/tccm_{y}.png', caption=f"TCCM map ({y})", use_column_width=True)
    st.subheader('Analysis')

    # wip
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)

# ww
if page == 'Water and Wetness':
    st.header('HRL Water and Wetness (WW)')
    # display ww map according to year selected by the user (status)
    years = ['2015', '2018']
    y = st.selectbox("Select a year : ", options=years)
    st.image(f'data/images/clms/waw_{y}.png', caption=f"WW map ({y})", use_column_width=True)

    # wip
    st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)