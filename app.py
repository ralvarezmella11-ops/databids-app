import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN DE NIVEL PROFESIONAL ---
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="centered"
)

# --- CSS: DISEÑO PREMIUM "NAVY & CIAN" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fondo y Fuente Global */
    .stApp {
        background: radial-gradient(circle at top, #0A192F 0%, #020617 100%);
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
    }

    /* Tarjetas Blancas/Translúcidas para Contraste */
    .st-emotion-cache-12w0qpk, .css-1r6slb0, .data-card {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* Títulos y Encabezados */
    h1 { color: #F8FAFC; font-weight: 900; font-size: 3rem !important; letter-spacing: -2px; }
    h3 { color: #38BDF8; font-weight: 400; letter-spacing: 1px; }
    
    /* Botón de Pago (Call to Action) */
    .stLinkButton > a {
        background: linear-gradient(90deg, #0284C7 0%, #0EA5E9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        transition: all 0.4s ease !important;
        text-align: center;
        display: block;
        box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.4);
    }
    .stLinkButton > a:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(14, 165, 233, 0.5);
    }

    /* Campos de Entrada */
    input {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    /* Ocultar elementos de marca Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NOTIFICACIÓN (BACKEND) ---
def notify_telegram(mail, company, id_lic):
    # Tus credenciales exactas
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    
    mensaje = f"🚀 *NUEVA ORDEN DATABIDS*\n\n🏢 *Empresa:* {company}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {mail}\n💰 *Monto:* $20.000 CLP"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        requests.post(url, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

def save_order(mail, company, id_lic):
    filename = "ventas_databids.csv"
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    new_data = pd.DataFrame([[timestamp, mail, company, id_lic, "PAGADO", "20000"]], 
                            columns=["Fecha", "Email", "Empresa", "ID_Lic", "Estado", "Monto"])
    try:
        if os.path.exists(filename):
            new_data.to_csv(filename, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_data.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        return False

# --- ESTRUCTURA DE LA INTERFAZ (UI) ---

# Header: Logo y Título
col_l, col_r = st.columns([1, 3])
with col_l:
    st.image("https://i.postimg.cc/K8jf9Vr0/Gemini-Generated-Image-rsq4ghrsq4ghrsq4.png", width=140)
with col_r:
    st.markdown("<h1>DataBids</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Informes y análisis estratégicos de licitaciones</h3>", unsafe_allow_html=True)

st.write("")

# Tarjeta de Producto
with st.container():
    st.markdown('<div class


