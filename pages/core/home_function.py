import streamlit as st
import pages.core.text as txt
import base64

def Home():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # Image
    file_ = open("logo.png", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    html = f'<a href="https://escla.com.br/" target="_blank"><div class="fade-in"><img src="data:image/gif;base64,{data_url}" alt="logo" style="height: 100%; width: 100%; object-fit: contain"></div></a>'
    t1, t2, t3 = st.columns([2.5, 2, 2.5])
    with t2:
        st.markdown(html, unsafe_allow_html=True)
        # https://stackoverflow.com/questions/3029422/how-do-i-auto-resize-an-image-to-fit-a-div-container (solução para ajuste automático e link)

    # Page title
    txt.title('TG-142 quality assurance (QA) tool', 40, '#253856')
    txt.title('With Pylinac 3.1.0', 25, "#8C438D")
    st.markdown("---")

    # Modules description
    st.markdown(
        f'<div class="fade-in"><h3 font-weight:normal; style="font-size:30px;color:#000000; text-align:justify;">Modules Overview</h3></div>',
        unsafe_allow_html=True)

    st.markdown(f'<div class="fade-in"><html font-weight:normal; style="color:#000000; text-align:justify;">Brief explanation about each module extracted directly from Pylinac docs. Head over to Pylinac 3.1.0 <a href="https://pylinac.readthedocs.io/en/release-v3.1/index.html"'
                'target="_blank">documentation</a> for more.</html></div>', unsafe_allow_html=True)
    st.write("")


    h1, h2, h3 = st.columns([2,0.25,2])
    
    with h1:
        txt.title2("1. VMAT - DRGS and DRMLC", 20, "#8C438D")
        t = '''The VMAT module consists of the class VMAT, which is capable of loading an EPID DICOM Open field image and 
            MLC field image and analyzing the images according to the Varian RapidArc QA tests and procedures, specifically 
            the Dose-Rate & Gantry-Speed (DRGS) and Dose-Rate & MLC speed (DRMLC) tests. '''
        txt.t_fade(t, 17, "black")
        st.write(" ")

        txt.title2("2. Starshot", 20, "#8C438D")
        t2 = '''The Starshot module analyses a starshot image made of radiation spokes, whether gantry, collimator, 
        MLC or couch. It is based on ideas from Depuydt et al and Gonzalez et al.'''
        txt.t_fade(t2, 17, 'black')
        st.write(" ") 

        txt.title2("3. Picket Fence", 20, "#8C438D")
        t3 = '''The picket fence module is meant for analyzing EPID images where a “picket fence” MLC pattern has been 
        made. Physicists regularly check MLC positioning through this test. It can load in an EPID dicom image 
        (or superimpose multiple images) and determine the MLC peaks, error of each MLC pair to the picket, and give a 
        few visual indicators for passing/warning/failing.'''
        txt.t_fade(t3, 17, 'black')
        st.write("")


    with h3:
        txt.title2("4. Winston-Lutz", 20, "#8C438D")
        t4 = '''The Winston-Lutz module loads and processes EPID images that have acquired Winston-Lutz type images.'''
        txt.t_fade(t4, 17, 'black')
        st.write("")

        txt.title2("5. Field Analysis", 20, "#8C438D")
        #txt.title2('Field Analysis','#field-analysis-epid-images')
        t5 = '''The field analysis module (pylinac.field_analysis) allows a physicist to analyze metrics from an EPID to measure penumbra, field width, etc. Additionally, protocols can be used which can calculate 
            flatness & symmetry. The module is very flexible, allowing users to choose different types of interpolation, 
            normalization, centering, etc. '''
        txt.t_fade(t5, 17, 'black')
        st.write(" ")
        with st.expander("⚠️ IMPORTANT", expanded=True):
            st.write("")

    st.markdown('''
    <div class="footer">
    <p>Developed with Streamlit, Pylinac and ❤ by <a style='display: block; text-align: center;' href="https://www.buymeacoffee.com/samaraprass" target="_blank">Samara Prass dos Santos</a></p>
    </div>
    ''', unsafe_allow_html=True)

