import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="Perplexity AI Chatbot", page_icon="🤖")
st.title("Perplexity AI Chatbot 🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call Perplexity API
def get_perplexity_response(messages):
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "sonar",  # Using the standard sonar model
        "messages": [
            {
                "role": m["role"],
                "content": m["content"]
            } for m in messages
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        if hasattr(e.response, 'text'):
            return f"Error: {e.response.text}"
        return f"Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = [
                {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
                *st.session_state.messages
            ]
            response = get_perplexity_response(messages)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response}) 