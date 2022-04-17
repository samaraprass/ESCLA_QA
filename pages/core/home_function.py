import streamlit as st
import pages.core.text as txt
import base64

def Home():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # Image
    file_ = open("pages/core/logo.png", "rb")
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
            st.markdown('''
                <p>This app should not be used as the sole source of QA. As mentioned in <a style='text-align: center;' href="https://pylinac.readthedocs.io/en/latest/overview.html#what-is-pylinac-not" target=>Pylinac's documentation</a>, the library itself is not responsible for erroneous output. It is recommended to validate any kind of results with another known methodology</p>
                </div>
                ''', unsafe_allow_html=True)
            st.write("This web application was developed to allow professionals with little or no programming knowledge to use this library.")
    
    st.markdown('''
    <style>div.card{background-color: lightblue;  text-align:center; padding: 10px; border-radius: 3px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s;}</style>
    <div class="card">
    <div class="container">
    <p> 💻 For better usability and experience, please use this web app on a computer. <br>
      📤 If you have any questions or suggestions, please send a message to <a href="mailto:samaraprass@gmail.com">samaraprass@gmail.com</a> / <a href="mailto:contato@escla.com.br">contato@escla.com.br</a>.
    </p></div></div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    # References
    st.markdown(
        f'<div class="fade-in"><h3 font-weight:normal; style="font-size:30px;color:#000000; text-align:justify;">Acknowledgements</h3></div>',
        unsafe_allow_html=True)

    t6 = '''The development of this web app was only possible due to the existence of the following amazing works.: '''
    txt.t_fade(t6, 17, 'black')
    st.write('➜ James Kerns - [Pylinac: A TG-142 toolkit for doing routine linear accelerator quality assurance](https://github.com/jrkerns/pylinac)')
    st.write('➜ Mohammad Khorasani - [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)')
    #st.write('➜ Ken McGrady - [streamlit-autorefresh: An autorefresh component for Streamlit apps](https://github.com/kmcgrady/streamlit-autorefresh)')
    st.write('➜ Fanilo Andrianasolo - [Streamlit-ECharts](https://github.com/andfanilo/streamlit-echarts) and [Streamlit Lottie](https://github.com/andfanilo/streamlit-lottie)')
    st.write('➜ [st-btn-select: Streamlit Button Select Component](https://github.com/0phoff/st-btn-select)')
    st.write('➜ [hydralits_components: A package of custom components for Streamlit and Hydralit](https://github.com/TangleSpace/hydralit_components)')
    st.markdown('')
    st.markdown('')
    st.markdown('''
    <div class="footer">
    <p>Developed with Streamlit, Pylinac and ❤️ by <a style='display: block; text-align: center;' href="https://www.buymeacoffee.com/samaraprass" target="_blank">Samara Prass dos Santos</a></p>
    </div>
    ''', unsafe_allow_html=True)

