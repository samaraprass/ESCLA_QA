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

#Importing Inside modules
# -- Core
import pages.core.home_function as HomePage
import pages.core.login as LOGIN
import pages.core.charts as CHART
import pages.core.dataframes as DF

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

    {'id': 'timeline', 'label': 'Timeline'}
]

