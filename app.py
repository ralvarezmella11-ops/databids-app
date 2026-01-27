import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN ESTRUCTURAL ---
st.set_page_config(
    page_title="DataBids Pro | Inteligencia Estratégica",
    page_icon="📈",
    layout="centered"
)

# --- CSS DE ALTA GAMA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Fondo y Tipografía */
    .stApp {
        background: linear-gradient(180deg, #001220 0%, #001F33 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Tarjetas Premium (Glassmorphism sutil) */
    .service-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }

    /* Botón de Pago: El foco del negocio */
    .stLinkButton > a {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        display: block;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 114, 255, 0.3);
    }

    .stLinkButton > a:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 114, 255, 0.5);
    }

    /* Inputs Elegantes */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        color: #fff !important;
        padding: 14px !important;
    }

    /* Títulos y Subtítulos */
    h1 { color: #FFFFFF; font-weight: 800; font-size: 3rem !important; letter-spacing: -1px; }
    .subtitle { color: #00C6FF; font-weight: 600; font-size: 1.2rem; margin-bottom: 2rem; }
    
    /* Footer y Menú */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NOTIFICACIÓN ---
def notify_telegram(email, empresa, id_lic):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    msg = f"💎 *NUEVA CONSULTORÍA SOLICITADA*\n\n🏢 *Empresa:* {empresa}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {email}\n💰 *Monto:* $20.000 CLP"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# --- INTERFAZ ---
# Header con Logo
st.image("https://i.ibb.co/276P7mP/fdwwXykc.jpg", width=160)
st.markdown("<h1>DataBids Insights</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Consultoría Estratégica en Mercado Público</p>', unsafe_allow_html=True)

# Sección de Venta
st.markdown('<div class="service-card">', unsafe_allow_html=True)
st.markdown("### 🎯 Maximiza tus posibilidades")
st.write("Analizamos datos históricos, competidores y bases administrativas para que tu oferta sea la ganadora.")
st.write("---")
st.write("✨ **¿Qué incluye?**")
st.write("• Análisis de precios de la competencia • Revisión de cumplimiento de bases • Reporte de factibilidad técnica.")
st.write("")
st.link_button("💳 CONTRATAR ANÁLISIS ($20.000 CLP)", "https://www.mercadopago.cl") # Pon tu link real aquí
st.markdown('</div>', unsafe_allow_html=True)

# Registro
st.markdown('<div class="service-card">', unsafe_allow_html=True)
st.markdown("#### 📝 Registro de Licitación")
st.caption("Completa los datos después de realizar el pago.")
with st.form("pro_form", clear_on_submit=True):
    mail = st.text_input("Correo electrónico corporativo")
    emp = st.text_input("Razón Social / Nombre")
    lic = st.text_input("ID de Licitación (Ej: 1234-56-L123)")
    
    btn = st.form_submit_button("


