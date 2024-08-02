""" 
Falcon.py 

-- Contains functions that help communicate with the FalconLLM.
"""
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize LLM client
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = os.getenv("AI71_API_KEY")

client = openai.OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

def daily_checkup(user_report):
    """Function to interact with Falcon LLM and display the response."""
    try:
        response = client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": "You are a helpful mental health assistant. You are receiving the daily medical report of a patient. As a mental health professional, instruct the patient on how they can execute today's day in the best way!"},
                {"role": "user", "content": user_report}
            ]
        )

        # ai_response = response['choices'][0]['message']['content']
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
            print(f"An error occurred: {e}")

def llm(prompt, data):
    """Function to interact with Falcon LLM with custom prompt and data."""
    try:
        response = client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": data}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
            print(f"An error occurred: {e}")