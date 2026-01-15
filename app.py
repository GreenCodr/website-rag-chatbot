import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from openai import OpenAI

# ===============================
# Setup
# ===============================
load_dotenv()
client = OpenAI()

FAISS_PATH = "faiss_index"

st.set_page_config(page_title="Website RAG Chatbot", layout="wide")
st.title("🌐 Website-Based AI Chatbot")
st.write("Ask questions strictly based on the provided website.")

url = st.text_input("Enter Website URL")

# ===============================
# Session Memory Init
# ===============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===============================
# Website Extraction
# ===============================
def extract_website_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    text = "\n".join(
        p.get_text().strip()
        for p in paragraphs
        if p.get_text().strip()
    )
    return text

# ===============================
# Chunking
# ===============================
def create_documents(text: str, source: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=120
    )
    chunks = splitter.split_text(text)
    return [
        Document(page_content=chunk, metadata={"source": source})
        for chunk in chunks
    ]

# ===============================
# Vector Store (Persistent)
# ===============================
def build_or_load_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(FAISS_PATH):
        return FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(FAISS_PATH)
    return vector_store

# ===============================
# Index Website
# ===============================
if st.button("Index Website"):
    if not url:
        st.warning("Please enter a website URL.")
    else:
        with st.spinner("Indexing website..."):
            try:
                text = extract_website_text(url)
                docs = create_documents(text, url)

                st.session_state["vector_store"] = build_or_load_vector_store(docs)
                st.session_state.chat_history = []  # reset memory on new site

                st.success(f"Website indexed successfully! Total chunks: {len(docs)}")
            except Exception as e:
                st.error(f"Indexing failed: {e}")

# ===============================
# Question Answering
# ===============================
st.divider()
st.subheader("💬 Ask a question")

question = st.text_input("Your question")

if question:
    if "vector_store" not in st.session_state:
        st.warning("Please index a website first.")
        st.stop()

    retriever = st.session_state["vector_store"].as_retriever(
        search_kwargs={"k": 15}
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Build short-term memory context (last 2 Q&A)
    history_text = ""
    for msg in st.session_state.chat_history[-4:]:
        history_text += f"{msg['role'].capitalize()}: {msg['content']}\n"

    prompt = f"""
You are a factual assistant.

Conversation so far:
{history_text}

Answer the question using ONLY the context below.
You may synthesize information across multiple parts of the context.

If the answer is not present in the context, respond exactly with:
"The answer is not available on the provided website."

Context:
{context}

Question:
{question}

Answer:
"""

    with st.spinner("Generating answer..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Use only the provided context. Do not use outside knowledge."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    answer = response.choices[0].message.content.strip()

    # Store memory
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )
    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    st.markdown("### 🤖 Answer")
    st.write(answer)