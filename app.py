import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: REPLICANDO EL DISEÑO REPLIT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Fondo y Tipografía General */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        color: #111827;
    }

    /* Título Principal */
    h1 {
        color: #0070F3 !important;
        font-weight: 800;
        font-size: 3rem !important;
        text-align: center;
        line-height: 1.2;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #4B5563;
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0 auto 2rem auto;
    }

    /* Tarjetas de Características */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 2rem;
        text-align: left;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    .feature-icon {
        color: #0070F3;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #4B5563;
        font-size: 0.95rem;
    }

    /* Secciones de Pasos */
    .step-header {
        font-weight: 700;
        color: #4B5563;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }

    /* Precio y Beneficios */
    .price-tag {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
    }
    .price-currency {
        font-size: 1.5rem;
        color: #4B5563;
    }
    .benefit-list {
        list-style: none;
        padding: 0;
        color: #4B5563;
    }
    .benefit-list li {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    .benefit-list li::before {
        content: "•";
        color: #0070F3;
        font-weight: bold;
        margin-right: 0.5rem;
    }

    /* Botones Azules */
    .stLinkButton > a, .stButton > button {
        background-color: #0070F3 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100%;
        text-align: center;
        transition: background-color 0.2s;
    }
    .stLinkButton > a:hover, .stButton > button:hover {
        background-color: #005bb5 !important;
    }
    .stLinkButton > a { display: block; text-decoration: none; }

    /* Inputs del Formulario */
    .stTextInput input {
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        color: #111827 !important;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE BACKEND (Telegram y CSV) ---
def notify_telegram(mail, company, id_lic):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0" # Tu Token
    chat_id = "7619400780" # Tu ID
    msg = f"🚀 *NUEVA ORDEN*\n\n🏢 *Empresa:* {company}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {mail}\n💰 *Monto:* $20.000 CLP"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

def save_order(mail, company, id_lic):
    filename = "ventas_databids.csv"
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
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

# --- INTERFAZ PRINCIPAL ---

# Título y Subtítulo
st.markdown("<h1>Informes y análisis estratégicos de licitaciones</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Bienvenido. Optimiza tu participación en Mercado Público con nuestra inteligencia de datos. Toma decisiones informadas y aumenta tus probabilidades de éxito.</p>', unsafe_allow_html=True)

# Banner de Servicio Premium
st.info("💡 **Servicio Premium:** Análisis completo de competencia y factibilidad por solo **$20.000 CLP**.")

# --- SECCIÓN DE CARACTERÍSTICAS (3 Columnas) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Análisis de Competencia</div>
            <div class="feature-desc">Identificamos a tus principales competidores y sus estrategias de precios históricos.</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Evaluación de Riesgo</div>
            <div class="feature-desc">Calculamos la probabilidad de adjudicación basada en variables clave de la licitación.</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Reportes Detallados</div>
            <div class="feature-desc">Recibe un informe PDF completo con gráficos y recomendaciones accionables.</div>
        </div>
    """, unsafe_allow_html=True)

# --- PASO 1: PAGO ---
st.markdown('<div class="step-header">1 PASO INICIAL</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Realiza tu pago")
        st.write("Procesamos los pagos de manera segura a través de WebPay.")
        st.write("Costo del servicio")
        st.markdown("""
            <ul class="benefit-list">
                <li>Pago único por licitación</li>
                <li>Boleta o factura disponible</li>
                <li>Garantía de satisfacción</li>
            </ul>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="text-align: right;"><span class="price-tag">$20.000</span> <span class="price-currency">CLP</span></div>', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/6963/6963703.png", width=80) # Icono de tarjeta
        
    st.write("")
    st.link_button("💳 PAGAR ANÁLISIS", "https://www.mercadopago.cl") # Reemplaza con tu link real
    st.markdown('</div>', unsafe_allow_html=True)

# --- PASO 2: REGISTRO ---
st.markdown('<div class="step-header">2 PASO FINAL</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Registra la Licitación")
    st.write("Ingresa los datos para que nuestro sistema genere tu reporte.")
    
    with st.form("registro_form"):
        u_mail = st.text_input("Tu Correo", placeholder="nombre@empresa.com")
        u_emp = st.text_input("Empresa / Nombre", placeholder="Tu Empresa SpA")
        u_lic = st.text_input("ID de la Licitación", placeholder="Ej: 1234-56-LE24")
        
        submitted = st.form_submit_button("Confirmar Solicitud")
        
        if submitted:
            if u_mail and u_lic:
                if save_order(u_mail, u_emp, u_lic):
                    notify_telegram(u_mail, u_emp, u_lic)
                    st.success("✅ ¡Solicitud recibida! Tu informe estará listo en 24 horas.")
                else:
                    st.error("❌ Error al guardar. Por favor contacta soporte.")
            else:
                st.warning("⚠️ Por favor completa los campos obligatorios.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.title("⚙️ Admin")
    if st.text_input("Contraseña", type="password") == "bids2026":
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            st.dataframe(df)
