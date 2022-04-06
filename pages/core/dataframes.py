from optparse import Values
from turtle import color
import streamlit as st
from deta import Deta
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go

def dataframe_drgs():
    #Connect Database
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'VMAT_DRGS'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")
    
    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'CAX', 'SID', 'Tolerance', 'Absolute Mean Deviation (%)',  'Maximum Deviation (%)', 
                        'Result']

                files = []
                date_analysis = []
                date_linac = []
                cax = []
                sid = []
                tolerance = []
                abs_mean_dev = []
                max_dev = []
                results = []
                for i in st.session_state['sorted_dates_drgs']:
                    fetch_res2 = db.fetch({"date_linac": i})
                    files.append(fetch_res2.items[0]["key"])
                    date_analysis.append(fetch_res2.items[0]['date_analysis'])
                    date_linac.append(fetch_res2.items[0]['date_linac'])
                    cax.append(fetch_res2.items[0]['cax'])
                    sid.append(fetch_res2.items[0]['sid'])
                    tolerance.append(fetch_res2.items[0]['tolerance'])
                    abs_mean_dev.append(fetch_res2.items[0]["abs_mean_dev"])
                    max_dev.append(fetch_res2.items[0]["max_dev"])
                    results.append(fetch_res2.items[0]['result'])
                        
                data = {names[0]: files, names[1]: date_analysis, names[2]: date_linac, names[3]: cax, names[4]: sid, names[5]: tolerance, 
                        names[6]: abs_mean_dev, names[7]: max_dev, names[8]: results}

                
                df_drgs = pd.DataFrame(data)

                st.dataframe(df_drgs)

def dataframe_drmlc():
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'VMAT_DRMLC'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")
    
    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'CAX', 'SID', 'Tolerance', 'Absolute Mean Deviation (%)',  'Maximum Deviation (%)', 
                        'Result']

                files = []
                date_analysis = []
                date_linac = []
                cax = []
                sid = []
                tolerance = []
                abs_mean_dev = []
                max_dev = []
                results = []
                for i in st.session_state['sorted_dates_drgs']:
                    fetch_res2 = db.fetch({"date_linac": i})
                    files.append(fetch_res2.items[0]["key"])
                    date_analysis.append(fetch_res2.items[0]['date_analysis'])
                    date_linac.append(fetch_res2.items[0]['date_linac'])
                    cax.append(fetch_res2.items[0]['cax'])
                    sid.append(fetch_res2.items[0]['sid'])
                    tolerance.append(fetch_res2.items[0]['tolerance'])
                    abs_mean_dev.append(fetch_res2.items[0]["abs_mean_dev"])
                    max_dev.append(fetch_res2.items[0]["max_dev"])
                    results.append(fetch_res2.items[0]['result'])
                        
                data = {names[0]: files, names[1]: date_analysis, names[2]: date_linac, names[3]: cax, names[4]: sid, names[5]: tolerance, 
                        names[6]: abs_mean_dev, names[7]: max_dev, names[8]: results}

                
                df_drmlc = pd.DataFrame(data)

                st.dataframe(df_drmlc)

def dataframe_star():
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Starshot'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")

    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'Circle Center', 'Circle Diameter', 'Circle Radius', 'Tolerance', 'Result']

                files = []
                date_analysis = []
                date_linac = []
                circle_center = []
                circle_diameter = []
                circle_radius = []
                tolerance = []
                results = []
                for i in st.session_state['sorted_dates_star']:
                    fetch_res2 = db.fetch({"date_linac": i})
                    files.append(fetch_res2.items[0]["key"])
                    date_analysis.append(fetch_res2.items[0]['date_analysis'])
                    date_linac.append(fetch_res2.items[0]['date_linac'])
                    circle_center.append(fetch_res2.items[0]['circle_center'])
                    circle_diameter.append(fetch_res2.items[0]['circle_diameter'])
                    tolerance.append(fetch_res2.items[0]['tolerance'])
                    circle_radius.append(fetch_res2.items[0]["circle_radius"])
                    results.append(fetch_res2.items[0]['result'])
                
                data = {names[0]: files, names[1]: date_analysis, names[2]: date_linac, names[3]: circle_center, names[4]: circle_diameter, names[5]: circle_radius, 
                        names[6]: tolerance, names[7]: results}

                
                df_star = pd.DataFrame(data)

                colors = ['rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)',
                        'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(107, 174, 214)']         
                
        
                
                st.dataframe(df_star)

