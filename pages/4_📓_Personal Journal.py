from datetime import datetime

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

st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

st.logo("logo.png")
# Initializing Session state
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
    
# Initialize session state for journal entries
if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = []

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'

isAuth = st.session_state['authentication_status']

# Function to add a new journal entry
def add_journal_entry(date, mood, content):
    st.session_state.journal_entries.append({"date": date, "mood": mood, "content": content})

if (isAuth == True):
    # Page layout
    username = st.session_state['username']
    st.title(f"My Journal 📔")
    st.write(f"Welcome to your personal journal {username}. Write down your thoughts, track your moods, and reflect on your experiences.")

    # New Journal Entry Form
    st.subheader("New Entry")
    entry_date = st.date_input("Date", datetime.today())
    entry_mood = st.selectbox("Mood", ["Happy", "Sad", "Anxious", "Excited", "Calm", "Angry"])
    entry_content = st.text_area("What's on your mind?", height=200)
    if st.button("Save Entry"):
        add_journal_entry(entry_date, entry_mood, entry_content)
        st.success("Entry saved successfully!")

    # Display Journal Entries
    st.subheader("Your Entries")

    # Search and Filter
    search_query = st.text_input("Search Entries")
    filtered_entries = [entry for entry in st.session_state.journal_entries if search_query.lower() in entry["content"].lower()]

    if filtered_entries:
        for idx, entry in enumerate(filtered_entries):
            st.write(f"**Date:** {entry['date']} | **Mood:** {entry['mood']}")
            st.write(entry["content"])
            
            # Create three columns for Edit, Delete, and Analyze buttons
            col1, col2, col3 = st.columns([1,1,1])
            
            # Place the Edit button in the first column
            with col1:
                if st.button("Edit", key=f"edit_{idx}_{entry['date']}"):
                    # Logic to edit the entry
                    pass
            
            # Place the Delete button in the second column
            with col2:
                if st.button("Delete", key=f"delete_{idx}_{entry['date']}"):
                    # Logic to delete the entry
                    st.session_state.journal_entries.remove(entry)
                    st.success("Entry deleted successfully!")
            
            # Place the Analyze button in the third column
            with col3:
                if st.button("Analyze", key=f"analyze_{idx}_{entry['date']}"):
                    # Logic to analyze the entry
                    prompt = f"You are Dr. Falcon. A mental health professional. Act like an expert in the field of mental health. A patient has come to you with the name {username}. Analyze their journal entry and provide insights."
                    analysis = llm(prompt, entry["content"])
                    st.write("**Analysis:**")
                    st.write(analysis)


    else:
        st.write("No journal entries found.")

else:
    st.error("Please login first!")