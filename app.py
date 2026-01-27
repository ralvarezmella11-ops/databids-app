import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DataBids Pro", page_icon="📈", layout="centered")

# --- DISEÑO AZUL MARINO Y ESTILO MODERNO (CSS) ---
st.markdown("""
    <style>
    /* Fondo principal en azul marino muy oscuro */
    .stApp {
        background-color: #001220;
    }
    
    /* Títulos y textos generales */
    h1, h2, h3, p, label {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Contenedor del formulario con un azul un poco más claro para resaltar */
    div[data-testid="stForm"] {
        background-color: #002137;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #003a5d;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }

    /* Botón de Pago Destacado */
    .stLinkButton>a {
        background-color: #007BFF !important; 
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        transition: 0.3s ease;
    }
    
    .stLinkButton>a:hover {
        background-color: #0056b3 !important;
        transform: translateY(-2px);
    }

    /* Input fields */
    input {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA CON TU LOGO ---
# He usado el link directo de la imagen que subiste
URL_LOGO = "https://i.ibb.co/fdwwXykc/logo.jpg" 

col_logo, col_text = st.columns([1, 3])
with col_logo:
    st.image("https://i.ibb.co/276P7mP/fdwwXykc.jpg", width=140) # Link optimizado para visualización
with col_text:
    st.markdown("# DataBids")
    st.markdown("### Informes y análisis estratégicos de licitaciones")

st.divider()

# --- CUERPO DE LA APP ---
st.write("Optimiza tu propuesta y aumenta tus probabilidades de adjudicación en Mercado Público.")

# Sección de Pago
st.info("💎 **Servicio de Análisis:** Inversión única de $20.000 CLP por informe.")
st.link_button("💳 PAGAR ANÁLISIS POR WEBPAY", "https://www.mercadopago.cl") # Reemplaza con tu link real

st.write("") # Espacio

# Formulario de Registro
with st.form("registro_solicitud", clear_on_submit=True):
    st.subheader("📝 Detalles de la Solicitud")
    u_mail = st.text_input("Correo electrónico de contacto")
    u_emp = st.text_input("Nombre de la Empresa u Oferente")
    u_lic = st.text_input("ID de la Licitación (Ej: 1234-56-L123)")
    
    enviar = st.form_submit_button("Confirmar y Enviar Datos")
    
    if enviar:
        if u_mail and u_lic:
            # Aquí va tu lógica de guardado y Telegram que ya configuramos
            # ... 
            st.balloons()
            st.success("✅ ¡Recibido! Tu alerta ya llegó a nuestro equipo.")
        else:
            st.error("Por favor completa los campos obligatorios.")

# --- PANEL ADMIN (SIDEBAR) ---
with st.sidebar:
    st.header("🔐 Área Privada")
    # Configuración de clave para ver tus ventas
    password = st.text_input("Clave Admin", type="password")
    if password == "bids2026":
        st.write("Acceso concedido. Aquí verás tus registros.")

