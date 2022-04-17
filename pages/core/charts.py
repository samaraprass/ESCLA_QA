from streamlit_echarts import st_echarts
from deta import Deta
import streamlit as st
import numpy as np

if 'sorted_dates_drgs' not in st.session_state:
    st.session_state['sorted_dates_drgs'] = None

if 'sorted_dates_drmlc' not in st.session_state:
    st.session_state['sorted_dates_drmlc'] = None

if 'sorted_dates_star' not in st.session_state:
    st.session_state['sorted_dates_star'] = None

if 'sorted_dates_pf' not in st.session_state:
    st.session_state['sorted_dates_pf'] = None

if 'sorted_dates_wl' not in st.session_state:
    st.session_state['sorted_dates_wl'] = None

def line_chart_vmat_drgs():
    # Connect to database
    # Deta Database Connection
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'VMAT_DRGS'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")

    else:
        # list of dates from dicom images
        dates = []
        for i in range(fetch_res.count):
            item = fetch_res.items[i]
            dates.append(item['date_linac'])

        st.session_state['sorted_dates_drgs'] = sorted(dates)

        abs_mean_dev = []
        max_dev = []
        for i in st.session_state['sorted_dates_drgs']:
            fetch_res2 = db.fetch({"date_linac": i})
            abs_mean_dev.append(fetch_res2.items[0]["abs_mean_dev"])
            max_dev.append(fetch_res2.items[0]["max_dev"])

        
        options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Mean Deviation (%)', 'Maximum Deviation (%)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_drgs']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Mean Deviation (%)',
                    'type': 'line',
                    'data': abs_mean_dev
                },
                {
                    'name': 'Maximum Deviation (%)',
                    'type': 'line',
                    'data': max_dev
                }
            ]
        }

        st_echarts(options=options, height='400px')

def line_chart_vmat_drmlc():
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'VMAT_DRMLC'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")
    
    else:
        # list of dates from dicom images
        dates = []
        for i in range(fetch_res.count):
            item = fetch_res.items[i]
            dates.append(item['date_linac'])

        st.session_state['sorted_dates_drmlc'] = sorted(dates)

        abs_mean_dev = []
        max_dev = []
        for i in st.session_state['sorted_dates_drmlc']:
            fetch_res2 = db.fetch({"date_linac": i})
            abs_mean_dev.append(fetch_res2.items[0]["abs_mean_dev"])
            max_dev.append(fetch_res2.items[0]["max_dev"])

        options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Mean Deviation (%)', 'Maximum Deviation (%)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_drmlc']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Mean Deviation (%)',
                    'type': 'line',
                    'data': abs_mean_dev
                },
                {
                    'name': 'Maximum Deviation (%)',
                    'type': 'line',
                    'data': max_dev
                }
            ]
        }

        st_echarts(options=options, height='400px')

def line_chart_star():
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Starshot'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")

    else:
        # list of dates from dicom images
        dates = []
        for i in range(fetch_res.count):
            item = fetch_res.items[i]
            #st.write(item['date_linac'])
            if item['date_linac'] != 'None':
                dates.append(item['date_linac'])

        st.session_state['sorted_dates_star'] = sorted(dates)

        circle_diameter_mm = []
        circle_radius_mm = []
        for i in st.session_state['sorted_dates_star']:
            fetch_res2 = db.fetch({"date_linac": i})
            circle_diameter_mm.append(fetch_res2.items[0]["circle_diameter"])
            circle_radius_mm.append(fetch_res2.items[0]["circle_radius"])

        options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Mean Deviation (%)', 'Maximum Deviation (%)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_star']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Mean Deviation (%)',
                    'type': 'line',
                    'data': circle_diameter_mm
                },
                {
                    'name': 'Maximum Deviation (%)',
                    'type': 'line',
                    'data': circle_radius_mm
                }
            ]
        }

        st_echarts(options=options, height='400px')

