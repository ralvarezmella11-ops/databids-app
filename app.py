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

# --- GESTIÓN DE SECRETOS Y CREDENCIALES ---
# Intentamos leer de st.secrets (lo correcto para producción). 
# Si no existen, usamos las variables por defecto (para pruebas locales).
def get_secret(key, default):
    try:
        return st.secrets.get(key, default)
    except FileNotFoundError:
        return default

# NOTA DE SEGURIDAD: Para producción, mueve estos valores a .streamlit/secrets.toml
TELEGRAM_TOKEN = get_secret("telegram_token", "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0")
TELEGRAM_CHAT_ID = get_secret("telegram_chat_id", "7619400780")
ADMIN_PASSWORD = get_secret("admin_password", "bids2026")

# ==========================================
# 2. DISEÑO CORPORATIVO (CSS)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;800&display=swap');

    /* --- BASE --- */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; color: #1E293B; }

    /* --- HEADER --- */
    .header-container {
        background-color: #FFFFFF; padding: 4rem 1rem 3rem 1rem;
        border-bottom: 1px solid #E2E8F0; text-align: center;
        margin-top: -5rem; margin-left: -5rem; margin-right: -5rem; margin-bottom: 3rem;
    }
    .brand-name { font-size: 3.5rem; font-weight: 800; color: #0F172A; letter-spacing: -1.5px; }
    .brand-accent { color: #2563EB; }
    .value-prop { font-size: 1.25rem; color: #64748B; max-width: 800px; margin: 1rem auto 0 auto; line-height: 1.6; }

    /* --- CARDS (4 COLUMNAS) --- */
    .method-card {
        background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #2563EB;
        padding: 1.5rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
        border-radius: 8px;
    }
    .method-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }
    .method-title { 
        font-size: 1rem; font-weight: 700; color: #0F172A; 
        margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;
        min-height: 3rem; /* Alineación visual de títulos largos */
        display: flex; align-items: center;
    }
    .method-desc { font-size: 0.9rem; color: #475569; line-height: 1.5; }

    /* --- ACTION SECTION --- */
    .action-container {
        background: #FFFFFF; border-radius: 12px; border: 1px solid #E2E8F0;
        padding: 3rem; margin-top: 2rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .price-display { font-size: 2.5rem; font-weight: 800; color: #0F172A; }
    
    /* --- ELEMENTS --- */
    .stButton > button {
        background-color: #2563EB !important; color: white !important; border: none !important;
        padding: 0.75rem 2rem !important; border-radius: 6px !important;
        font-weight: 600 !important; width: 100%; transition: all 0.2s;
    }
    .stButton > button:hover { background-color: #1D4ED8 !important; }
    .stTextInput input {
        background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important; padding: 0.8rem !important; color: #1E293B !important;
    }
    .stTextInput input:focus { border-color: #2563EB !important; }

    /* File Uploader Customization */
    .stFileUploader label { font-size: 0.9rem; font-weight: 600; color: #1E293B; }
    
    #MainMenu, footer, header {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE NEGOCIO (BACKEND)
# ==========================================

def save_order(mail, company, id_lic):
    filename = "ventas_databids.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data = pd.DataFrame([[timestamp, mail, company, id_lic, "PENDIENTE_REVISION", "20000"]], 
                            columns=["Fecha", "Email", "Empresa", "ID_Lic", "Estado", "Monto"])
    try:
        if os.path.exists(filename):
            # Modo append (a) y encoding compatible con Excel
            new_data.to_csv(filename, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_data.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        # Esto pasa si tienes el Excel abierto mientras intentas guardar
        return False
    except Exception as e:
        print(f"Error guardando CSV: {e}")
        return False

def notify_telegram_with_photo(mail, company, id_lic, uploaded_file):
    """Envía los datos Y la foto del comprobante a Telegram con control de errores"""
    
    msg = (
        f"🏛️ *NUEVA SOLICITUD (CON COMPROBANTE)*\n\n"
        f"🏢 *Cliente:* {company}\n"
        f"🆔 *Lic:* `{id_lic}`\n"
        f"📧 *Email:* {mail}\n"
        f"📎 *Estado:* Comprobante adjunto para revisión."
    )
    
    url_msg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    try:
        # 1. Enviar Texto (con timeout para que no se cuelgue)
        requests.post(url_msg, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
        
        # 2. Enviar Foto si existe
        if uploaded_file is not None:
            uploaded_file.seek(0) # Resetear puntero
            files = {'photo': (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': f'🧾 Comprobante: {company}'}
            requests.post(url_photo, data=data, files=files, timeout=10)
            
        return True
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")
        # No retornamos False aquí para no bloquear al usuario si falla Telegram pero se guardó el CSV
        return True 

# ==========================================
# 4. INTERFAZ (FRONTEND)
# ==========================================

# --- HERO ---
st.markdown("""
    <div class="header-container">
        <div class="brand-name">DataBids<span class="brand-accent">.</span></div>
        <div class="value-prop">Consultoría estratégica para licitaciones en Mercado Público.</div>
    </div>
""", unsafe_allow_html=True)

# --- METODOLOGÍA (LOS 4 PILARES SOLICITADOS) ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">01. Admisibilidad</div>
            <div class="method-desc">Auditoría exhaustiva de requisitos mandatorios para blindar la oferta ante rechazos administrativos.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">02. Criterios de Evaluación y Estrategia</div>
            <div class="method-desc">Ingeniería inversa de puntajes y diseño táctico para maximizar la calificación técnica.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">03. Riesgos Críticos</div>
            <div class="method-desc">Detección de multas, boletas de garantía y cláusulas operativas de alto impacto.</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">04. Viabilidad Económica y Recomendación</div>
            <div class="method-desc">Análisis de márgenes, flujo de caja y conclusión estratégica Go/No-Go.</div>
        </div>
        """, unsafe_allow_html=True)

# --- ZONA DE CONTRATACIÓN ---
c_spacer_L, c_main, c_spacer_R = st.columns([1, 8, 1])

with c_main:
    st.markdown('<div class="action-container">', unsafe_allow_html=True)
    col_offer, col_form = st.columns([1, 1.5], gap="large")
    
    # IZQUIERDA: PAGO (PASO 1)
    with col_offer:
        st.markdown("### Paso 1: Pago del Servicio")
        st.write("Para iniciar el análisis, realice el pago único.")
        st.markdown("""
        <div style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
            <div class="price-display">$20.000</div>
            <div style="color: #64748B;">Pesos Chilenos + IVA</div>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Importante:** Guarde su comprobante, lo necesitará para el siguiente paso.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("💳 Pagar Ahora (WebPay/MercadoPago)", "https://www.mercadopago.cl")

    # DERECHA: DATOS + COMPROBANTE (PASO 2)
    with col_form:
        st.markdown("### Paso 2: Validación y Datos")
        st.write("Adjunte su comprobante para activar la solicitud.")
        
        with st.form("contract_form"):
            st.markdown("<br>", unsafe_allow_html=True)
            
            u_emp = st.text_input("Razón Social", placeholder="Ej: Constructora del Norte SpA")
            u_mail = st.text_input("Correo de Entrega", placeholder="informes@tuempresa.cl")
            u_lic = st.text_input("ID de Licitación", placeholder="Ej: 5544-22-LE24")
            
            st.divider()
            
            st.markdown("**Adjuntar Comprobante de Pago (Obligatorio)**")
            uploaded_file = st.file_uploader("Subir imagen (JPG, PNG) o PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("ENVIAR SOLICITUD VALIDADA")
            
            if submitted:
                if u_emp and u_mail and u_lic and uploaded_file is not None:
                    
                    # Intentamos guardar primero en CSV
                    if save_order(u_mail, u_emp, u_lic):
                        # Si guarda bien, notificamos
                        notify_telegram_with_photo(u_mail, u_emp, u_lic, uploaded_file)
                        
                        st.success("✅ Solicitud recibida. Nuestro equipo de analistas comenzará la revisión en breve.")
                        st.balloons()
                    else:
                        st.error("⚠️ Error guardando el pedido. Por favor cierre el archivo Excel si lo tiene abierto o reintente.")
                else:
                    if uploaded_file is None:
                        st.error("⚠️ Falta el comprobante de pago.")
                    else:
                        st.warning("⚠️ Por favor complete todos los datos.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('<div style="text-align: center; margin-top: 3rem; color: #94A3B8; font-size: 0.8rem;">DataBids Intelligence &copy; 2026.</div>', unsafe_allow_html=True)

# --- ADMIN PANEL (SEGURIDAD BÁSICA) ---
with st.sidebar:
    st.markdown("### 🔒 Acceso Interno")
    pwd_input = st.text_input("Clave Admin", type="password")
    
    if pwd_input == ADMIN_PASSWORD:
        st.success("Conectado")
        if os.path.exists("ventas_databids.csv"):
            df = pd.read_csv("ventas_databids.csv", sep=';', encoding='utf-8-sig')
            
            # Formateo visual simple para la tabla
            st.dataframe(df, use_container_width=True)
            
            # Botón de descarga
            with open("ventas_databids.csv", "rb") as f:
                st.download_button("📥 Bajar Excel", f, file_name="ventas_databids.csv", mime="text/csv")

