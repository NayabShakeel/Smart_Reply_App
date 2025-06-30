import os
import streamlit as st
import requests

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
st.write("🔐 API Key Loaded:", bool(api_key))  # Debug line

# Page config
st.set_page_config(page_title="Smart Email Reply", layout="centered")

# Page Header
st.markdown("""
    <style>
        .title { text-align: center; color: #61dafb; font-size: 3em; font-weight: bold; margin-top: 30px; }
        .subtitle { text-align: center; color: #ccc; font-size: 1.3em; margin-bottom: 30px; }
        .response-box { background-color: #2C2C2C; color: #fff; padding: 20px; border-radius: 10px; font-size: 1em; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📨 Smart Email Reply</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by OpenRouter (Free Mistral Model)</div>", unsafe_allow_html=True)

# Email input
email_input = st.text_area("📩 Paste your received email below:", height=200)

# Generate reply
def generate_reply(email_text):
    # Use referer version first (Streamlit Cloud only works with real app link)
    headers_with_referer = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://smartemailreply.streamlit.app",  # Change to your actual app URL
        "X-Title": "SmartEmailReplyApp"
    }

    # Backup header (for local testing)
    headers_simple = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": f"Write a professional and polite reply to the following email:\n\n{email_text}\n\nReply:"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        # Try with full headers first
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers_with_referer, json=payload)
        result = response.json()

        # Debug output
        st.write("🧾 Request Headers:", headers_with_referer)
        st.write("📦 Payload Sent:", payload)
        st.write("📬 Raw Response:", result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            # Try again using simple headers (for local fallback)
            fallback_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers_simple, json=payload)
            fallback_result = fallback_response.json()
            st.write("🪛 Fallback Headers:", headers_simple)
            st.write("🪛 Fallback Raw Response:", fallback_result)

            if "choices" in fallback_result:
                return fallback_result["choices"][0]["message"]["content"].strip()
            elif "error" in fallback_result:
                return f"❌ API Error (Fallback too): {fallback_result['error']['message']}"
            else:
                return f"❌ Unexpected fallback response: {fallback_result}"
        else:
            return f"❌ Unexpected response: {result}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# Button to trigger reply
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Thinking..."):
        reply = generate_reply(email_input)
        st.markdown("### 💬 Suggested Reply:")
        st.markdown(f"<div class='response-box'>{reply}</div>", unsafe_allow_html=True)
