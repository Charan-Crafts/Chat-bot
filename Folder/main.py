import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate


load_dotenv()
api_key = st.secrets["OPENROUTER_API_KEY"]
    

import streamlit as st

st.write()  # This will print available keys


model = ChatOpenAI(
    model="google/gemini-pro",
    # openai_api_base="https://openrouter.ai/api/v1",
    openai_api_base="https://openrouter.ai/api/v1/chat/completions",
    openai_api_key=st.secrets["OPENROUTER_API_KEY"],
    temperature=0
)

# Create a folder for uploaded PDF files
folder_name = "UserUploadedFiles"
os.makedirs(folder_name, exist_ok=True)


user_file = st.file_uploader("Upload PDF", type=["pdf"])
pdf_content = ""
if user_file:
    file_name = user_file.name
    store_file = os.path.join(folder_name, file_name)
    
    
    with open(store_file, 'wb') as f:
        f.write(user_file.getbuffer())
    
    st.success(f"✅ File '{file_name}' uploaded successfully!")

    
    loader = PyPDFLoader(store_file)
    documents = loader.load()
    
    
    pdf_content = "\n".join([doc.page_content for doc in documents])


prompt = PromptTemplate(
    template=(
        "Answer the following question based on the provided context:\n\n"
        "{context}\n\n"
        "Question:\n{question}\n"
    ),
    input_variables=["context", "question"]
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.header("AI Helper Chat")


user_input = st.chat_input("Enter your question...")

if user_input:
    
    formatted_prompt = prompt.format(context=pdf_content, question=user_input)
    
    
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    
    
    response = model.invoke(formatted_prompt)
    bot_response = response.content
    
    
    st.session_state.chat_history.append({"role": "bot", "message": bot_response})


for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["message"])