def dataframe_picket_fence(angle):
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Picket_Fence'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")

    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'Angle', 'Absolute Median Error (mm)', 
                'Maximum Error (mm)', 'Mean Picket Spacing (mm)', 'MLC Type', 'Number Pickets', 'Percent Leaves Passing (%)',
                'Tolerance (mm)', 'Result']

                colors = ['rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)',
                        'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)',
                        'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(189, 215, 231)', 'rgb(107, 174, 214)']

                same_angle0 = []
                same_angle90 = []
                same_angle180 = []
                same_angle270 = []
                for i in st.session_state['sorted_dates_pf']:
                    fetch_res2 = db.fetch({"date_linac": i})
                    same_angle0.append(fetch_res2.items[0])
                    same_angle90.append(fetch_res2.items[3])
                    same_angle180.append(fetch_res2.items[1])
                    same_angle270.append(fetch_res2.items[2])

                
                # Variables for 0º
                files = []
                date_analysis = []
                date_linac = []
                angle_file = []
                abs_median_error0 = []
                max_error0 = []
                mean_picket_spacing0 = []
                mlc_type = []
                number_pickets = []
                percent_leaves = []
                tolerance = []
                results = []
                for i in range(len(st.session_state['sorted_dates_pf'])):
                    files.append(same_angle0[i]["key"])
                    date_analysis.append(same_angle0[i]["date_analysis"])
                    date_linac.append(same_angle0[i]["date_linac"])
                    angle_file.append(same_angle0[i]['angle'])
                    abs_median_error0.append(same_angle0[i]["abs_median_error"])
                    max_error0.append(same_angle0[i]["max_error"])
                    mean_picket_spacing0.append(same_angle0[i]["mean_picket_spacing"])
                    mlc_type.append(same_angle0[i]["mlc_type"])
                    number_pickets.append(same_angle0[i]["number_pickets"])
                    percent_leaves.append(same_angle0[i]["percent_leaves_pass"])
                    tolerance.append(same_angle0[i]["tolerance"])
                    results.append(same_angle0[i]["result"])

                # Variables for 90º
                files_90 = []
                date_analysis_90 = []
                date_linac_90 = []
                angle_file_90 = []
                abs_median_error_90 = []
                max_error_90 = []
                mean_picket_spacing_90 = []
                mlc_type_90 = []
                number_pickets_90 = []
                percent_leaves_90 = []
                tolerance_90 = []
                results_90 = []
                for i in range(len(st.session_state['sorted_dates_pf'])):
                    files_90.append(same_angle90[i]["key"])
                    date_analysis_90.append(same_angle90[i]["date_analysis"])
                    date_linac_90.append(same_angle90[i]["date_linac"])
                    angle_file_90.append(same_angle90[i]['angle'])
                    abs_median_error_90.append(same_angle90[i]["abs_median_error"])
                    max_error_90.append(same_angle90[i]["max_error"])
                    mean_picket_spacing_90.append(same_angle90[i]["mean_picket_spacing"])
                    mlc_type_90.append(same_angle90[i]["mlc_type"])
                    number_pickets_90.append(same_angle90[i]["number_pickets"])
                    percent_leaves_90.append(same_angle90[i]["percent_leaves_pass"])
                    tolerance_90.append(same_angle90[i]["tolerance"])
                    results_90.append(same_angle90[i]["result"])

                # Variables for 180º
                files_180 = []
                date_analysis_180 = []
                date_linac_180 = []
                angle_file_180 = []
                abs_median_error_180 = []
                max_error_180 = []
                mean_picket_spacing_180 = []
                mlc_type_180 = []
                number_pickets_180 = []
                percent_leaves_180 = []
                tolerance_180 = []
                results_180 = []
                for i in range(len(st.session_state['sorted_dates_pf'])):
                    files_180.append(same_angle180[i]["key"])
                    date_analysis_180.append(same_angle180[i]["date_analysis"])
                    date_linac_180.append(same_angle180[i]["date_linac"])
                    angle_file_180.append(same_angle180[i]['angle'])
                    abs_median_error_180.append(same_angle180[i]["abs_median_error"])
                    max_error_180.append(same_angle180[i]["max_error"])
                    mean_picket_spacing_180.append(same_angle180[i]["mean_picket_spacing"])
                    mlc_type_180.append(same_angle180[i]["mlc_type"])
                    number_pickets_180.append(same_angle180[i]["number_pickets"])
                    percent_leaves_180.append(same_angle180[i]["percent_leaves_pass"])
                    tolerance_180.append(same_angle180[i]["tolerance"])
                    results_180.append(same_angle180[i]["result"])

                # Variables for 270º
                files_270 = []
                date_analysis_270 = []
                date_linac_270 = []
                angle_file_270 = []
                abs_median_error_270 = []
                max_error_270 = []
                mean_picket_spacing_270 = []
                mlc_type_270 = []
                number_pickets_270 = []
                percent_leaves_270 = []
                tolerance_270 = []
                results_270 = []
                for i in range(len(st.session_state['sorted_dates_pf'])):
                    files_270.append(same_angle270[i]["key"])
                    date_analysis_270.append(same_angle270[i]["date_analysis"])
                    date_linac_270.append(same_angle270[i]["date_linac"])
                    angle_file_270.append(same_angle270[i]['angle'])
                    abs_median_error_270.append(same_angle270[i]["abs_median_error"])
                    max_error_270.append(same_angle270[i]["max_error"])
                    mean_picket_spacing_270.append(same_angle270[i]["mean_picket_spacing"])
                    mlc_type_270.append(same_angle270[i]["mlc_type"])
                    number_pickets_270.append(same_angle270[i]["number_pickets"])
                    percent_leaves_270.append(same_angle270[i]["percent_leaves_pass"])
                    tolerance_270.append(same_angle270[i]["tolerance"])
                    results_270.append(same_angle270[i]["result"])

                if angle == 0:
                    data1 = {names[0]: files, names[1]: date_analysis, names[2]: date_linac, names[3]: angle_file, names[4]: abs_median_error0, 
                    names[5]: max_error0, names[6]: mean_picket_spacing0, names[7]: mlc_type, names[8]: number_pickets, 
                    names[9]: percent_leaves, names[10]: tolerance, names[11]: results}                
                    df_pf1 = pd.DataFrame(data1)
                    
                    st.dataframe(df_pf1)
                
                if angle == 90:
                    data2 = {names[0]: files_90, names[1]: date_analysis_90, names[2]: date_linac_90, names[3]: angle_file_90, names[4]: abs_median_error_90, 
                    names[5]: max_error_90, names[6]: mean_picket_spacing_90, names[7]: mlc_type_90, names[8]: number_pickets_90, 
                    names[9]: percent_leaves_90, names[10]: tolerance_90, names[11]: results_90}                
                    df_pf2 = pd.DataFrame(data2)
                    
                    st.dataframe(df_pf2)
                
                if angle == 180:
                    data3 = {names[0]: files_180, names[1]: date_analysis_180, names[2]: date_linac_180, names[3]: angle_file_180, names[4]: abs_median_error_180, 
                    names[5]: max_error_180, names[6]: mean_picket_spacing_180, names[7]: mlc_type_180, names[8]: number_pickets_180, 
                    names[9]: percent_leaves_180, names[10]: tolerance_180, names[11]: results_180}                
                    df_pf3 = pd.DataFrame(data3)
                    
                    st.dataframe(df_pf3)
                
                if angle == 270:
                    data4 = {names[0]: files_270, names[1]: date_analysis_270, names[2]: date_linac_270, names[3]: angle_file_270, names[4]: abs_median_error_270, 
                    names[5]: max_error_270, names[6]: mean_picket_spacing_270, names[7]: mlc_type_270, names[8]: number_pickets_270, 
                    names[9]: percent_leaves_270, names[10]: tolerance_270, names[11]: results_270}                
                    df_pf4 = pd.DataFrame(data4)
            
                    st.dataframe(df_pf4)


