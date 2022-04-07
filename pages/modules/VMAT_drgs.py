import streamlit as st
from pylinac import DRGS
from pylinac.core.image import DicomImage
from pylinac.core.decorators import lru_cache
import zipfile
import io
from pylinac.vmat import ImageType
import matplotlib.pyplot as plt
import pages.core.text as text
import pages.core.table_function as table
import pages.core.pdf_new as PDF_N
import pandas as pd
from io import BytesIO
from st_btn_select import st_btn_select
import pages.core.database as DB
from deta import Deta
from datetime import datetime
import pydicom
import os
import tempfile
import shutil
import pytz
import chime

if 'filedrgs_zip' not in st.session_state:
    st.session_state['filedrgs_zip'] = None

if 't_dmlc' not in st.session_state:
    st.session_state['t_dmlc'] = None

if 'drmlc_name' not in st.session_state:
    st.session_state['drmlc_name'] = None

if 'openbeam_name' not in st.session_state:
    st.session_state['openbeam_name'] = None

if 't_open' not in st.session_state:
    st.session_state['t_open'] = None

if 'r' not in st.session_state:
    st.session_state['r'] = None

if 'sid' not in st.session_state:
    st.session_state['sid'] = None

if 'cax' not in st.session_state:
    st.session_state['cax'] = None

if 'keys' not in st.session_state:
    st.session_state['keys'] = None

if 'values' not in st.session_state:
    st.session_state['values'] = None

if 'mydrgs' not in st.session_state:
    st.session_state['mydrgs'] = None

if 'keys1' not in st.session_state:
    st.session_state['keys1'] = None

if 'values1' not in st.session_state:
    st.session_state['values1'] = None

if 't_drmlc1' not in st.session_state:
    st.session_state['t_drmlc1'] = None

if 'drmlc_name1' not in st.session_state:
    st.session_state['drmlc_name1'] = None

if 'openbeam_name1' not in st.session_state:
    st.session_state['openbeam_name1'] = None

if 't_open1' not in st.session_state:
    st.session_state['t_open1'] = None

if 'r1' not in st.session_state:
    st.session_state['r1'] = None 

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None


