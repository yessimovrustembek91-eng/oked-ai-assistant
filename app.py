import streamlit as st
import pandas as pd
from openai import OpenAI
from docx import Document
import os

# Подключение к Gemini через API
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"], 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.set_page_config(page_title="OKED Expert 2.0", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("ОКЭД.XLSX", dtype=str)

def get_context():
    text = ""
    # Читаем все ваши документы для контекста
    for file in ["Национальный классификатор oked-5_руссайт.docx", "БАЗА ЗНАНИЙ 2026.docx", "Методика_ru.docx"]:
        if os.path.exists(file):
            doc = Document(file)
            text += "\n".join([p.text for p in doc.paragraphs])
    return text[:8000] 

df = load_data()

st.title("🟢 OKED Expert System 2.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Введите вид деятельности..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        matches = df[df.apply(lambda row: prompt.lower() in str(row).lower(), axis=1)].head(5)
        context = get_context()
        
        full_prompt = f"Контекст методологии: {context}\n\nНайденные коды: {matches.to_string()}\n\nЗапрос: {prompt}"
        
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "system", "content": "Ты эксперт ОКЭД РК. Отвечай кратко, обоснованно, в конце задавай 2 уточняющих вопроса."},
                      {"role": "user", "content": full_prompt}]
        )
        
        reply = response.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})