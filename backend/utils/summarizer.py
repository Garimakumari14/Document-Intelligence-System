import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_text(text, max_len=150):
    url = "https://api.groq.com/v1/engines/text-generation/jobs"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    chunk_size = 1000  # chunk size to avoid token limit issues
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following text in under {max_len} words:\n\n{chunk}\n\nSummary:"
        payload = {
            "prompt": prompt,
            "max_tokens": max_len,
            "temperature": 0.3,
            "stop_sequences": ["\n"]
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            generated_text = result['data'][0]['text'].strip()
            summaries.append(generated_text)
        else:
            raise Exception(f"Groq API error {response.status_code}: {response.text}")

    final_summary = " ".join(summaries)
    return final_summary.strip()
