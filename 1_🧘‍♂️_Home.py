import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="MindfulNest",
    page_icon="🧘‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# Initializing Session state

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'

st.write(st.session_state)
# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authentication
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Main Page Layout
def main():
    st.logo("logo.png")
    st.title("Welcome to MindfulNest 🧘‍♂️🧘‍♀️")
    st.markdown("""
    ## Your Personalized Mental Health Companion 🌼
    MindfulNest is here to support your mental well-being. Whether you're feeling overwhelmed, anxious, or simply need a space to reflect, we're here to help. Explore various tools and resources designed to assist you on your mental health journey.
    """)

    # Buttons for Login and Register
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Login 🔐"):
            st.switch_page("pages/login.py")

    with col2:
        if st.button("Forgot Password 🤔"):
            forgot()

    with col3:
        if st.button("Register 📝"):
            register()

def login():
    st.subheader("Login 🔐")
    # st.success(f"Authenticated - Welcome")
    name, status, username = authenticator.login()
    if status == True:
        st.success(f"Authenticated - Welcome, {name}!")
        print(f"Authenticated - Welcome, {name}!")
        # Set session state variables
        st.session_state["authenticated"] = "True"
        st.session_state["username"] = username
    elif status == False:
        st.error("Authentication failed.")
        print("Authentication failed.")
    elif status == None:
        st.warning("Please enter your credentials.")

def register():
    st.subheader("Register 📝")
    # Registration logic heretry:
    try:
        email, username, name = authenticator.register_user(pre_authorization=False)
        if email:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

def forgot():
    st.subheader("Forgot Password 🤔")
    st.write("WIP...")


if __name__ == "__main__":
    main()
