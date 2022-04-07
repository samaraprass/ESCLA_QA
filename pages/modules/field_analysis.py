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
import pytz

if 'test2' not in st.session_state:
    st.session_state['test2'] = None

if 'names' not in st.session_state:
    st.session_state['names'] = None

if 'values' not in st.session_state:
    st.session_state['values'] = None

if 'f_name' not in st.session_state:
    st.session_state['f_name'] = None

def FA():
    file = st.file_uploader("Upload image for field analysis", type=["DCM"])
    st.markdown("---")

    if file is None:
        text.title("Choose your files to start using this app!", 20, "#8C438D")

    else:
        fa1, fa2, fa3 = st.columns([1.5, 2, 0.88])
        with fa2:
            subpages = st_btn_select(("1. PERFORM TEST", "2. CREATE PDF REPORT"), nav=False)

        if subpages == "1. PERFORM TEST":
            st.session_state['test2'], st.session_state['names'], st.session_state['values'], st.session_state['f_name']= FA_EPID.faepid(file)
            # st.write(st.session_state['names'])
            # st.write(st.session_state['values'])

            with st.spinner("Database inserting/uploading..."):
                if st.session_state['authentication_status'] is not None:
                    t_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                    t = str(t_timezone.replace(tzinfo=None))
                    date_table = (str(t.day) + '/' + str(t.month) + '/' + str(t.year) + ' ' + str(t.hour) + ':' + 
                                            str(t.minute) + ':' + str(t.second))

                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'Field_Analysis'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()

                    # INFO from DICOM images
                    dcm_read = DicomImage(file)
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
                    key = file.name

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