from fpdf import FPDF
import streamlit as st
from pylinac.vmat import ImageType
import pandas as pd
#from pages.home.starshot import star
import pages.core.table_function as TABLE
from datetime import datetime
import base64
import io
import chime

# Add page number
class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_text_color(r=58, g=73, b=107)
        self.set_font('Courier', 'I', 10)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')
#-----------------------------------------------------------------------------------------------------------------------------------------
# Create link for report download
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
#-----------------------------------------------------------------------------------------------------------------------------------------
# Add new page with template
def new_page(pdf_file, t_name, institution, author, unit):
    # Background
    pdf_file.add_page()
    pdf_file.set_text_color(0, 0, 0)
    pdf_file.image('template.png', x = 0, y = 0, w = 210, h = 297)

    # Title
    pdf_file.set_text_color(r=58, g=73, b=107)
    pdf_file.set_font('Courier', 'B', 25)
    pdf_file.set_xy(100, 25)
    pdf_file.cell(10, 20, t_name, border=0, align='C')

    # Institute Name
    pdf_file.set_text_color(r=0, g=0, b=0)
    pdf_file.set_font('Courier', '', 12)
    pdf_file.set_xy(27,53)
    pdf_file.cell(10, 20, institution, border=0, align='C')

    # Author Name
    pdf_file.set_xy(85,53)
    pdf_file.cell(10, 20, author, border=0, align='C')

    # Date&Hour
    date_i = str(datetime.now())
    format_date = "%Y-%m-%d %H:%M:%S.%f"
    real_date = datetime.strptime(date_i, format_date)
    date_table = (str(real_date.day) + '/' + str(real_date.month) + '/' + str(real_date.year) + ' ' + str(real_date.hour) + ':' + 
                            str(real_date.minute)) 

    pdf_file.set_xy(135,53)
    pdf_file.cell(10, 20, date_table, border=0, align='C')

    # LINAC model
    pdf_file.set_xy(178,53)
    pdf_file.cell(10, 20, unit, border=0, align='C')
# ----------------------------------------------------------------------------------------------------------------------------------------
# @st.cache(allow_output_mutation=True)
def create_pdf_VMAT(test, keys, values, t_dmlc, drmlc_name, t_open, openbeam_name, t_name, institution, author, unit, r, file_name):

    # render table
    t = pd.DataFrame(values, columns=["Results"])
    t.insert(0, "Parameters", keys, True)
    tab = t.round(decimals=4)
    fig, ax = TABLE.render_mpl_table(tab)

    # PDF creation
    pdf = PDF(orientation='P', unit='mm', format='A4')
    new_page(pdf, t_name, institution, author, unit)

    pdf.set_font('Courier', '', 11)
    pdf.set_xy(50,76)
    pdf.cell(10, 20, t_dmlc, border=0, align='C')
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(50,82)
    pdf.cell(10, 20, drmlc_name, border=0, align='C')
    stream = io.BytesIO()
    test._save_analyzed_subimage(stream, ImageType.DMLC, transparent=True, bbox_inches='tight')
    pdf.image(stream, 20, 95, 70, 50)

    pdf.set_font('Courier', '', 11)
    pdf.set_xy(150,76)
    pdf.cell(10, 20, t_open, border=0, align='C')
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(150,82)
    pdf.cell(10, 20, openbeam_name, border=0, align='C')
    stream2 = io.BytesIO()
    test._save_analyzed_subimage(stream2, ImageType.OPEN, transparent=True, bbox_inches='tight')
    pdf.image(stream2, 120, 95, 70, 50)

    pdf.set_font('Courier', '', 11)
    pdf.set_xy(50,152)
    pdf.cell(10, 20, "Median Profiles", border=0, align='C')
    stream3 = io.BytesIO()
    test._save_analyzed_subimage(stream3, ImageType.PROFILE, transparent=True, dpi=200)
    pdf.image(stream3, 5, 160, 100, 60)

    pdf.set_font('Courier', '', 11)
    pdf.set_xy(150, 156)
    pdf.cell(10, 20, "Results Summary", border=0, align='C')
    stream4 = io.BytesIO()
    fig.savefig(stream4)
    pdf.image(stream4, 110, 170, 90, 35)

    if r == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(100, 235)
        pdf.cell(10, 20, "RESULT: " + str(r), border=0, align='C')
    
    elif r == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(100, 235)
        pdf.cell(10, 20, "RESULT: " + str(r), border=0, align='C')

    html = create_download_link(pdf.output(dest="S"), file_name)
    
    chime.theme('mario')
    chime.success()
    st.success("Your PDF report is ready!")
    st.markdown(html, unsafe_allow_html=True)