def line_chart_picket_fence(angle):
    # Connecting database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Picket_Fence'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")

    else:
        # list of dates from dicom images
        angles = [0, 90, 180, 270]

        # for i in angles:
        #     fetch_res2 = db.fetch({"angle": i})
        #     st.write(fetch_res2.items)
        
        dates = []
        for i in range(fetch_res.count):
            item = fetch_res.items[i]
            dates.append(item['date_linac'])
        
        st.session_state['sorted_dates_pf'] = list(np.unique(sorted(dates)))

        same_angle0 = []
        same_angle90 = []
        same_angle180 = []
        same_angle270 = []
        for i in st.session_state['sorted_dates_pf']:
            fetch_res2 = db.fetch({"date_linac": i})
            for j in range(len(fetch_res2.items)):
                if int(round(fetch_res2.items[j]['angle'])) == 0:
                    same_angle0.append(fetch_res2.items[j])

                if int(round(fetch_res2.items[j]['angle'])) == 90:
                    same_angle90.append(fetch_res2.items[j])

                if int(round(fetch_res2.items[j]['angle'])) == 180:
                    same_angle180.append(fetch_res2.items[j])

                if int(round(fetch_res2.items[j]["angle"])) == 270:
                    same_angle270.append(fetch_res2.items[j])
            

        # Variables for 0º
        abs_median_error0 = []
        max_error0 = []
        mean_picket_spacing0 = []
        for i in range(len(same_angle0)):
            abs_median_error0.append(same_angle0[i]["abs_median_error"])
            max_error0.append(same_angle0[i]["max_error"])
            mean_picket_spacing0.append(same_angle0[i]["mean_picket_spacing"])
        
        # Variables for 90º
        abs_median_error90 = []
        max_error90 = []
        mean_picket_spacing90 = []
        for i in range(len(same_angle90)):
            abs_median_error90.append(same_angle90[i]["abs_median_error"])
            max_error90.append(same_angle90[i]["max_error"])
            mean_picket_spacing90.append(same_angle90[i]["mean_picket_spacing"])

        # Variables for 180º
        abs_median_error180 = []
        max_error180 = []
        mean_picket_spacing180 = []
        for i in range(len(same_angle180)):
            abs_median_error180.append(same_angle180[i]["abs_median_error"])
            max_error180.append(same_angle180[i]["max_error"])
            mean_picket_spacing180.append(same_angle180[i]["mean_picket_spacing"])

        # Variables for 270º
        abs_median_error270 = []
        max_error270 = []
        mean_picket_spacing270 = []
        for i in range(len(same_angle270)):
            abs_median_error270.append(same_angle270[i]["abs_median_error"])
            max_error270.append(same_angle270[i]["max_error"])
            mean_picket_spacing270.append(same_angle270[i]["mean_picket_spacing"])
        

        if angle == 0:
            options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Median Error (mm)', 'Maximum Error (mm)', 'Mean Picket Spacing (mm)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_pf']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Median Error (mm)',
                    'type': 'line',
                    'data': abs_median_error0
                },
                {
                    'name': 'Maximum Error (mm)',
                    'type': 'line',
                    'data': max_error0
                },
                {
                    'name': 'Mean Picket Spacing (mm)',
                    'type': 'line',
                    'data': mean_picket_spacing0
                        }
                    ]
                }

            st_echarts(options=options, height='400px')

        elif angle == 90:
            options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Median Error (mm)', 'Maximum Error (mm)', 'Mean Picket Spacing (mm)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_pf']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Median Error (mm)',
                    'type': 'line',
                    'data': abs_median_error90
                },
                {
                    'name': 'Maximum Error (mm)',
                    'type': 'line',
                    'data': max_error90
                },
                {
                    'name': 'Mean Picket Spacing (mm)',
                    'type': 'line',
                    'data': mean_picket_spacing90
                        }
                    ]
                }

            st_echarts(options=options, height='400px')
            
        elif angle == 180:
            options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Median Error (mm)', 'Maximum Error (mm)', 'Mean Picket Spacing (mm)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_pf']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Median Error (mm)',
                    'type': 'line',
                    'data': abs_median_error180
                },
                {
                    'name': 'Maximum Error (mm)',
                    'type': 'line',
                    'data': max_error180
                },
                {
                    'name': 'Mean Picket Spacing (mm)',
                    'type': 'line',
                    'data': mean_picket_spacing180
                        }
                    ]
                }

            st_echarts(options=options, height='400px')
        
        elif angle == 270:
            options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Absolute Median Error (mm)', 'Maximum Error (mm)', 'Mean Picket Spacing (mm)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_pf']
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Absolute Median Error (mm)',
                    'type': 'line',
                    'data': abs_median_error270
                },
                {
                    'name': 'Maximum Error (mm)',
                    'type': 'line',
                    'data': max_error270
                },
                {
                    'name': 'Mean Picket Spacing (mm)',
                    'type': 'line',
                    'data': mean_picket_spacing270
                        }
                    ]
                }

            st_echarts(options=options, height='400px')

