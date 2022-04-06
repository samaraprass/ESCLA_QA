from pickletools import bytes1
import streamlit as st
from pylinac import DRGS
import matplotlib
from pylinac.core.image import DicomImage
import matplotlib.pyplot as plt
from pylinac.vmat import ImageType
import pydicom
import pages.core.text as txt
import pandas as pd
import io
import pages.core.table_function as table
from pylinac.core.decorators import lru_cache
from deta import Deta

def vmat_demo_drgs():
    #database connection
    data_connection = Deta(st.secrets['database']['data_key'])
    

    # DEMO DRGS
    # Loading images
    file_drgs_demo = "C:\\Users\\samar\\PycharmProjects\\pylinac_deploy\\pages\\home\\modules\\demo\\DRGS_dmlc.dcm"
    file_open_drgs_demo = "C:\\Users\\samar\\PycharmProjects\\pylinac_deploy\\pages\\home\\modules\\demo\\DRGS_open.dcm"
    dmlc_img = pydicom.dcmread(file_drgs_demo)
    open_img = pydicom.dcmread(file_open_drgs_demo)

    # Creating parameters form
    reset = st.checkbox("Reset to default parameters", key="r1",
                        help="Click here if you prefer to reset to default parameters "
                             "every time you apply new ones.")
    if reset:
        r = True
    else:
        r = False

    with st.form(key="drgs_demo", clear_on_submit=r):
        t_drgs = 'Analysis parameters'
        txt.body(t_drgs, 18, "black")
        col1, col2, col3 = st.columns(3)
        with col1:
            tolerance1 = st.number_input("Choose your tolerance value", min_value=0.0, max_value=8.0, value=1.5,
                                         step=0.5,
                                         help="The tolerance of the sample deviations in percent. Default is 1.5. "
                                              "Must be between 0 and 8.")
            lru_cache(tolerance1)

        with col2:
            w1 = st.number_input("Set the width of the ROI segments in mm", min_value=0, max_value=1000, value=5,
                                 help="Integer value")
            lru_cache(w1)

        with col3:
            h1 = st.number_input("Set the height of the ROI segments in mm", min_value=0, max_value=1000, value=100,
                                 help="Integer value")
            lru_cache(h1)

        submit_button = st.form_submit_button(label='Apply')

    # Display demo images
    txt.title("Demo Images", 20, "#8C438D")

    dcol1, dcol2, dcol3, dcol4, dcol5 = st.columns([1.1, 2, 1.1, 2, 1.1])
    
    @st.cache(allow_output_mutation=True)
    def img1():
        fig, ax = plt.subplots()  # https://discuss.byteslit.io/t/wordcloud-error/18672
        cmap_reversed = matplotlib.cm.get_cmap('gray_r')
        ax.axis('off')
        ax.imshow(dmlc_img.pixel_array, cmap=cmap_reversed)
        return fig
    
    @st.cache(allow_output_mutation=True)
    def img2():
        fig2, ax2 = plt.subplots()  
        cmap_reversed = matplotlib.cm.get_cmap('gray_r')
        ax2.axis('off')
        ax2.imshow(open_img.pixel_array, cmap=cmap_reversed)
        return fig2

    with dcol2:
        st.pyplot(img1())

    with dcol4:
        st.pyplot(img2())

    # Pylinac analyze
    drgs_demo = DRGS(image_paths=(file_drgs_demo,
                                  file_open_drgs_demo))
    drgs_demo.analyze(tolerance=tolerance1, segment_size_mm=(w1, h1))

    txt.title("Test results", 20, "#8C438D")
    dict_data_drgs = drgs_demo.results_data(as_dict=True)
    dcm_img = DicomImage(file_drgs_demo)
    result = drgs_demo.passed
    if str(result) == 'True':
        r1 = "PASS"

    elif str(result) == 'False':
        r1 = "FAIL"

    # Creating table results
    names = ["Test Results", "Source-to-Image Distance (mm)", "Beam Central Axis (CAX)", "Tolerance (%)",
             "Absolute mean deviation (%)", "Maximum deviation (%)"]

    values_drgs = [r1, str(dcm_img.sid), str(dcm_img.cax), str(dict_data_drgs['tolerance_percent']),
                   str(round(dict_data_drgs['abs_mean_deviation'], 4)),
                   str(round(dict_data_drgs['max_deviation_percent'], 4))]

    t = pd.DataFrame(values_drgs, columns=["Results"])
    t.insert(0, "Parameters", names, True)
    tab = t.round(decimals=4)
    fig, ax = table.render_mpl_table(tab)
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

    t_1, t_2, t_3 = st.columns([0.75, 1.5, 0.75])
    with t_2:
        st.image(buf, width=500, use_column_width=True)

    # Displaying analyzed images (with pylinac)
    col1_demo, col2_demo, col3_demo, col4_demo, col5_demo = st.columns([0.5, 4, 0.2, 4, 0.5])  # for DMLC and Open
    with col2_demo:
        bytes1 = io.BytesIO()
        drgs_demo._save_analyzed_subimage(bytes1, ImageType.DMLC, transparent=True)
        st.image(bytes1, caption='DMLC Image - DRGS')

    with col4_demo:
        bytes2 = io.BytesIO()
        drgs_demo._save_analyzed_subimage(bytes2, ImageType.OPEN, transparent=True)
        st.image(bytes2, caption="OPEN Image - OpenBeam")


    Col1_demo, Col2_demo, Col3_demo = st.columns([1, 3, 1])
    with Col2_demo:
        bytes3 = io.BytesIO()
        drgs_demo._save_analyzed_subimage(bytes3, ImageType.PROFILE, transparent=False)  # for PROFILE
        st.image(bytes3, caption="PROFILE Image")