# -----------------------------------------------------------------------------------------------------------------------------------------
def create_pdf_WL(test, values, names, t_name, institution, author, unit, file_name, single_imgs):
    if single_imgs == True:
        # Template
        pdf_wl = PDF(orientation='P', unit='mm', format='A4')
        new_page(pdf_wl, t_name, institution, author, unit)

        # Summary Plot
        pdf_wl.set_font('Courier', '', 12)
        pdf_wl.set_xy(100,75)
        pdf_wl.cell(10, 15, "Summary Plot", border=0, align='C')
        stream0 = io.BytesIO()
        test.save_summary(stream0, transparent=True, bbox_inches='tight')
        pdf_wl.image(stream0, 10, 90, 190, 150)
        
        # SECOND PAGE - Table
        t_wl = pd.DataFrame(values, columns=["Results"])
        t_wl.insert(0, "Parameters", names, True)
        fig_wl, ax_wl = TABLE.render_mpl_table(t_wl)
        new_page(pdf_wl, t_name, institution, author, unit)
        stream1 = io.BytesIO()
        fig_wl.savefig(stream1, bbox_inches='tight', dpi=200, format="png", transparent=True)
        pdf_wl.image(stream1, 25, 75, 165, 185)
    
        # THIRD PAGE
        new_page(pdf_wl, t_name, institution, author, unit)
        stream2 = io.BytesIO()
        test.save_images(stream2, axis = 'Gantry', transparent=True, bbox_inches='tight')
        pdf_wl.image(stream2, 9, 75, 195, 100)
        
        # FOURTH PAGE
        new_page(pdf_wl, t_name, institution, author, unit)
        stream3 = io.BytesIO()
        test.save_images(stream3, axis = 'Collimator', transparent=True, bbox_inches='tight')
        pdf_wl.image(stream3, 9, 75, 195, 100)
        
        # FIFTH PAGE
        new_page(pdf_wl, t_name, institution, author, unit)
        stream4 = io.BytesIO()
        test.save_images(stream4, axis = 'Couch', transparent=True, bbox_inches='tight')
        pdf_wl.image(stream4, 9, 75, 195, 100)
        
    elif single_imgs == False:
        # Template
        pdf_wl = PDF(orientation='P', unit='mm', format='A4')
        new_page(pdf_wl, t_name, institution, author, unit)

        # Summary Plot
        pdf_wl.set_font('Courier', '', 12)
        pdf_wl.set_xy(100,75)
        pdf_wl.cell(10, 15, "Summary Plot", border=0, align='C')
        stream5 = io.BytesIO()
        test.save_summary(stream5, transparent=True, bbox_inches='tight')
        pdf_wl.image(stream5, 10, 90, 190, 150)
    
        
        t_wl = pd.DataFrame(values, columns=["Results"])
        t_wl.insert(0, "Parameters", names, True)
        fig_wl, ax_wl = TABLE.render_mpl_table(t_wl)
        
        # SECOND PAGE
        new_page(pdf_wl, t_name, institution, author, unit)
        stream6 = io.BytesIO()
        fig_wl.savefig(stream6, bbox_inches='tight', dpi=200, format="png", transparent=True)
        pdf_wl.image(stream6, 25, 75, 165, 185)

    # Link Download
    html = create_download_link(pdf_wl.output(dest="S"), file_name)

    chime.theme('mario')
    chime.success()
    st.success("Your PDF report is ready!")
    st.markdown(html, unsafe_allow_html=True)
# ---------------------------------------------------------------------------------------------------------
def create_PDF_PF1(test, names_pf, values_pf, t_name, institution, author, unit, name_fig, results):

    #add new page to pdf
    pdf_pf = PDF(orientation='P', unit='mm', format='A4')
    new_page(pdf_pf, t_name, institution, author, unit)

    # Analyzed image
    pdf_pf.set_font('Courier', '', 11)
    pdf_pf.set_xy(100,75)
    pdf_pf.cell(10, 20, name_fig, border=0, align='C')
    stream0 = io.BytesIO()
    test.save_analyzed_image(stream0, mlc_peaks=True, overlay=True, transparent=True, bbox_inches='tight', leaf_error_subplot=True)
    pdf_pf.image(stream0, 55, 90, 100, 55)

    t_pf = pd.DataFrame(values_pf, columns=["Results"])
    t_pf.insert(0, "Parameters", names_pf, True)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream1 = io.BytesIO()
    fig_pf.savefig(stream1, bbox_inches='tight', dpi=200, format="png", transparent=True)
    pdf_pf.image(stream1, 54, 150, 100, 110) 
    
    if results == "PASS":
        pdf_pf.set_text_color(r=58, g=73, b=107)
        pdf_pf.set_font('Courier', 'B', 16)
        pdf_pf.set_xy(97.5, 255)
        pdf_pf.cell(10, 20, "RESULT: " + str(results), border=0, align='C')
    
    elif results == "FAIL":
        pdf_pf.set_text_color(r=175, g=35, b=35)
        pdf_pf.set_font('Courier', 'B', 16)
        pdf_pf.set_xy(97.5, 255)
        pdf_pf.cell(10, 20, "RESULT: " + str(results), border=0, align='C')

    return pdf_pf

