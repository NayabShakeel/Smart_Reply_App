def generate_reply(email_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": f"You are an assistant. Write a professional and polite reply to the following email:\n\n{email_text}\n\nReply:"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 256,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # Parse JSON safely
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            return f"❌ API Error: {result['error']['message']}"
        else:
            return f"❌ Unexpected response format: {result}"
    except Exception as e:
        return f"⚠️ Exception: {e}"
