# 🌐 Website-Based RAG Chatbot (Live Demo)

🚀 **Streamlit Cloud App:**  
👉 https://<(https://website-rag-chatbot-n2pyufbatadovrferm9hwe.streamlit.app/)>

---

## 📌 Project Overview

This project is a **Website-Based AI Chatbot** that answers user questions **strictly based on the content of a provided website URL**.

It uses **Retrieval-Augmented Generation (RAG)** to ensure:
- Answers are grounded only in the website data
- No hallucinated or external information is used
- Responses remain factual and verifiable

---

## 🧠 System Architecture (High-Level)

1. User provides a website URL  
2. Website content is extracted and cleaned  
3. Text is split into semantic chunks  
4. Chunks are converted into embeddings  
5. Embeddings are stored in a FAISS vector database  
6. Relevant chunks are retrieved for each query  
7. OpenAI LLM generates an answer using **only retrieved context**

---

## 🛠️ Tech Stack & Frameworks (With Justification)

### Frontend / UI — **Streamlit**
- Simple and fast UI development
- Ideal for rapid AI prototyping
- Native support for deployment on Streamlit Cloud

### AI Framework — **LangChain**
- Provides structured abstractions for:
  - Text splitting
  - Vector stores
  - Retrieval pipelines
- Well-suited for RAG-based applications

### LLM — **OpenAI GPT-3.5-Turbo**
- Stable and production-ready
- Strong instruction-following behavior
- Excellent at using provided context accurately
- Cost-effective compared to larger models

### Embeddings — **Sentence Transformers (all-MiniLM-L6-v2)**
- Lightweight and fast
- High-quality semantic representations
- Well-suited for similarity search tasks

### Vector Database — **FAISS**
- High-performance similarity search
- Lightweight and local-first
- No external service dependency
- Ideal for small to medium-scale projects

### Web Scraping — **BeautifulSoup**
- Reliable HTML parsing
- Effective for Wikipedia and general websites
- Allows controlled text extraction

### Programming Language — **Python**
- Strong ecosystem for AI/ML
- Excellent library support
- Clean and readable syntax

---

## 🤖 LLM Choice & Justification

**Model Used:** `gpt-3.5-turbo`

**Why this model?**
- Strong contextual grounding when used with RAG
- Reliable adherence to system instructions
- Low latency and stable outputs
- Suitable for production deployment
- Cost-efficient for iterative querying

The LLM is **never allowed to use external knowledge** — it answers only from retrieved website content.

---

## 📦 Vector Database Choice & Justification

**Vector Store:** FAISS

**Why FAISS?**
- Extremely fast similarity search
- Lightweight and easy to manage
- No cloud dependency
- Works well with local embedding persistence

Embeddings are **stored and reused**, not regenerated on every query.

---

## 🔍 Embedding & Retrieval Strategy

- Website content is split into overlapping semantic chunks
- Each chunk is embedded using `all-MiniLM-L6-v2`
- Metadata (source URL) is preserved
- High-recall retrieval (`top-k = 15`) is used
- Only retrieved chunks are sent to the LLM
- This ensures:
  - Better coverage
  - Reduced hallucination
  - Context-aware responses

---

## 💬 Short-Term Conversation Memory

- Maintains conversation context during a session
- Enables follow-up questions
- Memory is session-based (no long-term storage)
- Automatically resets when the session ends

---

## 🖥️ User Interface Experience

The Streamlit interface allows users to:
- Enter any public website URL
- Index the website content
- Ask questions via a simple chat input
- Receive grounded, factual answers
- Get clear feedback when answers are unavailable

---

## ▶️ Setup & Run Instructions (Local)

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/GreenCodr/website-rag-chatbot.git
cd website-rag-chatbot

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Environment Setup

Create a .env file:
OPENAI_API_KEY=your_openai_api_key_here

4️⃣ Run the App
streamlit run app.py


##☁️ Deployment
	•	Deployed using Streamlit Cloud
	•	Secure environment variable handling
	•	Publicly accessible live demo link
