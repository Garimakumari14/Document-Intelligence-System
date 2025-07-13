#Document Intelligent System

````markdown
# GenAI Research Assistant

An AI-powered web application that helps users quickly understand large research documents. Upload PDFs or TXT files, get instant summaries, ask questions, and test your comprehension — all powered by Groq API and semantic similarity evaluation.

---

## Features

- Upload `.pdf` or `.txt` research documents
- Generate concise summaries using Groq AI models
- Ask detailed questions about the document with contextual answers
- Test your understanding by answering AI-generated challenge questions
- Semantic similarity scoring for answer evaluation using Sentence Transformers
- User-friendly and interactive frontend built with Streamlit
- Lightweight backend built with Flask

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/genai-research-assistant.git
cd genai-research-assistant
````

### 2. Create and activate a Python virtual environment

```bash
python -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the backend server

```bash
python backend.py
```

### 6. Run the Streamlit frontend (in a new terminal window)

```bash
streamlit run frontend/streamlit_app.py
```

### 7. Access the app

Open your browser and navigate to:

```
http://localhost:8501
```

---

## Architecture & Reasoning Flow

### Overview

The GenAI Research Assistant comprises two main components:

1. **Backend (Flask API)**
2. **Frontend (Streamlit UI)**

---

### Backend (Flask)

* **Document Upload & Text Extraction**
  Users upload PDF or TXT files through the frontend. The backend extracts text using PyPDF2 for PDFs and decodes text files.

* **Groq API Integration**
  The backend sends prompts to the Groq API (large language model) to generate summaries, answers, and challenge questions. The API is called via HTTP requests with proper authorization.

* **Context Management**
  The uploaded document’s extracted text is cached in memory (`document_store`) for subsequent question-answering and challenge generation requests.

* **Question Answering**
  When users ask questions, the backend crafts a prompt including the question and document context, sends it to Groq, and returns the generated answer.

* **Challenge Question Evaluation**
  For user-submitted challenge answers, the backend:

  * Generates the "correct" answer via Groq API.
  * Computes semantic similarity between the user answer and correct answer using Sentence Transformers (`all-MiniLM-L6-v2` model).
  * Returns feedback based on similarity score.

* **Challenge Question Generation**
  On request, generates 3 reasoning and inference questions from the document text to test user comprehension.

---

### Frontend (Streamlit)

* **User Interface**
  A clean, interactive UI guiding users to upload documents, read summaries, ask questions, and take comprehension challenges.

* **State Management**
  Streamlit session state stores document summaries, messages, questions, and evaluation results for a seamless interactive experience.

* **Interaction Flow**

  * User uploads a document → backend extracts text and returns a summary.
  * User asks questions → frontend sends them to backend and displays answers with justification.
  * User tries challenge questions → frontend sends answers for evaluation and shows feedback and expected answers.

* **Error Handling**
  The UI provides clear messages when errors occur (e.g., API errors, missing uploads).

---

### Data Flow Summary

1. **Upload** → Extract text → Summarize via Groq API → Return summary
2. **Ask Question** → Prompt built with context → Send to Groq API → Return answer
3. **Generate Challenge Questions** → Use document context → Request Groq API → Return questions
4. **Evaluate Challenge Answer** → Get Groq answer → Compute semantic similarity → Provide feedback

---

## License

MIT License — See the LICENSE file for details.

---

## Contact

Your Name
Email: garimakumari2006@gmail.com
GitHub: [https://github.com/Garimakumari14](https://github.com/Garimakumari14)

---

## Acknowledgments

* [Groq API](https://groq.com/)
* [Sentence Transformers](https://www.sbert.net/)
* [Streamlit](https://streamlit.io/)
* [Flask](https://flask.palletsprojects.com/)

```

---

If you want, I can also help generate a `requirements.txt` or deployment instructions next!
```
