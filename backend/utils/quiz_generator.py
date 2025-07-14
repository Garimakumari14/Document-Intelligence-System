import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_questions(text):
    url = "https://api.groq.com/v1/engines/text-generation/jobs"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Generate 3 reasoning questions from the following text:\n\n{text[:1000]}\n\nQuestions:"

    payload = {
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7,
        "stop_sequences": ["\n\n"]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        generated_text = data['data'][0]['text'].strip()
        return generated_text
    else:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")
