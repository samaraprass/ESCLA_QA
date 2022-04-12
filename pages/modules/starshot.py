from reprlib import recursive_repr
import streamlit as st
from pylinac.core.image import DicomImage
from pylinac.core.decorators import lru_cache
import io
import pages.core.text as text
import pages.core.table_function as table
from pylinac import Starshot
import pandas as pd
from datetime import datetime
from pylinac.core.image import load_multiples
from st_btn_select import st_btn_select
import pages.core.pdf_new as PDF
import chime
from deta import Deta
import pages.core.database as DB
import pytz
import numpy as np

if 'min_peak_height' not in st.session_state:
    st.session_state['min_peak_height'] = None

if 'tolerance' not in st.session_state:
    st.session_state['tolerance'] = None

if 'start_point' not in st.session_state:
    st.session_state['start_point'] = None

if 'fwhm' not in st.session_state:
    st.session_state['fwhm'] = None

if 'invert' not in st.session_state:
    st.session_state['invert'] = None

if 'names_figs' not in st.session_state:
    st.session_state['names_figs'] = None

if 'star' not in st.session_state:
    st.session_state['star'] = None

if 'table' not in st.session_state:
    st.session_state['table'] = None

if 'names_stars' not in st.session_state:
    st.session_state['names_stars'] = None

if 'values_stars' not in st.session_state:
    st.session_state['values_stars'] = None

if 'files_names' not in st.session_state:
    st.session_state['files_names'] = None

if 'rs' not in st.session_state:
    st.session_state['rs'] = None

if 'star_s' not in st.session_state:
    st.session_state['star_s'] = None

if 'names_s' not in st.session_state:
    st.session_state['names_s'] = None

if 'values_s' not in st.session_state:
    st.session_state['values_s'] = None

if 'r_s' not in st.session_state:
    st.session_state['r_s'] = None

