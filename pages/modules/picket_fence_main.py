import streamlit as st
from pylinac.core.decorators import lru_cache
from st_btn_select import st_btn_select
import pages.modules.pf_one_img as PF_ONE
import pages.modules.pf_four_img as PF_FOUR

if 'Filter' not in st.session_state:
    st.session_state['Filter'] = None

if 'log' not in st.session_state:
    st.session_state['log'] = None

if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

if 'ml_c' not in st.session_state:
    st.session_state['ml_c'] = None

if 'crop' not in st.session_state:
    st.session_state['crop'] = None

if 'tolerance' not in st.session_state:
    st.session_state['tolerance'] = None

if 'action_t' not in st.session_state:
    st.session_state['action_t'] = None

if 'number_p' not in st.session_state:
    st.session_state['number_p'] = None

if 'sag_ad' not in st.session_state:
    st.session_state['sag_ad'] = None

if 'orient' not in st.session_state:
    st.session_state['orient'] = None

if 'inv' not in st.session_state:
    st.session_state['inv'] = None

if 'leaf_w' not in st.session_state:
    st.session_state['leaf_w'] = None

if 'picket_spacing' not in st.session_state:
    st.session_state['picket_spacing'] = None

if 'height_threshold' not in st.session_state:
    st.session_state['height_threshold'] = None

if 'edge_threshold' not in st.session_state:
    st.session_state['edge_threshold'] = None

if 'peak_sort' not in st.session_state:
    st.session_state['peak_sort'] = None

if 'required_prominence' not in st.session_state:
    st.session_state['required_prominence'] = None

if 'a1' not in st.session_state:
    st.session_state['a1'] = None

if 'a2' not in st.session_state:
    st.session_state['a2'] = None

if 'c3' not in st.session_state:
    st.session_state['c3'] = None

if 'b' not in st.session_state:
    st.session_state['b'] = None

if 'c1' not in st.session_state:
    st.session_state['c1'] = None

if 'c2' not in st.session_state:
    st.session_state['c2'] = None

if 'c3' not in st.session_state:
    st.session_state['c3'] = None

if 'd' not in st.session_state:
    st.session_state['d'] = None

if 'e1' not in st.session_state:
    st.session_state['e1'] = None

if 'e2' not in st.session_state:
    st.session_state['e2'] = None

if 'e3' not in st.session_state:
    st.session_state['e3'] = None

if 'f' not in st.session_state:
    st.session_state['f'] = None
 
if 'g1' not in st.session_state:
    st.session_state['g1'] = None

if 'g2' not in st.session_state:
    st.session_state['g2'] = None

if 'g3' not in st.session_state:
    st.session_state['g3'] = None

if 'h' not in st.session_state:
    st.session_state['h'] = None

if 'i1' not in st.session_state:
    st.session_state['i1'] = None

if 'i2' not in st.session_state:
    st.session_state['i2'] = None

if 'c3' not in st.session_state:
    st.session_state['c3'] = None

if 'j' not in st.session_state:
    st.session_state['j'] = None

if 'name0' not in st.session_state:
    st.session_state['name0'] = None

if 'name1' not in st.session_state:
    st.session_state['name1'] = None

if 'name2' not in st.session_state:
    st.session_state['name2'] = None

if 'name3' not in st.session_state:
    st.session_state['name3'] = None

if 'name4' not in st.session_state:
    st.session_state['name4'] = None

if 'r1' not in st.session_state:
    st.session_state['r1'] = None

if 'r2' not in st.session_state:
    st.session_state['r2'] = None

if 'r3' not in st.session_state:
    st.session_state['r3'] = None

if 'r4' not in st.session_state:
    st.session_state['r4'] = None

if 'r5' not in st.session_state:
    st.session_state['r5'] = None

def Picket_Fence():
    main_pages = st_btn_select(('One image analysis', 'Four images analysis'), nav=False)

    # ONE IMAGE ANALYSIS 
    if main_pages == 'One image analysis':
        PF_ONE.pf_one()                

    # FOUR IMAGES ANALYSIS
    elif main_pages == 'Four images analysis':
        PF_FOUR.pf_four()