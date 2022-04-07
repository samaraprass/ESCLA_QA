import streamlit as st
import io
import matplotlib.pyplot as plt
import matplotlib
import pages.core.text as text
import pages.core.table_function as table
import pandas as pd
from pylinac.picketfence import PicketFence
import pydicom
from datetime import datetime
import pydicom.uid
import pytz

if 'names_pf' not in st.session_state:
    st.session_state['names_pf'] = None

if 'values_pf' not in st.session_state:
    st.session_state['values_pf'] = None

if 'test_results' not in st.session_state:
    st.session_state['test_results'] = None

if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

@st.cache(allow_output_mutation=True, show_spinner=False)
def dicom_img(input_img):
    dcm_img = pydicom.dcmread(input_img)
    fig, ax1 = plt.subplots()
    cmap = matplotlib.cm.get_cmap('gray')
    ax1.imshow(dcm_img.pixel_array, cmap=cmap)
    ax1.axis("off")
    return fig
    
def input_image(pf_img):
    r1, r2, r3 = st.columns(3)
    with r2:
        text.title("Input Image", 15, "#8C438D")
        st.pyplot(dicom_img(pf_img))

@st.cache(allow_output_mutation=True, show_spinner=False)
def dicom_img2(input_img):
    dcm_img = pydicom.dcmread(input_img)
    fig, ax1 = plt.subplots()
    cmap = matplotlib.cm.get_cmap('gray')
    ax1.imshow(dcm_img.pixel_array, cmap=cmap)
    ax1.axis("off")
    return fig

def input_image2(pf_img):
    r1, r2, r3 = st.columns(3)
    with r2:
        text.title("Input Image", 15, "#8C438D")
        st.pyplot(dicom_img2(pf_img))

def image_analysis(pf_img):                
    pf_f = PicketFence(pf_img, use_filename=st.session_state['file_name'], log=st.session_state['log'], crop_mm=st.session_state['crop'], 
                        mlc=st.session_state['ml_c'], filter=st.session_state['Filter'])

    pf_f.analyze(tolerance=st.session_state['tolerance'], action_tolerance=st.session_state['action_t'], num_pickets=st.session_state['number_p'], 
                sag_adjustment=st.session_state['sag_ad'], orientation=st.session_state['orient'], invert=st.session_state['inv'], 
                leaf_analysis_width_ratio=st.session_state['leaf_w'], picket_spacing=st.session_state['picket_spacing'], 
                height_threshold=st.session_state['height_threshold'], edge_threshold=st.session_state['edge_threshold'], 
                peak_sort=st.session_state['peak_sort'], required_prominence=st.session_state['required_prominence'])

    results = pf_f.results_data(as_dict=True)

    if results['passed'] == True:
        st.session_state['test_results'] = 'PASS'
    else:
        st.session_state['test_results'] = 'FAIL'
                
    if results['action_tolerance_mm'] == None:
        results['action_tolerance_mm'] = 'None choosed'

                
    @st.cache(allow_output_mutation=True, show_spinner=False)
    def table_pf():
                    
        st.session_state['names_pf'] = ["MLC Type","Date of Analysis", "Tolerance (mm)", "Action Tolerance (mm)", "Percent Leaves Passing", 
                    "Number of pickets", "Absolute Median Error (mm)", "Maximum Error (mm)", "Mean Picket Spacing (mm)"]

        for i in range(pf_f.num_pickets):
            row = "Offset from CAX (mm) - leaf " + str(i)
            st.session_state['names_pf'].append(row)
        
        st.session_state['names_pf'].append("Test Results")

        date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
        date_i = str(date_timezone.replace(tzinfo=None))
        format_date = "%Y-%m-%d %H:%M:%S.%f"
        real_date = datetime.strptime(date_i, format_date)
        date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                str(real_date.minute) + ':' + str(real_date.second)) 
                    
        st.session_state['values_pf'] = [st.session_state['ml_c'], date_table, results['tolerance_mm'], results['action_tolerance_mm'], results['percent_leaves_passing'], results['number_of_pickets'],
                                round(results['absolute_median_error_mm'], 4), round(results['max_error_mm'], 4), round(results['mean_picket_spacing_mm'], 4)]

        for j in range(pf_f.num_pickets):
            r = results['offsets_from_cax_mm'][j]
            st.session_state['values_pf'].append(round(r, 4))

        st.session_state['values_pf'].append(st.session_state['test_results'])  

        t = pd.DataFrame(st.session_state['values_pf'], columns=["Results"])
        t.insert(0, "Parameters", st.session_state['names_pf'], True)
        tab = t.round(decimals=4)
        fig, ax = table.render_mpl_table(tab)
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

        return buf, st.session_state['names_pf'], st.session_state['values_pf']

    table_1, st.session_state['names_pf'], st.session_state['values_pf'] = table_pf()
        
    return table_1, st.session_state['names_pf'][:-1], st.session_state['values_pf'][:-1], pf_f, st.session_state['test_results']