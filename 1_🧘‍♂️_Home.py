import json

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from utils import get_path

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
st.logo("logo.png")

# Initializing Session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'

# st.write(st.session_state)

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
    st.image("logo.png")
    st.title("Welcome to MindfulNest 🧘‍♂️🧘‍♀️")
    st.markdown("""
    ## Your Personalized Mental Health Companion 🌼
    MindfulNest is here to support your mental well-being. Whether you're feeling overwhelmed, anxious, or simply need a space to reflect, we're here to help. Explore various tools and resources designed to assist you on your mental health journey.
    """)

    st.divider()
    
    isAuth = st.session_state['authentication_status']

    if (isAuth == True):
        # Data Visualization Section
        st.subheader("Mood Reports Data Visualization 📊")

        # Refresh Data Button
        refresh_data = st.button("Refresh Data 🔄")
        if refresh_data:
            st.session_state['data_loaded'] = False

        # Load JSON Data
        if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
            try:
                with open(get_path(st.session_state['username']), 'r') as f:
                    data = json.load(f)

                # Convert JSON to DataFrame
                df = pd.DataFrame(data)

                # Apply the parsing function to each row
                df[['Mood', 'Stress Level', 'Overall Well-being', 'Notes']] = df['report'].apply(parse_report).tolist()
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.drop(columns=['report'], inplace=True)

                # Store the DataFrame in session state to persist across refreshes
                st.session_state['data'] = df
                st.session_state['data_loaded'] = True

            except Exception as e:
                st.error(f"Error loading data: {e}")

        # Retrieve data from session state
        df = st.session_state.get('data', pd.DataFrame())

        # Display the DataFrame
        with st.expander("Data"):
            st.write(df)

        # Visualization: Stress Level Over Time
        st.write("### Stress Level Over Time")
        st.line_chart(df.set_index('timestamp')['Stress Level'])

        # Visualization Layout
        col1, col2 = st.columns(2)

        with col1:
            # Visualization: Mood Distribution
            st.write("### Mood Distribution")
            mood_counts = df['Mood'].value_counts()
            st.bar_chart(mood_counts)
            

        with col2:
            # Visualization: Overall Well-being Distribution
            st.write("### Overall Well-being Distribution")
            well_being_counts = df['Overall Well-being'].value_counts()
            st.bar_chart(well_being_counts)
    else:
        st.error("Please login first to view your metrics!")
        if st.button("Login 🔐"):
            st.switch_page("pages/4_🔒_Login.py")

def login():
    st.subheader("Login 🔐")
    # st.success(f"Authenticated - Welcome")
    name, status, username = authenticator.login()
    if status:
        st.success(f"Authenticated - Welcome, {name}!")
        # Set session state variables
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
    elif status == False:
        st.error("Authentication failed.")
    elif status == None:
        st.warning("Please enter your credentials.")

def register():
    st.subheader("Register 📝")
    # Registration logic here
    try:
        email, username, name = authenticator.register_user(pre_authorization=False)
        if email:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

def forgot():
    st.subheader("Forgot Password 🤔")
    st.write("WIP...")

# Function to parse the report string
def parse_report(report):
    mood, stress_level, well_being, notes = None, None, None, None
    for line in report.split('\n'):
        if "Mood:" in line:
            mood = line.split("Mood:")[1].strip()
        elif "Stress Level:" in line:
            stress_level = int(line.split("Stress Level:")[1].strip())
        elif "Overall Well-being:" in line:
            well_being = line.split("Overall Well-being:")[1].strip()
        elif "Notes:" in line:
            notes = line.split("Notes:")[1].strip()
    return mood, stress_level, well_being, notes

if __name__ == "__main__":
    main()
