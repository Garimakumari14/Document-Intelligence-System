# Document-Intelligent-System

# GenAI Research Assistant

An interactive AI-powered web app to help users quickly understand research documents. Upload PDFs or TXT files to get instant summaries, ask questions, and test your comprehension with challenge questions — all powered by Groq API and semantic similarity evaluation.

---

## Features

- Upload `.pdf` or `.txt` research documents
- Generate concise summaries using Groq AI models
- Ask free-form questions about the document and get detailed answers with justifications
- Challenge yourself with automatically generated reasoning questions and get instant feedback
- Intuitive, interactive UI built with Streamlit
- Backend powered by Flask, PyPDF2, and Sentence Transformers for semantic similarity scoring

---

## Technology Stack

- **Backend:** Python, Flask, PyPDF2, Sentence Transformers, Requests
- **Frontend:** Streamlit
- **AI Model API:** Groq API (GPT-based large language models)
- **Environment Variables:** `.env` file for API key management

---

## Installation and Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/genai-research-assistant.git
   cd genai-research-assistant
