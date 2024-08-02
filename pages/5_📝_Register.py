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
# Initializing Session state
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'
    
# st.write(st.session_state)

isAuth = st.session_state['authentication_status']

if (isAuth == False):
    def register_user(user_info):
        print(user_info)
        pass
    st.title("Register User 📝")
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False, callback=register_user)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
else:
    st.error("You're already logged in!")