def create_PDF_PF4(t_name, institution, author, unit,
                   test1, names1, values1, name_fig1, t_results1,
                   test2, names2, values2, name_fig2, t_results2,
                   test3, names3, values3, name_fig3, t_results3,
                   test4, names4, values4, name_fig4, t_results4):
    pdf = PDF(orientation='P', unit='mm', format='A4')

    #FIRST PAGE
    new_page(pdf, t_name, institution, author, unit)
    # Analyzed image
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name_fig1, border=0, align='C')
    stream0 = io.BytesIO()
    test1.save_analyzed_image(stream0, mlc_peaks=True, overlay=True, transparent=True, bbox_inches='tight', leaf_error_subplot=True)
    pdf.image(stream0, 55, 90, 100, 55)

    # Table
    t_pf = pd.DataFrame(values1, columns=["Results"])
    t_pf.insert(0, "Parameters", names1, True)
    #tab = t.round(decimals=4)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream1 = io.BytesIO()
    fig_pf.savefig(stream1, bbox_inches='tight', dpi=200, format="png", transparent=True)
    pdf.image(stream1, 54, 150, 100, 110) 
    
    if t_results1 == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')
    
    if t_results1 == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')

    
    #SECOND PAGE
    new_page(pdf, t_name, institution, author, unit)
    # Analyzed image
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name_fig2, border=0, align='C')
    stream2 = io.BytesIO()
    test2.save_analyzed_image(stream2, mlc_peaks=True, overlay=True, transparent=True, bbox_inches='tight', leaf_error_subplot=True)
    pdf.image(stream2, 55, 90, 100, 55)
    
    # Table
    t_pf = pd.DataFrame(values2, columns=["Results"])
    t_pf.insert(0, "Parameters", names2, True)
    #tab = t.round(decimals=4)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream3 = io.BytesIO()
    fig_pf.savefig(stream3, bbox_inches='tight', dpi=200, format="png", transparent=True)
    pdf.image(stream3, 54, 150, 100, 110) 
    
    if t_results2 == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')
    
    if t_results2 == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')
    

    #THIRD PAGE
    new_page(pdf, t_name, institution, author, unit)
    # Analyzed image
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name_fig3, border=0, align='C')
    stream4 = io.BytesIO()
    test3.save_analyzed_image(stream4, mlc_peaks=True, overlay=True, transparent=True, bbox_inches='tight', leaf_error_subplot=True)
    pdf.image(stream4, 55, 90, 100, 55)
    
    # Table
    t_pf = pd.DataFrame(values3, columns=["Results"])
    t_pf.insert(0, "Parameters", names3, True)
    #tab = t.round(decimals=4)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream5 = io.BytesIO()
    fig_pf.savefig(stream5, bbox_inches='tight', dpi=200, format="png", transparent=True)
    pdf.image(stream5, 54, 150, 100, 110) 
    
    if t_results3 == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')
    
    if t_results3 == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')

    
    #FOURTH IMAGE
    new_page(pdf, t_name, institution, author, unit)
    # Analyzed image
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name_fig4, border=0, align='C')
    stream6 = io.BytesIO()
    test4.save_analyzed_image(stream6, mlc_peaks=True, overlay=True, transparent=True, bbox_inches='tight', leaf_error_subplot=True)
    pdf.image(stream6, 55, 90, 100, 55)
    
    # Table
    t_pf = pd.DataFrame(values4, columns=["Results"])
    t_pf.insert(0, "Parameters", names4, True)
    #tab = t.round(decimals=4)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream7 = io.BytesIO()
    fig_pf.savefig(stream7, bbox_inches='tight', dpi=200, format="png", transparent=True)
    pdf.image(stream7, 54, 150, 100, 110) 
    
    if t_results4 == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')
    
    if t_results4 == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.5, 255)
        pdf.cell(10, 20, "RESULT: " + str(t_results1), border=0, align='C')

    return pdf
