from datetime import datetime

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
    
# Initialize session state for journal entries
if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = []

if 'username' not in st.session_state:
    st.session_state['username'] = 'Undefined'
    
# st.write(st.session_state)

isAuth = st.session_state['authentication_status']

# Function to add a new journal entry
def add_journal_entry(date, mood, content):
    st.session_state.journal_entries.append({"date": date, "mood": mood, "content": content})

if (isAuth == True):
    # Page layout
    st.title("My Journal 📔")
    st.write("Welcome to your personal journal. Write down your thoughts, track your moods, and reflect on your experiences.")

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
            if st.button("Edit", key=f"edit_{idx}_{entry['date']}"):
                # Logic to edit the entry
                pass
            if st.button("Delete", key=f"delete_{idx}_{entry['date']}"):
                # Logic to delete the entry
                st.session_state.journal_entries.remove(entry)
                st.success("Entry deleted successfully!")

    else:
        st.write("No journal entries found.")

else:
    st.error("Please login first!")