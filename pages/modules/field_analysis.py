import streamlit as st
import pages.core.text as text
import pages.modules.fa_epid as FA_EPID
from st_btn_select import st_btn_select
import pages.core.pdf_new as PDF
import chime
from datetime import datetime
from deta import Deta
import pages.core.database as DB
from pylinac.core.image import DicomImage
from pylinac import DeviceFieldAnalysis, Protocol, Centering, Interpolation, Normalization, Edge
import pytz

if 'test2' not in st.session_state:
    st.session_state['test2'] = None

if 'names' not in st.session_state:
    st.session_state['names'] = None

if 'values' not in st.session_state:
    st.session_state['values'] = None

if 'f_name' not in st.session_state:
    st.session_state['f_name'] = None

if 'file_field_analysis' not in st.session_state:
    st.session_state['file_field_analysis'] = None

if 'p' not in st.session_state:
    st.session_state['p'] = None

if 'protocol' not in st.session_state:
    st.session_state['protocol'] = None

if 'c' not in st.session_state:
    st.session_state['c'] = None

if 'centering' not in st.session_state:
    st.session_state['centering'] = None

if 'e' not in st.session_state:
    st.session_state['e'] = None

if 'edge' not in st.session_state:
    st.session_state['edge'] = None

if 'n' not in st.session_state:
    st.session_state['n'] = None

if 'normalization' not in st.session_state:
    st.session_state['normalization'] = None

if 'i' not in st.session_state:
    st.session_state['i'] = None

if 'interpolation' not in st.session_state:
    st.session_state['interpolation'] = None

if 'i_r' not in st.session_state:
    st.session_state['i_r'] = None

if 'vert_width' not in st.session_state:
    st.session_state['vert_width'] = None

if 'horiz_width' not in st.session_state:
    st.session_state['horiz_width'] = None

if 'in_field_ratio' not in st.session_state:
    st.session_state['in_field_ratio'] = None

if 'invert' not in st.session_state:
    st.session_state['invert'] = None

if 'ground' not in st.session_state:
    st.session_state['ground'] = None

if 'edge_smoothing' not in st.session_state:
    st.session_state['edge_smoothing'] = None

if 'vert_p' not in st.session_state:
    st.session_state['vert_p'] = None

if 'hor_p' not in st.session_state:
    st.session_state['hor_p'] = None

if 'w_w' not in st.session_state:
    st.session_state['w_w'] = None