def line_chart_wl():
    #Database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Winston_Lutz'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")

    #st.write(fetch_res.items)
    else:
        dates = []
        for i in range(fetch_res.count):
            item = fetch_res.items[i]
            #st.write(item['date_linac'])
            dates.append(item['date_linac'])

        st.session_state['sorted_dates_wl'] = sorted(dates)
        
        coll_2d_iso_diam = []
        couch_2d_iso = []
        gantry_3d_iso_diameter = []
        #gantry_coll_3d_iso_diam = []
        max_2d_cax_to_bb = []
        #max_2d_cax_to_epid = []
        max_coll_rms_deviation = []
        max_couch_rms_deviation = []
        #max_epid_rms_deviation = []
        max_gantry_rms_deviation = []
        # median_2d_cax_to_bb = []
        # median_2d_cax_to_epid = []
        for i in st.session_state['sorted_dates_wl']:
            fetch_res2 = db.fetch({"date_linac": i})
            coll_2d_iso_diam.append(fetch_res2.items[0]["coll_2d_iso_diam"])
            couch_2d_iso.append(fetch_res2.items[0]["couch_2d_iso"])
            gantry_3d_iso_diameter.append(fetch_res2.items[0]["gantry_3d_iso_diameter"])
            #gantry_coll_3d_iso_diam.append(fetch_res2.items[0]["gantry_coll_3d_iso_diam"])
            max_2d_cax_to_bb.append(fetch_res2.items[0]["max_2d_cax_to_bb"])
            #max_2d_cax_to_epid.append(fetch_res2.items[0]["max_2d_cax_to_epid"])
            max_coll_rms_deviation.append(fetch_res2.items[0]["max_coll_rms_deviation"])
            max_couch_rms_deviation.append(fetch_res2.items[0]["max_couch_rms_deviation"])
            #max_epid_rms_deviation.append(fetch_res2.items[0]["max_epid_rms_deviation"])
            max_gantry_rms_deviation.append(fetch_res2.items[0]["max_gantry_rms_deviation"])
            # median_2d_cax_to_bb.append(fetch_res2.items[0]["median_2d_cax_to_bb"])
            # median_2d_cax_to_epid.append(fetch_res2.items[0]["median_2d_cax_to_epid"])
        
        options = {
            'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Collimator 2D isocenter diameter (mm)', 'Couch 2D isocenter diameter (mm)', 'Gantry 3D isocenter diameter (mm)',
                                'Gantry+Collimator 3D isocenter diameter (mm)', 'Maximum 2D CAX to BB (mm)', 'Maximum 2D CAX to EPID (mm)', 
                                'Maximum Collimator RMS deviation (mm)', 'Maximum Couch RMS deviation (mm)', 'Maximum EPID RMS deviation (mm)',
                                'Maximum Gantry RMS deviation (mm)', 'Median 2D CAX to BB (mm)', 'Median 2D CAX to EPID (mm)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": st.session_state['sorted_dates_wl']
            },
            'yAxis': {'type': 'value'},
            'series': [
                    {
                        'name': 'Collimator 2D isocenter diameter (mm)',
                        'type': 'line',
                        'data': coll_2d_iso_diam
                    },
                    {
                        'name': 'Couch 2D isocenter diameter (mm)',
                        'type': 'line',
                        'data': couch_2d_iso
                    },
                    {
                        'name': 'Gantry 3D isocenter diameter (mm)',
                        'type': 'line',
                        'data': gantry_3d_iso_diameter
                    },
                    # {
                    #     'name': 'Gantry+Collimator 3D isocenter diameter (mm)',
                    #     'type': 'line',
                    #     'data': gantry_coll_3d_iso_diam
                    # },
                    {
                        'name': 'Maximum 2D CAX to BB (mm)',
                        'type': 'line',
                        'data': max_2d_cax_to_bb
                    },
                    # {
                    #     'name': 'Maximum 2D CAX to EPID (mm)',
                    #     'type': 'line',
                    #     'data': max_2d_cax_to_epid
                    # },
                    {
                        'name': 'Maximum Collimator RMS deviation (mm)',
                        'type': 'line',
                        'data': max_coll_rms_deviation    
                    },
                    {
                        'name': 'Maximum Couch RMS deviation (mm)',
                        'type': 'line',
                        'data': max_couch_rms_deviation
                    },
                    # {
                    #     'name': 'Maximum EPID RMS deviation (mm)',
                    #     'type': 'line',
                    #     'data': max_epid_rms_deviation
                    # },
                    {
                        'name': 'Maximum Gantry RMS deviation (mm)',
                        'type': 'line',
                        'data': max_gantry_rms_deviation
                    }
                    # {
                    #     'name': 'Median 2D CAX to BB (mm)',
                    #     'type': 'line',
                    #     'data': median_2d_cax_to_bb
                    # },
                    # {
                    #     'name': 'Median 2D CAX to EPID (mm)',
                    #     'type': 'line',
                    #     'data': median_2d_cax_to_epid
                    # }
                    
                    ]
        }
            

        st_echarts(options=options, height='600px')

