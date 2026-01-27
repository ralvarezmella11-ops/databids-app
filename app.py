import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN ESTRUCTURAL ---
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="centered"
)

# --- 2. UI/UX: ESTILO PREMIUM AZUL MARINO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Fondo y Tipografía Global */
    .stApp {
        background: linear-gradient(180deg, #050A18 0%, #0A1E32 100%);
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
    }

    /* Tarjetas de Información (Glassmorphism) */
    .st-emotion-cache-12w0qpk, .data-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }

    /* Botón de Pago: Gradiente de Acción */
    .stLinkButton > a {
        background: linear-gradient(90deg, #0070F3 0%, #00A3FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: transform 0.3s ease !important;
        display: block;
        text-align: center;
    }
    .stLinkButton > a:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 112, 243, 0.4);
    }

    /* Inputs Modernos */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Títulos e Identidad */
    h1 { font-weight: 800; color: #F8FAFC; letter-spacing: -1.5px; }
    h3 { color: #94A3B8; font-weight: 400; }
    
    /* Limpieza de interfaz Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE NEGOCIO (BACKEND) ---
def notify_telegram(mail, company, id_lic):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0" # Tu Token
    chat_id = "7619400780" # Tu ID
    msg = f"🚀 *NUEVA VENTA DATABIDS*\n\n🏢 *Empresa:* {company}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {mail}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

def save_data(mail, company, id_lic):
    db = "registro_ventas.csv"
    # CORRECCIÓN DE SINTAXIS: Se cierran correctamente los corchetes
    new_row = pd.DataFrame([[datetime.now().strftime("%d-%m-%Y %H:%M"), mail, company, id_lic, "PAGADO"]], 
                           columns=["Fecha", "Email", "Empresa", "ID_Licitacion", "Estado"])
    try:
        if os.path.exists(db):
            new_row.to_csv(db, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_row.to_csv(db, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        return False

# --- 4. INTERFAZ DE USUARIO ---
# Header con tu Logo
col_logo, col_vacia = st.columns([1, 2])
with col_logo:
    st.image("https://i.ibb.co/276P7mP/fdwwXykc.jpg", width=140) # Tu logo

st.markdown("<h1>DataBids</h1>", unsafe_allow_html=True)
st.markdown("<h3>Informes y análisis estratégicos de licitaciones</h3>", unsafe_allow_html=True)

# Sección de Pago
st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.write("#### 🎯 Maximiza tu probabilidad de adjudicación")
st.write("Análisis experto de competencia y cumplimiento de bases en 24 horas.")
st.write("")
st.link_button("💳 PAGAR ANÁLISIS ($20.000 CLP)", "https://www.mercadopago.cl") # Reemplaza con tu link real
st.markdown('</div>', unsafe_allow_html=True)

# Formulario de Envío
with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.write("#### 📝 Envío de Antecedentes")
    with st.form("main_form", clear_on_submit=True):
        email = st.text_input("Correo electrónico corporativo")
        empresa = st.text_input("Razón Social / Nombre")
        licitacion = st.text_input("ID de la Licitación (Ej: 1234-56-L123)")
        
        btn_enviar = st.form_submit_button("CONFIRMAR Y COMENZAR")
        
        if btn_enviar:
            if email and licitacion:
                if save_data(email, empresa, licitacion):
                    notify_telegram(email, empresa, licitacion)
                    st.balloons()
                    st.success("✅ Recibido. Te hemos notificado por Telegram y ya estamos trabajando.")
                else:
                    st.error("❌ El archivo Excel está abierto. Ciérralo para procesar el pedido.")
            else:
                st.warning("⚠️ El Correo y el ID son obligatorios para el informe.")
    st.markdown('</div>', unsafe_allow_html=True)

# Panel de Control (Admin)
with st.sidebar:
    st.title("🔐 Admin")
    if st.text_input("Acceso", type="password") == "bids2026": # Tu clave
        if os.path.exists("registro_ventas.csv"):
            df_admin = pd.read_csv("registro_ventas.csv", sep=';', encoding='utf-8-sig')
            st.dataframe(df_admin)
            st.download_button("📥 Descargar Excel", df_admin.to_csv(sep=';', index=False).encode('utf-8-sig'), "ventas.csv")