# ------------------------------------------------------------------------------------------------------------------------------------------
def pdf_star_mf(t_name, institution, author, unit,
                test, names, values, names_files, t_results):
    
    # Creating First Page
    pdf = PDF(orientation='P', unit='mm', format='A4')

    new_page(pdf, t_name, institution, author, unit)

    names_figs = "Starshot analysis of superimposed image generated from: "

    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, names_figs, border=0, align='C')
    pdf.set_xy(100,83)
    pdf.cell(10, 20, str(names_files[0]) + ',' + str(names_files[1]) + ',', border=0, align='C')
    pdf.set_xy(100,88)
    pdf.cell(10, 20, str(names_files[2]) + ',' + str(names_files[3]) + '.', border=0, align='C')

    # FIRST IMAGE
    stream0 = io.BytesIO
    test.save_analyzed_subimage(stream0, 'whole', transparent=True, bbox_inches='tight', dpi=250)
    pdf.image(stream0, 30, 115, 70, 55)
    

    # SECOND IMAGE
    stream1 = io.BytesIO()
    test.save_analyzed_subimage(stream1, 'wobble', transparent=True, bbox_inches='tight', dpi=250)
    pdf.image(stream1, 115, 115, 65, 62)
    
    # TABLE
    t_pf = pd.DataFrame(values[1:], columns=["Results"])
    t_pf.insert(0, "Parameters", names[1:], True)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream2 = io.BytesIO()
    fig_pf.savefig(stream2, bbox_inches='tight', dpi=300, format="png", transparent=True)
    pdf.image(stream2, 39.5, 185, 130, 48) 
    
    if t_results == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.8, 230)
        pdf.cell(10, 20, "RESULT: " + str(t_results), border=0, align='C')
    
    if t_results == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.8, 230)
        pdf.cell(10, 20, "RESULT: " + str(t_results), border=0, align='C')

    return pdf

def pdf_star_sf(t_name, institution, author, unit,
                test, names, values, name_file, t_results):
    
    # Creating Template
    pdf = PDF(orientation='P', unit='mm', format='A4')

    new_page(pdf, t_name, institution, author, unit)

    name1 = 'Analysis result - ' + name_file
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name1, border=0, align='C')

    # FIRST IMAGE
    stream3 = io.BytesIO()
    test.save_analyzed_subimage(stream3, 'whole', transparent=True, bbox_inches='tight', dpi=250)
    pdf.image(stream3, 30, 95, 65, 65)    

    # SECOND IMAGE
    stream4 = io.BytesIO()
    test.save_analyzed_subimage(stream4, 'wobble', transparent=True, bbox_inches='tight', dpi=250)
    pdf.image(stream4, 115, 95, 65, 62)

    # TABLE
    t_pf = pd.DataFrame(values[1:], columns=["Results"])
    t_pf.insert(0, "Parameters", names[1:], True)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream5 = io.BytesIO()
    fig_pf.savefig(stream5, bbox_inches='tight', dpi=300, format="png", transparent=True)
    pdf.image(stream5, 39.5, 165, 130, 48) 
    
    if t_results == "PASS":
        pdf.set_text_color(r=58, g=73, b=107)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.8, 215)
        pdf.cell(10, 20, "RESULT: " + str(t_results), border=0, align='C')
    
    if t_results == "FAIL":
        pdf.set_text_color(r=175, g=35, b=35)
        pdf.set_font('Courier', 'B', 16)
        pdf.set_xy(97.8, 215)
        pdf.cell(10, 20, "RESULT: " + str(t_results), border=0, align='C')

    return pdf
# ------------------------------------------------------------------------------------------------------------------------------------------
def pdf_fa(t_name, institution, author, unit,
                test, names, values, name_file):
    
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.allow_images_transparency = True

    new_page(pdf, t_name, institution, author, unit)
    
    pdf.set_font('Courier', '', 11)
    pdf.set_xy(100,75)
    pdf.cell(10, 20, name_file, border=0, align='C')

    # FIRST IMAGE (image)
    stream0 = io.BytesIO()
    test._save_plot(test._plot_image, stream0)
    pdf.image(stream0, 55, 90, 100, 50)

    # SECOND IMAGE (horizontal)
    stream1 = io.BytesIO()
    test._save_plot(test._plot_horiz, stream1)
    pdf.image(stream1, 50, 145, 115, 55)

    # THIRD IMAGE (vertical)
    stream2 = io.BytesIO()
    test._save_plot(test._plot_vert, stream2)
    pdf.image(stream2, 50, 203, 115, 55)

    # SECOND PAGE - TABLE
    new_page(pdf, t_name, institution, author, unit)
    t_pf = pd.DataFrame(values[1:], columns=["Results"])
    t_pf.insert(0, "Parameters", names[1:], True)
    fig_pf, ax_pf = TABLE.render_mpl_table(t_pf)
    stream3 = io.BytesIO()
    fig_pf.savefig(stream3, bbox_inches='tight', dpi=300, format="png", transparent=True)
    pdf.image(stream3, 45, 70, 120, 205) 



    return pdf