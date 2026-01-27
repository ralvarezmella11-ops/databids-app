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
# Esta función evita que la app se rompa si no hay claves configuradas
def get_secret(section, key, default=None):
    try:
        # Intenta acceder a los secretos de forma segura
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
""", unsafe_allow_html=True)

# --- 4. LÓGICA ---
DATA_FILE = "ventas_databids.csv"

def save_data(email, company, lic_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data = pd.DataFrame([{
        "Fecha": timestamp, "Email": email, "Empresa": company, 
        "ID_Lic": lic_id, "Monto": 20000
    }])
    
    try:
        if os.path.exists(DATA_FILE):
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_data.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        st.error("❌ Error: Cierra el archivo Excel antes de guardar.")
        return False
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        return False

def send_telegram(email, company, lic_id):
    token = get_secret("telegram", "token")
    chat_id = get_secret("telegram", "chat_id")
    
    if not token or not chat_id:
        print("⚠️ Telegram no configurado (modo local)")
        return

    msg = f"🚀 NUEVA VENTA:\nEmpresa: {company}\nLic: {lic_id}\nEmail: {email}"
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",



