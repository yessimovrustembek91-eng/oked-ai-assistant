import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI OKED Classifier", layout="centered")

# Получение ключа из Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API ключ не найден. Проверьте настройки Secrets в Streamlit Cloud.")
    st.stop()

st.title("AI-CLASSIFIER OKED")

model_choice = st.sidebar.selectbox("Модель", ["gemini-1.5-flash", "gemini-1.5-pro"])
model = genai.GenerativeModel(model_choice)

user_query = st.text_area("ОПИШИТЕ ВАШУ ДЕЯТЕЛЬНОСТЬ:")

if st.button("КЛАССИФИЦИРОВАТЬ"):
    if user_query:
        with st.spinner("Анализ..."):
            try:
                response = model.generate_content(f"Ты эксперт ОКЭД. Определи код для: {user_query}")
                st.success(response.text)
            except Exception as e:
                st.error(f"Ошибка при обращении к модели: {e}")
    else:
        st.warning("Введите описание деятельности.")
