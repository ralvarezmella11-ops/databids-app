import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DataBids Pro", page_icon="📊", layout="centered")

# --- CSS: DISEÑO LIMPIO Y PROFESIONAL ---
st.markdown("""
    <style>
    /* Fondo claro para máxima legibilidad */
    .stApp {
        background-color: #F8F9FA;
        color: #1A1A1A;
    }
    
    /* Tarjetas blancas con bordes redondeados y sombra suave */
    .main-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #E9ECEF;
    }

    /* Títulos en Azul Marino */
    h1, h2, h3 {
        color: #002147 !important; /* Azul Marino Corporativo */
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Botón de Pago: Azul Marino y Redondeado */
    .stLinkButton > a {
        background-color: #002147 !important;
        color: white !important;
        border-radius: 50px !important; /* Estilo píldora */
        padding: 12px 30px !important;
        font-weight: bold !important;
        border: none !important;
        text-align: center;
        display: block;
        transition: 0.3s;
    }
    .stLinkButton > a:hover {
        background-color: #003366 !important;
        transform: scale(1.02);
    }

    /* Botón de Formulario */
    .stButton > button {
        background-color: #002147;
        color: white;
        border-radius: 12px;
        width: 100%;
        border: none;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER: LOGO Y TÍTULO ---
# Intenta usar el link directo. Si no carga, mostrará el texto.
URL_DIRECTA_LOGO = "https://i.ibb.co/n8m6mGz/fdwwXykc.jpg" # Ajustado a formato directo

col1, col2 = st.columns([1, 4])
with col1:
    st.image(URL_DIRECTA_LOGO, width=100)
with col2:
    st.markdown("# DataBids")
    st.markdown("### Inteligencia Estratégica en Licitaciones")

st.divider()

# --- SECCIÓN DE VENTA ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("🎯 Asegura tu próxima adjudicación")
st.write("Analizamos tu competencia y optimizamos tu oferta para Mercado Público.")
st.write("**Inversión por informe: $20.000 CLP**")
st.write("")
st.link_button("💳 PAGAR ANÁLISIS AHORA", "https://www.mercadopago.cl")
st.markdown('</div>', unsafe_allow_html=True)

# --- FORMULARIO DE REGISTRO ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("📝 Registro de Solicitud")
with st.form("registro_final", clear_on_submit=True):
    u_mail = st.text_input("Tu Correo Electrónico")
    u_emp = st.text_input("Nombre de la Empresa")
    u_lic = st.text_input("ID de Licitación (Ej: 1234-56-L123)")
    
    enviar = st.form_submit_button("CONFIRMAR Y ENVIAR")
    
    if enviar:
        if u_mail and u_lic:
            # Lógica de Telegram y Guardado (Reemplaza con tus IDs)
            token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
            chat_id = "7619400780"
            msg = f"🚀 NUEVA VENTA: {u_emp}\nID: {u_lic}\nMail: {u_mail}"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg})
            
            st.balloons()
            st.success("✅ ¡Recibido! Te contactaremos en menos de 24 horas.")
        else:
            st.warning("⚠️ Por favor completa el correo y el ID.")
st.markdown('</div>', unsafe_allow_html=True)
