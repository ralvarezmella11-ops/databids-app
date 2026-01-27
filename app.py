import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(
    page_title="DataBids | Inteligencia de Licitaciones",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VARIABLES (Aquí pones tus claves directamente) ---
TELEGRAM_TOKEN = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"  # Tu token
TELEGRAM_CHAT_ID = "7619400780"  # Tu ID
ADMIN_PASSWORD = "bids2026"

# ==========================================
# 2. DISEÑO PREMIUM (CSS AVANZADO)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* --- GLOBAL --- */
    .stApp {
        background-color: #F8FAFC; /* Gris muy suave, más profesional que blanco puro */
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* --- BRANDING HEADER --- */
    .brand-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
    }
    .brand-logo {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #0F172A, #0070F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 1.2rem;
        color: #64748B;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* --- CARDS (Tarjetas) --- */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        height: 100%;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #0070F3;
    }
    .icon-box {
        width: 50px;
        height: 50px;
        background: #EFF6FF;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: #0070F3;
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #0F172A;
    }
    .card-text {
        color: #64748B;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* --- SECTION CONTAINERS --- */
    .step-badge {
        display: inline-block;
        background: #0F172A;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 2rem;
    }

    /* --- PRICE TAG --- */
    .price-big {
        font-size: 3rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -1px;
    }
    .price-small {
        font-size: 1.25rem;
        color: #64748B;
        font-weight: 500;
    }

    /* --- BUTTONS & INPUTS --- */
    .stButton > button {
        background-color: #0070F3 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 112, 243, 0.2) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background-color: #005bb5 !important;
        transform: scale(1.02);
    }
    
    /* Inputs más bonitos */
    .stTextInput input {
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        color: #334155 !important;
    }
    .stTextInput input:focus {
        border-color: #0070F3 !important;
        box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1) !important;
    }

    /* Ocultar elementos default */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE NEGOCIO (Simple y Directa)
# ==========================================

def save_order(mail, company, id_lic):
    filename = "ventas_databids.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data = pd.DataFrame([[timestamp, mail, company, id_lic, "PAGADO", "20000"]], 
                            columns=["Fecha", "Email", "Empresa", "ID_Lic", "Estado", "Monto"])
    try:
        if os.path.exists(filename):
            new_data.to_csv(filename, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_data.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        return False

def notify_telegram(mail, company, id_lic):
    msg = f"🚀 *NUEVO CLIENTE DATABIDS*\n\n🏢 *Empresa:* {company}\n🆔 *Lic:* `{id_lic}`\n📧 *Email:* {mail}\n💰 *Monto:* $20.000"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# ==========================================
# 4. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- HERO SECTION ---
st.markdown("""
    <div class="brand-container">
        <div class="brand-logo">DataBids.</div>
        <div class="brand-subtitle">
            Inteligencia estratégica para licitaciones públicas. 
            Aumenta tu probabilidad de adjudicación con análisis de datos premium.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FEATURES SECTION ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-box">📊</div>
        <div class="card-title">Análisis Competitivo</div>
        <div class="card-text">Descubre los precios históricos y estrategias de tus competidores directos en licitaciones similares.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-box">🎯</div>
        <div class="card-title">Score de Probabilidad</div>
        <div class="card-text">Nuestro algoritmo calcula tus posibilidades reales de éxito basándose en 12 variables clave.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-box">📑</div>
        <div class="card-title">Reporte Ejecutivo</div>
        <div class="card-text">Recibe un PDF profesional con gráficos, insights y recomendaciones accionables en 24 horas.</div>
    </div>
    """, unsafe_allow_html=True)

st.write(" ") # Espacio
st.write(" ") 

# --- PASO 1: PAGO ---
col_layout = st.columns([1, 8, 1]) # Centrado
with col_layout[1]:
    st.markdown('<div class="step-badge">Paso 1: Pago Seguro</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        cols_pay = st.columns([2, 1])
        with cols_pay[0]:
            st.subheader("Acceso a DataBids Premium")
            st.write("Invierte en información, no en suerte.")
            st.markdown("""
            - ✅ **Informe completo en PDF**
            - ✅ **Factura deducible de impuestos**
            - ✅ **Soporte prioritario**
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("💳 Proceder al Pago (MercadoPago)", "https://www.mercadopago.cl")
        
        with cols_pay[1]:
            st.markdown("""
            <div style="text-align: right;">
                <div class="price-big">$20k</div>
                <div class="price-small">Pesos Chilenos</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 10px;">Pago Único</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: FORMULARIO ---
with col_layout[1]:
    st.markdown('<div class="step-badge">Paso 2: Datos del Proyecto</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("Configura tu Análisis")
        st.write("Ingresa los detalles de la licitación para iniciar el motor de inteligencia.")
        
        with st.form("main_form"):
            col_inp1, col_inp2 = st.columns(2)
            with col_inp1:
                u_mail = st.text_input("Correo Electrónico Corporativo", placeholder="ej: contacto@tuempresa.cl")
            with col_inp2:
                u_emp = st.text_input("Razón Social / Empresa", placeholder="ej: Constructora Global SpA")
            
            u_lic = st.text_input("ID de Licitación (Mercado Público)", placeholder="Ej: 5544-22-LE24")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 GENERAR INFORME ESTRATÉGICO")
            
            if submitted:
                if u_mail and u_emp and u_lic:
                    if save_order(u_mail, u_emp, u_lic):
                        notify_telegram(u_mail, u_emp, u_lic)
                        st.success("✅ ¡Excelente! Hemos recibido tu solicitud. Tu informe DataBids estará en tu correo en breve.")
                        st.balloons()
                    else:
                        st.error("❌ Error: Por favor cierra el archivo Excel si lo tienes abierto en el servidor.")
                else:
                    st.warning("⚠️ Por favor completa todos los campos para continuar.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN PANEL (Oculto) ---
with st.sidebar:
    st.markdown("### 🔒 DataBids Admin")
    if st.text_input("Access Key", type="password") == ADMIN_PASSWORD:
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            st.dataframe(df)
            csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
            st.download_button("📥 Descargar Base de Datos", csv, "ventas_databids.csv", "text/csv")
        else:
            st.info("No hay transacciones recientes.")

