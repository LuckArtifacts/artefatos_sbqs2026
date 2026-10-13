import requests
def chamar_llama(prompt):
    payload = {
        "model"  : "llama3.1",
        "prompt" : prompt,
        "stream" : False,
        "options": {
            "temperature": 0.3,   #baixo para respostas mais consistentes
            "num_predict": 512,
        }
    }
    try:
        resp = requests.post("http://localhost:11434/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        return f"ERRO: {e}"