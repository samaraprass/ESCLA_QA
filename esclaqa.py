# Importing Libraries
import streamlit as st
import hydralit_components as hc
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import pylinac
import base64
import requests
from streamlit_lottie import st_lottie
from st_btn_select import st_btn_select
from deta import Deta
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import numpy as np

#Importing Inside modules
# -- Core
import pages.core.home_function as HomePage
import pages.core.login as LOGIN
import pages.core.charts as CHART
import pages.core.dataframes as DF
import pages.core.login_authenticated as LOGIN_PASS

# -- Pylinac modules implementation 
import pages.modules.VMAT_drgs as VMATDRGS
import pages.modules.VMAT_demo_drmlc as VMATDemo_dmlc
import pages.modules.VMAT_demo_drgs as VMATDemo_drgs
import pages.modules.field_analysis as FieldAnalysis
import pages.modules.VMAT_drmlc as VMATDRMLC
import pages.modules.picket_fence_main as PF
import pages.modules.winston_lutz as Winston_Lutz
import pages.modules.starshot as Star

# Sessions States
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if 'name_user' not in st.session_state:
    st.session_state['name_user'] = None

# Streamlit main setup
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Escla QA - Pylinac", page_icon="📋", layout="wide",
                   initial_sidebar_state="expanded")

pylinac.settings.DICOM_COLORMAP = 'gray'
plt.style.use('seaborn-muted')

# Deta Database Connection
data_connection = Deta(st.secrets['database']['data_key'])

# Menu
menu_data = [
    {'id': 'Tutorial', 'label': 'Tutorial', 'ttip': 'How to use this app'},

    {'id': 'VMAT', 'label': "VMAT", 'ttip': "VMAT QA Analysis", 'submenu': [{'id': 'DRGS', 'label': 'DRGS',
                                                                             'ttip': "Dose-Rate & Gantry-Speed"},
                                                                            {'id': 'DRMLC', 'label': 'DRMLC',
                                                                             'ttip': "Dose-Rate & MLC-Speed"}]},
    {'id': 'Star', 'label': 'Starshot', 'ttip': 'Starshot module'},

    {'id': 'PF', 'label': 'Picket Fence', 'ttip': 'Picket Fence module'},

    {'id': 'WL', 'label': 'Winston-Lutz', 'ttip': "Winston-Lutz module"},

    {'id': '#field-analysis-epid-images', 'label': 'Field Analysis', 'ttip': "Field Analysis module"},

    {'id': 'timeline', 'label': 'Results Timeline'}
]

over_theme = {'txc_inassssctive': '#CED4DE '}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Login',
    use_animation=True,
    hide_streamlit_markers=True,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode='pinned',  # jumpy or not-jumpy, but sticky or pinned
)

st.markdown(
    """
     <style>
     .css-15tags5 {
         background: -webkit-linear-gradient(left, #FFFFFF 20px, transparent 1%) center, -webkit-linear-gradient(#FFFFFF 20px, transparent 1%) center, #F1F1F7;
         background: linear-gradient(90deg, #FFFFFF 20px, transparent 1%) center, linear-gradient(#FFFFFF 20px, transparent 1%) center, #F1F1F7;
   	    background-size: 22px 22px;
     }
     .css-18e3th9 {
         padding: 0rem 5rem 5rem;
         padding-bottom: 0rem;
     }
    </style>
     """,
     unsafe_allow_html=True
) # https://codepen.io/edmundojr/pen/xOYJGw

if menu_id == 'Home':
    # Styling with css
    HomePage.Home()

#Tutorial
if menu_id == 'Tutorial':
    t1, t2, t3 = st.columns([1.1, 2, 0.5])
    with t2:
        subpages = st_btn_select(("VMAT - DRGS Demo", 'VMAT - DRMLC Demo'), nav=False)
    if subpages == 'VMAT - DRGS Demo':
        st.subheader("Demonstration for Dose-Rate & Gantry-Speed")
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        VMATDemo_drgs.vmat_demo_drgs()
    
    elif subpages == "VMAT - DRMLC Demo":
        st.subheader("Demonstration for Dose-Rate & MLC-Speed")
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        VMATDemo_dmlc.vmat_demo_dmlc()

# VMAT
if menu_id == "DRGS":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader('VMAT - Dose-Rate & Gantry-Speed')
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    VMATDRGS.vmat_drgs()

if menu_id == "DRMLC":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader('VMAT - Dose-Rate & MLC Speed')
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    VMATDRMLC.vmat_drmlc()


if menu_id == "Star":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader("Starshot Module")
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    Star.star()

if menu_id == "PF":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader("Picket Fence")

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    PF.Picket_Fence()

if menu_id == "WL":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader("Winston-Lutz Module")
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    Winston_Lutz.wl()


# Field Analysis for EPID IMAGES
if menu_id == "#field-analysis-epid-images":
    if st.session_state['authentication_status'] is not None:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))

    st.subheader("Field Analysis - EPID Images")
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    FieldAnalysis.FA()

if menu_id == 'Login':
    with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    LOGIN.authentication()

    if st.session_state['authentication_status']:
        LOGIN_PASS.login_verified()
        
        
if menu_id == 'timeline':
    if st.session_state['authentication_status'] == False or st.session_state['authentication_status'] == None:
        st.warning("This section is available for ESCLA members only")

        # count = st_autorefresh(interval=600000, limit=100, key="dataframes")
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_url_secure = 'https://assets8.lottiefiles.com/private_files/lf30_ulp9xiqw.json'
        lottie_secure = load_lottieurl(lottie_url_secure)
        st_lottie(lottie_secure, key="hello", loop = True, height=500)
        
    else:
        st.warning('You are logged in as *%s*' % (st.session_state['name_user']))
        with st.expander(' 🔎  INFOS (click here to expand/collapse)', expanded=True):
            st.write(' 🔹 This is an interactive time chart. You can click on the variable names to change which ones you want to see;')
            st.write(' 🔹 The file name are the key to identifying data in the database. Be sure to ALWAYS upload files with DIFFERENT names;')
            st.write(' 🔹 This timeline does not distinguish between data from different linacs. For this reason, you should upload data from the same linac to '
            'better interpret the results of the timeline. This differentiation feature will be included in the next update of the app.')
            st.write('Thanks 🤙🏻')

        #st.info(' 🤙🏻 INFO: This is a interactive graph. You can click the variables names to change which one to see.')
        t1, t2, t3 = st.columns([1, 5, 0.8])
        with t2:
            pages = st_btn_select(('VMAT - DRGS', 'VMAT - DRMLC', 'Starshot', 'Picket Fence', 'Winston-Lutz', 'Field Analysis'), nav=False)
        
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        if pages == 'VMAT - DRGS':
            CHART.line_chart_vmat_drgs()
            DF.dataframe_drgs()
        
        elif pages == 'VMAT - DRMLC':
            CHART.line_chart_vmat_drmlc()
            DF.dataframe_drmlc()
        
        elif pages == 'Starshot':
            CHART.line_chart_star()
            DF.dataframe_star()
        
        elif pages == 'Picket Fence':
            angle = st.select_slider("Angle visualization", [0, 90, 180, 270])
            CHART.line_chart_picket_fence(angle)
            DF.dataframe_picket_fence(angle)
        
        elif pages == 'Winston-Lutz':
            CHART.line_chart_wl()
            DF.dataframe_wl()

        elif pages == 'Field Analysis':
            type = st.selectbox("Type", ['6MV', '10MV', '15MV', '6SRS'])
            CHART.line_chart_fa(type)
            DF.dataframe_fa(type)
