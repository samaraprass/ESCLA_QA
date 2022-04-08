import base64
import streamlit as st
from pylinac import FieldAnalysis
from pylinac import Protocol, Centering, Interpolation, Normalization, Edge
from pathlib import Path
import pandas as pd
from io import BytesIO
import pages.core.text as text
import pages.core.table_function as table
import distutils.util
from pylinac.core.image import DicomImage

if 'names2' not in st.session_state:
    st.session_state['names2'] = None

if 'val2' not in st.session_state:
    st.session_state['val2'] = None

if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

def faepid(file):
    st.session_state['file_name'] = file.name

    st.session_state['my_file'] = FieldAnalysis(file)
    # Defining classes for analysis (Protocol, Centering, Normalization, Edge Detection and Interpolation)

    st.session_state['my_file'].analyze(edge_detection_method=st.session_state['edge'], edge_smoothing_ratio=st.session_state['edge_smoothing'], protocol=st.session_state['protocol'],
                        is_FFF=False, invert=distutils.util.strtobool(st.session_state['invert']),
                        ground=st.session_state['ground'], horiz_position=st.session_state['hor_p'], horiz_width=st.session_state['horiz_width'], in_field_ratio=st.session_state['in_field_ratio'],
                        interpolation=st.session_state['interpolation'], interpolation_resolution_mm=st.session_state['i_r'],
                        normalization_method=st.session_state['normalization'],
                        vert_position=st.session_state['vert_p'], vert_width=st.session_state['vert_width'], centering=st.session_state['centering'], hill_window_ratio=st.session_state['w_w'])
    #st.write(type(st.session_state['my_file']))
    #st.session_state['my_file'].save_analyzed_image('teste.png')
    load_img = DicomImage(file) #type - pylinac.core.image.DicomImage
    center = load_img.center # Return the center position of the image array as a Point
    array = load_img.array
    x = center.x 
    y = center.y
    v1 = array[int(x-0.5)][int(y-0.5)]
    v2 = array[int(x+0.5)][int(y+0.5)]
    value_center = (v1+v2)/2
    try:
        with st.spinner("Loading analysis..."):
            text.title("Your test results", 20, "#8C438D")
            dfa = st.session_state['my_file'].results_data(as_dict=True)
            st.session_state['names2'] = ['Pylinac Version', 'Date of Analysis', 'Protocol', 'Horizontal Symmetry (%)', 'Vertical Symmetry (%)', 'Horizontal Flatness (%)',
                'Vertical Flatness (%)', 'Center Pixel value (pylinac array)', 'Centering Method', 'Normalization Method', 'Interpolation Method', 'Edge Detection Method', 'Top Penumbra (mm)',
                'Bottom Penumbra (mm)', 'Left Penumbra (mm)', 'Right Penumbra (mm)', 'Geometric Center Index (x, y)', 'Beam Center Index (x, y)',
                'Vertical Field Size (mm)', 'Horizontal Field Size (mm)', 'Beam Center to Top (mm)', 'Beam Center to Bottom (mm)',
                'Beam Center to Left (mm)', 'Beam Center to Right (mm)', 'CAX to Top (mm)', 'CAX to Bottom (mm)', 'CAX to Left (mm)',
                'CAX to Right (mm)', 'Top position Index (x, y)', 'Top horizontal distance from CAX (mm)', 'Top vertical distance from CAX (mm)',
                'Top horizontal distance from Beam Center (mm)', 'Top vertical distance from Beam Center (mm)', 'Left Slope Percent (mm)',
                'Right Slope Percent (mm)', 'Top Slope Percent (mm)', 'Bottom Slope Percent (mm)', 'Top Penumbra Percent (mm)',
                'Bottom Penumbra Percent (mm)', 'Left Penumbra Percent (mm)', 'Right Penumbra Percent (mm)']
            l1 = [round(num, 4) for num in list(dfa["protocol_results"].values())]
            pixel_value = round(value_center, 4)
            l1.append(pixel_value)
            l2 = [round(num, 4) for num in list(dfa.values())[8:12]]
            l3 = [round(num, 4) for num in list(dfa.values())[29:33]]
            st.session_state['val2'] = list(dfa.values())[0:3] + l1 + list(dfa.values())[4:8] + l2 + list(dfa.values())[12:29] + l3 + list(dfa.values())[33:37]
            
            with st.container():
                Fa_Col1, Fa_Col2, Fa_Col3 = st.columns([2, 1.5, 2])
                with Fa_Col1:
                    st.write("")
                with Fa_Col2:
                    st.pyplot(st.session_state['my_file']._plot_image())
                with Fa_Col3:
                    st.write("")

            with st.container():
                fa_col1, fa_col2 = st.columns(2)
                with fa_col1:
                    # Table Function
                    t = pd.DataFrame(st.session_state['val2'], columns=["Values"])
                    t.insert(0, "Keys", st.session_state['names2'], True)
                    fig, ax = table.render_mpl_table(t)
                    buf = BytesIO()
                    fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)
                    st.image(buf, width=500, use_column_width=True)

                with fa_col2:
                    st.pyplot(st.session_state['my_file']._plot_horiz())

                    # legend centered
                    path = 'pages/modules/legend.png'

                    def img_to_bytes(img_path):
                        img_bytes = Path(img_path).read_bytes()
                        encoded = base64.b64encode(img_bytes).decode()
                        return encoded

                    header_html = "<img src='data:image/png;base64,{}' class='center'>".format(
                    img_to_bytes(path)
                    )
                    st.markdown(
                    header_html, unsafe_allow_html=True,
                    )
                    st.write('')
                    st.pyplot(st.session_state['my_file']._plot_vert())

    except Exception as ex:
        #st.write(ex)
        st.error('An error occured during analysis. Try changing some parameters in box above (i.e. MLC type, crop image, tolerance).' 
            ' Also, check if your image is a valid DICOM file.')
            
    return st.session_state['my_file'], st.session_state['names2'], st.session_state['val2'], st.session_state['file_name']