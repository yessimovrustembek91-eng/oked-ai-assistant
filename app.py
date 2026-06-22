import streamlit as st
import google.generativeai as genai

# Настройка
st.set_page_config(page_title="AI OKED Classifier", layout="centered")

# CSS для темной темы и "космического" стиля
st.markdown("""
    <style>
    .stApp { background-color: #050508; }
    h1 { color: #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI-CLASSIFIER OKED")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# ВАЖНО: используем f"models/{model_choice}"
model_choice = st.sidebar.selectbox("Модель", ["gemini-1.5-flash", "gemini-1.5-pro"])
model = genai.GenerativeModel(f"models/{model_choice}")

user_query = st.text_area("ОПИШИТЕ ВАШУ ДЕЯТЕЛЬНОСТЬ:")

if st.button("КЛАССИФИЦИРОВАТЬ"):
    if user_query:
        response = model.generate_content(f"Ты эксперт ОКЭД. Определи код для: {user_query}")
        st.success(response.text)
