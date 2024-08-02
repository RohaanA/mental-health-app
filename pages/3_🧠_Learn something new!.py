import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from falcon import llm

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
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'
    
# st.write(st.session_state)

isAuth = st.session_state['authentication_status']

if (isAuth == True):
    username = st.session_state.get("username", "User")  # Replace with actual username retrieval logic
    st.title(f"Welcome to the Resource Library 📖, {username}!")# Present options to the user
    st.subheader("Select topics you are interested in:")

    topics = {
        "Anxiety": "Understanding anxiety, its causes, and coping strategies.",
        "Depression": "Exploring depression, symptoms, and treatment options.",
        "Stress Management": "Techniques and strategies for managing stress.",
        "Coping Strategies": "Effective ways to handle everyday challenges and emotional difficulties.",
        "Mindfulness and Relaxation": "Practices for enhancing mindfulness and relaxation."
    }

    selected_topics = st.multiselect(
        "Choose the topics you're interested in:",
        options=list(topics.keys()),
        format_func=lambda x: f"{x}: {topics[x]}"
    )
    
    # Text input for user-added topics
    custom_topic = st.text_input("Add your own topic:")

    if st.button("Teach me! 🏫"):
        if custom_topic and custom_topic not in selected_topics:
            selected_topics.append(custom_topic)
        if selected_topics:
            st.success("Dr. Falcon is collecting information regarding your concerned topics")
            st.subheader("Generated Information")
            # Generate a combined response from the LLM
            prompt = f"Your name is Dr. Falcon. You are an expert in psychology and mental health. Act like an expert doctor, and educate your patient about the topics that they are concerned with."
            selected_topics_str = ', '.join(selected_topics)
            # print(type(selected_topics))
            response = llm(prompt, selected_topics_str)
            st.write(response)
        else:
            st.write("Please select at least one topic to get information.")
else:
    st.error("Please login first!")