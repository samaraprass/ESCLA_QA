from psutil import NIC_DUPLEX_UNKNOWN
import streamlit as st
from deta import Deta
from PIL import Image

if 'unit' not in st.session_state:
    st.session_state['unit'] = None

def login_verified():
    # Deta connection
    data_connection = Deta(st.secrets['database']['data_key'])
    logos = data_connection.Drive("logos")
    photos = data_connection.Drive("photos")

    # Login page authenticated
    if st.session_state['username'] == st.secrets['us'][0]:
        l1, l2, l3  = st.columns([1,4,1])
        with l2:
            logo = logos.get('corhmd.png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit'] = st.selectbox("Set unit for analysis", ['TRILOGY', 'CL 2100'])
    
    if st.session_state['username'] == st.secrets['us'][1]:
        l1, l2, l3  = st.columns(3)
        with l2:
            logo = logos.get('tacchini.png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit']=None

    if st.session_state['username'] == st.secrets['us'][2]:
        l1, l2, l3 = st.columns([1.8, 2, 1])
        with l2:
            logo = logos.get('CEBAMS.png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit']=None

    if st.session_state['username'] == st.secrets['us'][3]:
        l1, l2, l3  = st.columns(3)
        with l2:
            photo = photos.get('bage_crop2.jpg')
            image = Image.open(photo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit']=None
    
    if st.session_state['username'] == st.secrets['us'][4]:
        l1, l2, l3 = st.columns(3)
        with l2:
            logo = logos.get('hospital-ana-nery-rs.png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit'] = st.selectbox("Set unit for analysis", ['CLINAC 600', 'CLINAC CX'])
    

    if st.session_state['username'] == st.secrets['us'][5]:
        l1, l2, l3  = st.columns([2.3, 3, 1])
        with l2:
            logo = logos.get('sta_casa_uruguaiana.png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit']=None

    if st.session_state['username'] == st.secrets['us'][6]:
        l1, l2, l3  = st.columns(3)
        with l2:
            logo = logos.get('Logo_Santa-Casa-do-Rio-Grande-02-2(1).png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit']=None
    
    if st.session_state['username'] == st.secrets['us'][7]:
        l1, l2, l3 = st.columns([2.5, 3, 0.8])
        with l2:
            logo = logos.get('cor_uruguai(1).png')
            image = Image.open(logo)
            st.image(image)
        st.success('Welcome *%s*' % (st.session_state['name_user']))
        st.session_state['unit'] = st.selectbox("Set unit for analysis", ['UNIQUE', 'CLINAC 1', 'HALCYON'])
    
    if st.session_state['username'] == st.secrets['us'][8]:
        st.success('Welcome *%s*' % (st.session_state['name_user']))
    
    if st.session_state['username'] == st.secrets['us'][9]:
        st.success('Welcome *%s*' % (st.session_state['name_user']))