import streamlit as st
import pandas as pd
import requests
import os
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN (Debe ser la primera línea) ---
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTIÓN DE ERRORES Y SECRETOS ---
def get_secret(section, key, default=None):
    """Obtiene secretos de forma segura sin romper la app si faltan."""
    try:
        if hasattr(st, 'secrets') and section in st.secrets:
            return st.secrets[section][key]
    except Exception:
        pass
    return default

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; color: #111827; }
    h1 { color: #0070F3 !important; font-weight: 800; font-size: 2.5rem !important; text-align: center; }
    .subtitle { text-align: center; color: #6B7280; font-size: 1.1rem; margin-bottom: 2rem; }
    .card { background: white; border: 1px solid #E5E7EB; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 1rem; }
    .stButton>button { background-color: #0070F3 !important; color: white !important; border-radius: 8px; width: 100%; font-weight: 600; }
    .stTextInput input { border-radius: 8px; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>




