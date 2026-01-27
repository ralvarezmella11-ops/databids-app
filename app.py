import streamlit as st
import pandas as pd
import requests
import os
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN (Debe ser la primera línea) ---
st.set_page_config(
    page_title="DataBids | Inteligencia Estratégica",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTIÓN DE ERRORES Y SECRETOS ---
def get_secret(section, key, default=None):
    """Obtiene secretos de forma segura sin romper la app si faltan."""
    try:
        if hasattr(st, 'secrets') and section in st.secrets:
            return st.secrets[section][key]
    except Exception:
        pass
    return default

# --- 3. ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; color: #111827; }
    h1 { color: #0070F3 !important; font-weight: 800; font-size: 2.5rem !important; text-align: center; }
    .subtitle { text-align: center; color: #6B7280; font-size: 1.1rem; margin-bottom: 2rem; }
    .card { background: white; border: 1px solid #E5E7EB; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 1rem; }
    .stButton>button { background-color: #0070F3 !important; color: white !important; border-radius: 8px; width: 100%; font-weight: 600; }
    .stTextInput input { border-radius: 8px; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE NEGOCIO ---
DATA_FILE = "ventas_databids.csv"

def save_data(email, company, lic_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_data = pd.DataFrame([{
        "Fecha": timestamp, "Email": email, "Empresa": company, 
        "ID_Lic": lic_id, "Monto": 20000
    }])
    
    try:
        if os.path.exists(DATA_FILE):
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            new_data.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        st.error("❌ Error: El archivo Excel está abierto. Ciérralo para continuar.")
        return False
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        return False

def send_telegram(email, company, lic_id):
    token = get_secret("telegram", "token")
    chat_id = get_secret("telegram", "chat_id")
    
    # Si no hay configuración, no hacemos nada (evita errores)
    if not token or not chat_id:
        print("⚠️ Telegram no configurado (modo local)")
        return

    msg = f"🚀 NUEVA VENTA:\nEmpresa: {company}\nLic: {lic_id}\nEmail: {email}"
    
    try:
        # CORRECCIÓN AQUÍ: Todo en una sola línea para evitar SyntaxError
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg})
    except:
        pass

# --- 5. INTERFAZ DE USUARIO ---
st.markdown("<h1>DataBids Intelligence</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análisis estratégico de licitaciones públicas</p>', unsafe_allow_html=True)

# Tarjetas informativas
c1, c2, c3 = st.columns(3)
c1.info("📊 **Análisis de Competencia**")
c2.info("🛡️ **Evaluación de Riesgo**")
c3.info("📄 **Reporte PDF**")

# Sección de Pago y Formulario
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1. Realizar Pedido ($20.000 CLP)")
st.write("Ingresa los datos de la licitación que deseas analizar.")

with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Tu Email")
    with col2:
        company = st.text_input("Nombre Empresa")
    
    lic_id = st.text_input("ID Licitación (Ej: 555-22-LQ24)")
    
    submitted = st.form_submit_button("🚀 Solicitar Informe")
    
    if submitted:
        if email and company and lic_id:
            if save_data(email, company, lic_id):
                send_telegram(email, company, lic_id)
                st.success("✅ ¡Solicitud enviada con éxito!")
                st.balloons()
        else:
            st.warning("⚠️ Por favor completa todos los campos.")

st.markdown("</div>", unsafe_allow_html=True)

# Link de pago externo
st.link_button("💳 Pagar ahora con WebPay", "https://www.mercadopago.cl")

# Admin (Oculto en sidebar)
with st.sidebar:
    st.title("Admin")
    pwd = st.text_input("Password", type="password")
    
    # Intenta leer clave de secrets, sino usa '1234' por defecto
    admin_pass = get_secret("admin", "password", "1234") 
    
    if pwd == admin_pass:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE, sep=';')
            st.dataframe(df)
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar CSV",
                data=df.to_csv(index=False, sep=';').encode('utf-8-sig'),
                file_name='ventas.csv',
                mime='text/csv',
            )
        else:
            st.info("Aún no hay ventas registradas.")





