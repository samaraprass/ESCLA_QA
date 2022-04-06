import streamlit as st


def text_fail(txt):
    return f'<p style="font-family:DejaVu Sans; color:#FF0000; text-align:center, font-size: 15px;">{txt}</p>'


def text_pass(txt):
    return f'<p style="font-family:DejaVu Sans; color:#4B9A70; text-align:center, font-size: 17px;">{txt}</p>'


def title(text, size, color):
    return st.markdown(
        f'<div class="fade-in"><h1 font-weight:bold; style="font-family:sans-serif ; font-size:{size}px;color:{color}; text-align:center;">{text}</h1></div>',
        unsafe_allow_html=True)
    
def title2(text, size, color):
    return st.markdown(
        f'<div class="fade-in"><h6 font-weight:normal; style="font-size:{size}px;color:{color}; text-align:justify;">{text}</h6></div>',
        unsafe_allow_html=True)

def title_results(text, size, color):
    return st.markdown(
        f'<div class="fade-in"><html font-weight:bold; style="font-size:{size}px;color:{color}; text-align:center;">{text}</html></div>',
        unsafe_allow_html=True)
    
def title_fade(text, size, color):
    return st.markdown(
        f'<div class="fade-in"><html font-weight:normal; style="font-size:{size}px;color:{color}; text-align:justify;">{text}</html></div>',
        unsafe_allow_html=True)

def t_fade(text, size, color):
    return st.markdown(
        f'<div class="fade-in"><p font-weight:normal; style="font-size:{size}px;color:{color}; text-align:justify;">{text}</p></div>',
        unsafe_allow_html=True)


def body(text, size, color):
    return st.markdown(
        f'<p font-weight:normal; style="font-size:{size}px;color:{color};text-align:justify;">{text}</p>',
        unsafe_allow_html=True)


def body_center(text, size, color):
    return st.markdown(f'<p font-weight:bold, style="font-size:{size}px;color:{color};text-align:center;">{text}</p>',
                       unsafe_allow_html=True)
