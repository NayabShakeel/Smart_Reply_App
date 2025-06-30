import os
import streamlit as st
import requests

# Load API key from environment
api_key = os.getenv("OPENAI_API_KEY")
st.write("Headers:", headers)
st.write("Payload:", payload)
st.write("Raw Response:", result)
st.write("🔐 API Key Loaded:", bool(api_key))


# Set Streamlit page config
st.set_page_config(page_title="Smart Email Reply", layout="centered")

# ----- HTML Style -----
st.markdown("""
    <style>
    body {
        background-color: #1A1A19;
        color: #ccc;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        text-align: center;
        color: #61dafb;
        font-size: 3em;
        font-weight: bold;
        margin-top: 30px;
    }
    .subtitle {
        text-align: center;
        color: #ccc;
        font-size: 1.3em;
        margin-bottom: 30px;
    }
    .response-box {
        background-color: #2C2C2C;
        color: #fff;
        padding: 20px;
        border-radius: 10px;
        font-size: 1em;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>📨 Smart Email Reply</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Generate formal replies using DeepSeek R1 (via OpenRouter)</div>", unsafe_allow_html=True)

# Input
email_input = st.text_area("Paste the email you received:", height=200)

# Function to send request
def generate_reply(email_text):
    if not api_key:
        return "❌ API key not loaded."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",   # Required
        "X-Title": "SmartEmailReplyApp"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": f"Write a formal and polite professional reply to the following email:\n\n{email_text}\n\nReply:"
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
            return f"❌ API Error: {result['error']['message']}"
        else:
            return f"❌ Unexpected response: {result}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# Button to trigger
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Please wait..."):
        reply = generate_reply(email_input)
        st.markdown("### 💬 Suggested Reply:")
        st.markdown(f"<div class='response-box'>{reply}</div>", unsafe_allow_html=True)
