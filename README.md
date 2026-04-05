# 📚 Local RAG Study Agent

A locally hosted AI study assistant built with Python. It uses Retrieval-Augmented Generation (RAG) to answer questions based strictly on uploaded PDF textbooks, rather than general internet knowledge.

## 🛠️ Architecture & Tech Stack
* **Frontend:** Streamlit
* **Document Processing:** LangChain (`PyPDFLoader`, `RecursiveCharacterTextSplitter`)
* **Vector Database:** FAISS (Local storage)
* **AI Brain:** Google Gemini 2.5 Flash & Gemini Embeddings

## 🚀 How It Works
1. The app slices large PDF textbooks into small text chunks.
2. It converts those chunks into vector embeddings and stores them locally in FAISS.
3. When a user asks a question, a `RetrievalQA` chain searches the local database and forces the AI to cite specific textbook authors and formulas.

## 💻 How to Run Locally
1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and add your own Google API Key.
4. Run the app: `streamlit run app.py`