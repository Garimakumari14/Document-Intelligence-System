import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def answer_question(question, context):
    url = "https://api.groq.com/v1/engines/text-generation/jobs"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Based on the following context, answer the question.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    payload = {
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.0,
        "stop_sequences": ["\n"]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        answer = data['data'][0]['text'].strip()
        return answer
    else:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")
