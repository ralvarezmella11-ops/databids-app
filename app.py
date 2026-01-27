import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DataBids Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: DISEÑO MINIMALISTA Y PROFESIONAL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Fondo y Tipografía */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }

    /* NOMBRE GIGANTE DATABIDS */
    .brand-title {
        color: #0070F3;
        font-weight: 900;
        font-size: 5rem !important;
        text-align: center;
        margin-top: -2rem;
        margin-bottom: 0px;
        letter-spacing: -3px;
    }
    
    .main-subtitle {
        text-align: center;
        color: #111827;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }

    .description {
        text-align: center;
        color: #4B5563;
        font-size: 1.15rem;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.6;
    }

    /* Tarjetas de Contenedores */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    /* Características */
    .feature-box {
        padding: 1.5rem;
        border-radius: 16px;
        background: #F9FAFB;
        border: 1px solid #F3F4F6;
        height: 100%;
    }
    .feature-title { font-weight: 700; color: #111827; margin-bottom: 0.5rem; }
    .feature-text { color: #4B5563; font-size: 0.95rem; }

    /* Botones y Inputs */
    .stLinkButton > a, .stButton > button {
        background-color: #0070F3 !important;





