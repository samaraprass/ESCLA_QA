import streamlit as st
from pylinac import DRMLC
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


def vmat_demo_dmlc():
    # DEMONSTRATION DRMLC
    reset2 = st.checkbox("Reset to default parameters", key="r2",
                          help="Click here if you prefer to reset to default parameters "
                               "every time you apply new ones.")
    if reset2:
        r = True
    else:
        r = False

    with st.form(key="drmlc_demo", clear_on_submit=r):
        t_drgs = 'Analysis parameters'
        txt.body(t_drgs, 18, "black")
        col1, col2, col3 = st.columns(3)
        with col1:
            tolerance2 = st.number_input("Choose your tolerance value", min_value=0.0, max_value=8.0, value=1.5,
                                         step=0.5,
                                         help="The tolerance of the sample deviations in percent. Default is 1.5. "
                                              "Must be between 0 and 8.")
            lru_cache(tolerance2)

        with col2:
            w2 = st.number_input("Set the width of the ROI segments in mm", min_value=0, max_value=1000, value=5,
                                 help="Integer value")
            lru_cache(w2)

        with col3:
            h2 = st.number_input("Set the height of the ROI segments in mm", min_value=0, max_value=1000, value=100,
                                 help="Integer value")
            lru_cache(h2)

        submit_button = st.form_submit_button(label='Apply')

    txt.title("Demo Images", 20, "#8C438D")
    drmlc_dmlc = "C:\\Users\\samar\\PycharmProjects\\pylinac_deploy\\pages\\home\\modules\\demo\\DRMLC_dmlc.dcm"
    drmlc_open = "C:\\Users\\samar\\PycharmProjects\\pylinac_deploy\\pages\\home\\modules\\demo\\DRMLC_open.dcm"
    DRMLC_dmlc = pydicom.dcmread(drmlc_dmlc)
    DRMLC_open = pydicom.dcmread(drmlc_open)

    drmlc_demo = DRMLC(image_paths=(drmlc_dmlc,
                                    drmlc_open))
    drmlc_demo.analyze(tolerance=tolerance2, segment_size_mm=(w2, h2))

    dict_data = drmlc_demo.results_data(as_dict=True)
    dcm_img_drmlc = DicomImage(drmlc_dmlc) #calcular sid e cax
    result = drmlc_demo.passed

    d_col1, d_col2, d_col3, d_col4, d_col5 = st.columns([1.1, 2, 1.1, 2, 1.1])

    with d_col2:
        fig, ax3 = plt.subplots()  # https://discuss.byteslit.io/t/wordcloud-error/18672
        cmap_reversed = matplotlib.cm.get_cmap('gray_r')
        ax3.imshow(DRMLC_dmlc.pixel_array, cmap=cmap_reversed)
        ax3.axis("off")
        st.pyplot(fig)

    with d_col4:
        fig2, ax4 = plt.subplots()
        ax4.imshow(DRMLC_open.pixel_array, cmap=cmap_reversed)
        ax4.axis("off")
        st.pyplot(fig2)

    txt.title("Test Results", 20, "#8C438D")

    if str(result) == 'True':
        r2 = "PASS"

    elif str(result) == 'False':
        r2 = "FAIL"

    names = ["Test Results", "Source-to-Image Distance (mm)", "Beam Central Axis (CAX)", "Tolerance (%)",
             "Absolute mean deviation (%)", "Maximum deviation (%)"]

    values_drmlc = [r2, str(dcm_img_drmlc.sid), str(dcm_img_drmlc.cax), str(dict_data['tolerance_percent']),
                    str(round(dict_data['abs_mean_deviation'], 4)),
                    str(round(dict_data['max_deviation_percent'], 4))]

    t = pd.DataFrame(values_drmlc, columns=["Results"])
    t.insert(0, "Parameters", names, True)
    tab = t.round(decimals=4)
    fig, ax = table.render_mpl_table(tab)
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

    t1, t2, t3 = st.columns([0.75, 1.5, 0.75])

    with t2:
        st.image(buf, width=500, use_column_width=True)

    col1demo, col2demo, col3demo, col4demo, col5demo = st.columns([0.5, 3, 0.2, 3, 0.5])
    with col2demo:
        bytes1 = io.BytesIO()
        drmlc_demo._save_analyzed_subimage(bytes1, ImageType.DMLC, transparent=True)
        st.image(bytes1, caption='DMLC Image - DRMLC')

    with col4demo:
        bytes2 = io.BytesIO()
        drmlc_demo._save_analyzed_subimage(bytes2, ImageType.OPEN, transparent=True)
        st.image(bytes2, caption="OPEN Image - OpenBeam")

    Col1demo, Col2demo, Col3demo = st.columns([1,2,1])

    with Col2demo:
        bytes3 = io.BytesIO()
        drmlc_demo._save_analyzed_subimage(bytes3, ImageType.PROFILE, transparent=False)
        st.image(bytes3, caption="PROFILE Image")
