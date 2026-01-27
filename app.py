import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN PROFESIONAL ---
st.set_page_config(
    page_title="DataBids Pro | Consultoría",
    page_icon="📊",
    layout="centered"
)

# --- CSS: MÁXIMO CONTRASTE Y LEGIBILIDAD ---
st.markdown("""
    <style>
    /* Fondo Azul Marino Profundo */
    .stApp {
        background-color: #010B14;
        color: #FFFFFF;
    }

    /* Tarjetas de Contenido (Legibilidad Garantizada) */
    .st-emotion-cache-12w0qpk, .data-card {
        background-color: #0A192F !important;
        border: 1px solid #1E293B !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        margin-bottom: 20px;
    }

    /* Textos en Blanco Puro */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* Botón de Pago Estilo "Premium" */
    .stLinkButton > a {
        background: linear-gradient(90deg, #0072FF 0%, #00C6FF 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem !important;
        font-weight: 800 !important;
        text-align: center;
        display: block;
        transition: 0.3s;
        text-decoration: none;
    }
    .stLinkButton > a:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 198, 255, 0.4);
    }

    /* Botón de Envío Verde Éxito */
    .stButton > button {
        background-color: #22C55E !important;
        color: white !important;
        border-radius: 12px !important;
        width: 100%;
        height: 3.5em;
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND: FUNCIONES DE SEGURIDAD ---
def enviar_alerta(mail, empresa, licitacion):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    msg = f"🚀 *NUEVA ORDEN*\n\n🏢 {empresa}\n🆔 {licitacion}\n📧 {mail}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        st.warning("⚠️ Alerta: Los datos se guardaron, pero no se pudo enviar el mensaje a Telegram.")

def registrar_venta(mail, empresa, licitacion):
    archivo = "ventas_databids.csv"
    nuevo_dato = pd.DataFrame({
        "Fecha": [datetime.now().strftime("%d-%m-%Y %H:%M")],
        "Email": [mail],
        "Empresa": [empresa],
        "ID_Lic": [licitacion]
    })
    try:
        if os.path.exists(archivo):
            nuevo_dato.to_csv(archivo, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            nuevo_dato.to_csv(archivo, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        st.error("❌ El archivo Excel está abierto en otro programa. Ciérralo y reintenta.")
        return False

# --- FRONTEND: INTERFAZ DE USUARIO ---
# Header
col_logo, col_tit = st.columns([1, 3])
with col_logo:
    st.image("https://i.postimg.cc/K8jf9Vr0/Gemini-Generated-Image-rsq4ghrsq4ghrsq4.png", width=130)
with col_tit:
    st.markdown("# DataBids")
    st.markdown("### Consultoría Estratégica Digital")

st.write("---")

# Sección de Pago
st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.subheader("💎 Informe de Factibilidad")
st.write("Análisis profundo de competencia


