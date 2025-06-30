import os
import streamlit as st
import requests
import base64

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
st.write("API Key Loaded:", bool(api_key))  # Debug

# Set page config
st.set_page_config(page_title="Smart Email Reply", layout="centered")

# Read external CSS for cleaner GUI
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page structure
st.markdown("""
    <div class='title'>Smart Email Reply</div>
    <div class='subtitle'>Generate polished and professional email responses</div>
""", unsafe_allow_html=True)

# Email input
email_input = st.text_area("Paste your received email below:", height=200)

# Generate reply function
def generate_reply(email_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://smartemailreply.streamlit.app",
        "X-Title": "SmartEmailReplyApp"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": f"Write a formal, human-like reply to the following email without indicating that it's AI-generated:\n\n{email_text}\n\nReply:"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            return f"Error: {result['error']['message']}"
        else:
            return "Unexpected response structure."
    except Exception as e:
        return f"Exception: {e}"

# Button logic
if st.button("Generate Reply") and email_input.strip():
    with st.spinner("Generating..."):
        reply = generate_reply(email_input)
        st.markdown("<div class='response-box'>" + reply + "</div>", unsafe_allow_html=True)

        # Download button
        b64 = base64.b64encode(reply.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="smart_reply.txt" class="download-button">Download Reply</a>'
        st.markdown(href, unsafe_allow_html=True)
