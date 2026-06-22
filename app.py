import streamlit as st
import google.generativeai as genai

st.title("Тест бота")
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = st.text_input("Напиши что-нибудь:")
    if prompt:
        response = model.generate_content(prompt)
        st.write(response.text)
else:
    st.error("Ключ не найден!")
