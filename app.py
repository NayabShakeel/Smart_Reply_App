import os
import streamlit as st
import requests

# Load API Key securely
api_key = os.getenv("OPENAI_API_KEY")
st.write("🔐 API Key Loaded:", bool(api_key))

# Set up Streamlit page
st.set_page_config(page_title="Smart Email Reply", layout="centered")

st.markdown("<h1 class='title'>📨 Smart Email Reply Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generate professional replies using DeepSeek R1 (via OpenRouter)</p>", unsafe_allow_html=True)

# Input
email_input = st.text_area("📩 Paste the email you received:", height=200)

# Response area
def generate_reply(email_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://yourdomain.com",  # optional but recommended
        "X-Title": "SmartEmailApp",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": f"Write a professional, formal, and polite reply to this email:\n\n{email_text}\n\nReply:"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        
        # Check and parse
        reply = result.get("choices", [{}])[0].get("message", {}).get("content")
        if reply:
            return reply.strip()
        else:
            return f"❌ No reply received.\n\nFull Response:\n{result}"
    except Exception as e:
        return f"⚠️ Error: {e}"

# Button
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Generating your reply..."):
        reply = generate_reply(email_input)
        st.markdown("### 💬 Suggested Reply:")
        st.success(reply)

# Inject custom CSS if present
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
