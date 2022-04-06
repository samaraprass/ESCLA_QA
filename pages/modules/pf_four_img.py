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

def pf_four():
    # PARAMETERS
    pf_up2 = st.file_uploader("Upload your Picket Fence files", key='pf_file', accept_multiple_files=True, type=['DCM'], 
                            help="Files should be DICOM images acquired via the EPID.")

    if len(pf_up2) == 0:
        st.markdown("---")
        text.title("Choose your files to start using this app!", 20, "#8C438D")

    else:
        pf2_1 = pf_up2[0]
        pf2_2 = pf_up2[1]
        pf2_3 = pf_up2[2]
        pf2_4 = pf_up2[3]

        st.markdown("---")
        # User parameters input
        with st.expander("Click here if you would like to change Picket Fence and analysis parameters"):

            with st.form(key="pf2"):
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

        PF1, PF2, PF3 = st.columns([0.7, 5, 0.5])
                
        with PF2:
            pages = st_btn_select(('Test Results - Image 1', 'Test Results - Image 2', 'Test Results - Image 3', 'Test Results - Image 4', 'PDF Report'), 
                                        nav=False)

        if pages == 'Test Results - Image 1':    
            try:
                with st.spinner("Loading Analysis..."):
                    # FIRST PAGE
                    #Input Image
                    PF_function.input_image(pf2_1)

                    # 1st Image
                    st.session_state['a1'], st.session_state['a2'], st.session_state['a3'], st.session_state['b'], st.session_state['r2'] = PF_function.image_analysis(pf2_1)
                    st.session_state['name1'] = "Analysis result - " + pf2_1.name

                    # 2nd Image
                    st.session_state['c1'], st.session_state['c2'], st.session_state['c3'], st.session_state['d'], st.session_state['r3'] = PF_function.image_analysis(pf2_2)
                    st.session_state['name2'] = "Analysis result - " + pf2_2.name

                    # 3rd Image
                    st.session_state['e1'], st.session_state['e2'], st.session_state['e3'], st.session_state['f'], st.session_state['r4'] = PF_function.image_analysis(pf2_3)
                    st.session_state['name3'] = "Analysis result - " + pf2_3.name

                    # 4th Image
                    st.session_state['g1'], st.session_state['g2'], st.session_state['g3'], st.session_state['h'], st.session_state['r5'] = PF_function.image_analysis(pf2_4)
                    st.session_state['name4'] = "Analysis result - " + pf2_4.name
                    
                
                    # Analysis Images
                    text.title(st.session_state['name1'], 15, "#8C438D")
                    a1, a2 = st.columns(2)
                    with a1:
                        st.markdown("")
                        st.markdown("")
                        st.pyplot(st.session_state['b'].plot_analyzed_image(mlc_peaks=True, overlay=True))
                    with a2:
                        st.markdown("")
                        st.markdown("")
                        st.image(st.session_state['a1'], width=500, use_column_width=True)
                    
                    with st.spinner("Database inserting/uploading..."):

                        if st.session_state['authentication_status'] is not None:

                            # table date format
                            t = datetime.now()
                            date_table = (str(t.day) + '/' + str(t.month) + '/' + str(t.year) + ' ' + str(t.hour) + ':' + 
                                                    str(t.minute) + ':' + str(t.second))

                            # Deta Database Connection
                            data_connection = Deta(st.secrets['database']['data_key'])
                            user_test = st.session_state['username'] + 'Picket_Fence'
                            db = data_connection.Base(user_test)
                            fetch_res = db.fetch()

                            # INFO from DICOM images
                            dates = []
                            names = []
                            angles = []
                            for i in range(len(pf_up2)):
                                dcm_read = DicomImage(pf_up2[i])
                                date = dcm_read.metadata.AcquisitionDate
                                date_time_obj = datetime.strptime(date, '%Y%m%d')
                                date_obj = date_time_obj.date()
                                date_linac = str(date_obj)
                                name = pf_up2[i].name
                                names.append(name)
                                dates.append(date_linac)
                                angles.append(dcm_read.metadata.GantryAngle)
                            
                            # Database keys list
                            keys = [] # storing keys from database to list
                            for i in fetch_res.items:
                                keys.append(i['key'])

                            # FIRST IMAGE - Variables to db function
                            mlc1 = st.session_state['a3'][0].name
                            tol1 = st.session_state['a3'][2]
                            percent_leaves_pass1 = st.session_state['a3'][4]
                            number_pickets1 = st.session_state['a3'][5]
                            abs_median_error1 = st.session_state['a3'][6]
                            max_error1 = st.session_state['a3'][7]
                            mean_picket_spacing1 = st.session_state['a3'][8]
                            t_result1 = st.session_state['r2']
                            analy_date1 = date_table
                            date_linac1 = dates[0]
                            key1 = names[0]
                            angle1 = angles[0]

                            # SECOND IMAGE - Variables to db function
                            mlc2 = st.session_state['c3'][0].name
                            tol2 = st.session_state['c3'][2]
                            percent_leaves_pass2 = st.session_state['c3'][4]
                            number_pickets2 = st.session_state['c3'][5]
                            abs_median_error2 = st.session_state['c3'][6]
                            max_error2 = st.session_state['c3'][7]
                            mean_picket_spacing2 = st.session_state['c3'][8]
                            t_result2 = st.session_state['r3']
                            analy_date2 = date_table
                            date_linac2 = dates[1]
                            key2 = names[1]
                            angle2 = angles[1]

                            # THIRD IMAGE - Variables to db function
                            mlc3 = st.session_state['e3'][0].name
                            tol3 = st.session_state['e3'][2]
                            percent_leaves_pass3 = st.session_state['e3'][4]
                            number_pickets3 = st.session_state['e3'][5]
                            abs_median_error3 = st.session_state['e3'][6]
                            max_error3 = st.session_state['e3'][7]
                            mean_picket_spacing3 = st.session_state['e3'][8]
                            t_result3 = st.session_state['r4']
                            analy_date3 = date_table
                            date_linac3 = dates[2]
                            key3 = names[2]
                            angle3 = angles[2]

                            #FOURTH IMAGE - Variables to db function
                            mlc4 = st.session_state['g3'][0].name
                            tol4 = st.session_state['g3'][2]
                            percent_leaves_pass4 = st.session_state['g3'][4]
                            number_pickets4 = st.session_state['g3'][5]
                            abs_median_error4 = st.session_state['g3'][6]
                            max_error4 = st.session_state['g3'][7]
                            mean_picket_spacing4 = st.session_state['g3'][8]
                            t_result4 = st.session_state['r5']
                            analy_date4 = date_table
                            date_linac4 = dates[3]
                            key4 = names[3]
                            angle4 = angles[3]

                            if len([x for x in names if x in keys])==4:
                                chime.info()
                                st.warning("Analysis results already exist for this image on database. For saving new analysis, press button bellow.")
                                bs = st.button("Save", key='fourth_img')
                                if bs:
                                    DB.database_update_pf(db, mlc1, angle1, tol1, percent_leaves_pass1, number_pickets1, abs_median_error1, max_error1,
                                        mean_picket_spacing1, t_result1, analy_date1, date_linac1, key1)
                                    st.success(f"New analysis {key1} saved")
                                    chime.success()

                                    DB.database_update_pf(db, mlc2, angle2, tol2, percent_leaves_pass2, number_pickets2, abs_median_error2, max_error2,
                                        mean_picket_spacing2, t_result2, analy_date2, date_linac2, key2)
                                    st.success(f"New analysis {key2} saved")
                                    chime.success()

                                    DB.database_update_pf(db, mlc3, angle3, tol3, percent_leaves_pass3, number_pickets3, abs_median_error3, max_error3,
                                    mean_picket_spacing3, t_result3, analy_date3, date_linac3, key3)
                                    st.success(f"New analysis {key3} saved")
                                    chime.success()

                                    DB.database_update_pf(db, mlc4, angle4, tol4, percent_leaves_pass4, number_pickets4, abs_median_error4, max_error4,
                                    mean_picket_spacing4, t_result4, analy_date4, date_linac4, key4)
                                    st.success(f"New analysis {key4} saved")
                                    chime.success()

                            if len([x for x in names if x in keys]) != 4:            
                                DB.database_insert_pf(db, mlc1, angle1, tol1, percent_leaves_pass1, number_pickets1, abs_median_error1, max_error1,
                                        mean_picket_spacing1, t_result1, analy_date1, date_linac1, key1)
                                st.success(f"Analysis results for file {key1} saved")
                                chime.success()

                                                         
                                DB.database_insert_pf(db, mlc2, angle2, tol2, percent_leaves_pass2, number_pickets2, abs_median_error2, max_error2,
                                        mean_picket_spacing2, t_result2, analy_date2, date_linac2, key2)
                                st.success(f"Analysis results for file {key2} saved")
                                chime.success()

                                DB.database_insert_pf(db, mlc3, angle3, tol3, percent_leaves_pass3, number_pickets3, abs_median_error3, max_error3,
                                        mean_picket_spacing3, t_result3, analy_date3, date_linac3, key3)
                                st.success(f"Analysis results for file {key3} saved")
                                chime.success()

                                DB.database_insert_pf(db, mlc4, angle4, tol4, percent_leaves_pass4, number_pickets4, abs_median_error4, max_error4,
                                        mean_picket_spacing4, t_result4, analy_date4, date_linac4, key4)        
                                st.success(f"Analysis results for file {key4} saved")
                                chime.success()

            except Exception as error:
                # st.write(error)
                st.error('An error occured during analysis. Try changing some parameters in box above (i.e. MLC type, crop image, tolerance).' 
                    ' Also, check if your image is a valid DICOM file.')


        # SECOND PAGE
        if pages == 'Test Results - Image 2':
            PF_function.input_image(pf2_2)
            text.title(st.session_state['name2'], 15, "#8C438D")
            # Analysis Images
            a1, a2 = st.columns(2)
            with a1:
                st.markdown("")
                st.markdown("")
                st.pyplot(st.session_state['d'].plot_analyzed_image(mlc_peaks=True, overlay=True))
            with a2:
                st.markdown("")
                st.markdown("")
                st.image(st.session_state['c1'], width=500, use_column_width=True)


        # THIRD PAGE
        if pages == 'Test Results - Image 3':
            PF_function.input_image(pf2_3)
            text.title(st.session_state['name3'], 15, "#8C438D")
            a1, a2 = st.columns(2)
            with a1:
                st.markdown("")
                st.markdown("")
                st.pyplot(st.session_state['f'].plot_analyzed_image(mlc_peaks=True, overlay=True))

            with a2:
                st.markdown("")
                st.markdown("")
                st.image(st.session_state['e1'], width=500, use_column_width=True)

        
        # FOURTH PAGE
        if pages == "Test Results - Image 4":
            PF_function.input_image(pf2_4)
            text.title(st.session_state['name4'], 15, "#8C438D")
            a1, a2 = st.columns(2)
            with a1:
                st.markdown("")
                st.markdown("")
                st.pyplot(st.session_state['h'].plot_analyzed_image(mlc_peaks=True, overlay=True))

            with a2:
                st.markdown("")
                st.markdown("")
                st.image(st.session_state['g1'], width=500, use_column_width=True)
        
        # PDF REPORT GENERATOR
        if pages == 'PDF Report':
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
                    
                pdf_1, pdf_2, pdf_3 = st.columns(3)
                with pdf_2:
                        file_name = st.text_input("Choose the report file name")

                submit_button = st.form_submit_button(label='Apply')

            if submit_button:
                with st.spinner("Creating your PDF report..."):
                    pdf = PDF.create_PDF_PF4(t_name, institution, author, unit, 
                                        st.session_state['b'], st.session_state['a2'], st.session_state['c3'], st.session_state['name1'], st.session_state['r2'],
                                        st.session_state['d'], st.session_state['c2'], st.session_state['c3'], st.session_state['name2'], st.session_state['r3'],
                                        st.session_state['f'], st.session_state['e2'], st.session_state['e3'], st.session_state['name3'], st.session_state['r4'],
                                        st.session_state['h'], st.session_state['g2'], st.session_state['g3'], st.session_state['name4'], st.session_state['r5'])
                        
                html_pf = PDF.create_download_link(pdf.output(dest="S"), file_name)
                chime.theme('mario')
                chime.success()
                st.success("Your PDF report is ready!")
                st.markdown(html_pf, unsafe_allow_html=True)
