import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- TUS CREDENCIALES DE TELEGRAM ---
TOKEN_BOT = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
MI_ID_CHAT = "7619400780"

# Función para enviarte el aviso al celular
def enviar_aviso_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={MI_ID_CHAT}&text={mensaje}"
        requests.get(url)
    except Exception as e:
        st.error(f"Error al enviar aviso: {e}")

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="DataBids Pro", page_icon="📊")

# Base de datos local (Excel)
DB_FILE = "registro_ventas.csv"

def guardar_datos(email, empresa, id_lic):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    nuevo = pd.DataFrame([[fecha, email, empresa, id_lic, "20000", "PAGADO"]], 
                         columns=["Fecha", "Email", "Empresa", "ID Licitacion", "Monto", "Estado"])
    
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE, sep=';', encoding='utf-8-sig')
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo
    
    df.to_csv(DB_FILE, index=False, sep=';', encoding='utf-8-sig')
    
    # Enviar el aviso a tu Telegram
    texto_aviso = f"🚀 ¡NUEVA VENTA DATABIDS!\n\n🏢 Empresa: {empresa}\n🆔 ID Licitación: {id_lic}\n📧 Email: {email}\n💰 Monto: $20.000"
    enviar_aviso_telegram(texto_aviso)

# --- INTERFAZ VISUAL ---
st.title("📊 DataBids")
st.subheader("Informes y análisis estratégicos de licitaciones")
st.write("Bienvenido. Optimiza tu participación en Mercado Público con nuestra inteligencia de datos.")

st.info("💡 **Servicio:** Análisis de competencia y factibilidad por $20.000 CLP.")

# Paso 1: El Pago
st.subheader("1. Realiza tu pago")
# Reemplaza el link de abajo por tu link real de Mercado Pago cuando lo tengas
st.link_button("💳 PAGAR ANÁLISIS POR WEBPAY", "https://mpago.la/1SFz889") 

st.divider()

# Paso 2: El Registro
st.subheader("2. Registra los datos de la licitación")
with st.form("registro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        u_mail = st.text_input("Tu Correo")
        u_emp = st.text_input("Empresa / Nombre")
    with col2:
        u_lic = st.text_input("ID de la Licitación (Ej: 1234-56-L123)")
    
    if st.form_submit_button("Confirmar Solicitud"):
        if u_mail and u_lic:
            try:
                guardar_datos(u_mail, u_emp, u_lic)
                st.balloons()
                st.success("✅ ¡Recibido! Te avisaremos al correo cuando tu informe esté listo.")
            except PermissionError:
                st.error("❌ Cierra el archivo Excel para poder guardar los datos.")
        else:
            st.warning("⚠️ Por favor, rellena los campos obligatorios.")

# --- PANEL ADMIN (SIDEBAR) ---
with st.sidebar:
    st.header("🔑 Administración")
    clave = st.text_input("Contraseña", type="password")
    if clave == "bids2026": # Esta es tu clave para ver ventas
        if os.path.exists(DB_FILE):
            st.write("Ventas registradas:")
            st.dataframe(pd.read_csv(DB_FILE, sep=';', encoding='utf-8-sig'))
            with open(DB_FILE, "rb") as f:
                st.download_button("📥 Descargar Excel", f, file_name="ventas_databids.csv")
