import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
hashed_passwords = stauth.Hasher(['rohaan', 'adil']).generate()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

st.logo("logo.png")

# st.write(st.session_state)

name, authentication_status, username = authenticator.login()

if authentication_status:
    st.title(f'Welcome *{username}!*')
    st.subheader('We hope you\'ll learn something new today from Dr. Falcon! 🧑‍⚕️')
    authenticator.logout('Logout', 'main')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

