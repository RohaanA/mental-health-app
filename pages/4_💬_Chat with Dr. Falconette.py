import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from falcon import client

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
    st.title("Dr. Falconette 👩🏼‍⚕️")

    # Initialize chat history# Initialize session state for messages and model
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey there! 🦜 Dr. Falconette at your service! Ready to chat about anything and everything—whether you're curious about mental health or just need a friendly ear. Let's make your day a little brighter! 🌞 What's on your mind today?"}
        ]
    
    # # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     st.markdown("Hey there! 🦜 Dr. Falconette at your service! Ready to chat about anything and everything—whether you're curious about mental health or just need a friendly ear. Let's make your day a little brighter! 🌞 What's on your mind today?")

    
    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey there! 🦜 Dr. Falconette at your service! Ready to chat about anything and everything—whether you're curious about mental health or just need a friendly ear. Let's make your day a little brighter! 🌞 What's on your mind today?"}
        ]
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Get user input and handle the response
    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="tiiuae/falcon-180B-chat",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.error("Please login first!")