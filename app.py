import os
import streamlit as st
import requests
import base64

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
st.write("🔐 API Key Loaded:", bool(api_key))  # Keep only this debug

# Page config
st.set_page_config(page_title="Smart Email Reply", layout="centered")

# Custom Styles and JS
st.markdown("""
    <style>
        .title { text-align: center; color: #61dafb; font-size: 3em; font-weight: bold; margin-top: 30px; }
        .subtitle { text-align: center; color: #ccc; font-size: 1.3em; margin-bottom: 30px; }
        .response-box {
            background-color: #2C2C2C;
            color: #fff;
            padding: 20px;
            border-radius: 10px;
            font-size: 1em;
            margin-top: 20px;
            white-space: pre-wrap;
        }
        .copy-button {
            background-color: #3D0301;
            color: #FFEDFA;
            padding: 8px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            margin-right: 10px;
        }
        .download-button {
            background-color: #61dafb;
            color: #000;
            padding: 8px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            alert('✅ Copied to clipboard!');
        }, function(err) {
            alert('❌ Failed to copy text: ', err);
        });
    }
    </script>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📨 Smart Email Reply</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by OpenRouter (Free Mistral Model)</div>", unsafe_allow_html=True)

# Email input
email_input = st.text_area("📩 Paste your received email below:", height=200)

# Generate reply
def generate_reply(email_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://smartemailreply.streamlit.app",  # Update if needed
        "X-Title": "SmartEmailReplyApp"
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

# Button to trigger reply
if st.button("Generate Reply ✨") and email_input.strip():
    with st.spinner("Thinking..."):
        reply = generate_reply(email_input)
        st.markdown("### 💬 Suggested Reply:")
        st.markdown(f"<div class='response-box' id='replyBox'>{reply}</div>", unsafe_allow_html=True)

               # Download as TXT 
        b64 = base64.b64encode(reply.encode()).decode()
        href = f'''
            <a href="data:file/txt;base64,{b64}" download="smart_reply.txt" class="download-button">
                ⬇️ Download Reply
            </a>
        '''
        st.markdown(href, unsafe_allow_html=True)
