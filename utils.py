import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

# THE FIX: Ripping out the buggy Conversational chain for the stable RetrievalQA
from langchain_classic.chains import RetrievalQA 

load_dotenv(override=True)

def process_pdf(pdf_path: str):
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Using the embedding model that worked for you
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        return vector_store
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise

def get_chat_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # THE FIX: Direct chain. No secondary condensing calls.
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    return chain