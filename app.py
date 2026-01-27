import streamlit as st
import pandas as pd
import requests
import os
import re
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================

# Configuración de la página (Debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CLASE DE CONFIGURACIÓN SEGURA ---
class Config:
    """Maneja las configuraciones y secretos de forma segura."""
    # PRECIO
    PRICE = 20000
    
    # NOMBRE DEL ARCHIVO DE DATOS
    DATA_FILE = "ventas_databids.csv"

    @staticmethod
    def get_telegram_creds():
        """
        Intenta obtener credenciales de st.secrets.
        Si no existen, devuelve None para evitar crasheos.
        """
        try:
            return st.secrets["telegram"]["token"], st.secrets["telegram"]["chat_id"]
        except (FileNotFoundError, KeyError):
            return None, None

    @staticmethod
    def get_admin_password():
        """Obtiene pass de admin o usa uno por defecto inseguro si no hay config."""
        try:
            return st.secrets["admin"]["password"]
        except (FileNotFoundError, KeyError):
            return "bids2026"  # Contraseña de respaldo (solo para desarrollo)

# ==========================================
# 2. ESTILOS CSS (DISEÑO)
# ==========================================
CUSTOM_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; color: #111827; }
    
    /* Títulos */
    h1 { color: #0070F3 !important; font-weight: 800; font-size: 2.5rem !important; text-align: center; }
    .subtitle { text-align: center; color: #4B5563; font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem auto; }
    
    /* Tarjetas */
    .feature-card, .section-card {
        background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); padding: 2rem;
    }
    .section-card { padding: 2.5rem; margin-top: 1rem; }
    
    /* Elementos */
    .feature-icon { color: #0070F3; font-size: 1.5rem; margin-bottom: 1rem; }
    .feature-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .feature-desc { color: #4B5563; font-size: 0.95rem; }
    .step-header { font-weight: 700; color: #4B5563; margin-top: 3rem; margin-bottom: 0.5rem; text-transform: uppercase; font-size: 0.85rem;}
    .price-tag { font-size: 2.5rem; font-weight: 800; color: #111827; }
    
    /* Botones y Inputs */
    div.stButton > button, div.stLinkButton > a {
        background-color: #0070F3 !important; color: white !important; border: none !important;
        border-radius: 12px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important;
        width: 100%; transition: all 0.2s ease;
    }
    div.stButton > button:hover, div.stLinkButton > a:hover {
        background-color: #005bb5 !important; transform: translateY(-1px);
    }
    .stTextInput input { border: 1px solid #D1D5DB !important; border-radius: 8px !important; }
    
    /* Ocultar interfzas Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
"""

# ==========================================
# 3. LÓGICA DE NEGOCIO (BACKEND)
# ==========================================
class BusinessLogic:
    def __init__(self):
        self.file_path = Config.DATA_FILE
        self._init_db()

    def _init_db(self):
        """Crea el CSV si no existe."""
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["Fecha", "Email", "Empresa", "ID_Lic", "Estado", "Monto"])
            df.to_csv(self.file_path, sep=';', index=False, encoding='utf-8-sig')

    def validate_email(self, email):
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

    def register_order(self, email, company, lic_id):
        """Guarda la orden en el CSV."""
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        new_row = pd.DataFrame([{
            "Fecha": timestamp, "Email": email, "Empresa": company, 
            "ID_Lic": lic_id, "Estado": "SOLICITADO", "Monto": Config.PRICE
        }])
        try:
            new_row.to_csv(self.file_path, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
            return True
        except Exception as e:
            st.error(f"Error guardando datos: {e}")
            return False

    def send_notification(self, email, company, lic_id):
        """Envía notificación a Telegram si las credenciales existen."""
        token, chat_id = Config.get_telegram_creds()
        
        if not token or not chat_id:
            # Si no hay tokens, no hacemos nada (o imprimimos en consola local)
            print("⚠️ Telegram no configurado. Notificación saltada.")
            return

        msg = (f"🚀 *NUEVA ORDEN*\n\n🏢 *Empresa:* {company}\n"
               f"🆔 *Lic:* `{lic_