def star():
    pages = st_btn_select(('Multiple Files', 'Single File'), nav=False)

    # MULTIPLE FILES
    if pages == 'Multiple Files':
        star_imgs = st.file_uploader("Choose your Starshot files", accept_multiple_files=True, key="multiple_files", type=['DCM'])
        with st.expander(" 📊 Click here to change the analysis paremeters"):
            with st.form(key="analysis_m"):
                t_drgs = 'Analysis parameters'
                text.body(t_drgs, 18, "black")
                
                s1, s2 = st.columns(2)

                with s1:
                    st.session_state['radius'] = st.number_input("Choose distance in '%' between starting point and closest image edge",
                                            min_value=0.05, value=0.75, max_value=0.95, help="Used to build the circular profile which finds"
                                            " the radiation lines.")
                    
                    st.session_state['min_peak_height'] = st.number_input("Choose the percentage minimum height a peak must be to be considered a valid peak", 
                                                        min_value=0.05, max_value=0.95, value=0.25,
                                                        help="If necessary, lower value for gantry shots and increase for noisy images.")

                    st.session_state['tolerance'] = st.number_input("Choose tolerance in mm", max_value=10.0, min_value=0.1, value=1.0, help="The tolerance in mm" 
                                                " to test against for a pass/fail result.")

                with s2:
                    st.session_state['start_point'] = st.selectbox("Circle profile center coordinates", [None, "Manual insert"], help='The point where the algorithm' 
                    ' should center the circle profile. If "None" (default), pylinac will automatically search for maximum point nearest the center of the image.')

                    st.session_state['fwhm'] = st.selectbox("Full width at half maximum", [True, False], index=1, help='In practice, this ends up being a very small difference.' 
                                        'Set to false if peak locations are offset or unexpected.')

                    # recursive = st.selectbox("",[True, False])
                
                    st.session_state['invert'] = st.selectbox("Invert image values", [False, True], help="This should be set to True if the automatically-determined"
                                    " pylinac inversion is incorrect.")
                

                s_1, s_2, s_3 = st.columns([1,2,1])
                with s_2:
                    if st.session_state['start_point'] == "Manual insert":
                        x_c = st.number_input("Set the x-coordinate")
                        y_c = st.number_input("Set the y-coordinate")

                        start_point = (x_c, y_c)

                submit_button = st.form_submit_button(label='Apply')
        if len(star_imgs) == 0:
            st.markdown("---")
            text.title("Choose your files to start using this app!", 20, "#8C438D")
        
        else:
            st.markdown("---")
            ss1, ss2, ss3 = st.columns([1.3, 2, 0.5])
            with ss2:
                main_pages = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)
            if main_pages == '1. PERFORM TEST': 
                # Load Image to module
                with st.spinner("Loading analysis"):
                    paths = star_imgs
                    names = [paths[0].name, paths[1].name, paths[2].name, paths[3].name]
                    names_sorted = np.sort(names)
                    superimposed_img = load_multiples(paths)

                
                    st.session_state['star'] = Starshot(superimposed_img)
                    
                    # Analyze Image
                    st.session_state['star'].analyze(radius=st.session_state['radius'], min_peak_height=st.session_state['min_peak_height'], tolerance=st.session_state['tolerance'], 
                    start_point=st.session_state['start_point'], fwhm=st.session_state['fwhm'], invert=st.session_state['invert'], recursive=True)
                    # star.analyze()
                    # Results as dictionary
                    r  = st.session_state['star'].results_data(as_dict=True)
                    result = st.session_state['star'].passed

                    # RESULT TABLE
                    if str(result) == 'True':
                        st.session_state['rs'] = "PASS"

                    elif str(result) == 'False':
                        st.session_state['rs'] = "FAIL"

                
                    @st.cache(allow_output_mutation=True, show_spinner=False)
                    def table_4():
                        date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                        date_i = str(date_timezone.replace(tzinfo=None))
                        format_date = "%Y-%m-%d %H:%M:%S.%f"
                        real_date = datetime.strptime(date_i, format_date)
                        date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                    str(real_date.minute) + ':' + str(real_date.second)) 
                        names = ["Date of Analysis","Tolerance (mm)", "Circle Diameter (mm)", "Circle Radius (mm)", "Circle Center (x, y)", "Results"]
                        values = [date_table, r["tolerance_mm"], round(r['circle_diameter_mm'], 4), round(r["circle_radius_mm"], 4), r["circle_center_x_y"], st.session_state['rs']]
                        t = pd.DataFrame(values, columns=["Results"])
                        t.insert(0, "Parameters", names, True)
                        tab = t.round(decimals=4)
                        fig, ax = table.render_mpl_table(tab)
                        buf = io.BytesIO()
                        fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                        return buf, names, values, date_table

                text.title("Result Analysis", 20, "#8C438D")
                st.session_state['table'], st.session_state['names_stars'], st.session_state['values_stars'], st.session_state['date_table'] = table_4()
                S1, S2, S3 = st.columns([1,4,1])

                with S2:
                    st.image(st.session_state['table'])

                S_1, S_2, S_3, S_4, S_5 = st.columns([1,2,0.1,2,1])

                with S_2:
                    st.pyplot(st.session_state['star'].plot_analyzed_subimage('wobble'))

                with S_4:
                    st.pyplot(st.session_state['star'].plot_analyzed_subimage('whole'))
                
                st.session_state['files_names']=[]
                for i in star_imgs:
                    st.session_state['files_names'].append(i.name)

                # DATABASE
                if st.session_state['authentication_status'] is not None:
                    # Date from test image
                    dcm_read = DicomImage(star_imgs[0])
                    date_dcm = dcm_read.metadata.AcquisitionDate

                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'Starshot'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()
                    
                    keys = [] # database keys list
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    date_time_obj = datetime.strptime(date_dcm, '%Y%m%d')
                    date_obj = date_time_obj.date()
                    
                    # Variables to db function
                    tol = r["tolerance_mm"]
                    circ_diam = round(r['circle_diameter_mm'], 4)
                    circ_radius = round(r["circle_radius_mm"], 4)
                    circ_center = str(r["circle_center_x_y"])
                    t_result = st.session_state['rs']
                    analy_date = st.session_state['date_table']
                    date_linac = str(date_obj)
                    key_star = names_sorted[0]
                
                    # Update new registration
                    if key_star in keys:
                        chime.info()
                        st.warning("Analysis results already exist for this image in database. For saving new analysis, press 'Save'.")
                        bs = st.button("Save")
                        if bs:
                            DB.database_update_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key_star)
                            st.success(f"New analysis of {key_star} set saved")
                            chime.success()
                    
                    # Insert registration
                    elif key_star not in keys:
                        DB.database_insert_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key_star)
                        st.success("Analysis results saved")
                        chime.success()          

            if main_pages == '2. CREATE PDF REPORT':
                st.subheader("PDF Report")
                with st.form(key="pdf_report"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name = st.text_input("Test name", value="Starshot")

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
                            pdf = PDF.pdf_star_mf(t_name, institution, author, unit, 
                                                st.session_state['star'], st.session_state['names_stars'], st.session_state['values_stars'],
                                                st.session_state['files_names'], st.session_state['rs'])
                        html_pf = PDF.create_download_link(pdf.output(dest="S"), file_name)
                        chime.theme('mario')
                        chime.success()
                        st.success("Your PDF report is ready!")
                        st.markdown(html_pf, unsafe_allow_html=True)

                

    # SINGLE FILE
    elif pages == 'Single File':
        st.session_state['star_image'] = st.file_uploader("Choose your Starshot file", key="single_file", type=[".DCM"])
        with st.expander(" 📊 Click here to change the analysis paremeters"):
            with st.form(key="analysis_s"):
                t_star = 'Analysis parameters'
                text.body(t_star, 18, "black")
                
                s1, s2 = st.columns(2)

                with s1:
                    st.session_state['radius_s'] = st.number_input("Choose distance in '%' between starting point and closest image edge",
                                            min_value=0.05, max_value=0.95, value=0.85, help="Used to build the circular profile which finds"
                                            " the radiation lines.")
                    
                    st.session_state['min_peak_height_s'] = st.number_input("Choose the percentage minimum height a peak must be to be considered a valid peak", 
                                                        min_value=0.05, max_value=0.95, value=0.25,
                                                        help="If necessary, lower value for gantry shots and increase for noisy images.")

                    st.session_state['tolerance_s'] = st.number_input("Choose tolerance in mm", max_value=10.0, min_value=0.1, value=1.0, help="The tolerance in mm" 
                                                " to test against for a pass/fail result.")

                with s2:
                    st.session_state['start_point_s'] = st.selectbox("Circle profile center coordinates", [None, "Manual insert"], help='The point where the algorithm' 
                    ' should center the circle profile. If "None" (default), pylinac will automatically search for maximum point nearest the center of the image.')

                    st.session_state['fwhm_s'] = st.selectbox("Full width at half maximum", [True, False],help='In practice, this ends up being a very small difference.' 
                                        'Set to false if peak locations are offset or unexpected.')

                    # recursive = st.selectbox("",[True, False])
                
                    st.session_state['invert_s'] = st.selectbox("Invert image values", [False, True], help="This should be set to True if the automatically-determined"
                                    " pylinac inversion is incorrect.")
                    
                s_1, s_2, s_3 = st.columns([1,2,1])
                with s_2:
                    if st.session_state['start_point_s'] == "Manual insert":
                        x_c = st.number_input("Set the x-coordinate")
                        y_c = st.number_input("Set the y-coordinate")

                        st.session_state['start_point_s'] = (x_c, y_c)   

                submit_button = st.form_submit_button(label='Apply')

        if st.session_state['star_image'] is None:
            st.markdown('---')
            text.title("Choose your files to start using this app!", 20, "#8C438D")
        
        else:
            st.markdown('---')
            ss_1, ss_2, ss_3 = st.columns([1.3, 2, 0.5])
            with ss_2:
                main_pages = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)
            
            if main_pages == "1. PERFORM TEST":
                # PFA_IMAGE.input_image(star_image)
                # Load Image to module
                st.session_state['star_s'] = Starshot(st.session_state['star_image'])
            
                # Analyze Image
                st.session_state['star_s'].analyze(radius=st.session_state['radius_s'], min_peak_height=st.session_state['min_peak_height_s'], 
                             tolerance=st.session_state['tolerance_s'], start_point=st.session_state['start_point_s'], 
                             fwhm=st.session_state['fwhm_s'], invert=st.session_state['invert_s'])
                # star.analyze()
                # Results as dictionary
                r  = st.session_state['star_s'].results_data(as_dict=True)

                if r['passed'] == True:
                    st.session_state['r_s'] = "PASS"
                
                elif r["passed"] == False:
                    st.session_state['r_s'] = "FAIL"

                @st.cache(allow_output_mutation=True, show_spinner=False)
                def table_1():
                    date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                    date_i = str(date_timezone.replace(tzinfo=None))
                    format_date = "%Y-%m-%d %H:%M:%S.%f"
                    real_date = datetime.strptime(date_i, format_date)
                    date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                str(real_date.minute) + ':' + str(real_date.second)) 
                    names_s = ["Results", "Date of Analysis","Tolerance (mm)", "Circle Diameter (mm)", "Circle Radius (mm)", "Circle Center (x, y)"]
                    values_s = [st.session_state['r_s'], date_table, r["tolerance_mm"], round(r['circle_diameter_mm'], 4), round(r["circle_radius_mm"], 4), r["circle_center_x_y"]]
                    t = pd.DataFrame(values_s, columns=["Results"])
                    t.insert(0, "Parameters", names_s, True)
                    tab = t.round(decimals=4)
                    fig, ax = table.render_mpl_table(tab)
                    buf = io.BytesIO()
                    fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True)

                    return buf, names_s, values_s, date_table

                text.title("Result Analysis", 20, "#8C438D")
                table_s, st.session_state['names_s'], st.session_state['values_s'], st.session_state['date_table'] = table_1()
                S1, S2, S3 = st.columns([1,4,1])

                with S2:
                    st.image(table_s)

                S_1, S_2, S_3, S_4, S_5 = st.columns([1,2,0.1,2,1])

                with S_2:
                    st.pyplot(st.session_state['star_s'].plot_analyzed_subimage('wobble'))

                with S_4:
                    st.pyplot(st.session_state['star_s'].plot_analyzed_subimage('whole'))
                

                # DATABASE
                if st.session_state['authentication_status'] is not None:
                    # Deta Database Connection
                    data_connection = Deta(st.secrets['database']['data_key'])
                    user_test = st.session_state['username'] + 'Starshot'
                    db = data_connection.Base(user_test)
                    fetch_res = db.fetch()

                    # Date from test image
                    
                    try:
                        dcm_read = DicomImage(st.session_state['star_image'])
                        date_dcm = dcm_read.metadata.AcquisitionDate
                        date_time_obj = datetime.strptime(date_dcm, '%Y%m%d')
                        date_obj = date_time_obj.date()

                    except:
                        date_obj = None

                    keys = [] # database keys list
                    for i in fetch_res.items:
                        keys.append(i['key'])
                    
                    tol = r["tolerance_mm"]
                    circ_diam = round(r['circle_diameter_mm'], 4)
                    circ_radius = round(r["circle_radius_mm"], 4)
                    circ_center = str(r["circle_center_x_y"])
                    t_result = st.session_state['r_s']
                    analy_date = st.session_state['date_table']
                    date_linac = str(date_obj)
                    key_star = st.session_state['star_image'].name

                    # Update new registration
                    if key_star in keys:
                        chime.info()
                        st.warning("Analysis results already exist for this image in database. For saving new analysis, press 'Save'.")
                        bs = st.button("Save")
                        if bs:
                            DB.database_update_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key_star)
                            st.success("New analysis saved")
                            chime.success()
                    
                    # Insert registration
                    elif key_star not in keys:
                        DB.database_insert_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key_star)
                        st.success("Analysis results saved")
                        chime.success()

            if main_pages == "2. CREATE PDF REPORT":
                st.subheader("PDF Report")
                with st.form(key="pdf_report"):
                    pdf1, pdf2 = st.columns(2)
                    with pdf1:
                        test_name = st.text_input("Test name", value="Starshot")

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
                            pdf = PDF.pdf_star_sf(t_name, institution, author, unit, 
                                                st.session_state['star_s'], st.session_state['names_s'], st.session_state['values_s'],
                                                st.session_state['star_image'].name, st.session_state['r_s'])
                            html_pf = PDF.create_download_link(pdf.output(dest="S"), file_name)
                        chime.theme('mario')
                        chime.success()
                        st.success("Your PDF report is ready!")
                        st.markdown(html_pf, unsafe_allow_html=True)