

### 📄 `README.md` for **Document Intelligence System**

```markdown
# 🧠 Document Intelligence System (Powered by Groq)

A smart AI-powered assistant that helps you **summarize**, **interact**, and **test your understanding** of large documents using Groq’s LLaMA-3 API and advanced NLP models.

![banner](https://img.shields.io/badge/GenAI%20Assistant-Groq%20%7C%20LLM-blueviolet) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-Backend-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)

---

## 🚀 Features

- 📄 Upload `.pdf` or `.txt` files
- ✨ Get summarized insights from long documents
- 💬 Ask any question about the document
- 🎯 Challenge yourself with AI-generated quiz questions
- 🧠 Answer evaluation with similarity feedback using BERT embeddings

---

## 📂 Project Structure

```

Document-Intelligence-System/
│
├── backend/                    # Flask + Groq API backend
│   ├── app.py                  # Main backend logic
│   └── .env                    # Environment variables (API key)
│
├── frontend/                   # Streamlit frontend
│   └── streamlit\_app.py        # Interactive UI
│
├── utils/                      # Utility modules
│   ├── pdf\_reader.py
│   └── gpt\_helpers.py          # (if used for extensions)
│
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies

````

---

## 🛠️ Tech Stack

| Layer     | Technology                       |
|-----------|----------------------------------|
| Frontend  | `Streamlit`                      |
| Backend   | `Flask`, `SentenceTransformers`  |
| API       | `Groq LLaMA-3` via Chat API      |
| NLP Tools | `MiniLM-L6-v2`, `Cosine Similarity` |
| Format    | Supports `.pdf`, `.txt`          |

---

## 📸 Demo

> Upload → Summarize → Ask → Quiz → Evaluate

![screenshot](https://github.com/Garimakumari14/Document-Intelligence-System/assets/sample-demo.gif) <!-- optional GIF or image -->

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Garimakumari14/Document-Intelligence-System.git
cd Document-Intelligence-System
````

### 2. Install dependencies

Make a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

Then install:

```bash
pip install -r requirements.txt
```

### 3. Add your Groq API Key

Create a `.env` file inside the `backend/` directory:

```env
GROQ_API_KEY=your-groq-api-key-here
```

---

### 4. Run the app

In one terminal, run the **backend**:

```bash
cd backend
python app.py
```

In another terminal, run the **frontend**:

```bash
cd frontend
streamlit run streamlit_app.py
```

> Open `http://localhost:8501` in your browser!

---

## 🧠 How It Works (Architecture / Reasoning Flow)

```text
User Uploads File → Flask Extracts Text
            ↓
      Groq LLaMA-3 Summarizes
            ↓
   Streamlit Displays Summary
            ↓
User Asks a Question → Groq Answers It
            ↓
Challenge Questions Generated
            ↓
User Answers → MiniLM Model Evaluates Similarity
```

---

## 📌 To-Do (Future Improvements)

* [ ] Support DOCX, HTML, Markdown files
* [ ] Chat history and bookmarking
* [ ] Answer confidence scoring
* [ ] UI redesign with Tailwind or Bootstrap

---

## 🤝 Contributing

1. Fork this repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m 'Add feature xyz'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Create a pull request

---

## 📜 License

MIT License © 2025 [Garima Kumari](https://github.com/Garimakumari14)

```

---

Would you also like a `requirements.txt` file auto-generated from your code dependencies?
```
