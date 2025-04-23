import requests
import re
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

PROMPT_TEMPLATE = """
You are an AI assistant that extracts and computes deadlines from legal text.
Return the **exact due date** in YYYY-MM-DD format **only**. Do not include explanations.
Today's date is {today}.

Input: "{text}"
"""

def ask_ollama(text):
    today = datetime.today().strftime('%Y-%m-%d')
    prompt = PROMPT_TEMPLATE.format(today=today, text=text)

    response = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    try:
        full_response = response.json()["response"].strip()
        # Extract only YYYY-MM-DD
        match = re.search(r"\d{4}-\d{2}-\d{2}", full_response)
        return match.group(0) if match else None
    except Exception as e:
        print("Error:", e)
        return None
