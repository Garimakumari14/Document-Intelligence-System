

````markdown
** GenAI Research Assistant **

An AI-powered web application that helps users quickly understand large research documents. Upload PDFs or TXT files, get instant summaries, ask questions, and test your comprehension — all powered by the Groq API and semantic similarity evaluation using Sentence Transformers.

---

**Features**

- Upload `.pdf` or `.txt` research documents
- Generate concise summaries using Groq AI models
- Ask detailed questions about the document with contextual answers
- Test your understanding by answering AI-generated challenge questions
- Semantic similarity scoring for answer evaluation using Sentence Transformers
- Interactive and user-friendly frontend built with Streamlit
- Lightweight backend built with Flask

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/genai-research-assistant.git
cd genai-research-assistant
````

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the backend server

```bash
python backend.py
```

### 6. Run the Streamlit frontend (in a new terminal)

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

The GenAI Research Assistant consists of two main components:

* **Backend:** A Flask API server handling document processing, AI calls, and answer evaluation.
* **Frontend:** A Streamlit web app providing an interactive user interface.

---

### Backend (Flask)

1. **Document Upload & Text Extraction**
   Users upload PDF or TXT files. The backend extracts raw text using PyPDF2 for PDFs and standard decoding for TXT files.

2. **Groq API Integration**
   The backend sends prompts to the Groq API to generate:

   * Summaries of uploaded documents
   * Answers to user questions based on document context
   * Reasoning and inference challenge questions

3. **Context Storage**
   The extracted document text and filename are stored temporarily in memory for context reuse.

4. **Question Answering**
   The backend constructs prompts combining user questions and document text and sends them to Groq API for contextual answers.

5. **Challenge Question Evaluation**
   Upon receiving user answers to challenge questions:

   * The backend gets the "correct" answer from Groq API.
   * Uses Sentence Transformers (`all-MiniLM-L6-v2`) to compute semantic similarity between user and correct answers.
   * Provides feedback based on similarity thresholds.

6. **Challenge Question Generation**
   Generates 3 reasoning questions from the document to test user understanding.

---

### Frontend (Streamlit)

* **Upload Interface**
  Allows users to upload PDF or TXT files. Displays processing status and shows document summary once ready.

* **Interactive Q\&A**
  Users can ask free-form questions; answers and justifications are displayed dynamically.

* **Comprehension Challenges**
  Users can generate AI-created questions and submit answers for evaluation with immediate feedback.

* **State Management**
  Uses Streamlit's session state to keep track of uploaded document, messages, challenge questions, and evaluation results for smooth user experience.

* **Error Handling**
  Provides clear error messages on upload failures, backend issues, or API errors.

---

### Data & Interaction Flow Summary

1. **Upload Document:**
   Extract text → Summarize via Groq API → Show summary

2. **Ask Question:**
   Prompt constructed with question + document context → Groq API answer → Display answer & justification

3. **Generate Challenge Questions:**
   Use document context → Generate 3 inference questions via Groq API → Display questions

4. **Evaluate Challenge Answers:**
   Generate correct answer → Calculate semantic similarity → Provide detailed feedback to user

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

Your Name
Email: [your.email@example.com](mailto:your.email@example.com)
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

---

## Acknowledgments

* [Groq API](https://groq.com/)
* [Sentence Transformers](https://www.sbert.net/)
* [Streamlit](https://streamlit.io/)
* [Flask](https://flask.palletsprojects.com/)

```

---

Would you like me to help you create a `requirements.txt` file or deployment guide next?
```
