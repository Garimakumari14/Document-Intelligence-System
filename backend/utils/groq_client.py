import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

API_URL = "https://api.groq.com/v1/engines/text-generation/jobs"

def groq_api_call(prompt, max_tokens=150, temperature=0.3, stop_sequences=None):
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    if stop_sequences:
        payload["stop_sequences"] = stop_sequences

    response = requests.post(API_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]['text'].strip()
    else:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")

def groq_summarize(text, max_tokens=150):
    prompt = f"Summarize this document in under 150 words:\n\n{text}"
    return groq_api_call(prompt, max_tokens=max_tokens, temperature=0.3, stop_sequences=["\n\n"])

def groq_answer(question, context):
    prompt = (
        f"Based on the following context, answer the question.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )
    return groq_api_call(prompt, max_tokens=150, temperature=0.0, stop_sequences=["\n"])

def groq_generate_questions(text):
    prompt = (
        "Generate 3 reasoning and inference questions based on the following text:\n\n"
        + text[:1500]
    )
    return groq_api_call(prompt, max_tokens=250, temperature=0.7, stop_sequences=["\n\n"])

