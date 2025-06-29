import os
import streamlit as st
from openai import OpenAI

# Initialize client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Smart Reply with OpenAI", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FFEDFA;'>SMART REPLY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>AI-Powered Email Response Generator</p>", unsafe_allow_html=True)

email_input = st.text_area("Paste the email you received:", height=200)

def generate_reply_via_openai(email_text):
    prompt = (
        "You are an assistant. Write a professional and polite reply to the following email:\n\n"
        f"{email_text}\n\nReply:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=0.9,
            n=1,
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"Error generating reply: {e}"

if st.button("Generate Reply") and email_input.strip():
    with st.spinner("Generating reply..."):
        reply = generate_reply_via_openai(email_input)
        st.markdown("### Suggested Reply:")
        st.success(reply)
