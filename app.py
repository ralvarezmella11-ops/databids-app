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

# --- VARIABLES (Tus claves) ---
TELEGRAM_TOKEN = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
TELEGRAM_CHAT_ID = "7619400780"
ADMIN_PASSWORD = "bids2026"

# ==========================================
# 2. DISEÑO PREMIUM (CSS AVANZADO)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

    /* --- GLOBAL & FONDO --- */
    .stApp {
        background-color: #F1F5F9; /* Fondo general gris azulado sutil, menos duro que el blanco */
        font-family: 'Inter', sans-serif;
        color: #334155;
    }

    /* --- HEADER BRANDING --- */
    .header-bg {
        background: linear-gradient(to bottom, #FFFFFF, #F1F5F9);
        padding: 3rem 1rem 4rem 1rem;
        text-align: center;
        margin-top: -6rem; /* Truco para subirlo al tope */
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-logo {
        font-size: 4rem;
        font-weight: 900;
        color: #0F172A; /* Azul oscuro profundo */
        letter-spacing: -1.5px;
        line-height: 1;
    }
    .brand-dot { color: #0070F3; } /* El punto azul de la marca */
    .brand-subtitle {
        font-size: 1.25rem;
        color: #64748B;
        max-width: 650px;
        margin: 1rem auto 0 auto;
        font-weight: 500;
    }

    /* --- CARDS (Tarjetas) --- */
    .feature-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 2rem;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(255, 255, 255, 0); /* Borde transparente inicial */
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border-color: #BFDBFE; /* Borde azul sutil al pasar el mouse */
    }
    .icon-box {
        width: 56px; height: 56px;
        background: #EFF6FF; /* Azul muy claro */
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.75rem; color: #0070F3;
        margin-bottom: 1.25rem;
    }
    .card-title { font-weight: 700; font-size: 1.15rem; margin-bottom: 0.5rem; color: #0F172A; }
    .card-text { color: #475569; font-size: 0.95rem; line-height: 1.6; }

    /* --- SECCIONES PRINCIPALES --- */
    .step-container { margin-top: 3rem; }
    .step-badge {
        display: inline-flex; align-items: center;
        background: #DBEAFE; color: #1E40AF; /* Badges en azul marca */
        padding: 0.4rem 1rem; border-radius: 99px;
        font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 112, 243, 0.1);
    }
    .main-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 3.5rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
    }
    .section-title { font-size: 1.75rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem; }

    /* --- PRECIO --- */
    .price-box { text-align: right; background: #F8FAFC; padding: 1.5rem; border-radius: 16px; border: 1px solid #EDF2F7;}
    .price-big { font-size: 3.5rem; font-weight: 900; color: #0F172A; line-height: 1; }
    .price-currency { color: #0070F3; font-size: 1.5rem; font-weight: 700; }
    .price-sub { font-size: 0.9rem; color: #64748B; margin-top: 5px; font-weight: 500;}

    /* --- UI ELEMENTS --- */
    .stButton > button {
        background: linear-gradient(to bottom right, #0070F3, #0060DF) !important;
        color: white !important; border: none !important;
        padding: 0.85rem 1.5rem !important; border-radius: 12px !important;
        font-weight: 700 !important; font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(0, 112, 243, 0.3) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 6px 16px rgba(0, 112, 243, 0.4) !important; }
    .stTextInput input {
        background: #F8FAFC !important; border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important; padding: 1rem !important; color: #0F172A !important;
    }
    .stTextInput input:focus { border-color: #0070F3 !important; background: #FFFFFF !important; }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    div.block-container {padding-top: 0rem;} /* Sube todo el contenido */
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE NEGOCIO
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
    msg = f"💎 *NUEVO CLIENTE PREMIUM*\n\n🏢 *Empresa:* {company}\n🆔 *Lic:* `{id_lic}`\n📧 *Email:* {mail}\n💰 *Monto:* $20.000 CLP"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# ==========================================
# 4. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- HEADER BRANDING AREA ---
st.markdown("""
    <div class="header-bg">
        <div class="brand-logo">DataBids<span class="brand-dot">.</span></div>
        <div class="brand-subtitle">
            Inteligencia de mercado para licitaciones públicas. Toma decisiones basadas en datos, no en intuición.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FEATURES GRID ---
# Usamos un contenedor para centrar el grid si la pantalla es muy ancha
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🔎</div>
            <div class="card-title">Radiografía de Competencia</div>
            <div class="card-text">Analizamos los patrones de oferta históricos de tus rivales para que ajustes tu precio estratégicamente.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-box">🎯</div>
            <div class="card-title">Probabilidad de Éxito</div>
            <div class="card-text">Nuestro modelo predictivo evalúa 12 variables críticas de la licitación para calcular tus chances reales.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-box">⚡</div>
            <div class="card-title">Entrega Express 24h</div>
            <div class="card-text">Recibe un informe ejecutivo en PDF listo para presentar a directorio en menos de un día hábil.</div>
        </div>
        """, unsafe_allow_html=True)

# --- LAYOUT CENTRALIZADO PARA PASOS ---
# Usamos columnas vacías a los lados [1, 6, 1] para centrar el contenido principal
col_spacer_L, col_main, col_spacer_R = st.columns([1, 6, 1])

with col_main:
    # --- PASO 1: PAGO ---
    st.markdown('<div class="step-container"><span class="step-badge">Paso 1 / Activación</span></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        cols_pay = st.columns([1.8, 1]) # Proporción ajustada
        with cols_pay[0]:
            st.markdown('<h2 class="section-title">Invierte en Ventaja Competitiva</h2>', unsafe_allow_html=True)
            st.write("El costo de un mal precio es mucho mayor que el de este informe. Asegura tu participación con datos sólidos.")
            st.markdown("""
            <ul style="color: #475569; margin-top: 1.5rem; line-height: 2;">
                <li>✅ <b>Análisis profundo</b> de una (1) licitación específica.</li>
                <li>✅ <b>Soporte prioritario</b> vía email o WhatsApp.</li>
                <li>✅ <b>Garantía:</b> Si no encontramos datos relevantes, te reembolsamos.</li>
            </ul>
            <br>
            """, unsafe_allow_html=True)
            st.link_button("💳 Ir a Pago Seguro (WebPay/MercadoPago)", "https://www.mercadopago.cl")
        
        with cols_pay[1]:
            # Caja de precio destacada
            st.markdown("""
            <div class="price-box">
                <div><span class="price-big">20.000</span> <span class="price-currency">CLP</span></div>
                <div class="price-sub">Pago único · Facturable</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PASO 2: FORMULARIO ---
    st.markdown('<div class="step-container"><span class="step-badge">Paso 2 / Datos del Proyecto</span></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Configura tu Informe</h2>', unsafe_allow_html=True)
        st.write("Ingresa las coordenadas exactas de la licitación que deseas auditar.")
        
        with st.form("main_form"):
            st.markdown("<br>", unsafe_allow_html=True)
            col_inp1, col_inp2 = st.columns(2)
            with col_inp1:
                u_mail = st.text_input("Correo Electrónico de Entrega", placeholder="ej: reportes@tuempresa.cl")
            with col_inp2:
                u_emp = st.text_input("Nombre de tu Empresa / Razón Social", placeholder="ej: Constructora del Sur SpA")
            
            u_lic = st.text_input("ID de Licitación (Mercado Público)", placeholder="Ej: 5544-22-LE24 (Debe ser exacto)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            # El botón de submit se expandirá automáticamente por el CSS
            submitted = st.form_submit_button("🚀 CONFIRMAR Y GENERAR ANÁLISIS")
            
            if submitted:
                if u_mail and u_emp and u_lic:
                    # Validación simple de que el ID parece un ID de MP
                    if len(u_lic) > 5 and "-" in u_lic:
                        if save_order(u_mail, u_emp, u_lic):
                            notify_telegram(u_mail, u_emp, u_lic)
                            st.success("✅ ¡Operación exitosa! Tu solicitud ha entrado en nuestra cola de procesamiento. Recibirás una confirmación en tu correo.")
                            st.balloons()
                        else:
                            st.error("⚠️ Error de sistema: Por favor, asegúrate de que el archivo de base de datos no esté abierto en el servidor.")
                    else:
                        st.warning("⚠️ El ID de licitación no parece válido. Verifica el formato (Ej: 1234-56-AZ24).")
                else:
                    st.warning("⚠️ Todos los campos son obligatorios para iniciar el análisis.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Footer sutil
    st.markdown('<div style="text-align: center; color: #94A3B8; margin-top: 3rem; font-size: 0.9rem;">© 2024 DataBids Intelligence. Todos los derechos reservados.</div>', unsafe_allow_html=True)

# --- ADMIN PANEL (Sidebar Oculto) ---
with st.sidebar:
    st.markdown("### 🔐 Panel de Control")
    st.write("Acceso restringido a administradores.")
    if st.text_input("Clave de Acceso", type="password") == ADMIN_PASSWORD:
        st.success("Autenticado")
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            st.write(f"Total ventas: **{len(df)}**")
            st.dataframe(df, use_container_width=True)
            
            # Botón de descarga profesional
            csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="📥 Descargar Base de Datos Completa (CSV)",
                data=csv,
                file_name=f'databids_ventas_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )
        else:
            st.info("No hay transacciones registradas en el sistema.")