def line_chart_fa(type):
    # Database
    data_connection = Deta(st.secrets['database']['data_key'])
    user_test = st.session_state['username'] + 'Field_Analysis'
    db = data_connection.Base(user_test)
    fetch_res = db.fetch()

    if fetch_res.count == 0:
        st.info(" 📈 Run some tests and see the results timeline here")
    
    else:
        names = [] # armazena os nomes dos arquivos
        dates = [] # aramazena as datas 
        for i in range(fetch_res.count):
            names.append(fetch_res.items[i]['key'])
            dates.append(fetch_res.items[i]['date_linac'])

        sorted_dates = sorted(dates) #ordena as datas

        srs = [] #armazena os arquivos de 6SRS
        six_mv = [] #armazena os arquivos de 6MV
        ten_mv = [] #armazena todos os arquivos de 10MV
        fifteen_mv = [] #armazena todos os arquivos de 15MV
        for i in names:
            fetch_res3 = db.fetch({"key": i})
            if 'SRS' in fetch_res3.items[0]['key']:
                srs.append(fetch_res3.items[0])

            if '6MV' in fetch_res3.items[0]['key']:
                six_mv.append(fetch_res3.items[0])
            
            if '10MV' in fetch_res3.items[0]['key']:
                ten_mv.append(fetch_res3.items[0])
            
            if '15MV' in fetch_res3.items[0]['key']:
                fifteen_mv.append(fetch_res3.items[0])
        
        st.session_state['six_mv_sorted'] = [] #armazena os arquivos de 6MV ordenados 
        st.session_state['srs_sorted'] = [] #armazena os arquivos de 6SRS ordenados 
        st.session_state['ten_mv_sorted'] = [] #armazena os arquivos de 10MV ordenados 
        st.session_state['fifteen_mv_sorted'] = [] #armazena os arquivos de 15MV ordenados 
        for j in np.unique(sorted_dates):
            for i in range(len(six_mv)):
                if six_mv[i]['date_linac'] == j:
                    st.session_state['six_mv_sorted'].append(six_mv[i])

        for j in np.unique(sorted_dates):
            for i in range(len(srs)):
                if srs[i]['date_linac'] == j:
                    st.session_state['srs_sorted'].append(srs[i])
        
        for j in np.unique(sorted_dates):
            for i in range(len(ten_mv)):
                if ten_mv[i]['date_linac'] == j:
                    st.session_state['ten_mv_sorted'].append(ten_mv[i])

        for j in np.unique(sorted_dates):
            for i in range(len(fifteen_mv)):
                if fifteen_mv[i]['date_linac'] == j:
                    st.session_state['fifteen_mv_sorted'].append(fifteen_mv[i])

        
        dates_six_mv = []
        for i in range(len(st.session_state['six_mv_sorted'])):
            dates_six_mv.append(st.session_state['six_mv_sorted'][i]["date_linac"])
        
        dates_ten_mv = []
        for i in range(len(st.session_state['ten_mv_sorted'])):
            dates_ten_mv.append(st.session_state['ten_mv_sorted'][0]["date_linac"])
        
        dates_srs =[]
        for i in range(len(st.session_state['srs_sorted'])):
            dates_srs.append(srs[i]["date_linac"])
        
        dates_fifteen_mv = []
        for i in range(len(st.session_state['fifteen_mv_sorted'])):
            dates_fifteen_mv.append(st.session_state['fifteen_mv_sorted'][i]['date_linac'])
        
        sorted_dates_six_mv = sorted(dates_six_mv)
        sorted_dates_ten_mv = sorted(dates_ten_mv)
        sorted_dates_srs = sorted(dates_srs)
        sorted_dates_fifteen_mv = sorted(dates_fifteen_mv)


        if type == '6SRS':
            bottom_penumbra_srs = []
            cax_to_bottom_mm_srs = []
            cax_to_left_mm_srs = []
            cax_to_right_srs = []
            cax_to_top_mm_srs = []
            center_pixel_srs = []
            horizontal_field_size_srs = []
            horizontal_flatness_srs = []
            horizontal_symmetry_srs = []
            left_penumbra_srs = []
            right_penumbra_srs = []
            top_penumbra_srs = []
            vert_flatness_srs = []
            vert_symmetry_srs = []
            vertical_field_size_srs = []
            for i in range(len(st.session_state['srs_sorted'])):
                bottom_penumbra_srs.append(st.session_state['srs_sorted'][i]["bottom_penumbra"])
                cax_to_bottom_mm_srs.append(st.session_state['srs_sorted'][i]["cax_to_bottom_mm"])
                cax_to_left_mm_srs.append(st.session_state['srs_sorted'][i]["cax_to_left_mm"])
                cax_to_right_srs.append(st.session_state['srs_sorted'][i]["cax_to_right_mm"])
                cax_to_top_mm_srs.append(st.session_state['srs_sorted'][i]["cax_to_top_mm"])
                center_pixel_srs.append(st.session_state['srs_sorted'][i]['center_pixel'])
                horizontal_field_size_srs.append(st.session_state['srs_sorted'][i]["horizontal_field_size"])
                horizontal_flatness_srs.append(st.session_state['srs_sorted'][i]["horizontal_flatness"])
                horizontal_symmetry_srs.append(st.session_state['srs_sorted'][i]["horizontal_symmetry"])
                left_penumbra_srs.append(st.session_state['srs_sorted'][i]["left_penumbra"])
                right_penumbra_srs.append(st.session_state['srs_sorted'][i]["right_penumbra"])
                top_penumbra_srs.append(st.session_state['srs_sorted'][i]["top_penumbra"])
                vert_flatness_srs.append(st.session_state['srs_sorted'][i]["vert_flatness"])
                vert_symmetry_srs.append(st.session_state['srs_sorted'][i]["vert_symmetry"])
                vertical_field_size_srs.append(st.session_state['srs_sorted'][i]["vertical_field_size"])
            options = {
            #'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Horizontal Field Size (mm)', 'Horizontal Flatness (%)', 'Horizontal Symmetry (%)', 
                                'Vertical Flatness (%)', 'Vertical Symmetry (%)', 'Vertical Field Size (mm)', 'Center Pixel (pylinac array)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": list(np.unique(sorted_dates_srs))
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Horizontal Field Size (mm)',
                    'type': 'line',
                    'data': horizontal_field_size_srs
                },
                {
                    'name': 'Horizontal Flatness (%)',
                    'type': 'line',
                    'data': horizontal_flatness_srs
                },
                {
                    'name': 'Horizontal Symmetry (%)',
                    'type': 'line',
                    'data': horizontal_symmetry_srs
                },
                {
                    'name': 'Vertical Flatness (%)',
                    'type': 'line',
                    'data': vert_flatness_srs
                },
                {
                    'name': 'Vertical Symmetry (%)',
                    'type': 'line',
                    'data': vert_symmetry_srs
                },
                {
                    'name': 'Vertical Field Size (mm)',
                    'type': 'line',
                    'data': vertical_field_size_srs
                },
                {
                    'name': 'Center Pixel (pylinac array)',
                    'type': 'line',
                    'data': center_pixel_srs
                }
                    ]
                }

            st_echarts(options=options, height='400px')

        if type == '6MV':
            # bottom_penumbra = []
            # cax_to_bottom_mm = []
            # cax_to_left_mm = []
            # cax_to_right = []
            # cax_to_top_mm = []
            center_pixel = []
            horizontal_field_size = []
            horizontal_flatness = []
            horizontal_symmetry = []
            # left_penumbra = []
            # right_penumbra = []
            # top_penumbra = []
            vert_flatness = []
            vert_symmetry = []
            vertical_field_size = []
            for i in range(len(st.session_state['six_mv_sorted'])):
                # bottom_penumbra.append(six_mv_sorted[i]["bottom_penumbra"])
                # cax_to_bottom_mm.append(six_mv_sorted[i]["cax_to_bottom_mm"])
                # cax_to_left_mm.append(six_mv_sorted[i]["cax_to_left_mm"])
                # cax_to_right.append(six_mv_sorted[i]["cax_to_right_mm"])
                # cax_to_top_mm.append(six_mv_sorted[i]["cax_to_top_mm"])
                center_pixel.append(st.session_state['six_mv_sorted'][i]['center_pixel'])
                horizontal_field_size.append(st.session_state['six_mv_sorted'][i]["horizontal_field_size"])
                horizontal_flatness.append(st.session_state['six_mv_sorted'][i]["horizontal_flatness"])
                horizontal_symmetry.append(st.session_state['six_mv_sorted'][i]["horizontal_symmetry"])
                # left_penumbra.append(six_mv_sorted[i]["left_penumbra"])
                # right_penumbra.append(six_mv_sorted[i]["right_penumbra"])
                # top_penumbra.append(six_mv_sorted[i]["top_penumbra"])
                vert_flatness.append(st.session_state['six_mv_sorted'][i]["vert_flatness"])
                vert_symmetry.append(st.session_state['six_mv_sorted'][i]["vert_symmetry"])
                vertical_field_size.append(st.session_state['six_mv_sorted'][i]["vertical_field_size"])
            options = {
            #'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Horizontal Field Size (mm)', 'Horizontal Flatness (%)', 'Horizontal Symmetry (%)', 'Vertical Flatness (%)', 'Vertical Symmetry (%)', 'Vertical Field Size (mm)', 'Center Pixel (pylinac array)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": list(np.unique(sorted_dates_six_mv))
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Horizontal Field Size (mm)',
                    'type': 'line',
                    'data': horizontal_field_size
                },
                {
                    'name': 'Horizontal Flatness (%)',
                    'type': 'line',
                    'data': horizontal_flatness
                },
                {
                    'name': 'Horizontal Symmetry (%)',
                    'type': 'line',
                    'data': horizontal_symmetry
                },
                {
                    'name': 'Vertical Flatness (%)',
                    'type': 'line',
                    'data': vert_flatness
                },
                {
                    'name': 'Vertical Symmetry (%)',
                    'type': 'line',
                    'data': vert_symmetry
                },
                {
                    'name': 'Vertical Field Size (mm)',
                    'type': 'line',
                    'data': vertical_field_size
                },
                {
                    'name': 'Center Pixel (pylinac array)',
                    'type': 'line',
                    'data': center_pixel
                }
                    ]
                }

            st_echarts(options=options, height='400px')

        if type == '10MV':
            bottom_penumbra_ten = []
            cax_to_bottom_mm_ten = []
            cax_to_left_mm_ten = []
            cax_to_right_ten = []
            cax_to_top_mm_ten = []
            center_pixel_ten = []
            horizontal_field_size_ten = []
            horizontal_flatness_ten = []
            horizontal_symmetry_ten = []
            left_penumbra_ten = []
            right_penumbra_ten = []
            top_penumbra_ten = []
            vert_flatness_ten = []
            vert_symmetry_ten = []
            vertical_field_size_ten = []
            for i in range(len(st.session_state['ten_mv_sorted'])):
                bottom_penumbra_ten.append(st.session_state['ten_mv_sorted'][i]["bottom_penumbra"])
                cax_to_bottom_mm_ten.append(st.session_state['ten_mv_sorted'][i]["cax_to_bottom_mm"])
                cax_to_left_mm_ten.append(st.session_state['ten_mv_sorted'][i]["cax_to_left_mm"])
                cax_to_right_ten.append(st.session_state['ten_mv_sorted'][i]["cax_to_right_mm"])
                cax_to_top_mm_ten.append(st.session_state['ten_mv_sorted'][i]["cax_to_top_mm"])
                center_pixel_ten.append(st.session_state['ten_mv_sorted'][i]['center_pixel'])
                horizontal_field_size_ten.append(st.session_state['ten_mv_sorted'][i]["horizontal_field_size"])
                horizontal_flatness_ten.append(st.session_state['ten_mv_sorted'][i]["horizontal_flatness"])
                horizontal_symmetry_ten.append(st.session_state['ten_mv_sorted'][i]["horizontal_symmetry"])
                left_penumbra_ten.append(st.session_state['ten_mv_sorted'][i]["left_penumbra"])
                right_penumbra_ten.append(st.session_state['ten_mv_sorted'][i]["right_penumbra"])
                top_penumbra_ten.append(st.session_state['ten_mv_sorted'][i]["top_penumbra"])
                vert_flatness_ten.append(st.session_state['ten_mv_sorted'][i]["vert_flatness"])
                vert_symmetry_ten.append(st.session_state['ten_mv_sorted'][i]["vert_symmetry"])
                vertical_field_size_ten.append(st.session_state['ten_mv_sorted'][i]["vertical_field_size"])
            options = {
            #'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Horizontal Field Size (mm)', 'Horizontal Flatness (%)', 'Horizontal Symmetry (%)', 'Vertical Flatness (%)', 'Vertical Symmetry (%)', 'Vertical Field Size (mm)', 'Center Pixel (pylinac array)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": list(np.unique(sorted_dates_ten_mv))
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Horizontal Field Size (mm)',
                    'type': 'line',
                    'data': horizontal_field_size_ten
                },
                {
                    'name': 'Horizontal Flatness (%)',
                    'type': 'line',
                    'data': horizontal_flatness_ten
                },
                {
                    'name': 'Horizontal Symmetry (%)',
                    'type': 'line',
                    'data': horizontal_symmetry_ten
                },
                {
                    'name': 'Vertical Flatness (%)',
                    'type': 'line',
                    'data': vert_flatness_ten
                },
                {
                    'name': 'Vertical Symmetry (%)',
                    'type': 'line',
                    'data': vert_symmetry_ten
                },
                {
                    'name': 'Vertical Field Size (mm)',
                    'type': 'line',
                    'data': vertical_field_size_ten
                },
                {
                    'name': 'Center Pixel (pylinac array)',
                    'type': 'line',
                    'data': center_pixel_ten
                }
                    ]
                }

            st_echarts(options=options, height='400px')

        if type == '15MV':
            bottom_penumbra_fifteen = []
            cax_to_bottom_mm_fifteen = []
            cax_to_left_mm_fifteen = []
            cax_to_right_fifteen = []
            cax_to_top_mm_fifteen = []
            center_pixel_fifteen = []
            horizontal_field_size_fifteen = []
            horizontal_flatness_fifteen = []
            horizontal_symmetry_fifteen = []
            left_penumbra_fifteen = []
            right_penumbra_fifteen = []
            top_penumbra_fifteen = []
            vert_flatness_fifteen = []
            vert_symmetry_fifteen = []
            vertical_field_size_fifteen = []
            for i in range(len(st.session_state['fifteen_mv_sorted'])):
                bottom_penumbra_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["bottom_penumbra"])
                cax_to_bottom_mm_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["cax_to_bottom_mm"])
                cax_to_left_mm_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["cax_to_left_mm"])
                cax_to_right_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["cax_to_right_mm"])
                cax_to_top_mm_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["cax_to_top_mm"])
                center_pixel_fifteen.append(st.session_state['fifteen_mv_sorted'][i]['center_pixel'])
                horizontal_field_size_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_field_size"])
                horizontal_flatness_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_flatness"])
                horizontal_symmetry_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["horizontal_symmetry"])
                left_penumbra_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["left_penumbra"])
                right_penumbra_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["right_penumbra"])
                top_penumbra_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["top_penumbra"])
                vert_flatness_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["vert_flatness"])
                vert_symmetry_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["vert_symmetry"])
                vertical_field_size_fifteen.append(st.session_state['fifteen_mv_sorted'][i]["vertical_field_size"])
            options = {
            #'title': {'text': 'TIMELINE'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Horizontal Field Size (mm)', 'Horizontal Flatness (%)', 'Horizontal Symmetry (%)', 'Vertical Flatness (%)', 'Vertical Symmetry (%)', 'Vertical Field Size (mm)', 'Center Pixel (pylinac array)']},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            'xAxis': {
                "type": "category",
                'boundaryGap': True, 
                "data": list(np.unique(sorted_dates_fifteen_mv))
            },
            'yAxis': {'type': 'value'},
            'series': [
                {
                    'name': 'Horizontal Field Size (mm)',
                    'type': 'line',
                    'data': horizontal_field_size_fifteen
                },
                {
                    'name': 'Horizontal Flatness (%)',
                    'type': 'line',
                    'data': horizontal_flatness_fifteen
                },
                {
                    'name': 'Horizontal Symmetry (%)',
                    'type': 'line',
                    'data': horizontal_symmetry_fifteen
                },
                {
                    'name': 'Vertical Flatness (%)',
                    'type': 'line',
                    'data': vert_flatness_fifteen
                },
                {
                    'name': 'Vertical Symmetry (%)',
                    'type': 'line',
                    'data': vert_symmetry_fifteen
                },
                {
                    'name': 'Vertical Field Size (mm)',
                    'type': 'line',
                    'data': vertical_field_size_fifteen
                },
                {
                    'name': 'Center Pixel (pylinac array)',
                    'type': 'line',
                    'data': center_pixel_fifteen
                }
                    ]
                }

            st_echarts(options=options, height='400px')