def dataframe_wl():
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Winston_Lutz'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")

    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'Collimator 2D isocenter diameter (mm)', 
                        'Couch 2D isocenter diameter (mm)', 'Gantry 3D isocenter diameter (mm)', 'Maximum 2D CAX to BB (mm)', 
                        'Maximum Collimator RMS deviation (mm)', 'Maximum Couch RMS deviation (mm)', 'Maximum Gantry RMS deviation (mm)', 
                        'Nº Gantry Images', 'Nº Grantry&Collimator Images', 'Nº Collimator Images', 'Nº Couch Images', 'Total Nº Images', 
                        'Shift']

                files = []
                date_analysis = []
                date_linac = []
                coll_2d_iso_diam = []
                couch_2d_iso = []
                gantry_3d_iso_diameter = []
                max_2d_cax_to_bb = []
                max_coll_rms_deviation = []
                max_couch_rms_deviation = []
                max_gantry_rms_deviation = []
                n_gantry = []
                n_gantry_collimator = []
                n_collimator = []
                n_couch = []
                n_total = []
                shift = []
                for i in st.session_state['sorted_dates_wl']:
                    fetch_res2 = db.fetch({"date_linac": i})
                    files.append(fetch_res2.items[0]['key'])
                    date_analysis.append(fetch_res2.items[0]['date_analysis'])
                    date_linac.append(fetch_res2.items[0]['date_linac'])
                    coll_2d_iso_diam.append(fetch_res2.items[0]["coll_2d_iso_diam"])
                    couch_2d_iso.append(fetch_res2.items[0]["couch_2d_iso"])
                    gantry_3d_iso_diameter.append(fetch_res2.items[0]["gantry_3d_iso_diameter"])
                    max_2d_cax_to_bb.append(fetch_res2.items[0]["max_2d_cax_to_bb"])
                    max_coll_rms_deviation.append(fetch_res2.items[0]["max_coll_rms_deviation"])
                    max_couch_rms_deviation.append(fetch_res2.items[0]["max_couch_rms_deviation"])
                    max_gantry_rms_deviation.append(fetch_res2.items[0]["max_gantry_rms_deviation"])
                    n_gantry.append(fetch_res2.items[0]['number_gantry_images'])
                    n_gantry_collimator.append(fetch_res2.items[0]['number_gan_coll_images'])
                    n_collimator.append(fetch_res2.items[0]['number_coll_images'])
                    n_couch.append(fetch_res2.items[0]['number_couch_images'])
                    n_total.append(fetch_res2.items[0]['number_total_images'])
                    shift.append(fetch_res2.items[0]['shift'])
                
                data_wl = {names[0]: files, names[1]: date_analysis, names[2]: date_linac, names[3]: coll_2d_iso_diam, names[4]: couch_2d_iso, 
                    names[5]: gantry_3d_iso_diameter, names[6]: max_2d_cax_to_bb, names[7]: max_coll_rms_deviation, names[8]: max_couch_rms_deviation, 
                    names[9]: max_gantry_rms_deviation, names[10]: n_gantry, names[11]: n_gantry_collimator, names[12]: n_collimator, 
                    names[13]: n_couch, names[14]: n_total, names[15]: shift}                
                df_wl = pd.DataFrame(data_wl)

                st.dataframe(df_wl)

