import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_reply(email_text):
    prompt = (
        "You are an assistant. Write a professional and polite reply to the following email:\n\n"
        f"{email_text}\n\nReply:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=256,
        top_p=0.9,
        n=1,
    )
    return response.choices[0].message.content.strip()
