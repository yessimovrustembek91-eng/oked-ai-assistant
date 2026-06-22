import streamlit as st
import google.generativeai as genai

# Настройка страницы
st.set_page_config(page_title="OKED Expert System 2.0", page_icon="📊", layout="centered")

# Настройки в боковой панели
with st.sidebar:
    st.header("⚙️ Конфигурация")
    model_name = st.selectbox("Выбор модели", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.markdown("---")
    st.write("**Автор:** Есимов Р.")
    st.write("**Организация:** Бюро национальной статистики РК")

# Заголовок
st.title("📊 OKED Expert System 2.0")

# Таблоиды
col1, col2, col3 = st.columns(3)
col1.metric("Статус", "Online")
col2.metric("Версия", "2.0")
col3.metric("База", "2026")

st.divider()

# Логика классификации
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name)

user_query = st.text_area("Введите описание деятельности:", height=100, 
                         placeholder="Пример: Розничная торговля запчастями для сельхозтехники...")

if st.button("Классифицировать"):
    if user_query:
        with st.spinner('Идет анализ по классификатору...'):
            try:
                # Четкий промт для классификатора
                prompt = f"""
                Ты — профессиональный эксперт Бюро национальной статистики РК.
                Твоя задача: на основе описания деятельности подобрать наиболее точный код ОКЭД.
                
                Формат ответа:
                1. Код ОКЭД (номер и название).
                2. Обоснование выбора (кратко).
                3. Два уточняющих вопроса для проверки полноты данных.
                
                Описание деятельности: {user_query}
                """
                response = model.generate_content(prompt)
                st.subheader("Результат классификации")
                st.success(response.text)
            except Exception as e:
                st.error(f"Ошибка системы: {e}")
    else:
        st.warning("Введите описание для начала работы.")

st.markdown("---")
st.caption("Разработано: Есимов Р. | Бюро национальной статистики РК © 2026")
