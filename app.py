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
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VARIABLES ---
TELEGRAM_TOKEN = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
TELEGRAM_CHAT_ID = "7619400780"
ADMIN_PASSWORD = "bids2026"

# ==========================================
# 2. DISEÑO MINIMALISTA (CSS)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

    /* --- GLOBAL --- */
    .stApp {
        background-color: #F8FAFC; 
        font-family: 'Inter', sans-serif;
        color: #334155;
    }

    /* --- HEADER (Ajustado para no cortarse) --- */
    .header-bg {
        background: linear-gradient(to bottom, #FFFFFF, #F8FAFC);
        padding: 4rem 1rem 2rem 1rem;
        text-align: center;
        margin-top: -4rem; 
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-logo {
        font-size: 4rem;
        font-weight: 900;
        color: #0F172A;
        letter-spacing: -2px;
        line-height: 1.1;
    }
    .brand-dot { color: #0070F3; } 
    .brand-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        max-width: 600px;
        margin: 0.5rem auto 0 auto;
        font-weight: 500;
    }

    /* --- TARJETAS LIMPIAS (Sin Iconos) --- */
    .feature-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem; /* Menos padding para ser "justo y necesario" */
        height: 100%;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        transition: all 0.2s ease;
    }
    .feature-card:hover {
        border-color: #0070F3;
        transform: translateY(-2px);
    }
    
    /* Títulos en AZUL MARCA (#0070F3) */
    .card-title { 
        font-weight: 700; 
        font-size: 1.1rem; 
        margin-bottom: 0.5rem; 
        color: #0070F3; /* Cambio solicitado */
    }
    .card-text { 
        color: #475569; 
        font-size: 0.9rem; 
        line-height: 1.5; 
    }

    /* --- SECCIONES PRINCIPALES --- */
    .step-container { margin-top: 2rem; margin-bottom: 0.5rem; }
    .step-badge {
        color: #64748B;
        font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
    }
    .main-card {
        background: #FFFFFF; border-radius: 16px; padding: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #E2E8F0;
    }
    .section-title { font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem; }

    /* --- PRECIO --- */
    .price-box { 
        text-align: right; 
    }
    .price-big { font-size: 2.5rem; font-weight: 800; color: #0F172A; line-height: 1; }
    .price-currency { color: #0070F3; font-size: 1rem; font-weight: 700; }
    .price-sub { font-size: 0.8rem; color: #94A3B8; margin-top: 2px; }

    /* --- BOTONES E INPUTS --- */
    .stButton > button {
        background-color: #0070F3 !important;
        color: white !important; border: none !important;
        padding: 0.75rem 1.5rem !important; border-radius: 8px !important;
        font-weight: 600 !important;
        transition: background 0.2s !important;
    }
    .stButton > button:hover { background-color: #005bb5 !important; }
    
    .stTextInput input {
        background: #F8FAFC !important; border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important; padding: 0.75rem !important; color: #1E293B !important;
    }
    .stTextInput input:focus { border-color: #0070F3 !important; background: white !important; }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    div.block-container { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA
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
    msg = f"💎 *NUEVO CLIENTE*\n\n🏢 {company}\n🆔 `{id_lic}`\n📧 {mail}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# ==========================================
# 4. INTERFAZ
# ==========================================

# --- HEADER ---
st.markdown("""
    <div class="header-bg">
        <div class="brand-logo">DataBids<span class="brand-dot">.</span></div>
        <div class="brand-subtitle">Inteligencia de mercado para licitaciones públicas.</div>
    </div>
""", unsafe_allow_html=True)

# --- CARACTERÍSTICAS (Solo Texto) ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">Radiografía de Competencia</div>
            <div class="card-text">Analizamos los patrones de oferta históricos de tus rivales para ajustar tu precio.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">Probabilidad de Éxito</div>
            <div class="card-text">Modelo predictivo con 12 variables críticas para calcular tus chances reales.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">Entrega Express 24h</div>
            <div class="card-text">Informe ejecutivo en PDF listo para presentar a directorio en menos de un día.</div>
        </div>
        """, unsafe_allow_html=True)

# --- CONTENIDO CENTRAL ---
col_L, col_main, col_R = st.columns([1, 6, 1])

with col_main:
    # --- PASO 1 ---
    st.markdown('<div class="step-container"><span class="step-badge">01. Activación</span></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        cols_pay = st.columns([2, 1]) 
        with cols_pay[0]:
            st.markdown('<h2 class="section-title">Análisis Premium</h2>', unsafe_allow_html=True)
            st.write("Invierte en información, no en suerte.")
            st.link_button("💳 Pagar $20.000 (WebPay)", "https://www.mercadopago.cl")
        
        with cols_pay[1]:
            st.markdown("""
            <div class="price-box">
                <div><span class="price-big">20k</span> <span class="price-currency">CLP</span></div>
                <div class="price-sub">Pago único</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 2 ---
    st.markdown('<div class="step-container"><span class="step-badge">02. Datos</span></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Configuración</h2>', unsafe_allow_html=True)
        
        with st.form("main_form"):
            col_inp1, col_inp2 = st.columns(2)
            with col_inp1:
                u_mail = st.text_input("Tu Email", placeholder="correo@empresa.com")
            with col_inp2:
                u_emp = st.text_input("Tu Empresa", placeholder="Nombre Fantasía o Razón Social")
            
            u_lic = st.text_input("ID Licitación", placeholder="Ej: 5544-22-LE24")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 INICIAR ANÁLISIS")
            
            if submitted:
                if u_mail and u_emp and u_lic:
                    if save_order(u_mail, u_emp, u_lic):
                        notify_telegram(u_mail, u_emp, u_lic)
                        st.success("Solicitud recibida correctamente.")
                    else:
                        st.error("Error al guardar datos.")
                else:
                    st.warning("Completa todos los campos.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div style="text-align: center; color: #CBD5E1; margin-top: 3rem; font-size: 0.8rem;">DataBids Intelligence © 2026</div>', unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.markdown("### Admin")
    if st.text_input("Clave", type="password") == ADMIN_PASSWORD:
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button("Descargar CSV", csv, "ventas.csv", "text/csv")
