import os
import streamlit as st
import requests

# Load API Key securely
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit Page Config
st.set_page_config(page_title="Smart Reply with OpenRouter", layout="centered")

# Title and subtitle
st.markdown("<h1 class='title'>SMART REPLY</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Email Response Generator</p>", unsafe_allow_html=True)

# Text input
email_input = st.text_area("📩 Paste the email you received:", height=200)

# Function to get reply from OpenRouter/DeepSeek
def generate_reply(email_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": f"You are an assistant. Write a professional and polite reply to the following email:\n\n{email_text}\n\nReply:"}
        ],
        "temperature": 0.7,
        "max_tokens": 256,
        "top_p": 0.9
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = response.json()['choices'][0]['message']['content'].strip()
        return reply
    except Exception as e:
        return f"⚠️ Error: {e}"

# Button to trigger reply generation
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Generating your reply..."):
        response = generate_reply(email_input)
        st.markdown("### ✉️ Suggested Reply:")
        st.success(response)

# Custom styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
