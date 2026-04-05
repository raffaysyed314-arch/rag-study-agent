import streamlit as st
import os
from dotenv import load_dotenv
from utils import process_pdf, get_chat_chain

load_dotenv(override=True)

st.set_page_config(page_title="6th Sem Assistant", layout="wide")
st.title("📚 Study Agent: Chat with your Textbooks")

if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"]:
    st.error("⚠️ Please set your GOOGLE_API_KEY in the .env file!")
    st.stop()

if "chain" not in st.session_state:
    st.session_state.chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Upload Center")
    uploaded_file = st.file_uploader("Upload your PDF textbook", type="pdf")
    
    if st.button("Process Document") and uploaded_file:
        with st.spinner("Analyzing and building Vector Memory..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            vector_store = process_pdf("temp.pdf")
            st.session_state.chain = get_chat_chain(vector_store)
            st.session_state.chat_history = [] # Wipe UI history on new upload
            st.success("✅ Ready! Ask me anything.")

if st.session_state.chain:
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    user_input = st.chat_input("Ask a question about your textbook...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("Thinking..."):
            # THE FIX: Updated the dictionary keys to match RetrievalQA
            response = st.session_state.chain.invoke({"query": user_input})
            answer = response["result"] 
        
        with st.chat_message("assistant"):
            st.write(answer)
            
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", answer))
else:
    st.info("👈 Upload a PDF in the sidebar and click 'Process Document' to start.")