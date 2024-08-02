import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from falcon import daily_checkup
from utils import save_report

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
# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'

isAuth = st.session_state['authentication_status']

if (isAuth == True):
    username = st.session_state.get("username", "User")  # Replace with actual username retrieval logic
    st.title(f"Welcome to your daily checkup, {username}!")

    # Mood Selection
    st.subheader("How are you feeling today?")

    moods = {
        "😊": "Happy",
        "😟": "Sad",
        "😡": "Angry",
        "😐": "Neutral",
        "😌": "Relaxed",
        "😰": "Anxious"
    }

    selected_mood = st.radio(
        "Select your mood:",
        options=list(moods.keys()),
        format_func=lambda x: f"{moods[x]} {x}",
        horizontal=True
    )

    st.write(f"You selected: {moods[selected_mood]} {selected_mood}")

    # Stress Level Input
    st.subheader("Stress Levels")
    stress_level = st.slider(
        "On a scale from 0 (not stressed) to 10 (extremely stressed), how stressed are you feeling?",
        0, 10, 0
    )

    # Overall Well-being Input
    st.subheader("Overall Well-being")
    well_being = st.radio(
        "How would you rate your overall well-being?",
        options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
        index=2
    )

    # Additional Notes
    st.subheader("Additional Notes")
    notes = st.text_area(
        "Add any notes or describe specific events or feelings:",
        placeholder="Write about your day, thoughts, or anything you'd like to express..."
    )


    # Display the user's input
    st.subheader("Your Input Summary:")
    st.write(f"**Mood:** {moods[selected_mood]} {selected_mood}")
    st.write(f"**Stress Level:** {stress_level}")
    st.write(f"**Overall Well-being:** {well_being}")
    st.write(f"**Additional Notes:** {notes}")
    # Submit Button
    if st.button("Submit"):
        # Compile the user's input into a report
        user_report = f"""
            Mood: {moods[selected_mood]} {selected_mood}
            Stress Level: {stress_level}
            Overall Well-being: {well_being}
            Notes: {notes}
            """
        # Here, you would handle the form submission, such as saving the data
        st.success("Your daily checkup has been submitted. Dr. Falcon is now reading your checkup!")
        
        ai_response = daily_checkup(user_report)
        
        st.subheader("Dr. Falcon's Response 👨‍⚕️")
        st.write(ai_response)
        
        # Save the daily checkup in user's JSON file.
        save_report(username, user_report)
else:
    st.error("Please login first!")