def vmat_drgs():
    # Individual files        
    ind_files = st.checkbox("Click here if you want to upload individual files")
    if ind_files:
        # working with files: https://blog.jcharistech.com/2020/11/08/working-with-file-uploads-in-streamlit-python/
        file_open_drgs = st.file_uploader("Choose the open beam file", type=['dcm'])
        file_drgs = st.file_uploader("Choose the DRGS file", type=['dcm'])

        if (file_open_drgs and file_drgs) is None:
            st.markdown("---")
            text.title("Choose your files to start using this app!", 20, "#8C438D")

        if (file_open_drgs and file_drgs) is not None:

            d1, d2, d3 = st.columns(3)

            with d2:
                page = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)

            if page == "1. PERFORM TEST":
                with st.form(key="drgs_files"):
                    t_drgs = 'Analysis parameters'
                    text.body(t_drgs, 18, "black")
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

                st.session_state['mydrgs'] = DRGS(image_paths=(file_open_drgs, file_drgs))
                st.session_state['mydrgs'].analyze(tolerance=tolerance1, segment_size_mm=(w1, h1))
                dict_data1 = st.session_state['mydrgs'].results_data(as_dict = True)
                sid1 = DicomImage(file_open_drgs).sid
                cax1 = DicomImage(file_open_drgs).cax
                final_result = st.session_state['mydrgs'].passed

                if final_result == True:
                    st.session_state['r1'] = 'PASS'

                elif final_result == False:
                    st.session_state['r1'] = 'FAIL'

                text.title("Your test results", 20, "#8C438D")
                
                st.session_state['keys1'] = ['Source-to-Image Distance (mm)', 'Bem Central Axis (CAX)', 'Tolerance (%)',
                        'Absolute Mean Deviation (%)', 'Maximum Deviation (%)', 'Test Result']
                st.session_state['values1'] = [str(sid1), str(cax1), str(dict_data1['tolerance_percent']),
                        str(round(dict_data1['abs_mean_deviation'], 4)),
                        str(round(dict_data1['max_deviation_percent'], 4)), st.session_state['r1']]
                
                t1 = pd.DataFrame(st.session_state['values1'], columns=["Results"])
                t1.insert(0, "Parameters", st.session_state['keys1'], True)
                tab1 = t1.round(decimals=4)
                fig1, ax1 = table.render_mpl_table(tab1)
                buf1 = BytesIO()
                fig1.savefig(buf1, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                t_1, t_2, t_3 = st.columns([0.75, 1.5, 0.75])

                with t_2:
                    lru_cache(st.image(buf1, width=500, use_column_width=True))
                

                
                CoL1, CoL2, CoL3, CoL4, CoL5 = st.columns([1, 3, 0.5, 3, 1])
                with CoL2:
                    # st.session_state['t_drmlc1'] = 'DMLC Image - ' + str(file_open_drgs.name)
                    st.session_state['t_drmlc1'] = 'DMLC Image - '
                    st.session_state['drmlc_name1'] = str(file_drgs.name)
                    text.body_center(st.session_state['t_drmlc1'] + st.session_state['drmlc_name1'], 15, "gray")
                    st.pyplot(st.session_state['mydrgs']._plot_analyzed_subimage(ImageType.DMLC), clear_figure=True, transparent=True)

                with CoL4:
                    # st.session_state['t_open1'] = 'Open Image - ' + str(file_drgs.name)
                    st.session_state['t_open1'] = 'Open Image - '
                    st.session_state['openbeam_name1'] = str(file_open_drgs.name)
                    text.body_center(st.session_state['t_open1'] + st.session_state['openbeam_name1'], 15, "gray")
                    st.pyplot(st.session_state['mydrgs']._plot_analyzed_subimage(ImageType.OPEN), clear_figure=True, transparent=True)
                    #st.image('OPEN.png', caption='OPEN Image - ' + str(file_open_drgs.name))
                
                CoL_1, CoL_2, CoL_3 = st.columns([1, 2, 1])
                with CoL_2:
                    st.markdown("")
                    text.body_center("Median Profiles", 15, "gray")
                    st.pyplot(st.session_state['mydrgs']._plot_analyzed_subimage(ImageType.PROFILE), transparent=True)

                # Date Analysis (app)
                date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                date_i = str(date_timezone.replace(tzinfo=None))
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                real_date = datetime.strptime(date_i, format_date)
                date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second))

                # Date from test image
                dcm_read = DicomImage(file_open_drgs)
                date_dcm = dcm_read.metadata.AcquisitionDate


                # INSERTING/UPDATING IN DATABASE
                if st.session_state['authentication_status'] is not None: 
                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'VMAT_DRGS'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()
                     
                    # Database keys list
                    keys = [] 
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    # Variables to db function
                    date_time_obj = datetime.strptime(date_dcm, '%Y%m%d')
                    date_obj = date_time_obj.date()

                    sid = sid1
                    cax = cax1
                    tol = dict_data1['tolerance_percent']
                    abs_mean_dev = round(dict_data1['abs_mean_deviation'], 4)
                    max_dev = round(dict_data1['max_deviation_percent'], 4)
                    t_result = st.session_state['r1']
                    analy_date = date_table
                    date_linac = str(date_obj)
                    key = str(file_open_drgs.name) + '&' + str(file_drgs.name)

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


            elif page == "2. CREATE PDF REPORT":
                st.subheader("PDF Report")
                with st.form(key="pdf_report1"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name1 = st.text_input("Test name", value="VMAT/DRGS")

                        t_name1 = "Report - " + test_name1

                        institution1 = st.text_input("Institution name")
                        
                    with pdf2:
                        author1 = st.text_input("Author name")
                        unit1 = st.text_input("Unit model name")
                    
                    PDF1, PDF2, PDF3 = st.columns([1,2,1])
                    with PDF2:
                        file_name1 = st.text_input("Choose the report file name")

                    submit_button = st.form_submit_button(label='Apply')

                if submit_button: 

                    with st.spinner("Creating your PDF report..."):
                        PDF_N.create_pdf_VMAT(st.session_state['mydrgs'], st.session_state['keys1'][:len(st.session_state['keys1'])-1], 
                        st.session_state['values1'][:len(st.session_state['values1'])-1], st.session_state['t_drmlc1'], st.session_state['drmlc_name1'],
                        st.session_state['t_open1'], st.session_state['openbeam_name1'], t_name1, institution1, author1, unit1, 
                        st.session_state['r1'], file_name1)


    # ZIP file
    else:
        file_zip = st.file_uploader("Choose your DRGS images (upload a zip file)", type=["ZIP"], key='drgs')

        if file_zip is None:
            st.markdown("---")
            text.title("Choose your files to start using this app!", 20, "#8C438D")

        else:
            d1, d2, d3 = st.columns(3)

            with d2:

                page = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)
            
            if page == '1. PERFORM TEST':

                reset = st.checkbox("Reset to default parameters",
                                help="Click here if you prefer to reset to default parameters "
                                    "every time you apply new ones.")

                with st.form(key="drgs_zip", clear_on_submit=reset):
                    t_drgs = 'Analysis parameters'
                    text.body(t_drgs, 18, "black")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        tolerance = st.number_input("Choose your tolerance value", min_value=0.0, max_value=8.0, value=1.5,
                                                    step=0.5,
                                                    help="The tolerance of the sample deviations in percent. Default is 1.5. "
                                                        "Must be between 0 and 8.")
                        lru_cache(tolerance)

                    with col2:
                        w = st.number_input("Set the width of the ROI segments in mm", min_value=0, max_value=1000, value=5,
                                            help="Integer value")
                        lru_cache(w)

                    with col3:
                        h = st.number_input("Set the height of the ROI segments in mm", min_value=0, max_value=1000, value=100,
                                            help="Integer value")
                        lru_cache(h)

                    submit_button = st.form_submit_button(label='Apply')

                file = file_zip.read()
                zipfile_ob = zipfile.ZipFile(io.BytesIO(file))
                st.session_state['filedrgs_zip'] = DRGS.from_zip(io.BytesIO(file))
                lru_cache(st.session_state['filedrgs_zip'].analyze(tolerance=tolerance, segment_size_mm=(w, h)))
                drgs_name = zipfile_ob.namelist()[0]  # name of drgs image
                openbeam_name = zipfile_ob.namelist()[1]  # name of open beam image
                img_data = zipfile_ob.open(openbeam_name)
                st.session_state['sid'] = DicomImage(img_data).sid
                st.session_state['cax'] = DicomImage(img_data).cax

                with zipfile.ZipFile(io.BytesIO(file), 'r') as zip:
                    path = tempfile.mkdtemp()
                    zip.extractall(path)
                    # slices = []
                    for root, _, filenames in os.walk(path):
                        for filename in filenames:
                            filepath = os.path.join(root, filename)
                            dcm_read = pydicom.dcmread(filepath)
                            date_img = dcm_read.AcquisitionDate
                    shutil.rmtree(path)

                date_time_obj = datetime.strptime(date_img, '%Y%m%d')
                date_obj = date_time_obj.date()

                text.title("Test results", 20, "#8C438D")
                a = datetime.now(pytz.timezone("America/Sao_Paulo"))
                st.write(a.replace(tzinfo=None))
                st.write(datetime.now())
                dict_data = st.session_state['filedrgs_zip'].results_data(as_dict=True)
                result = st.session_state['filedrgs_zip'].passed

                # RESULT TABLE
                if str(result) == 'True':
                    st.session_state['r'] = "PASS"

                elif str(result) == 'False':
                    st.session_state['r'] = "FAIL"

                date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                date_i = str(date_timezone.replace(tzinfo=None))
                format_date = "%Y-%m-%d %H:%M:%S.%f"
                real_date = datetime.strptime(date_i, format_date)
                date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second))

                st.session_state['keys'] = ["Date of Analysis", 'Source-to-Image Distance (mm)', 'Bem Central Axis (CAX)', 'Tolerance (%)',
                        'Absolute Mean Deviation (%)', 'Maximum Deviation (%)', 'Test Result']

                st.session_state['values'] = [date_table, str(st.session_state['sid']), str(st.session_state['cax']), str(dict_data['tolerance_percent']),
                        str(round(dict_data['abs_mean_deviation'], 4)),
                        str(round(dict_data['max_deviation_percent'], 4)), st.session_state['r']]

                t = pd.DataFrame(st.session_state['values'], columns=["Results"])
                t.insert(0, "Parameters", st.session_state['keys'], True)
                tab = t.round(decimals=4)
                fig, ax = table.render_mpl_table(tab)
                buf = BytesIO()
                fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                t1, t2, t3 = st.columns([0.75, 1.5, 0.75])

                with t2:
                    lru_cache(st.image(buf, width=500, use_column_width=True))

                Col1, Col2, Col3, Col4, Col5 = st.columns([1, 3, 0.5, 3, 1])
                with Col2:
                    st.session_state["t_dmlc"] = 'DMLC Image - '
                    st.session_state['drgs_name'] = str(drgs_name)
                    text.body_center(st.session_state["t_dmlc"] + st.session_state['drgs_name'], 15, "gray")
                    drgs_plot = st.session_state['filedrgs_zip']._plot_analyzed_subimage(ImageType.DMLC)
                    lru_cache(drgs_plot)
                    plt.tight_layout()
                    st.pyplot(drgs_plot, clear_figure=True, transparent=True)

                with Col4:
                    st.session_state["t_open"] = 'Open Image - '
                    st.session_state['openbeam_name'] = str(openbeam_name)
                    text.body_center(st.session_state["t_open"] + st.session_state['openbeam_name'] , 15, "gray")
                    drgs_plot_open = st.session_state['filedrgs_zip']._plot_analyzed_subimage(ImageType.OPEN)
                    lru_cache(drgs_plot_open)
                    plt.tight_layout()
                    st.pyplot(drgs_plot_open, clear_figure=True, transparent=True)

                Col_1, Col_2, Col_3 = st.columns([1, 2, 1])
                with Col_2:
                    st.markdown("")
                    text.body_center("Median Profiles", 15, "gray")
                    st.pyplot(st.session_state['filedrgs_zip']._plot_analyzed_subimage(ImageType.PROFILE), transparent=True)
                
                if st.session_state['authentication_status'] is not None:   
                    # DATABASE 
                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'VMAT_DRGS'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()
                     
                    keys = [] # database keys list
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    sid = st.session_state['sid']
                    cax = st.session_state['cax']
                    tol = dict_data['tolerance_percent']
                    abs_mean_dev = round(dict_data['abs_mean_deviation'], 4)
                    max_dev = round(dict_data['max_deviation_percent'], 4)
                    t_result = st.session_state['r']
                    analy_date = date_table
                    date_linac = str(date_obj)
                    key = file_zip.name

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

            # creating PDF
            if page == '2. CREATE PDF REPORT':
                st.subheader("PDF Report")
                with st.form(key="pdf_report"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name = st.text_input("Test name", value="VMAT/DRGS")

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
                    with st.spinner("Creating your PDF report..."):
                        PDF_N.create_pdf_VMAT(st.session_state['filedrgs_zip'], st.session_state['keys'][:len(st.session_state['keys'])-1], 
                            st.session_state['values'][:len(st.session_state['values'])-1], st.session_state["t_dmlc"], st.session_state['drgs_name'],
                            st.session_state['t_open'], st.session_state['openbeam_name'], t_name, institution, author, unit, 
                            st.session_state['r'], file_name)