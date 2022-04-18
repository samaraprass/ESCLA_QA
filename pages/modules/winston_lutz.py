from pylinac import WinstonLutz
import streamlit as st
from pylinac.core.image import DicomImage
from pylinac.core.decorators import lru_cache
import zipfile
import io
import matplotlib.pyplot as plt
import pages.core.text as text
import pages.core.table_function as table
import pandas as pd
from datetime import datetime
import pages.core.pdf_new as PDF
from st_btn_select import st_btn_select
import os
from deta import Deta
import pages.core.database as DB
import tempfile
import shutil
import pytz

if 'gplot' not in st.session_state:
    st.session_state['gplot'] = None

if 'colplot' not in st.session_state:
    st.session_state['colplot'] = None

if 'cplot' not in st.session_state:
    st.session_state['cplot'] = None

if 'filewl' not in st.session_state:
    st.session_state['filewl'] = None

if 'names_wl' not in st.session_state:
    st.session_state['names_wl'] = None

# if 'values_wl' not in st.session_state:
#     st.session_state['values_wl'] = None


def wl():
    file_zip = st.file_uploader("Choose your Winston-Lutz images (please, upload a zip file)", type=["ZIP"], key='drgs')
    if file_zip is None:
        st.markdown("---")
        text.title("Choose your files to start using this app!", 20, "#8C438D")

    else:
        st.markdown("---")
        #st.write(file_zip)
        d1, d2, d3 = st.columns(3)

        with d2:
            page1 = st_btn_select(('1. PERFORM TEST', '2. CREATE PDF REPORT'), nav=False)

        if page1 == '1. PERFORM TEST':
            with st.spinner("Loading Analysis..."):
                @st.cache(allow_output_mutation=True, show_spinner=False)
                def wl_func(zip):
                    file = zip.read()
                    zipfile_ob = zipfile.ZipFile(io.BytesIO(file), 'r')
                    file_wl = WinstonLutz.from_zip(io.BytesIO(file))
                    # files_name = zipfile_ob.namelist()
                    file_wl.analyze()
                    return file_wl, zipfile_ob, file

                text.title("Result Analysis", 20, "#8C438D")

                wl1, wl2 = st.columns(2)
                with wl1:
                    st.session_state['filewl'], zipfileob, file = wl_func(file_zip)
                    #info_zip = zipfileob.getinfo('RI.10102015.Col_1-10_1_21.dcm')
                    #st.write(os.path.basename(info_zip.filename))
                    figt = plt.figure()
                    st.session_state['filewl'].plot_summary()
                    st.pyplot(figt.show())

                with wl2:
                    # @st.cache(allow_output_mutation=True, show_spinner=False)
                    def results_wl():
                        st.session_state['names_wl'] = ['Pylinac Version', 'Date of Analysis', 'Nº Gantry Images', 'Nº Gantry&Collimator Images', 'Nº Collimator Images', 'Nº Couch Images',
                                'Total Number of Images', 'Maximum 2D CAX to BB distance (mm)', 'Median 2D CAX to BB (mm)', 'Maximum 2D CAX to EPID (mm)', 'Median 2D CAX to EPID (mm)', 
                                'Gantry 3D isocenter diameter (mm)', 'Maximum Gantry RMS deviation (mm)', 'Maximum EPID RMS deviation (mm)', 
                                'Gantry+Collimator 3D isocenter diameter (mm)', 'Collimator 2D isocenter diameter (mm)', 'Maximum Collimator RMS deviation (mm)', 'Couch 2D isocenter diameter (mm)', 
                                'Maximum Couch RMS deviation (mm)','Shift to iso (facing gantry)']
                        
                        results = st.session_state['filewl'].results_data(as_dict=True)

                        date_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                        date_i = str(date_timezone.replace(tzinfo=None))
                        format_date = "%Y-%m-%d %H:%M:%S.%f"
                        real_date = datetime.strptime(date_i, format_date)
                        date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                                        str(real_date.minute) + ':' + str(real_date.second)) 

                        values_wl = [results['pylinac_version'], date_table]
                        l_r = list(results.values())

                        for i in range(2, 19):
                            values_wl.append(round(l_r[i], 4))

                        values_wl.append(st.session_state['filewl'].bb_shift_instructions())

                        t = pd.DataFrame(values_wl, columns=["Results"])
                        t.insert(0, "Parameters", st.session_state['names_wl'], True)
                        #tab = t.round(decimals=4)
                        fig, ax = table.render_mpl_table(t)
                        buf= io.BytesIO()
                        lru_cache(fig.savefig(buf, bbox_inches='tight', dpi=1000, format="png", transparent=True))

                        return buf, values_wl

                    table_wl, st.session_state['values_wl'] = results_wl()
                    #st.session_state['values_wl'] = values_wl
                    lru_cache(st.image(table_wl, width=500, use_column_width=True))
    
            with st.spinner("Loading Images..."):
                d1, d2, d3 = st.columns([2,4.25,1.5])
                with d2:
                    page2 = st_btn_select(('1.1. GANTRY IMAGES', '1.2. COLLIMATOR IMAGES', '1.3. COUCH IMAGES'), nav=False)

                
                if page2 == '1.1. GANTRY IMAGES':
                    st.session_state['gplot'] = st.session_state['filewl'].plot_images(axis = 'Gantry')
                    lru_cache(st.pyplot(st.session_state['gplot']))
                    
                if page2 == '1.2. COLLIMATOR IMAGES':
                    st.session_state['colplot'] = st.session_state['filewl'].plot_images(axis='Collimator')
                    lru_cache(st.pyplot(st.session_state['colplot']))

                if page2 == '1.3. COUCH IMAGES':
                    st.session_state['cplot'] = st.session_state['filewl'].plot_images(axis='Couch')
                    lru_cache(st.pyplot(st.session_state['cplot']))
            
            with st.spinner("Database inserting/uploading..."):
                if st.session_state['authentication_status'] is not None:
                    t_timezone = datetime.now(pytz.timezone("America/Sao_Paulo"))
                    t = t_timezone.replace(tzinfo=None)
                    date_table = (str(t.day) + '/' + str(t.month) + '/' + str(t.year) + ' ' + str(t.hour) + ':' + 
                                            str(t.minute) + ':' + str(t.second))

                    # Date from test image
                    with zipfile.ZipFile(io.BytesIO(file), 'r') as zip:
                        path = tempfile.mkdtemp()
                        zip.extractall(path)
                        for root, _, filenames_wl in os.walk(path):
                            #for filename in filenames_wl:
                            filename = filenames_wl[0]
                            filepath = os.path.join(root, filename)
                            dcm_read = DicomImage(filepath).metadata
                            date_img = dcm_read.AcquisitionDate
                        shutil.rmtree(path)
                    date_time_obj = datetime.strptime(date_img, '%Y%m%d')
                    date_obj = date_time_obj.date()

                    if st.session_state['unit'] != None:                
                        # Deta Database Connection
                        data_connection = Deta(st.secrets['database']['data_key'])
                        user_test = st.session_state['username'] + 'Winston_Lutz'+ '_' + st.session_state['unit']
                        db = data_connection.Base(user_test)
                        fetch_res = db.fetch()

                        keys = [] # database keys list
                        for i in fetch_res.items:
                            keys.append(i['key'])
                        
                        # Variables to db function
                        n_gantry_imgs = st.session_state['values_wl'][2]
                        n_gan_col_imgs = st.session_state['values_wl'][3]
                        n_col_imgs = st.session_state['values_wl'][4]
                        n_couch_imgs = st.session_state['values_wl'][5]
                        n_tot_imgs =st.session_state['values_wl'][6]
                        max_2d_cax_bb = st.session_state['values_wl'][7]
                        median_2d_cax_bb = st.session_state['values_wl'][8]
                        max_2d_cax_epid = st.session_state['values_wl'][9]
                        median_2d_cax_epid = st.session_state['values_wl'][10]
                        gantry_3d_iso_diam = st.session_state['values_wl'][11]
                        max_gantry_rms_dev = st.session_state['values_wl'][12]
                        max_epid_rms_dev = st.session_state['values_wl'][13]
                        gantry_coll_3d_iso_diam = st.session_state['values_wl'][14]
                        coll_2d_iso_diam = st.session_state['values_wl'][15]
                        max_coll_rms_dev = st.session_state['values_wl'][16]
                        couch_2d_iso = st.session_state['values_wl'][17]
                        max_couch_rms_dev = st.session_state['values_wl'][18]
                        shift = st.session_state['values_wl'][19]
                        analy_date = date_table
                        date_linac = str(date_obj)
                        key_w = file_zip.name
                        
                        # Insert new registration
                        if key_w in keys:
                            st.warning("Already exist analysis results for this image on database. For saving new analysis, press button bellow.")
                            bs = st.button("Save")
                            if bs:
                                DB.database_update_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb,
                                median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, max_epid_rms_dev,
                                gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, max_couch_rms_dev, shift, analy_date,
                                date_linac, key_w)
                                st.success(f"New analysis of {key_w} saved")
                        
                        # Updating registration
                        if key_w not in keys:
                            DB.database_insert_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb,
                                median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, max_epid_rms_dev,
                                gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, max_couch_rms_dev, shift, analy_date,
                                date_linac, key_w)
                            st.success(f"Analysis results of {key_w} saved")

                    if st.session_state['unit'] == None:                
                        # Deta Database Connection
                        data_connection = Deta(st.secrets['database']['data_key'])
                        user_test = st.session_state['username'] + 'Winston_Lutz'
                        db = data_connection.Base(user_test)
                        fetch_res = db.fetch()

                        keys = [] # database keys list
                        for i in fetch_res.items:
                            keys.append(i['key'])
                        
                        # Variables to db function
                        n_gantry_imgs = st.session_state['values_wl'][2]
                        n_gan_col_imgs = st.session_state['values_wl'][3]
                        n_col_imgs = st.session_state['values_wl'][4]
                        n_couch_imgs = st.session_state['values_wl'][5]
                        n_tot_imgs =st.session_state['values_wl'][6]
                        max_2d_cax_bb = st.session_state['values_wl'][7]
                        median_2d_cax_bb = st.session_state['values_wl'][8]
                        max_2d_cax_epid = st.session_state['values_wl'][9]
                        median_2d_cax_epid = st.session_state['values_wl'][10]
                        gantry_3d_iso_diam = st.session_state['values_wl'][11]
                        max_gantry_rms_dev = st.session_state['values_wl'][12]
                        max_epid_rms_dev = st.session_state['values_wl'][13]
                        gantry_coll_3d_iso_diam = st.session_state['values_wl'][14]
                        coll_2d_iso_diam = st.session_state['values_wl'][15]
                        max_coll_rms_dev = st.session_state['values_wl'][16]
                        couch_2d_iso = st.session_state['values_wl'][17]
                        max_couch_rms_dev = st.session_state['values_wl'][18]
                        shift = st.session_state['values_wl'][19]
                        analy_date = date_table
                        date_linac = str(date_obj)
                        key_w = file_zip.name
                        
                        # Insert new registration
                        if key_w in keys:
                            st.warning("Already exist analysis results for this image on database. For saving new analysis, press button bellow.")
                            bs = st.button("Save")
                            if bs:
                                DB.database_update_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb,
                                median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, max_epid_rms_dev,
                                gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, max_couch_rms_dev, shift, analy_date,
                                date_linac, key_w)
                                st.success(f"New analysis of {key_w} saved")
                        
                        # Updating registration
                        if key_w not in keys:
                            DB.database_insert_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb,
                                median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, max_epid_rms_dev,
                                gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, max_couch_rms_dev, shift, analy_date,
                                date_linac, key_w)
                            st.success(f"Analysis results of {key_w} saved")     

        elif page1 == '2. CREATE PDF REPORT':
            st.subheader("PDF Report")
            with st.form(key="pdf_report"):
                pdf1, pdf2 = st.columns(2)
                with pdf1:
                    test_name = st.text_input("Test name", value="Winston-Lutz")

                    t_name = "Report - " + test_name

                    institution = st.text_input("Institution name")
                    single_imgs = st.selectbox("Single Gantry, Collimator and Couch Images", [True, False], index=1, help="Apply 'True' if you "
                    "prefer to add single images of gantry, collimator and couch.")
                        
                with pdf2:
                    author = st.text_input("Author name")
                    unit = st.text_input("Unit model name")
                    file_name = st.text_input("Choose the report file name")

                submit_button = st.form_submit_button(label='Apply')

            if submit_button:
                if test_name or t_name or institution or author or unit or file_name is None:
                    st.warning("⚠️ All fields should be filled!")
                
                if test_name and t_name and institution and author and unit and file_name != None:
                    with st.spinner("Creating your PDF report..."):
                        PDF.create_pdf_WL(st.session_state['filewl'], st.session_state['values_wl'], st.session_state['names_wl'], t_name, 
                                            institution, author, unit, file_name, single_imgs)