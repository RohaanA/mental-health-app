import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("AI71_API_KEY"),
    base_url=os.getenv("AI71_BASE_URL"),
)

# Simple invocation:
print(client.chat.completions.create(
    model="tiiuae/falcon-180B-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
))

# Streaming invocation:
for chunk in client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a song about a ginger-colored fish on the moon."}],
    model="tiiuae/falcon-180B-chat",
    stream=True,
):
    delta_content = chunk.choices[0].delta.content
    if delta_content:
        print(delta_content, sep="", end="", flush=True)