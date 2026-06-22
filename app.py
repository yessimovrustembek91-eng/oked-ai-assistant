import os
import io
import pandas as pd
import streamlit as st
import sqlite3
import uuid
from datetime import datetime
from docx import Document
import google.generativeai as genai

# Настройка страницы
st.set_page_config(page_title="OKED Matrix Core", page_icon="🟢", layout="wide")

# [ЗДЕСЬ ОСТАВЬТЕ ВАШ CSS-БЛОК С МАТРИЦЕЙ БЕЗ ИЗМЕНЕНИЙ]
# (Скопируйте его из вашего предыдущего сообщения сюда)

# --- ОБЛАЧНАЯ КОНФИГУРАЦИЯ ---
# Убедитесь, что в Streamlit Secrets добавлен GEMINI_API_KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- ПУТИ К ФАЙЛАМ (ДЛЯ ОБЛАКА) ---
# Файлы должны лежать в корне репозитория рядом с app.py
EXCEL_PATH = "ОКЭД.XLSX"
RULES_PATH = "Правила методика oked-5_руссайт.docx"
AZA_PATH = "БАЗА ЗНАНИЙ 2026.docx"

# 2. Инициализация Базы Данных (остается прежней)
@st.cache_resource
def init_db():
    conn = sqlite3.connect('web_users_stats.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, timestamp TEXT, rating INTEGER, user_session TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS visitors (user_session TEXT PRIMARY KEY, first_seen TEXT)')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# --- ФУНКЦИИ (ОБНОВЛЕННЫЕ ДЛЯ GEMINI) ---
def get_knowledge_context(query):
    context = ""
    for path in [RULES_PATH, AZA_PATH]:
        if os.path.exists(path):
            doc = Document(path)
            context += "\n".join([p.text for p in doc.paragraphs if len(p.text) > 5])[:2500]
    return context

# --- ЛОГИКА ЗАПРОСА К МОДЕЛИ ---
# Внутри вашего блока, где раньше был клиент OpenAI, используйте:
def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# --- ОСТАЛЬНАЯ ЛОГИКА ---
# (Ваш код с вкладками, чатом и выводом результатов остается прежним)
# Просто замените вызов:
# resp = client.chat.completions.create(...)
# на:
# final_reply = ask_gemini(prompt)

# ВАЖНО: 
# 1. Загрузите файлы в GitHub (в корень репозитория).
# 2. Добавьте GEMINI_API_KEY в Secrets (Settings -> Secrets).
# 3. Добавьте google-generativeai в requirements.txt.
