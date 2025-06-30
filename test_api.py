import requests

api_key = "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"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "X-Title": "Test"
}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "user",
            "content": "Hello! Can you say hi back?"
        }
    ],
    "temperature": 0.5
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
