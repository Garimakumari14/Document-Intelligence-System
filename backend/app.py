import os
from flask import Flask, request, jsonify
import PyPDF2
import requests
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load Sentence-Transformer model for similarity evaluation
print("Loading Sentence-Transformer model...")
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Similarity model loaded successfully.")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

document_store = {
    "text": None,
    "filename": None
}

def extract_text_from_pdf(file_stream):
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_txt(file_stream):
    return file_stream.read().decode('utf-8')

def groq_call(prompt, model="llama3-8b-8192", max_tokens=500):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith('.txt'):
            text = extract_text_from_txt(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if not text.strip():
            return jsonify({"error": "Could not extract text from the document. It might be empty or scanned."}), 400

        document_store["text"] = text
        document_store["filename"] = file.filename

        prompt = f"Summarize the following document in under 150 words:\n\n{text[:4000]}"
        summary = groq_call(prompt)

        return jsonify({
            "filename": file.filename,
            "summary": summary,
            "message": "File uploaded and processed successfully."
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_anything():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    context = document_store.get("text")
    if not context:
        return jsonify({"error": "No document has been uploaded yet. Please upload a document first."}), 400

    prompt = f"Answer the following question based on the document below:\n\nQuestion: {question}\n\nDocument:\n{context[:4000]}\n\nAlso include the sentence that supports your answer."
    answer = groq_call(prompt)

    return jsonify({
        "question": question,
        "answer": answer,
        "justification": "(Provided in answer text)",
        "confidence_score": "N/A (Groq doesn't return score)"
    })

@app.route('/evaluate-challenge', methods=['POST'])
def evaluate_challenge_answer():
    data = request.get_json()
    question = data.get('question')
    source_context = data.get('source_context')
    user_answer = data.get('user_answer')

    if not all([question, source_context, user_answer]):
        return jsonify({"error": "Missing 'question', 'source_context', or 'user_answer' in request"}), 400

    prompt = f"Answer this question based on the following document:\n\nQuestion: {question}\nDocument:\n{source_context}"
    correct_answer = groq_call(prompt)

    embedding1 = similarity_model.encode(user_answer, convert_to_tensor=True)
    embedding2 = similarity_model.encode(correct_answer, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embedding1, embedding2).item()

    feedback = ""
    if similarity_score > 0.8:
        feedback = "Correct! Your answer is very similar to the information in the document."
    elif similarity_score > 0.5:
        feedback = "Partially correct. Your answer is on the right track but could be more precise."
    else:
        feedback = "Incorrect. Your answer does not seem to align with the information in the document."

    return jsonify({
        "feedback": feedback,
        "your_answer": user_answer,
        "expected_answer": correct_answer,
        "justification": source_context,
        "similarity_score": similarity_score
    })

@app.route('/generate-challenge', methods=['GET'])
def generate_challenge_questions():
    context = document_store.get("text")
    if not context:
        return jsonify({"error": "No document uploaded yet."}), 400

    prompt = (
        "Generate 3 reasoning and inference questions based on the following text:\n"
        + context[:4000]
    )

    try:
        questions_text = groq_call(prompt, max_tokens=250)
        questions = []
        for line in questions_text.split('\n'):
            q = line.strip()
            if q:
                questions.append({"question": q, "source_context": context[:4000]})

        return jsonify({"challenge_questions": questions})
    except Exception as e:
        return jsonify({"error": f"Failed to generate questions: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
