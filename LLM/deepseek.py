import os
import requests

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")

def chamar_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"ERRO: {e}"
