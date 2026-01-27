import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DataBids Pro", page_icon="📊", layout="centered")

# --- CSS: DISEÑO EMPRESARIAL LIMPIO ---
st.markdown("""
    <style>
    /* Fondo claro para profesionalismo */
    .stApp {
        background-color: #F8F9FA;
        color: #1A1A1A;
    }
    
    /* Tarjetas blancas con bordes redondeados */
    .main-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid #E9ECEF;
    }

    /* Títulos en Azul Marino */
    h1, h2, h3 {
        color: #002147 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }

    /* Botón de Pago Estilo Moderno */
    .stLinkButton > a {
        background: linear-gradient(90deg, #002147 0%, #003366 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        border: none !important;
        text-align: center;
        display: block;
        transition: 0.3s ease;
        text-decoration: none;
    }
    .stLinkButton > a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,33,71,0.3);
    }

    /* Estilo de los campos de texto */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #CED4DA !important;
    }

    /* Botón de envío del formulario */
    .stButton > button {
        background-color: #002147;
        color: white;
        border-radius: 12px;
        width: 100%;
        border: none;
        height: 3.5em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER: LOGO Y TÍTULO ---
# He insertado tu link directo aquí
URL_TU_LOGO = "https://i.postimg.cc/K8jf9Vr0/Gemini-Generated-Image-rsq4ghrsq4ghrsq4.png"

col1, col2 = st.columns([1, 4])
with col1:
    st.image(URL_TU_LOGO, width=120)
with col2:
    st.markdown("# DataBids")
    st.markdown("### Inteligencia Estratégica en Licitaciones")

st.divider()

# --- SECCIÓN DE VENTA ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("🎯 Optimiza tu oferta pública")
st.write("Analizamos la competencia y las bases administrativas para que tu propuesta sea la ganadora.")
st.write("**Servicio de Análisis Experto: $20.000 CLP**")
st.write("")
st.link_button("💳 CON
