import streamlit as st
import pages.core.text as txt
import streamlit_authenticator as stauth
import base64
from deta import Deta

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if 'name_user' not in st.session_state:
    st.session_state['name_user'] = None

if 'username' not in st.session_state:
    st.session_state['username'] = None

def authentication():
    names = st.secrets['ns']
    usernames = st.secrets['us']
    passwords = st.secrets['ps']
    hashed_passwords = stauth.Hasher(passwords).generate()


    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

    st.session_state['name_user'], st.session_state['authentication_status'], st.session_state['username'] = authenticator.login('ESCLA members authentication','main')

    
    if st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')

    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