def FA():
    st.session_state['file_field_analysis'] = st.file_uploader("Upload image for field analysis", type=["DCM"])

    with st.expander(" 📊 Click here to change the analysis paremeters"):
        reset = st.checkbox("Reset to default parameters", help="Click here if you prefer to reset to default parameters "
                                                                    "every time you apply new ones.")
        with st.form(key="FA form", clear_on_submit=reset):
            t_fa = 'Analysis parameters'
            text.body(t_fa, 18, "black")
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)

            with f_col1:
                st.session_state['p'] = st.selectbox("Protocol", ['None', 'Elekta', 'Varian', 'Siemens'], index=2,
                                    help="Varian: Flatness is defined by the difference across the field "
                                        "width and symmetry is defined as the point difference. Elekta: "
                                        "Flatness is defined by the ratio of max/min across the field values within the "
                                        "field width and symmetry is defined as the Point Difference Quotient."
                                        "Siemens: Flatness is defined by the variation across the field values within the "
                                        "field width and symmetry is defined as the ratio of area on each side about the "
                                        "CAX.")

                st.session_state['c'] = st.selectbox("Centering method", ['Manual', 'Beam Center', 'Geometric Center'],
                                    index=1, help="Manual: user specify  the position of the image that the profiles are taken"
                                                " from. Beam Center: Default for EPID images; looks for the field to find "
                                                "the approximate center along each axis and extracts the profiles and "
                                                "continues.")
                                                
                st.session_state['e'] = st.selectbox("Edge detection method", ['Full Width at Half Maximum', 'Inflection via Derivative',
                                                            'Inflection via Hill function'], index=1,
                                    help='Important for determining the field width and beam center '
                                        '(which is often used for symmetry). There are 3 detection strategies: FWHM, '
                                        'inflection via derivative, and inflection via the Hill/sigmoid/4PNLR function. '
                                        'FWHM works for flat beams. Inflection via Derivative (default for edge detection '
                                        'method is useful for both flat and FFF beams, but is not recommended for 2D device '
                                        'arrays.')

            with f_col2:
                st.session_state['n'] = st.selectbox("Normalization Method", ['None', 'Geometric Center', 'Beam Center', 'Max'], index=2)
                st.session_state['i'] = st.selectbox("Interpolation Method", ['None', 'Linear', 'Cubic Spline'], index=1)
                st.session_state['i_r'] = st.number_input("Interpolation Resolution (mm): ", min_value=0.0,
                                        max_value=2.0,
                                        value=0.1, help="Determine the amount of interpolation. E.g. a value of 0.1 will "
                                                        "resample the data to get data points 0.1mm apart.")

            with f_col3:
                st.session_state['vert_width'] = st.number_input("Vertical Width", min_value=0.0, max_value=1.0,
                                                value=0.0,
                                                help="The width ratio of the image to sample. E.g. at the default "
                                                    "of 0.0 a 1 pixel wide profile is extracted. Value 0.0 would "
                                                    "be 1 pixel wide and 1.0 would be the vertical image width.")
                st.session_state['horiz_width'] = st.number_input("Horizontal width", min_value=0.0, max_value=1.0, value=0.0,
                                                help="The width ratio of the image to sample. E.g. at the default of "
                                                    "0.0 a 1 "
                                                    "pixel wide profile is extracted. Value 0.0 would be 1 pixel wide "
                                                    "and "
                                                    "1.0 would be the horizontal image width.")

                st.session_state['in_field_ratio'] = st.number_input("Ratio of the field", min_value=0.0, max_value=1.0, value=0.8,
                                                    help="The ratio of the field width to use for protocol values. "
                                                        "E.g. 0.8 means use the 80% field width.")

            with f_col4:
                st.session_state['invert'] = st.selectbox("Invert the image", ["True", "False"], index=1,
                                        help="Setting this to True will override the default inversion. This is useful "
                                            "if "
                                            "pylinac's automatic inversion is incorrect.")

                st.session_state['ground'] = st.selectbox("Ground the image", ["True", "False"], index=0,
                                        help="Whether to ground the profile (set min value to 0). Helpful most of the "
                                            "time.")

                st.session_state['edge_smoothing'] = st.number_input("Edge Smoothing Ratio", min_value=0.000, step=0.001, max_value=1.000,
                                                    help='', format="%f", value=0.005)

            submit_button = st.form_submit_button(label='Apply')

        # 1) == manual & != hill
        if st.session_state['c'] == "Manual" and st.session_state['e'] != 'Inflection via Hill function':
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns([1.5, 2.5, 0.2, 2.5, 1.5])
            with m_col2:
                with st.form(key="vert_p", clear_on_submit=reset):
                    st.session_state['vert_p'] = st.number_input("Vertical Position", min_value=0.0,
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
            with m_col4:
                with st.form(key="hor_p", clear_on_submit=reset):
                    st.session_state['hor_p'] = st.number_input("Horizontal Position", min_value=0.0, max_value=1.0, value=0.5,
                                                help="The distance ratio of the image to sample. E.g. At the default of "
                                                    "0.5 the "
                                                    "profile is extracted in the middle of the image. 0.0 is at the top "
                                                    "edge "
                                                    "of the image and 1.0 is at the bottom edge of the image.")

                    submit_button = st.form_submit_button(label='Apply')
            st.session_state['w_w'] = 0.15

        # 2) != manual & = hill
        elif st.session_state['e'] == 'Inflection via Hill function' and st.session_state['c'] != "Manual":
            e_col1, e_col2, e_col3 = st.columns([1.5, 2, 1.5])
            with e_col2:
                with st.form(key="w_w", clear_on_submit=reset):
                    st.session_state['w_w'] = st.number_input("Hill window ratio", min_value=0.0, max_value=1.0, value=0.2,
                                            help="This is the size of the window (as a ratio) to use to fit the field "
                                                "edge to the Hill function. E.g. 0.2 will using a window centered about each"
                                                "edge "
                                                "with a width of 20% the size of the field width. Only applies when the edge"
                                                "detection is 'INFLECTION_HILL'.")
                    submit_button = st.form_submit_button(label='Apply')
                st.session_state['hor_p'] = 0.5
                st.session_state['vert_p'] = 0.5

        # 3) == manual & == hill
        elif st.session_state['e'] == 'Inflection via Hill function' and st.session_state['c'] == "Manual":
            with st.form(key="hill_manual", clear_on_submit=reset):
                ec_col1, ec_col2, ec_col3 = st.columns(3)
                with ec_col1:
                    st.session_state['vert_p'] = st.number_input("Vertical Position", min_value=0.0,
                                                max_value=1.0,
                                                value=0.5, help="The distance ratio of the image to sample. E.g. At the "
                                                                "default "
                                                                "of 0.5 the profile is extracted in the middle of the image. "
                                                                "The 0.0 is at "
                                                                "the left edge of the image and 1.0 is at the right edge "
                                                                "of the "
                                                                "image. This value only applies when centering is 'Manual'.")
                with ec_col2:
                    st.session_state['hor_p'] = st.number_input("Horizontal Position", min_value=0.0, max_value=1.0, value=0.5,
                                                help="The distance ratio of the image to sample. E.g. At the default of 0.5 the"
                                                    "profile is extracted in the middle of the image. 0.0 is at the top edge "
                                                    "of the image and 1.0 is at the bottom edge of the image."
                                                    "This value only applies when centering is 'Manual'.")

                with ec_col3:
                    st.session_state['w_w'] = st.number_input("Hill window ratio", min_value=0.0, max_value=1.0, value=0.2,
                                            help="This is the size of the window (as a ratio) to use to fit the field "
                                                "edge to the Hill function. E.g. 0.2 will be using a window centered about each"
                                                " edge "
                                                "with a width of 20% the size of the field width. Only applies when the edge"
                                                "detection is 'INFLECTION_HILL'.")
                submit_button = st.form_submit_button(label='Apply')

    # 4) != manual & != hill
    if st.session_state['e'] != 'Inflection via Hill function' and st.session_state['c'] != "Manual":
        st.session_state['hor_p'] = 0.5
        st.session_state['vert_p'] = 0.5
        st.session_state['w_w'] = 0.15

    # Defining Protocol
    if st.session_state['p'] == "Varian":
        st.session_state['protocol'] = Protocol.VARIAN

    elif st.session_state['p'] == "Elekta":
        st.session_state['protocol'] = Protocol.ELEKTA

    elif st.session_state['p'] == "Siemens":
        st.session_state['protocol'] = Protocol.SIEMENS

    # Defining Centering
    if st.session_state['c'] == "Manual":
        st.session_state['centering'] = Centering.MANUAL

    elif st.session_state['c'] == "Beam Center":
        st.session_state['centering'] = Centering.BEAM_CENTER

    elif st.session_state['c'] == "Geometric Center":
        st.session_state['centering'] = Centering.GEOMETRIC_CENTER

    # Defining Normalization
    if st.session_state['n'] == "None":
        st.session_state['normalization'] = Normalization.NONE

    elif st.session_state['n'] == "Geometric Center":
        st.session_state['normalization'] = Normalization.GEOMETRIC_CENTER

    elif st.session_state['n'] == "Beam Center":
        st.session_state['normalization'] = Normalization.BEAM_CENTER

    elif st.session_state['n'] == "Max":
        st.session_state['normalization'] = Normalization.MAX

    # Defining Edge
    if st.session_state['e'] == "Full Width at Half Maximum":
        st.session_state['edge'] = Edge.FWHM

    elif st.session_state['e'] == "Inflection via Derivative":
        st.session_state['edge'] = Edge.INFLECTION_DERIVATIVE

    elif st.session_state['e'] == "Inflection via Hill function":
        st.session_state['edge'] = Edge.INFLECTION_HILL

    # Defining Interpolation
    if st.session_state['i'] == "None":
        st.session_state['interpolation'] = Interpolation.NONE

    elif st.session_state['i'] == "Linear":
        st.session_state['interpolation'] = Interpolation.LINEAR

    elif st.session_state['i'] == "Cubic Spline":
        st.session_state['interpolation'] = Interpolation.SPLINE
    st.markdown("---")

    if st.session_state['file_field_analysis'] is None:
        text.title("Choose your files to start using this app!", 20, "#8C438D")

    else:
        fa1, fa2, fa3 = st.columns([1.5, 2, 0.88])
        with fa2:
            subpages = st_btn_select(("1. PERFORM TEST", "2. CREATE PDF REPORT"), nav=False)
    
        if subpages == "1. PERFORM TEST":
            try:
                st.session_state['test2'], st.session_state['names'], st.session_state['values'], st.session_state['f_name']= FA_EPID.faepid(st.session_state['file_field_analysis'])

                with st.spinner("Database inserting/uploading..."):
                    if st.session_state['authentication_status'] is not None:
                        t_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                        t = t_timezone.replace(tzinfo=None)
                        date_table = (str(t.day) + '/' + str(t.month) + '/' + str(t.year) + ' ' + str(t.hour) + ':' + 
                                                str(t.minute) + ':' + str(t.second))

                        # Deta Database Connection
                        data_connection = Deta(st.secrets['database']['data_key'])
                        user_test = st.session_state['username'] + 'Field_Analysis'
                        db = data_connection.Base(user_test)
                        fetch_res = db.fetch()

                        # INFO from DICOM images
                        dcm_read = DicomImage(st.session_state['file_field_analysis'])
                        date = dcm_read.metadata.AcquisitionDate
                        date_time_obj = datetime.strptime(date, '%Y%m%d')
                        date_obj = date_time_obj.date()
                        date_linac = str(date_obj) 

                        # Database keys list
                        keys = [] # storing keys from database to list
                        for i in fetch_res.items:
                            keys.append(i['key'])

                        # Variables to db function
                        horiz_symmetry = st.session_state['values'][3]
                        vert_symmetry = st.session_state['values'][4]
                        horiz_flatness = st.session_state['values'][5]
                        vert_flatness = st.session_state['values'][6]
                        center_pixel = st.session_state['values'][7]
                        center_method = st.session_state['values'][8]
                        normal_method = st.session_state['values'][9]
                        interpol_method = st.session_state['values'][10]
                        edge_method = st.session_state['values'][11]
                        top_penum = st.session_state['values'][12]
                        bottom_penum = st.session_state['values'][13]
                        left_penum = st.session_state['values'][14]
                        right_penum = st.session_state['values'][15]
                        vert_fs = st.session_state['values'][18]
                        horiz_fs = st.session_state['values'][19]
                        cax_top = st.session_state['values'][24]
                        cax_bottom = st.session_state['values'][25]
                        cax_left = st.session_state['values'][26]
                        cax_right = st.session_state['values'][27]
                        analy_date = date_table
                        key = st.session_state['file_field_analysis'].name

                        # Inserting in database
                        if key in keys:
                            chime.info()
                            st.warning("Already exist analysis results for this image on database. For saving new analysis, press button bellow.")
                            bs = st.button("Save")
                            if bs:
                                DB.database_update_fa(db, horiz_symmetry, vert_symmetry, horiz_flatness, vert_flatness, center_pixel, center_method, normal_method, interpol_method, edge_method,
                                                    top_penum, bottom_penum, left_penum, right_penum, vert_fs, horiz_fs, cax_top, cax_bottom, cax_left, cax_right, 
                                                    analy_date, date_linac, key)
                                st.success(f"New analysis of {key} saved")
                                chime.success()

                        # Uploading database
                        if key not in keys:
                            DB.database_insert_fa(db, horiz_symmetry, vert_symmetry, horiz_flatness, vert_flatness, center_pixel, center_method, normal_method, interpol_method, edge_method,
                                                top_penum, bottom_penum, left_penum, right_penum, vert_fs, horiz_fs, cax_top, cax_bottom, cax_left, cax_right, 
                                                analy_date, date_linac, key)
                            st.success(f"Analysis results of {key} saved")
                            chime.success()  
                             
            except Exception as error:
                # st.write(error)
                st.error('An error occured during analysis. Try changing some parameters in box above (i.e. MLC type, crop image, tolerance).' 
                    ' Also, check if your image is a valid DICOM file.') 

        
        elif subpages == "2. CREATE PDF REPORT":
            st.subheader("PDF Report")
            with st.form(key="pdf_report"):
                pdf1, pdf2 = st.columns(2)
                with pdf1:
                    test_name = st.text_input("Test name", value="Field Analysis")

                    t_name = "Report - " + test_name

                    institution = st.text_input("Institution name")
                                    
                with pdf2:
                    author = st.text_input("Author name")

                    unit = st.text_input("Unit model name")
                                
                pdf_1, pdf_2, pdf_3 = st.columns([1,2,1])
                with pdf_2:
                    file_name = st.text_input("Choose the report file name")

                submit_button0 = st.form_submit_button(label='Apply')

            if submit_button0:
                with st.spinner("Creating your PDF report..."):
                    pdf = PDF.pdf_fa(t_name, institution, author, unit, 
                                        st.session_state['test2'], st.session_state['names'], 
                                        st.session_state['values'], st.session_state['f_name'])

                    html_pf = PDF.create_download_link(pdf.output(dest="S"), file_name)
                chime.theme('mario')
                chime.success()
                st.success("Your PDF report is ready!")
                st.markdown(html_pf, unsafe_allow_html=True)