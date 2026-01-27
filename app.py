import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DataBids | Consultoría Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DISEÑO EXPERTO (CSS CUSTOM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* Reset y Estilo Global */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }

    /* NOMBRE GIGANTE DATABIDS */
    .hero-title {
        color: #0070F3;
        font-weight: 900;
        font-size: 6rem !important; /* Tamaño monumental */
        text-align: center;
        margin-top: -3rem;
        margin-bottom: 0px;
        letter-spacing: -4px;
        animation: fadeIn 1.5s ease;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #111827;
        font-weight: 700;
        font-size: 2rem;
        margin-top: -10px;
        margin-bottom: 1rem;
    }

    .hero-description {
        text-align: center;
        color: #4B5563;
        font-size: 1.2rem;
        max-width: 850px;
        margin: 0 auto 4rem auto;
        line-height: 1.6;
    }

    /* Tarjetas de Contenido */
    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        transition: transform 0.3s ease;
    }

    /* Características (Features) */
    .feature-item {
        padding: 2rem;
        border-radius: 20px;
        background: #F8FAFC;
        border: 1px solid #F1F5F9;
        text-align: center;
        height: 100%;
    }
    .feature-title { font-weight: 700; font-size: 1.2rem; color: #0F172A; margin-bottom: 0.5rem; }
    .feature-text { color: #64748B; font-size: 1rem; }

    /* Botones de Acción */
    .stLinkButton > a, .stButton > button {
        background: #0070F3 !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(0, 118, 255, 0.39);
    }
    .stLinkButton > a:hover {
        background: #0061d5 !important;
        box-shadow: 0 6px 20px rgba(0, 118, 255, 0.23);
        transform: translateY(-2px);
    }

    /* Formulario */
    .stTextInput input {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1rem !important;
    }

    /* Limpieza UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND (LOGIC) ---
def send_telegram(mail, company, id_lic):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    msg = f"💎 *NUEVO PROYECTO DATABIDS*\n\n🏢 *Empresa:* {company}\n🆔 *ID:* {id_lic}\n📧 *Email:* {mail}"
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    except: pass

def save_to_csv(mail, company, id_lic):
    db_file = "ventas_databids.csv"
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), mail, company, id_lic, "20000"]], 
                             columns=["Fecha", "Email", "Empresa", "ID_Lic", "Monto"])
    if os.path.exists(db_file):
        new_entry.to_csv(db_file, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
    else:
        new_entry.to_csv(db_file, index=False, sep=';', encoding='utf-8-sig')

# --- INTERFAZ ---

# Hero Section
st.markdown('<h1 class="hero-title">DataBids</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Informes y análisis estratégicos de licitaciones</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-description">Potenciamos tu competitividad en Mercado Público mediante inteligencia de datos avanzada. Toma decisiones estratégicas basadas en hechos y maximiza tus tasas de adjudicación.</div>', unsafe_allow_html=True)

# Grid de Beneficios
b1, b2, b3 = st.columns(3, gap="large")
with b1:
    st.markdown('<div class="feature-item"><p class="feature-title">📊 Competencia</p><p class="feature-text">Descubre el comportamiento histórico y precios de tus rivales.</p></div>', unsafe_allow_html=True)
with b2:
    st.markdown('<div class="feature-item"><p class="feature-title">🛡️ Factibilidad</p><p class="feature-text">Análisis riguroso de cumplimiento para evitar descalificaciones.</p></div>', unsafe_allow_html=True)
with b3:
    st.markdown('<div class="feature-item"><p class="feature-title">⏱️ Rapidez</p><p class="feature-text">Informes ejecutivos entregados en menos de 24 horas hábiles.</p></div>', unsafe_allow_html=True)

st.write("")
st.write("")

# Área de Acción (Pago y Registro integrados)
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💳 Contratar Servicio")
    st.write("Inicia tu análisis estratégico de inmediato.")
    st.markdown("<h2 style='color:#111827;'>$20.000 <span style='font-size:1.2rem; color:#6B7280; font-weight:400;'>CLP</span></h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="color: #4B5563; margin-bottom: 20px;">
        ✓ Reporte PDF Detallado<br>
        ✓ Verificación de ID Mercado Público<br>
        ✓ Sugerencias de Oferta Económica
        </div>
    """, unsafe_allow_html=True)
    st.link_button("ACCEDER A PAGAR", "https://www.mercadopago.cl") # Link de pago
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Datos de Licitación")
    st.write("Completa los datos tras realizar tu transacción.")
    with st.form("form_final", clear_on_submit=True):
        email_input = st.text_input("Correo electrónico", placeholder="ejemplo@empresa.com")
        empresa_input = st.text_input("Razón Social", placeholder="Nombre de tu empresa")
        id_input = st.text_input("ID de Licitación", placeholder="Ej: 1234-56-LP24")
        
        btn_confirmar = st.form_submit_button("ENVIAR SOLICITUD")
        
        if btn_confirmar:
            if email_input and id_input:
                save_to_csv(email_input, empresa_input, id_input)
                send_telegram(email_input, empresa_input, id_input)
                st.balloons()
                st.success("✅ ¡Recibido! Tu analista experto ha sido notificado.")
            else:
                st.warning("⚠️ El Correo y el ID son obligatorios.")
    st.markdown('</div>', unsafe_allow_html=True)

# Admin Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Administración")
    if st.text_input("Clave de Acceso", type="password") == "bids2026":
        if os.path.exists("ventas_databids.csv"):
            st.write("Ventas Recientes:")
            st.dataframe(pd.read_csv("ventas_databids.csv", sep=';'))





