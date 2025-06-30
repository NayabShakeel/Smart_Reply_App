import os
import streamlit as st
import requests

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page setup
st.set_page_config(page_title="Smart Email Reply", layout="centered")
st.markdown("<h1 class='title'>📨 Smart Email Reply Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generate formal email replies using DeepSeek R1</p>", unsafe_allow_html=True)

# Input
email_input = st.text_area("📩 Paste the email you received:", height=200)

# Generate reply function
def generate_reply(email_text):
    if not api_key:
        return "❌ API key is missing."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",  # required for OpenRouter
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

        # Debugging logs
        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            return f"❌ API Error: {result['error']['message']}"
        else:
            return f"❌ Unexpected response:\n{result}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# Run when button clicked
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Generating your reply..."):
        reply = generate_reply(email_input)
        st.markdown("### 💬 Suggested Reply:")
        st.success(reply)

# Inject style if available
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
