import streamlit as st
import google.generativeai as genai

st.title("🟢 ИИ-Классификатор ОКЭД")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Ключ API не найден!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

user_input = st.text_area("ОПИШИТЕ ВАШУ ДЕЯТЕЛЬНОСТЬ:")

if st.button("КЛАССИФИЦИРОВАТЬ"):
    # ДОБАВЛЕНА ПРОВЕРКА НА ПУСТОТУ
    if user_input and user_input.strip() != "":
        with st.spinner("Анализ..."):
            try:
                # Отправляем запрос только если текст реально есть
                response = model.generate_content(f"Ты эксперт. Определи код ОКЭД для: {user_input}")
                st.write(response.text)
            except Exception as e:
                st.error(f"Ошибка API: {e}")
    else:
        st.warning("Пожалуйста, введите описание деятельности!")
