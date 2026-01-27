import streamlit as st
import requests
from datetime import datetime
import os

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
st.set_page_config(
    page_title="DataBids Pro",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================
# VARIABLES SEGURAS
# ==============================
TELEGRAM_TOKEN = os.getenv("TG_TOKEN", "PEGA_AQUI_TU_TOKEN")
TELEGRAM_CHAT = os.getenv("TG_CHAT", "PEGA_AQUI_TU_CHAT")

LOGO_URL = "https://i.postimg.cc/K8jf9Vr0/Gemini-Generated-Image-rsq4ghrsq4ghrsq4.png"

# ==============================
# ESTILOS CORPORATIVOS
# ==============================
st.markdown("""
<style>
    .stApp {
        background: #F4F6F9;
        color: #1F2937;
        font-family: 'Inter', sans-serif;
    }

    .card {
        background: white;
        padding: 32px;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0,0,0,.05);
        margin-bottom: 28px;
        border: 1px solid #E5E7EB;
    }

    h1, h2, h3 {
        color: #0F172A;
        font-weight: 800;
    }

    .stTextInput input {
        border-radius: 12px;
        padding: 10px;
    }

    .stButton button {
        background: linear-gradi


