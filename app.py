import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA
# ==========================================
st.set_page_config(
    page_title="DataBids | Strategic Intelligence",
    page_icon="🟦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VARIABLES DE ENTORNO ---
# (Mantengo tus credenciales anteriores para que funcione directo)
TELEGRAM_TOKEN = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
TELEGRAM_CHAT_ID = "7619400780"
ADMIN_PASSWORD = "bids2026"

# ==========================================
# 2. DISEÑO CORPORATIVO (CSS)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;800&display=swap');

    /* --- BASE --- */
    .stApp {
        background-color: #F8FAFC; /* Gris corporativo muy suave */
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B; /* Slate 800 - Mejor lectura que el negro puro */
    }

    /* --- HEADER --- */
    .header-container {
        background-color: #FFFFFF;
        padding: 4rem 1rem 3rem 1rem;
        border-bottom: 1px solid #E2E8F0;
        text-align: center;
        margin-top: -5rem;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 3rem;
    }
    .brand-name {
        font-size: 3.5rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -1.5px;
    }
    .brand-accent { color: #2563EB; } /* Azul Medio Claro (Royal Blue) */
    
    .value-prop {
        font-size: 1.25rem;
        color: #64748B;
        font-weight: 400;
        max-width: 800px;
        margin: 1rem auto 0 auto;
        line-height: 1.6;
    }

    /* --- TARJETAS METODOLOGÍA (LOS 3 PUNTOS) --- */
    /* Diseño sobrio con borde lateral de acento */
    .method-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB; /* El toque de color de la marca */
        padding: 2rem;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .method-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .method-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .method-desc {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.5;
    }

    /* --- SECCIÓN DE CONTRATACIÓN --- */
    .action-container {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .price-display {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0F172A;
    }
    .price-sub {
        color: #64748B;
        font-size: 1rem;
        font-weight: 500;
    }

    /* --- UI ELEMENTS --- */
    /* Botones elegantes y modernos */
    .stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 6px !important; /* Bordes menos redondeados = más serio */
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1D4ED8 !important; /* Azul un poco más oscuro al hover */
    }

    /* Inputs limpios */
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        padding: 0.8rem !important;
        color: #1E293B !important;
    }
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
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
    msg = f"🏛️ *NUEVO INFORME SOLICITADO*\n\n🏢 *Cliente:* {company}\n🆔 *Licitación:* `{id_lic}`\n📧 *Email:* {mail}\n💵 *Estado:* Pagado ($20.000)"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

# ==========================================
# 4. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- HERO SECTION (LIMPIO Y DIRECTO) ---
st.markdown("""
    <div class="header-container">
        <div class="brand-name">DataBids<span class="brand-accent">.</span></div>
        <div class="value-prop">
            Consultoría estratégica para licitaciones en Mercado Público. 
            Transformamos bases complejas en decisiones ganadoras en menos de 24 horas.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- METODOLOGÍA (LOS 3 PUNTOS) ---
# Usamos un contenedor para dar estructura
with st.container():
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">01. Admisibilidad</div>
            <div class="method-desc">
                Auditoría exhaustiva de requisitos mandatorios. Filtramos los errores administrativos que causan el 40% de los rechazos inmediatos antes de evaluar la oferta técnica.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">02. Punto Crítico</div>
            <div class="method-desc">
                Identificación algorítmica y cualitativa del factor determinante de la adjudicación. Te decimos exactamente dónde debes concentrar tus recursos para ganar.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">03. Matriz de Riesgos</div>
            <div class="method-desc">
                Evaluación profunda de riesgos operativos y financieros implícitos en las bases. Protegemos tu margen y aseguramos la viabilidad del contrato a largo plazo.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write(" ") # Espaciador elegante

# --- SECCIÓN DE CONTRATACIÓN (SPLIT LAYOUT) ---
# Dividimos la pantalla: 1/3 para el precio/pago y 2/3 para el formulario
c_spacer_L, c_main, c_spacer_R = st.columns([1, 8, 1])

with c_main:
    st.markdown('<div class="action-container">', unsafe_allow_html=True)
    
    col_offer, col_form = st.columns([1, 1.5], gap="large")
    
    # Columna Izquierda: La Oferta
    with col_offer:
        st.markdown("### Informe Ejecutivo")
        st.write("Análisis completo de una ID de Mercado Público.")
        st.markdown("""
        <div style="margin-top: 2rem; margin-bottom: 2rem;">
            <div class="price-display">$20.000</div>
            <div class="price-sub">Pesos Chilenos + IVA</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Incluye:**")
        st.markdown("""
        <ul style="color: #475569; padding-left: 1.2rem; font-size: 0.9rem; line-height: 1.8;">
            <li>Checklist de Admisibilidad</li>
            <li>Estrategia de Oferta</li>
            <li>Análisis de Multas y Garantías</li>
            <li>Entrega < 24 Horas</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("💳 Pagar ahora (MercadoPago)", "https://www.mercadopago.cl")

    # Columna Derecha: El Formulario
    with col_form:
        st.markdown("### Configuración del Servicio")
        st.write("Ingrese los datos para iniciar el proceso de inteligencia.")
        
        with st.form("contract_form"):
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Inputs limpios
            u_emp = st.text_input("Razón Social", placeholder="Ej: Constructora del Norte SpA")
            u_mail = st.text_input("Correo de Entrega", placeholder="informes@tuempresa.cl")
            u_lic = st.text_input("ID de Licitación (Exacto)", placeholder="Ej: 5544-22-LE24")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # El botón de envío
            submitted = st.form_submit_button("SOLICITAR INFORME")
            
            if submitted:
                if u_emp and u_mail and u_lic:
                    if save_order(u_mail, u_emp, u_lic):
                        notify_telegram(u_mail, u_emp, u_lic)
                        st.success("Solicitud procesada correctamente. Recibirá su informe en el plazo establecido.")
                    else:
                        st.error("Error de conexión. Por favor intente nuevamente.")
                else:
                    st.warning("Todos los campos son requeridos para iniciar el análisis.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER MINIMALISTA ---
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #94A3B8; font-size: 0.8rem;">
        DataBids Intelligence &copy; 2026. Santiago, Chile.<br>
        Servicios de consultoría estratégica para el sector público y privado.
    </div>
""", unsafe_allow_html=True)

# --- ADMIN PANEL (Discreto) ---
with st.sidebar:
    st.markdown("### Acceso Interno")
    if st.text_input("Clave", type="password") == ADMIN_PASSWORD:
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button("Descargar Registros", csv, "databids_ventas.csv", "text/csv")
