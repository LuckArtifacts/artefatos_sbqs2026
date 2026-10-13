import os
import requests

OPENAI_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

def chamar_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-5o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
    }
    try:
        resp = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"ERRO: {e}"
