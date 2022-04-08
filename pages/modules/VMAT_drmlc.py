import streamlit as st
from pylinac import DRMLC
import zipfile
import matplotlib.pyplot as plt
from pylinac.vmat import ImageType
import io
import pages.core.text as text
import pages.core.table_function as table
import pandas as pd
from pylinac.core.image import DicomImage, BaseImage
from st_btn_select import st_btn_select
import pages.core.pdf_new as PDF
from datetime import datetime
import pages.core.database as DB
from deta import Deta
import chime
import pytz

# -------------------------------------------

if 'filedrmlc_zip' not in st.session_state:
    st.session_state['filedrmlc_zip'] = None

if 'keys2' not in st.session_state:
    st.session_state['keys2'] = None

if 'values2' not in st.session_state:
    st.session_state['values2'] = None

if 't_dmlc' not in st.session_state:
    st.session_state['t_dmlc'] = None

if 't_open2' not in st.session_state:
    st.session_state['t_open2'] = None

if 'r2' not in st.session_state:
    st.session_state['r2'] = None

if 'sid2' not in st.session_state:
    st.session_state['sid2'] = None

if 'cax2' not in st.session_state:
    st.session_state['cax2'] = None

# -------------------------------------------

if 'mydrmlc' not in st.session_state: 
    st.session_state['mydrmlc'] = None

if 'keys3' not in st.session_state:
    st.session_state['keys3'] = None

if 'values3' not in st.session_state:
    st.session_state['values3'] = None

if 't_drmlc' not in st.session_state:
    st.session_state['t_drmlc'] = None

if 't_open3' not in st.session_state:
    st.session_state['t_open3'] = None

if 'r_drmlc' not in st.session_state:
    st.session_state['r_drmlc'] = None

if ['sid3'] not in st.session_state:
    st.session_state['sid3'] = None

if ['cax3'] not in st.session_state:
    st.session_state['cax3'] = None

# -------------------------------------------