def dataframe_fa(type):
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Field_Analysis'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info("Run some tests and see the results timeline here")

    else:
        with st.expander('Click here to expand data'):
            with st.container():
                names = ['File', 'Analysis Date (app)', 'Test Date (from DICOM)', 'Horizontal Field Size (mm)', 'Horizontal Flatness (%)', 
                'Horizontal Symmetry (%)', 'Vertical Flatness (%)', 'Vertical Symmetry (%)', 'Vertical Field Size (mm)']

                if type == '6MV':
                    files_6MV = []
                    date_analysis_6MV = []
                    date_linac_6MV = []
                    horizontal_field_size_6MV = []
                    horizontal_flatness_6MV = []
                    horizontal_symmetry_6MV = []
                    vert_flatness_6MV = []
                    vert_symmetry_6MV = []
                    vertical_field_size_6MV = []
                    for i in range(len(st.session_state['six_mv_sorted'])):
                        files_6MV.append(st.session_state['six_mv_sorted'][i]['key'])
                        date_analysis_6MV.append(st.session_state['six_mv_sorted'][i]['date_analysis'])
                        date_linac_6MV.append(st.session_state['six_mv_sorted'][i]['date_linac'])
                        horizontal_field_size_6MV.append(st.session_state['six_mv_sorted'][i]["horizontal_field_size"])
                        horizontal_flatness_6MV.append(st.session_state['six_mv_sorted'][i]["horizontal_flatness"])
                        horizontal_symmetry_6MV.append(st.session_state['six_mv_sorted'][i]["horizontal_symmetry"])
                        vert_flatness_6MV.append(st.session_state['six_mv_sorted'][i]["vert_flatness"])
                        vert_symmetry_6MV.append(st.session_state['six_mv_sorted'][i]["vert_symmetry"])
                        vertical_field_size_6MV.append(st.session_state['six_mv_sorted'][i]["vertical_field_size"])
                    
                    data_6MV = {names[0]: files_6MV, names[1]: date_analysis_6MV, names[2]: date_linac_6MV, names[3]: horizontal_field_size_6MV, names[4]: horizontal_flatness_6MV, 
                    names[5]: horizontal_symmetry_6MV, names[6]: vert_flatness_6MV, names[7]: vert_symmetry_6MV, names[8]: vertical_field_size_6MV}                
                    df_6MV = pd.DataFrame(data_6MV)

                    st.dataframe(df_6MV)


                if type == '6SRS':
                    files_6SRS = []
                    date_analysis_6SRS = []
                    date_linac_6SRS = []
                    horizontal_field_size_6SRS = []
                    horizontal_flatness_6SRS = []
                    horizontal_symmetry_6SRS = []
                    vert_flatness_6SRS = []
                    vert_symmetry_6SRS = []
                    vertical_field_size_6SRS = []
                    for i in range(len(st.session_state['srs_sorted'])):
                        files_6SRS.append(st.session_state['srs_sorted'][i]['key'])
                        date_analysis_6SRS.append(st.session_state['srs_sorted'][i]['date_analysis'])
                        date_linac_6SRS.append(st.session_state['srs_sorted'][i]['date_linac'])
                        horizontal_field_size_6SRS.append(st.session_state['srs_sorted'][i]["horizontal_field_size"])
                        horizontal_flatness_6SRS.append(st.session_state['srs_sorted'][i]["horizontal_flatness"])
                        horizontal_symmetry_6SRS.append(st.session_state['srs_sorted'][i]["horizontal_symmetry"])
                        vert_flatness_6SRS.append(st.session_state['srs_sorted'][i]["vert_flatness"])
                        vert_symmetry_6SRS.append(st.session_state['srs_sorted'][i]["vert_symmetry"])
                        vertical_field_size_6SRS.append(st.session_state['srs_sorted'][i]["vertical_field_size"])
                    data_6SRS = {names[0]: files_6SRS, names[1]: date_analysis_6SRS, names[2]: date_linac_6SRS, names[3]: horizontal_field_size_6SRS, names[4]: horizontal_flatness_6SRS, 
                    names[5]: horizontal_symmetry_6SRS, names[6]: vert_flatness_6SRS, names[7]: vert_symmetry_6SRS, names[8]: vertical_field_size_6SRS}                
                    df_6SRS = pd.DataFrame(data_6SRS)

                    st.dataframe(df_6SRS)
                
                if type == '10MV':
                    files_10MV = []
                    date_analysis_10MV = []
                    date_linac_10MV = []
                    horizontal_field_size_10MV = []
                    horizontal_flatness_10MV = []
                    horizontal_symmetry_10MV = []
                    vert_flatness_10MV = []
                    vert_symmetry_10MV = []
                    vertical_field_size_10MV = []
                    for i in range(len(st.session_state['ten_mv_sorted'])):
                        files_10MV.append(st.session_state['ten_mv_sorted'][i]['key'])
                        date_analysis_10MV.append(st.session_state['ten_mv_sorted'][i]['date_analysis'])
                        date_linac_10MV.append(st.session_state['ten_mv_sorted'][i]['date_linac'])
                        horizontal_field_size_10MV.append(st.session_state['ten_mv_sorted'][i]["horizontal_field_size"])
                        horizontal_flatness_10MV.append(st.session_state['ten_mv_sorted'][i]["horizontal_flatness"])
                        horizontal_symmetry_10MV.append(st.session_state['ten_mv_sorted'][i]["horizontal_symmetry"])
                        vert_flatness_10MV.append(st.session_state['ten_mv_sorted'][i]["vert_flatness"])
                        vert_symmetry_10MV.append(st.session_state['ten_mv_sorted'][i]["vert_symmetry"])
                        vertical_field_size_10MV.append(st.session_state['ten_mv_sorted'][i]["vertical_field_size"])
                    data_10MV = {names[0]: files_10MV, names[1]: date_analysis_10MV, names[2]: date_linac_10MV, names[3]: horizontal_field_size_10MV, names[4]: horizontal_flatness_10MV, 
                    names[5]: horizontal_symmetry_10MV, names[6]: vert_flatness_10MV, names[7]: vert_symmetry_10MV, names[8]: vertical_field_size_10MV}                
                    df_10MV = pd.DataFrame(data_10MV)

                    st.dataframe(df_10MV)
                
                if type == '15MV':
                    files_15MV = []
                    date_analysis_15MV = []
                    date_linac_15MV = []
                    horizontal_field_size_15MV = []
                    horizontal_flatness_15MV = []
                    horizontal_symmetry_15MV = []
                    vert_flatness_15MV = []
                    vert_symmetry_15MV = []
                    vertical_field_size_15MV = []
                    for i in range(len(st.session_state['fifteen_mv_sorted'])):
                        files_15MV.append(st.session_state['fifteen_sorted'][i]['key'])
                        date_analysis_15MV.append(st.session_state['fifteen_mv_sorted'][i]['date_analysis'])
                        date_linac_15MV.append(st.session_state['fifteen_mv_sorted'][i]['date_linac'])
                        horizontal_field_size_15MV.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_field_size"])
                        horizontal_flatness_15MV.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_flatness"])
                        horizontal_symmetry_15MV.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_symmetry"])
                        vert_flatness_15MV.append(st.session_state['fifteen_mv_sorted'][i]["vert_flatness"])
                        vert_symmetry_15MV.append(st.session_state['fifteen_mv_sorted'][i]["vert_symmetry"])
                        vertical_field_size_15MV.append(st.session_state['fifteen_mv_sorted'][i]["vertical_field_size"])
                    data_15MV = {names[0]: files_15MV, names[1]: date_analysis_15MV, names[2]: date_linac_15MV, names[3]: horizontal_field_size_15MV, names[4]: horizontal_flatness_15MV, 
                    names[5]: horizontal_symmetry_15MV, names[6]: vert_flatness_15MV, names[7]: vert_symmetry_15MV, names[8]: vertical_field_size_15MV}                
                    df_15MV = pd.DataFrame(data_15MV)

                    st.dataframe(df_15MV)



                