import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
def setup_professional_ui():
    st.set_page_config(page_title="DataBids | Consultoría", page_icon="📈", layout="centered")
    
    # CSS de Grado Industrial
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
        
        /* Base de la Aplicación */
        .stApp {
            background-color: #050A18; /* Azul Medianoche */
            font-family: 'Inter', sans-serif;
        }

        /* Contenedores de Información */
        .data-card {
            background-color: #0F172A;
            padding: 2.5rem;
            border-radius: 20px;
            border: 1px solid #1E293B;
            margin-bottom: 20px;
        }

        /* Botón de Pago Principal */
        .stLinkButton > a {
            background: #0070F3 !important; /* Azul Eléctrico */
            color: white !important;
            border-radius: 12px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 700 !important;
            text-align: center;
            display: block;
            border: none !important;
            transition: all 0.2s ease;
        }
        .stLinkButton > a:hover {
            background: #0056b3 !important;
            transform: scale(1.01);
        }

        /* Títulos y Tipografía */
        h1 { color: #F8FAFC; font-weight: 800; font-size: 2.5rem !important; }
        h3 { color: #94A3B8; font-weight: 400; font-size: 1.1rem !important; margin-bottom: 2rem; }
        label { color: #CBD5E1 !important; font-weight: 500 !important; }

        /* Inputs */
        .stTextInput input {
            background-color: #1E293B !important;
            color: white !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        /* Ocultar elementos innecesarios */
        #MainMenu, footer, header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND LOGIC ---
def notify_admin(mail, company, id_lic):
    # Tus credenciales verificadas
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    message = f"✅ *NUEVA SOLICITUD DATABIDS*\n\n🏢 *Empresa:* {company}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {mail}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

def save_to_database(mail, company, id_lic):
    file_path = "registros.csv"
    new_data = pd.DataFrame([[datetime.now().strftime("%d-%m-%Y %H:%M"), mail, company, id_lic