# Creating function for DRMLC test
def vmat_drmlc():
    ind_files = st.checkbox("Click here if you want to upload individual files")
    if ind_files:
        file_open = st.file_uploader("Choose the Open Beam file", type=['dcm'])
        file_drmlc = st.file_uploader("Choose the MLC file", type=['dcm'])

        if (file_open and file_drmlc) is None:
            st.markdown("---")
            text.title("Choose your files to start using this app!", 20, "#8C438D")

        if (file_open and file_drmlc) is not None:
            st.markdown("---")
            d1, d2, d3 = st.columns(3)

            with d2:

                page = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)
            
            if page == '1. PERFORM TEST':
                with st.form(key="drmlc__single_files"):
                    t_drgs = 'Analysis parameters'
                    text.body(t_drgs, 18, "black")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        tolerance = st.number_input("Choose your tolerance value", min_value=0.0, max_value=8.0, value=3.0,
                                                    step=0.5,
                                                    help="The tolerance of the sample deviations in percent. Default is 1.5. "
                                                        "Must be between 0 and 8.")
                    with col2:
                        w = st.number_input("Set the width of the ROI segments in mm", min_value=0, max_value=1000, value=5,
                                            help="Integer value")

                    with col3:
                        h = st.number_input("Set the height of the ROI segments in mm", min_value=0, max_value=1000, value=100,
                                            help="Integer value")

                    submit_button = st.form_submit_button(label='Apply')

                st.session_state['mydrmlc'] = DRMLC(image_paths=(file_open, file_drmlc))
                st.session_state['mydrmlc'].analyze(tolerance=tolerance, segment_size_mm=(w, h))
                dict_imgs = st.session_state['mydrmlc'].results_data(as_dict=True)
                drmlc_name1 = file_drmlc.name
                openbeam_name1 = file_open.name

                result = st.session_state['mydrmlc'].passed
                if str(result) == 'True':
                    st.session_state['r_drmlc'] = "PASS"

                elif str(result) == 'False':
                    st.session_state['r_drmlc'] = "FAIL"
                
                # date
                date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                date_i = str(date_timezone.replace(tzinfo=None))
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                real_date = datetime.strptime(date_i, format_date)
                date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second))

                # Results
                img = DicomImage(file_drmlc)
                st.session_state['sid3'] = str(img.sid)
                st.session_state['cax3'] = str(img.cax)
                st.session_state['keys3'] = ["Date of Analysis", "Source-to-Image Distance (mm)", "Beam Central Axis (CAX)", "Tolerance (%)",
                        "Absolute mean deviation (%)", "Maximum deviation (%)", "Test Results"]
                st.session_state['values3'] = [date_table, st.session_state['sid3'], st.session_state['cax3'], str(round(dict_imgs['tolerance_percent'], 4)),
                        str(round(dict_imgs['abs_mean_deviation'], 4)), str(round(dict_imgs['max_deviation_percent'], 4)), 
                        st.session_state['r_drmlc']]
                date_dcm_sf = img.metadata.AcquisitionDate

                t = pd.DataFrame(st.session_state['values3'], columns=["Results"])
                t.insert(0, "Parameters", st.session_state['keys3'], True)
                tab = t.round(decimals=4)
                fig, ax = table.render_mpl_table(tab)
                buf = io.BytesIO()
                fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                text.title("Test results", 20, "#8C438D")

                t1, t2, t3 = st.columns([0.75, 1.5, 0.75])
                with t2:
                    st.image(buf, width=500, use_column_width=True)


                with st.container():
                    cc1, cc2, cc3, cc4, cc5 = st.columns([1, 3, 1, 3, 1])

                    with cc2:
                        st.session_state['t_drmlc'] = 'DMLC Image - ' + str(drmlc_name1)
                        text.body_center(st.session_state['t_drmlc'], 15, "gray")
                        drmlc_plot = st.session_state['mydrmlc']._plot_analyzed_subimage(ImageType.DMLC)
                        plt.tight_layout()
                        st.pyplot(drmlc_plot, clear_figure=True, transparent=True)

                    with cc4:
                        st.session_state['t_open3'] = 'Open Image - ' + str(openbeam_name1)
                        text.body_center(st.session_state['t_open3'], 15, "gray")
                        drmlc_plot_open = st.session_state['mydrmlc']._plot_analyzed_subimage(ImageType.OPEN)
                        st.pyplot(drmlc_plot_open, clear_figure=True, transparent=True)

                with st.container():
                    Cc1, Cc2, Cc3 = st.columns([1, 2, 1])
                    with Cc2:
                        text.body_center("Median Profiles", 15, "gray")
                        drmlc_plot_profile = st.session_state['mydrmlc']._plot_analyzed_subimage(ImageType.PROFILE)
                        st.pyplot(drmlc_plot_profile, clear_figure=True, transparent=True)
                
                if st.session_state['authentication_status'] is not None:   
                    # DATABASE 
                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'VMAT_DRMLC'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()
                     
                    keys = [] # database keys list
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    # Variables to db function
                    date_time_obj = datetime.strptime(date_dcm_sf, '%Y%m%d')
                    date_obj = date_time_obj.date()
                    
                    sid = st.session_state['sid3']
                    cax = st.session_state['cax3']
                    tol = round(dict_imgs['tolerance_percent'], 4)
                    abs_mean_dev = round(dict_imgs['abs_mean_deviation'], 4)
                    max_dev = round(dict_imgs['max_deviation_percent'], 4)
                    t_result = st.session_state['r_drmlc']
                    analy_date = date_table
                    date_linac = str(date_obj)
                    key = str(file_open.name) + '&' + str(file_drmlc.name)

                    # Insert new registration
                    if key in keys:
                        chime.info()
                        st.warning("Already exist analysis results for this image on database. For saving new analysis, press button bellow.")
                        bs = st.button("Save")
                        if bs:
                            DB.database_update_VMAT_DRGS(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key)
                            st.success("New analysis saved")
                            chime.success()
                    
                    # Update registration
                    elif key not in keys:
                        DB.database_insert_VMAT_DRGS(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key)
                        st.success("Analysis results saved")
                        chime.success()
                    
            elif page == '2. CREATE PDF REPORT':
                st.subheader("PDF Report")
                with st.form(key="pdf_report_single_files"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name = st.text_input("Test name", value="VMAT/DRMLC")

                        t_name = "Report - " + test_name

                        institution = st.text_input("Institution name")
                        
                    with pdf2:
                        author = st.text_input("Author name")
                        unit = st.text_input("Unit model name")
                    
                    PDF1, PDF2, PDF3 = st.columns([1,2,1])
                    with PDF2:
                        file_name = st.text_input("Choose the report file name")

                    submit_button = st.form_submit_button(label='Apply')

                    if submit_button:
                        if test_name or t_name or institution or author or unit or file_name is None:
                            st.info("⚠️ All fields should be filled!")
                
                        if test_name and t_name and institution and author and unit and file_name != None:
                            with st.spinner("Creating your PDF report..."):
                                PDF.create_pdf_VMAT(st.session_state['mydrmlc'], st.session_state['keys3'][:len(st.session_state['keys3'])-1], 
                                    st.session_state['values3'][:len(st.session_state['values3'])-1], st.session_state["t_drmlc"], st.session_state['t_open3'], 
                                    t_name, institution, author, unit, st.session_state['r_drmlc'], file_name)

    # -----------------------------------------------------------------------------------------------------------------------------------------
    
    # ZIP file
    else:
        filezip = st.file_uploader("Choose your DRMLC images (upload a zip file)", type=["ZIP"], key='drmlc')
        if filezip is None:
            st.markdown("---")
            text.title("Choose your files to start using this app!", 20, "#8C438D")

        else:
            st.markdown("---")
            d1, d2, d3 = st.columns(3)

            with d2:

                page = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)
            
            if page == '1. PERFORM TEST':
                with st.form(key="drmlc_zip"):
                    t_drgs = 'Analysis parameters'
                    text.body(t_drgs, 18, "black")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        tolerance = st.number_input("Choose tolerance value", min_value=0.0, max_value=8.0, value=3.0,
                                                    step=0.5,
                                                    help="The tolerance of the sample deviations in percent. Default is 1.5. "
                                                        "Must be between 0 and 8.")
                    with col2:
                        w = st.number_input("Set the width of the ROI segments in mm", min_value=0, max_value=1000, value=5,
                                            help="Integer value")

                    with col3:
                        h = st.number_input("Set the height of the ROI segments in mm", min_value=0, max_value=1000, value=100,
                                            help="Integer value")

                    submit_button = st.form_submit_button(label='Apply')

                file = filezip.read()
                zipfile_ob = zipfile.ZipFile(io.BytesIO(file))
                st.session_state['filedrmlc_zip'] = DRMLC.from_zip(io.BytesIO(file))
                st.session_state['filedrmlc_zip'].analyze(tolerance=tolerance, segment_size_mm=(w, h))
                st.session_state['drmlc_name2'] = zipfile_ob.namelist()[0]  # name of drmlc image
                st.session_state['openbeam_name2'] = zipfile_ob.namelist()[1]  # name of open beam image
                img_data = zipfile_ob.open(st.session_state['openbeam_name2'])
                st.session_state['sid2'] = DicomImage(img_data).sid
                st.session_state['cax2'] = DicomImage(img_data).cax

                text.title("Test results", 20, "#8C438D")

                dict_data_drmlc = st.session_state['filedrmlc_zip'].results_data(as_dict=True)
                result = st.session_state['filedrmlc_zip'].passed

                # RESULT TABLE
                if str(result) == 'True':
                    st.session_state['r2'] = "PASS"

                elif str(result) == 'False':
                    st.session_state['r2'] = "FAIL"

                # date
                date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                date_i = str(date_timezone.replace(tzinfo=None))
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                real_date = datetime.strptime(date_i, format_date)
                date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second))

                # Date from test image
                dcm_read = DicomImage(img_data)
                date_dcm = dcm_read.metadata.AcquisitionDate

                st.session_state['keys2'] = ["Date of Analysis", 'Source-to-Image Distance (mm)', 'Bem Central Axis (CAX)', 'Tolerance (%)',
                        'Absolute Mean Deviation (%)', 'Maximum Deviation (%)', 'Test Result']

                st.session_state['values2'] = [date_table, str(st.session_state['sid2']), str(st.session_state['cax2']), str(dict_data_drmlc['tolerance_percent']),
                        str(round(dict_data_drmlc['abs_mean_deviation'], 4)),
                        str(round(dict_data_drmlc['max_deviation_percent'], 4)), st.session_state['r2']]

                t = pd.DataFrame(st.session_state['values2'], columns=["Results"])
                t.insert(0, "Parameters", st.session_state['keys2'], True)
                tab = t.round(decimals=4)
                fig, ax = table.render_mpl_table(tab)
                buf = io.BytesIO()
                fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                t1, t2, t3 = st.columns([0.75, 1.5, 0.75])

                with t2:
                    st.image(buf, width=500, use_column_width=True)

                Col1, Col2, Col3, Col4, Col5 = st.columns([1, 3, 0.5, 3, 1])
                with Col2:
                    st.session_state['t_dmlc'] = 'DMLC Image - '
                    text.body_center(st.session_state['t_dmlc'], 15, "gray")
                    # filedrgs_zip._save_analyzed_subimage('DRGS.png', ImageType.DMLC, transparent=True)
                    # st.image('DRGS.png', caption='DMLC Image - ' + str(drgs_name))
                    drmlc_plot = st.session_state['filedrmlc_zip']._plot_analyzed_subimage(ImageType.DMLC)
                    plt.tight_layout()
                    st.pyplot(drmlc_plot, clear_figure=True, transparent=True)

                with Col4:
                    st.session_state['t_open2'] = 'Open Image - ' 
                    text.body_center(st.session_state['t_open2'], 15, "gray")
                    drgs_plot_open = st.session_state['filedrmlc_zip']._plot_analyzed_subimage(ImageType.OPEN)
                    plt.tight_layout()
                    st.pyplot(drgs_plot_open, clear_figure=True, transparent=True)

                Col_1, Col_2, Col_3 = st.columns([1, 2, 1])
                with Col_2:
                    st.markdown("")
                    text.body_center("Median Profiles", 15, "gray")
                    st.pyplot(st.session_state['filedrmlc_zip']._plot_analyzed_subimage(ImageType.PROFILE), transparent=True)

                if st.session_state['authentication_status'] is not None:   
                    # DATABASE 
                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'VMAT_DRMLC'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()
                     
                    keys = [] # database keys list
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    # Variables to db function
                    date_time_obj = datetime.strptime(date_dcm, '%Y%m%d')
                    date_obj = date_time_obj.date()
                    
                    sid = st.session_state['sid2']
                    cax = st.session_state['cax2']
                    tol = dict_data_drmlc['tolerance_percent']
                    abs_mean_dev = round(dict_data_drmlc['abs_mean_deviation'], 4)
                    max_dev = round(dict_data_drmlc['max_deviation_percent'], 4)
                    t_result = st.session_state['r2']
                    analy_date = date_table
                    date_linac = str(date_obj)
                    key = filezip.name

                    # Insert new registration
                    if key in keys:
                        chime.info()
                        st.warning("Already exist analysis results for this image on database. For saving new analysis, press button bellow.")
                        bs = st.button("Save")
                        if bs:
                            DB.database_update_VMAT_DRMLC(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key)
                            st.success("New analysis saved")
                            chime.success()
                    
                    # Update registration
                    elif key not in keys:
                        DB.database_insert_VMAT_DRMLC(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key)
                        st.success("Analysis results saved")
                        chime.success()       
            
            elif page == '2. CREATE PDF REPORT':
                st.subheader("PDF Report")
                with st.form(key="pdf_report"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name = st.text_input("Test name", value="VMAT/DRMLC")

                        t_name = "Report - " + test_name

                        institution = st.text_input("Institution name")
                        
                    with pdf2:
                        author = st.text_input("Author name")
                        unit = st.text_input("Unit model name")
                    
                    PDF1, PDF2, PDF3 = st.columns([1,2,1])
                    with PDF2:
                        file_name = st.text_input("Choose the report file name")

                    submit_button = st.form_submit_button(label='Apply')
                    
                if submit_button: 
                    if t_name or institution or author or unit or file_name is None:
                        st.info("⚠️ All fields should be filled!")
                                   
                    if t_name and institution and author and unit and file_name is not None:
                        with st.spinner("Creating your PDF report..."):
                            PDF.create_pdf_VMAT(st.session_state['filedrmlc_zip'], st.session_state['keys2'][:len(st.session_state['keys2'])-1], 
                                st.session_state['values2'][:len(st.session_state['values2'])-1], st.session_state["t_dmlc"], st.session_state['drmlc_name2'], 
                                st.session_state['t_open2'], st.session_state['openbeam_name2'], t_name, institution, author, unit, st.session_state['r2'], 
                                file_name)

                        
