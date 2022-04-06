from datetime import date
from unittest import result
from deta import Deta
import streamlit as st

def database_insert_VMAT_DRGS(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key):
    # Creating database for user's tests results
    db.insert({
            'sid': sid,
            'cax': str(cax),
            'tolerance': tol,
            'abs_mean_dev': abs_mean_dev,
            'max_dev': max_dev, 
            'result': t_result,
            'date_analysis': analy_date, 
            'date_linac': date_linac
    }, key=key)
    
def database_update_VMAT_DRGS(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, key):
    # Creating database for user's tests results
    db.update({
            'sid': sid,
            'cax': str(cax),
            'tolerance': tol,
            'abs_mean_dev': abs_mean_dev,
            'max_dev': max_dev, 
            'result': t_result,
            'date_analysis': analy_date,
            'date_linac': date_linac 
        }, key=key)

def database_insert_VMAT_DRMLC(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, file_name):
    db.insert({
        'sid': sid,
        'cax': str(cax),
        'tolerance': tol,
        'abs_mean_dev': abs_mean_dev,
        'max_dev': max_dev,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=file_name)

def database_update_VMAT_DRMLC(db, sid, cax, tol, abs_mean_dev, max_dev, t_result, analy_date, date_linac, file_name):
    db.update({
        'sid': sid,
        'cax': str(cax),
        'tolerance': tol,
        'abs_mean_dev': abs_mean_dev,
        'max_dev': max_dev,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=file_name)

def database_insert_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key):
    db.insert({
        'tolerance': tol,
        'circle_diameter': circ_diam,
        'circle_radius': circ_radius,
        'circle_center': circ_center,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac 
    }, key=key)

def database_update_star(db, tol, circ_diam, circ_radius, circ_center, t_result, analy_date, date_linac, key):
    db.update({
        'tolerance': tol,
        'circle_diameter': circ_diam,
        'circle_radius': circ_radius,
        'circle_center': circ_center,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=key)

def database_insert_pf(db, mlc, angle, tol, percent_leaves_pass, number_pickets, abs_median_error, max_error,
                        mean_picket_spacing, t_result, analy_date, date_linac, key):
    db.insert({
        'mlc_type': mlc,
        'angle': angle,
        'tolerance': tol,
        'percent_leaves_pass': percent_leaves_pass,
        'number_pickets': number_pickets,
        'abs_median_error': abs_median_error,
        'max_error': max_error,
        'mean_picket_spacing': mean_picket_spacing,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=key)    

def database_update_pf(db, mlc, angle, tol, percent_leaves_pass, number_pickets, abs_median_error, max_error,
                        mean_picket_spacing, t_result, analy_date, date_linac, key):
    db.update({
        'mlc_type': mlc,
        'angle': angle,
        'tolerance': tol,
        'percent_leaves_pass': percent_leaves_pass,
        'number_pickets': number_pickets,
        'abs_median_error': abs_median_error,
        'max_error': max_error,
        'mean_picket_spacing': mean_picket_spacing,
        'result': t_result,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=key)    


def database_insert_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb, 
                        median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, 
                        max_epid_rms_dev, gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, 
                        max_couch_rms_dev, shift, analy_date, date_linac, key):
    db.insert({
        'number_gantry_images': n_gantry_imgs,
        'number_gan_coll_images': n_gan_col_imgs,
        'number_coll_images': n_col_imgs,
        'number_couch_images': n_couch_imgs,
        'number_total_images': n_tot_imgs,
        'max_2d_cax_to_bb': max_2d_cax_bb,
        'median_2d_cax_to_bb': median_2d_cax_bb,
        'max_2d_cax_to_epid': max_2d_cax_epid,
        'median_2d_cax_to_epid': median_2d_cax_epid,
        'gantry_3d_iso_diameter': gantry_3d_iso_diam,
        'max_gantry_rms_deviation': max_gantry_rms_dev,
        'max_epid_rms_deviation': max_epid_rms_dev,
        'gantry_coll_3d_iso_diam': gantry_coll_3d_iso_diam,
        'coll_2d_iso_diam': coll_2d_iso_diam,
        'max_coll_rms_deviation': max_coll_rms_dev,
        'couch_2d_iso': couch_2d_iso,
        'max_couch_rms_deviation': max_couch_rms_dev,
        'shift': shift,
        'date_analysis': analy_date,
        'date_linac': date_linac 
    }, key=key)

def database_update_wl(db, n_gantry_imgs, n_gan_col_imgs, n_col_imgs, n_couch_imgs, n_tot_imgs, max_2d_cax_bb, 
                        median_2d_cax_bb, max_2d_cax_epid, median_2d_cax_epid, gantry_3d_iso_diam, max_gantry_rms_dev, 
                        max_epid_rms_dev, gantry_coll_3d_iso_diam, coll_2d_iso_diam, max_coll_rms_dev, couch_2d_iso, 
                        max_couch_rms_dev, shift, analy_date, date_linac, key):
    db.update({
        'number_gantry_images': n_gantry_imgs,
        'number_gan_coll_images': n_gan_col_imgs,
        'number_coll_images': n_col_imgs,
        'number_couch_images': n_couch_imgs,
        'number_total_images': n_tot_imgs,
        'max_2d_cax_to_bb': max_2d_cax_bb,
        'median_2d_cax_to_bb': median_2d_cax_bb,
        'max_2d_cax_to_epid': max_2d_cax_epid,
        'median_2d_cax_to_epid': median_2d_cax_epid,
        'gantry_3d_iso_diameter': gantry_3d_iso_diam,
        'max_gantry_rms_deviation': max_gantry_rms_dev,
        'max_epid_rms_deviation': max_epid_rms_dev,
        'gantry_coll_3d_iso_diam': gantry_coll_3d_iso_diam,
        'coll_2d_iso_diam': coll_2d_iso_diam,
        'max_coll_rms_deviation': max_coll_rms_dev,
        'couch_2d_iso': couch_2d_iso,
        'max_couch_rms_deviation': max_couch_rms_dev,
        'shift': shift,
        'date_analysis': analy_date,
        'date_linac': date_linac 
    }, key=key)

def database_insert_fa(db, horiz_symmetry, vert_symmetry, horiz_flatness, vert_flatness, center_pixel, center_method, normal_method, interpol_method, edge_method,
                     top_penum, bottom_penum, left_penum, right_penum, vert_fs, horiz_fs, cax_top, cax_bottom, cax_left, cax_right, 
                     analy_date, date_linac, key):
    db.insert({
        'horizontal_symmetry': horiz_symmetry,
        'vert_symmetry': vert_symmetry,
        'horizontal_flatness': horiz_flatness, 
        'vert_flatness': vert_flatness,
        'center_pixel': center_pixel,
        'centering_method': center_method,
        'normal_method': normal_method,
        'interpol_method': interpol_method,
        'edge_method': edge_method,
        'top_penumbra':top_penum,
        'bottom_penumbra': bottom_penum,
        'left_penumbra':left_penum,
        'right_penumbra': right_penum,
        'vertical_field_size': vert_fs,
        'horizontal_field_size': horiz_fs,
        'cax_to_top_mm': cax_top,
        'cax_to_bottom_mm': cax_bottom,
        'cax_to_left_mm': cax_left,
        'cax_to_right_mm': cax_right,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=key)

def database_update_fa(db, horiz_symmetry, vert_symmetry, horiz_flatness, vert_flatness, center_pixel, center_method, normal_method, interpol_method, edge_method,
                     top_penum, bottom_penum, left_penum, right_penum, vert_fs, horiz_fs, cax_top, cax_bottom, cax_left, cax_right, 
                     analy_date, date_linac, key):
    db.update({
        'horizontal_symmetry': horiz_symmetry,
        'vert_symmetry': vert_symmetry,
        'horizontal_flatness': horiz_flatness, 
        'vert_flatness': vert_flatness,
        'center_pixel': center_pixel,
        'centering_method': center_method,
        'normal_method': normal_method,
        'interpol_method': interpol_method,
        'edge_method': edge_method,
        'top_penumbra':top_penum,
        'bottom_penumbra': bottom_penum,
        'left_penumbra':left_penum,
        'right_penumbra': right_penum,
        'vertical_field_size': vert_fs,
        'horizontal_field_size': horiz_fs,
        'cax_to_top_mm': cax_top,
        'cax_to_bottom_mm': cax_bottom,
        'cax_to_left_mm': cax_left,
        'cax_to_right_mm': cax_right,
        'date_analysis': analy_date,
        'date_linac': date_linac
    }, key=key)
