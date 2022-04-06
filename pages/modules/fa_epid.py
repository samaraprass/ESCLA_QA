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

# if 'my_file' not in st.session_state:
#     st.session_state['my_file'] = None

def faepid(file):
    st.session_state['file_name'] = file.name
    with st.expander("Click here to change the analysis paremeters"):
        reset = st.checkbox("Reset to default parameters", help="Click here if you prefer to reset to default parameters "
                                                                    "every time you apply new ones.")
        with st.form(key="FA form", clear_on_submit=reset):
            t_fa = 'Analysis parameters'
            text.body(t_fa, 18, "black")
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)

            with f_col1:
                p = st.selectbox("Protocol", ['None', 'Elekta', 'Varian', 'Siemens'], index=2,
                                    help="Varian: Flatness is defined by the difference across the field "
                                        "width and symmetry is defined as the point difference. Elekta: "
                                        "Flatness is defined by the ratio of max/min across the field values within the "
                                        "field width and symmetry is defined as the Point Difference Quotient."
                                        "Siemens: Flatness is defined by the variation across the field values within the "
                                        "field width and symmetry is defined as the ratio of area on each side about the "
                                        "CAX.")

                c = st.selectbox("Centering method", ['Manual', 'Beam Center', 'Geometric Center'],
                                    index=1, help="Manual: user specify  the position of the image that the profiles are taken"
                                                " from. Beam Center: Default for EPID images; looks for the field to find "
                                                "the approximate center along each axis and extracts the profiles and "
                                                "continues.")
                                                
                e = st.selectbox("Edge detection method", ['Full Width at Half Maximum', 'Inflection via Derivative',
                                                            'Inflection via Hill function'], index=1,
                                    help='Important for determining the field width and beam center '
                                        '(which is often used for symmetry). There are 3 detection strategies: FWHM, '
                                        'inflection via derivative, and inflection via the Hill/sigmoid/4PNLR function. '
                                        'FWHM works for flat beams. Inflection via Derivative (default for edge detection '
                                        'method is useful for both flat and FFF beams, but is not recommended for 2D device '
                                        'arrays.')

            with f_col2:
                n = st.selectbox("Normalization Method", ['None', 'Geometric Center', 'Beam Center', 'Max'], index=2)
                i = st.selectbox("Interpolation Method", ['None', 'Linear', 'Cubic Spline'], index=1)
                i_r = st.number_input("Interpolation Resolution (mm): ", min_value=0.0,
                                        max_value=2.0,
                                        value=0.1, help="Determine the amount of interpolation. E.g. a value of 0.1 will "
                                                        "resample the data to get data points 0.1mm apart.")

            with f_col3:
                vert_width = st.number_input("Vertical Width", min_value=0.0, max_value=1.0,
                                                value=0.0,
                                                help="The width ratio of the image to sample. E.g. at the default "
                                                    "of 0.0 a 1 pixel wide profile is extracted. Value 0.0 would "
                                                    "be 1 pixel wide and 1.0 would be the vertical image width.")
                horiz_width = st.number_input("Horizontal width", min_value=0.0, max_value=1.0, value=0.0,
                                                help="The width ratio of the image to sample. E.g. at the default of "
                                                    "0.0 a 1 "
                                                    "pixel wide profile is extracted. Value 0.0 would be 1 pixel wide "
                                                    "and "
                                                    "1.0 would be the horizontal image width.")

                in_field_ratio = st.number_input("Ratio of the field", min_value=0.0, max_value=1.0, value=0.8,
                                                    help="The ratio of the field width to use for protocol values. "
                                                        "E.g. 0.8 means use the 80% field width.")

            with f_col4:
                invert = st.selectbox("Invert the image", ["True", "False"], index=1,
                                        help="Setting this to True will override the default inversion. This is useful "
                                            "if "
                                            "pylinac's automatic inversion is incorrect.")

                ground = st.selectbox("Ground the image", ["True", "False"], index=0,
                                        help="Whether to ground the profile (set min value to 0). Helpful most of the "
                                            "time.")

                edge_smoothing = st.number_input("Edge Smoothing Ratio", min_value=0.000, step=0.001, max_value=1.000,
                                                    help='', format="%f", value=0.005)

            submit_button = st.form_submit_button(label='Apply')

        # 1) == manual & != hill
        if c == "Manual" and e != 'Inflection via Hill function':
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns([1.5, 2.5, 0.2, 2.5, 1.5])

            with m_col1:
                st.write("")

            with m_col2:
                with st.form(key="vert_p", clear_on_submit=reset):
                    vert_p = st.number_input("Vertical Position", min_value=0.0,
                                                max_value=1.0,
                                                value=0.5, help="The distance ratio of the image to sample. E.g. At the "
                                                                "default "
                                                                "of 0.5 the profile is extracted in the middle of the "
                                                                "image. "
                                                                "The 0.0 is at "
                                                                "the left edge of the image and 1.0 is at the right edge "
                                                                "of the "
                                                                "image. This value only applies when centering is "
                                                                "'Manual'.")
                    submit_button = st.form_submit_button(label='Apply')

            with m_col3:
                st.write("")

            with m_col4:
                with st.form(key="hor_p", clear_on_submit=reset):
                    hor_p = st.number_input("Horizontal Position", min_value=0.0, max_value=1.0, value=0.5,
                                                help="The distance ratio of the image to sample. E.g. At the default of "
                                                    "0.5 the "
                                                    "profile is extracted in the middle of the image. 0.0 is at the top "
                                                    "edge "
                                                    "of the image and 1.0 is at the bottom edge of the image.")

                    submit_button = st.form_submit_button(label='Apply')

            with m_col5:
                st.write("")
            w_w = 0.15

        # 2) != manual & = hill
        elif e == 'Inflection via Hill function' and c != "Manual":
            e_col1, e_col2, e_col3 = st.columns([1.5, 2, 1.5])
            with e_col2:
                with st.form(key="w_w", clear_on_submit=reset):
                    w_w = st.number_input("Hill window ratio", min_value=0.0, max_value=1.0, value=0.2,
                                            help="This is the size of the window (as a ratio) to use to fit the field "
                                                "edge to the Hill function. E.g. 0.2 will using a window centered about each"
                                                "edge "
                                                "with a width of 20% the size of the field width. Only applies when the edge"
                                                "detection is 'INFLECTION_HILL'.")
                    submit_button = st.form_submit_button(label='Apply')
                hor_p = 0.5
                vert_p = 0.5

        # 3) == manual & == hill
        elif e == 'Inflection via Hill function' and c == "Manual":
            with st.form(key="hill_manual", clear_on_submit=reset):
                ec_col1, ec_col2, ec_col3 = st.columns(3)
                with ec_col1:
                    vert_p = st.number_input("Vertical Position", min_value=0.0,
                                                max_value=1.0,
                                                value=0.5, help="The distance ratio of the image to sample. E.g. At the "
                                                                "default "
                                                                "of 0.5 the profile is extracted in the middle of the image. "
                                                                "The 0.0 is at "
                                                                "the left edge of the image and 1.0 is at the right edge "
                                                                "of the "
                                                                "image. This value only applies when centering is 'Manual'.")
                with ec_col2:
                    hor_p = st.number_input("Horizontal Position", min_value=0.0, max_value=1.0, value=0.5,
                                                help="The distance ratio of the image to sample. E.g. At the default of 0.5 the"
                                                    "profile is extracted in the middle of the image. 0.0 is at the top edge "
                                                    "of the image and 1.0 is at the bottom edge of the image."
                                                    "This value only applies when centering is 'Manual'.")

                with ec_col3:
                        w_w = st.number_input("Hill window ratio", min_value=0.0, max_value=1.0, value=0.2,
                                            help="This is the size of the window (as a ratio) to use to fit the field "
                                                "edge to the Hill function. E.g. 0.2 will using a window centered about each"
                                                "edge "
                                                "with a width of 20% the size of the field width. Only applies when the edge"
                                                "detection is 'INFLECTION_HILL'.")
                submit_button = st.form_submit_button(label='Apply')

    # 4) != manual & != hill
    if e != 'Inflection via Hill function' and c != "Manual":
        hor_p = 0.5
        vert_p = 0.5
        w_w = 0.15

    # Defining Protocol
    if p == "Varian":
        protocol = Protocol.VARIAN

    elif p == "Elekta":
        protocol = Protocol.ELEKTA

    elif p == "Siemens":
        protocol = Protocol.SIEMENS

    # Defining Centering
    if c == "Manual":
        centering = Centering.MANUAL

    elif c == "Beam Center":
        centering = Centering.BEAM_CENTER

    elif c == "Geometric Center":
        centering = Centering.GEOMETRIC_CENTER

    # Defining Normalization
    if n == "None":
        normalization = Normalization.NONE

    elif n == "Geometric Center":
        normalization = Normalization.GEOMETRIC_CENTER

    elif n == "Beam Center":
        normalization = Normalization.BEAM_CENTER

    elif n == "Max":
        normalization = Normalization.MAX

    # Defining Edge
    if e == "Full Width at Half Maximum":
        edge = Edge.FWHM

    elif e == "Inflection via Derivative":
        edge = Edge.INFLECTION_DERIVATIVE

    elif e == "Inflection via Hill function":
        edge = Edge.INFLECTION_HILL

    # Defining Interpolation
    if i == "None":
        interpolation = Interpolation.NONE

    elif i == "Linear":
        interpolation = Interpolation.LINEAR

    elif i == "Cubic Splie":
        interpolation = Interpolation.SPLINE

    st.session_state['my_file'] = FieldAnalysis(file)
    # Defining classes for analysis (Protocol, Centering, Normalization, Edge Detection and Interpolation)

    st.session_state['my_file'].analyze(edge_detection_method=edge, edge_smoothing_ratio=edge_smoothing, protocol=protocol,
                        is_FFF=False, invert=distutils.util.strtobool(invert),
                        ground=ground, horiz_position=hor_p, horiz_width=horiz_width, in_field_ratio=in_field_ratio,
                        interpolation=interpolation, interpolation_resolution_mm=i_r,
                        normalization_method=normalization,
                        vert_position=vert_p, vert_width=vert_width, centering=centering, hill_window_ratio=w_w)
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
                path = 'legend.png'

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

    return st.session_state['my_file'], st.session_state['names2'], st.session_state['val2'], st.session_state['file_name']