import streamlit as st
import requests
import io

# --- Configuration ---
st.set_page_config(page_title="GenAI Research Assistant", page_icon="🧠")

BACKEND_URL = "http://127.0.0.1:5000"

# --- Session State Initialization ---
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'challenge_questions' not in st.session_state:
    st.session_state.challenge_questions = []
if 'challenge_results' not in st.session_state:
    st.session_state.challenge_results = {}

# --- UI Layout ---
st.title("🧠 Document Intelligent System (DIS) ")
st.markdown("""
This tool uses Generative AI to help you read and understand large documents faster.
1.  **Upload a document** (`.pdf` or `.txt`).
2.  Get an **instant summary**.
3.  Use the **"Ask Anything"** mode for free-form questions or the **"Challenge Me"** mode to test your comprehension.
""")

with st.sidebar:
    st.header("1. Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        on_change=lambda: st.session_state.update(summary=None, messages=[], challenge_questions=[], challenge_results={})
    )

    if uploaded_file is not None and st.session_state.summary is None:
        with st.spinner("Processing document... This may take a moment."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.summary = data.get("summary")
                    st.session_state.filename = data.get("filename")
                    st.success(f"Successfully processed '{st.session_state.filename}'")
                else:
                    st.error(f"Error from server: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend. Please ensure the backend server is running. Error: {e}")

if st.session_state.summary:
    st.header("2. Auto-Generated Summary")
    st.info(st.session_state.summary)

    st.header("3. Interact with the Document")
    tab1, tab2 = st.tabs(["💬 Ask Anything", "🎯 Challenge Me"])

    with tab1:
        st.subheader("Free-form Question Answering")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "justification" in message:
                    with st.expander("Show Justification"):
                        st.write(message["justification"])

        if prompt := st.chat_input("Ask a question about the document"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = requests.post(f"{BACKEND_URL}/ask", json={"question": prompt})
                        if response.status_code == 200:
                            data = response.json()
                            answer = data.get("answer")
                            justification = data.get("justification")

                            response_text = f"{answer}"
                            st.markdown(response_text)
                            with st.expander("Show Justification"):
                                st.info(justification)

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response_text,
                                "justification": justification
                            })
                        else:
                            st.error(f"Error: {response.json().get('error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")

    with tab2:
        st.subheader("Test Your Comprehension")

        # Button to generate challenge questions
        if not st.session_state.challenge_questions:
            if st.button("🚀 Generate Challenge Questions"):
                with st.spinner("Generating questions..."):
                    try:
                        response = requests.get(f"{BACKEND_URL}/generate-challenge")
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.challenge_questions = data.get("challenge_questions", [])
                            st.session_state.challenge_results = {}
                            st.rerun()
                        else:
                            st.error(f"Error generating questions: {response.json().get('error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")

        if st.session_state.challenge_questions:
            for i, q_data in enumerate(st.session_state.challenge_questions):
                question = q_data["question"]
                source_context = q_data["source_context"]

                st.markdown(f"---")
                st.markdown(f"**Question {i+1}:** {question}")

                if i in st.session_state.challenge_results:
                    result = st.session_state.challenge_results[i]
                    st.info(f"Your Answer: {result['your_answer']}")
                    st.success(f"Feedback: {result['feedback']}")
                    with st.expander("See Expected Answer and Justification"):
                        st.write(f"**Expected Answer:** {result['expected_answer']}")
                        st.write(f"**Justification (Source Context):** {result['justification']}")
                else:
                    with st.form(key=f'challenge_form_{i}'):
                        user_answer = st.text_area("Your Answer:", key=f'user_answer_{i}')
                        submitted = st.form_submit_button("Submit Answer")

                        if submitted:
                            if not user_answer.strip():
                                st.warning("Please provide an answer.")
                            else:
                                with st.spinner("Evaluating your answer..."):
                                    payload = {
                                        "question": question,
                                        "source_context": source_context,
                                        "user_answer": user_answer
                                    }
                                    response = requests.post(f"{BACKEND_URL}/evaluate-challenge", json=payload)
                                    if response.status_code == 200:
                                        st.session_state.challenge_results[i] = response.json()
                                        st.rerun()
                                    else:
                                        st.error(f"Error evaluating answer: {response.json().get('error')}")
else:
    st.info("Please upload a document using the sidebar to get started.")
