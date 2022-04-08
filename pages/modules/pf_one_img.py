import streamlit as st
from pylinac.core.image import DicomImage
from pylinac.core.decorators import lru_cache
import pages.core.text as text
from pylinac.picketfence import MLC
from datetime import datetime
from st_btn_select import st_btn_select
import pages.modules.pf_analysis as PF_function
import pages.core.pdf_new as PDF
import chime
from deta import Deta
import pages.core.database as DB
import pytz

if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None

if 'r1' not in st.session_state:
    st.session_state['r1'] = None

def pf_one():
    pf = st.file_uploader("Upload your Picket Fence file", key='pf_file', accept_multiple_files=False, type=['DCM'], 
                                help="The image must be a DICOM image acquired via the EPID.")
    
    # User parameters input
    with st.expander("📊 Click here to change Picket Fence and analysis parameters"):
        with st.form(key="pf"):
            t_drgs = "Picket Fence Parameters"
            text.body(t_drgs, 18, "black")
            pf1, pf2, pf3 = st.columns([2, 0.1, 2])
            with pf1:
                filter = st.selectbox("Apply Filter", [None, 'Median'], help="If None (default), no filtering will be "
                                                                                    "done to the image. If an integer, will "
                                                                                    "size "
                                                                                    "'filter'. Choose 'Median' in options below "
                                                                                    "to customize this.")

                st.session_state['log'] = st.selectbox("Choose True if you have a log file", [None, 'True'])

                
            with pf3:
                st.session_state['file_name'] = st.selectbox("Use filename", [False, True], help="If False (default), "
                                                                            "no action will be performed. If True, the "
                                                                            "filename will be searched for keywords that "
                                                                            "describe the gantry and/or collimator angle. "
                                                                            "For example, if set to True and the file "
                                                                            "name was 'PF_gantry45.dcm' the gantry would "
                                                                            "be interpreted as being at 45 degrees.")

                st.session_state['ml_c'] = st.selectbox("Choose the MLC type", ["Millennium", 'HD Millennium', 'Halcyon Distal',
                                                        'Halcyon Proximal'], index=1)

            pf_1, pf_2, pf_3 = st.columns([1, 1.5, 1])
            with pf_2:
                st.session_state['crop'] = st.number_input("Crop (mm)", help="The number of mm to crop from all edges.", min_value=0, value=3,
                                    max_value=100)

            # CONDITIONS: LOG & FILTER FORMS
            # only log 
            if st.session_state['log'] == "True" and filter != "Median":
                with pf_2:
                    st.session_state['log'] = st.file_uploader("Upload your log file", type=["BIN"], help="You can load a "
                                                                                                        "machine log "
                                                                                                        "along with "
                                                                                                        "your picket "
                                                                                                        "fence image")
            # log and filter 
            elif st.session_state['log'] == "True" and filter == "Median":
                with pf_2:
                    st.session_state['log'] = st.file_uploader("Upload your log file", type=["BIN"], help="You can load a "
                                                                                                        "machine log "
                                                                                                        "along with "
                                                                                                        "your picket "
                                                                                                        "fence image")

                    filter = st.number_input("Choose size of the filter", min_value=1, step=1, max_value=13, key='filter')

            # only filter 
            elif st.session_state['log'] != "True" and filter == "Median":
                with pf_2:
                    filter = st.number_input("Choose size of the filter", min_value=1, step=1, max_value=13, key='filter')

            st.session_state['Filter'] = filter

            submit_button1 = st.form_submit_button(label='Apply')

    
        # Setting MLC's Type
        if st.session_state['ml_c'] == "Millennium":
            st.session_state['ml_c'] = MLC.MILLENNIUM
        
        if st.session_state['ml_c'] == "HD Millennium":
            st.session_state['ml_c'] = MLC.HD_MILLENNIUM

        if st.session_state['ml_c'] == "Halcyon Distal":
            st.session_state['ml_c'] = MLC.HALCYON_DISTAL
        
        if st.session_state['ml_c'] == "Halcyon Proximal":
            st.session_state['ml_c'] = MLC.HALCYON_PROXIMAL
    

        with st.form(key="pf_a"):
            t_drgs = 'Analysis Parameters'
            text.body(t_drgs, 18, "black")
            pf_a1, pf_a2, pf_c3 = st.columns(3)
            with pf_a1:
                st.session_state['tolerance'] = st.number_input("Tolerance", min_value=0.0, max_value=5.0, step=0.1, value=0.5,
                                            help="The tolerance of difference in mm between an MLC pair position and "
                                                "the picket fit line")

                st.session_state['action_t'] = st.selectbox("Action tolerance value. None is default",
                                        [None, "True"], help="This value is usually meant "
                                                            "to indicate that a physicist should take an 'action' to "
                                                            "reduce the error, "
                                                            "but should not stop treatment.")

                st.session_state['number_p'] = st.selectbox("Number of pickets.", [None, 'Add Manually'], help="The number of pickets in the image. "
                                        "A helper parameter to limit the total number of pickets, only needed if "
                                        "analysis is catching more pickets than there really are.")

                st.session_state['sag_ad'] = st.number_input("Correct EPID sag (mm)", min_value=0.0, max_value=10.0, value=0.0,step=0.1,help="Pylinac assumes a perfect panel. If image provided has sag (older linacs)," 
                                        " the analysis will not be centered exactly on the MLC leaves. For correction, simply pass the EPIF sag in mm."
                                        " For Up-Down picket images, positive value moves image down and negative value moves image up."
                                        " For Left-Right picket images, positive value moves image to left and negative to right orientation. Default is 0.0 mm.")
            with pf_a2:
                st.session_state['orient'] = st.selectbox("Image orientation", [None, 'Up-Down', 'Left-Right'], help="For automatic detection (default), choose 'None'."
                                                            " If detection is incorrect, choose directly here the right orientation.")
                
                st.session_state['inv']  = st.selectbox("Automatic detection of image inversion", [False, True], help="'False' option (default): automatic detection"
                                    " of image inversion. 'True' option: image inversion is reversed from the automatic detection; useful for runtime errors")
                
                st.session_state['leaf_w'] = st.number_input("Leaf Analysis Width Ratio", min_value=0.1, max_value=5.0, value=0.4, step=0.1, help="Parameter for ratio of the leaf"
                                        " as part of the evaluation. Helps to avoid tongue and groove effect. E.g. for a ratio=0.5, the center"
                                        " half of the leaf will be used.")
                
                st.session_state['picket_spacing'] = st.selectbox("Spacing between pickets", [None, "Add Manually"], help="'None': spacing is automatically determined. " 
                                                                                                    " 'Add Manually': specify the number of PIXELS the pickets are apart.")
                
            with pf_c3:
                st.session_state['height_threshold'] = st.number_input("Height threshold for MLC peak", min_value=0.0, max_value=0.9, value=0.5, help="Height threshold for MLC peak to be"
                                                                                                                                " considered a picket. If not all leaves are being caught,"
                                                                                                                                " try lowing this parameter. ")

                st.session_state['edge_threshold'] = st.number_input("Edge threshold for MLC leaf", min_value=1.2, max_value=10.0, value=1.5, help="The threshold of pixel value standard deviation within the analysis" 
                                                                                                                        " window of the MLC leaf to be considered a full leaf. This is how pylinac"
                                                                                                                        " removes MLCs that are eclipsed by the jaw. This also is how to omit or catch"
                                                                                                                        " leaves at the edge of the field. Raise to catch more edge leaves.")
                
                st.session_state['peak_sort'] = st.selectbox("Method for detecting the peaks", ["peak_heights", "prominences"], help="Usually not needed unless the wrong number of pickets have been detected.")


                st.session_state['required_prominence'] = st.number_input("Height of the picket", min_value=0.0, max_value=0.5, value=0.2, help='The required height of the picket to be considered a peak.')

            if st.session_state['number_p'] is not None:
                at1, at2, at3 = st.columns([1, 2, 1])
                with at2:
                    st.session_state['number_p'] = st.number_input("Number of pickets.", help="The number of pickets in the image. "
                                        "A helper parameter to limit the total number of pickets, only needed if "
                                        "analysis is catching more pickets than there really are.")
            
            if st.session_state['action_t'] == "True" and st.session_state['picket_spacing'] == "Add Manually":
                at1, at2, at3 = st.columns([1, 2, 1])
                with at2:
                    at = st.session_state['tolerance'] - 0.1
                    st.session_state['action_t'] = st.number_input("Choose action tolerance", min_value=0.0, max_value=at, step=0.10,
                                                value=at, help="If None (default), no action tolerance is set or compared"
                                                " to. If an int or float, the MLC pair measurement is also compared to"
                                                " this tolerance. Must be lower than tolerance.")
                    st.session_state['picket_spacing'] = st.number_input("Spacing between pickets", min_value=0.0, max_value=10.0, value=0.5, help="Specify the number of PIXELS the pickets are apart")
            
            if st.session_state['action_t'] == "True" and st.session_state['picket_spacing'] != "Add Manually":
                at1, at2, at3 = st.columns([1, 2, 1])
                with at2:
                    at = st.session_state['tolerance'] - 0.1
                    st.session_state['action_t'] = st.number_input("Choose action tolerance", min_value=0.0, max_value=at, step=0.10,
                                                value=at, help="If None (default), no action tolerance is set or compared"
                                                " to. If an int or float, the MLC pair measurement is also compared to"
                                                " this tolerance. Must be lower than tolerance.")

            if st.session_state['action_t'] != "True" and st.session_state['picket_spacing'] == "Add Manually":
                at1, at2, at3 = st.columns([1, 2, 1])
                with at2:
                    st.session_state['picket_spacing'] = st.number_input("Spacing between pickets", min_value=0.0, max_value=10.0, value=0.5, help="Specify the number of PIXELS the pickets are apart")
            

            submit_button = st.form_submit_button(label='Apply')
    
        
    if pf == None:
        st.markdown("---")
        text.title("Choose your files to start using this app!", 20, "#8C438D")

    else:
        pf1_1, pf1_2, pf1_3 = st.columns([1.8,3,0.5])
        with pf1_2:
            subpages = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'))
        if subpages == '1. PERFORM TEST':
            st.markdown("---")
            try:
                with st.spinner('Loading Analysis...'):
                    #Input Image
                    PF_function.input_image(pf)
                    st.session_state['i1'], st.session_state['i2'], st.session_state['i3'], st.session_state['j'], st.session_state['r1'] = PF_function.image_analysis(pf)
                    st.session_state['name0'] = "Analysis result - " + pf.name
                    text.title(st.session_state['name0'], 15, "#8C438D")
                    # Analysis Images
                    a1, a2 = st.columns(2)
                    with a1:
                        st.markdown("")
                        st.markdown("")
                        st.pyplot(st.session_state['j'].plot_analyzed_image(mlc_peaks=True, overlay=True))
                    with a2:
                        st.markdown("")
                        st.markdown("")
                        st.image(st.session_state['i1'], width=500, use_column_width=True)
                
                # Date Analysis (app)
                date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                date_i = str(date_timezone.replace(tzinfo=None))
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                real_date = datetime.strptime(date_i, format_date)
                date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second))

                # Date from test image
                dcm_read = DicomImage(pf)
                date_dcm = dcm_read.metadata.AcquisitionDate

                with st.spinner("Database inserting/uploading..."):
                    # INSERTING/UPDATING IN DATABASE
                    if st.session_state['authentication_status'] is not None: 
                        # Deta Database Connection
                        data_connection = Deta(st.secrets['database']['data_key'])
                        user_test = st.session_state['username'] + 'Picket_Fence'
                        db = data_connection.Base(user_test)
                        fetch_res = db.fetch()
                        
                        # Database keys list
                        keys = [] 
                        for i in fetch_res.items:
                            keys.append(i['key'])
                        
                        # Variables to db function
                        date_time_obj = datetime.strptime(date_dcm, '%Y%m%d')
                        date_obj = date_time_obj.date()

                        mlc = st.session_state['i3'][0].name
                        tol = st.session_state['i3'][2]
                        percent_leaves_pass = st.session_state['i3'][4]
                        number_pickets = st.session_state['i3'][5]
                        abs_median_error = st.session_state['i3'][6]
                        max_error = st.session_state['i3'][7]
                        mean_picket_spacing = st.session_state['i3'][8]
                        t_result = st.session_state['r1']
                        analy_date = date_table
                        date_linac = str(date_obj)
                        file_name = pf.name
                        angle = dcm_read.metadata.GantryAngle

                        # Insert new registration
                        if file_name in keys:
                            event = st.warning("Analysis results already exist for this image in database. For saving new analysis, press button bellow.")
                            chime.info()
                            bs = st.button("Save")
                            if bs:
                                DB.database_update_pf(db, mlc, angle, tol, percent_leaves_pass, number_pickets, abs_median_error, max_error,
                                mean_picket_spacing, t_result, analy_date, date_linac, file_name)
                                st.success("New analysis saved to database")
                                chime.success()
                        
                        # Update registration
                        elif file_name not in keys:
                            DB.database_insert_pf(db, mlc, angle, tol, percent_leaves_pass, number_pickets, abs_median_error, max_error,
                                mean_picket_spacing, t_result, analy_date, date_linac, file_name)
                            st.success("Analysis results saved to database")
                            chime.success()      

            except Exception as ex:
                #st.write(ex)
                st.error('An error occured during analysis. Try changing some parameters in box above (i.e. MLC type, crop image, tolerance).' 
                    ' Also, check if your image is a valid DICOM file.')
            
        
        elif subpages == '2. CREATE PDF REPORT':
            st.subheader("PDF Report")
            with st.form(key="pdf_report"):
                pdf1, pdf2 = st.columns(2)
                with pdf1:
                    test_name = st.text_input("Test name", value="Picket Fence")

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
                if test_name or t_name or institution or author or unit or file_name is None:
                    st.warning("⚠️ All fields should be filled!")
                
                if test_name and t_name and institution and author and unit and file_name != None:
                    with st.spinner("Creating your PDF report..."):
                        # Creating PDF file
                        pdf_pf = PDF.create_PDF_PF1(st.session_state['j'], st.session_state['i2'], st.session_state['i3'], t_name, institution, author, unit, st.session_state['name0'], st.session_state['r1'])
                    # Link Download
                    html_pf = PDF.create_download_link(pdf_pf.output(dest="S"), file_name)
                    chime.theme('mario')
                    chime.success()
                    st.success("Your PDF report is ready!")
                    st.markdown(html_pf, unsafe_allow_html=True)