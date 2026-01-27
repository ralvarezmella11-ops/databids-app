import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE TELEGRAM ---
TOKEN_BOT = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
MI_ID_CHAT = "7619400780"

def enviar_aviso_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
        requests.post(url, data={"chat_id": MI_ID_CHAT, "text": mensaje})
    except:
        pass

# --- ESTILO PROFESIONAL (AZUL MARINO) ---
st.set_page_config(page_title="DataBids Pro", page_icon="📊")
st.markdown("""
    <style>
    .stApp { background-color: #050A18; color: white; }
    .stButton>button { border-radius: 20px; background-color: #0070F3; color: white; width: 100%; }
    .stTextInput>div>div>input { border-radius: 10px; }
    div[data-testid="stExpander"] { border-radius: 15px; background-color: #0F172A; }
    </style>
    """, unsafe_allow_html=True)

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
    enviar_aviso_telegram(f"🚀 ¡NUEVA VENTA!\n🏢 {empresa}\n🆔 {id_lic}\n📧 {email}")

# --- INTERFAZ ---
st.image("https://i.postimg.cc/K8jf9Vr0/Gemini-Generated-Image-rsq4ghrsq4ghrsq4.png", width=120)
st.title("DataBids Insights")
st.subheader("Análisis Estratégico de Licitaciones")

# --- PASO 1: EL PAGO ---
st.markdown("### Paso 1: Gestión de Pago")
st.info("Para habilitar el formulario de registro, primero debes completar el pago del servicio.")
st.link_button("💳 PAGAR ANÁLISIS ($20.000)", "https://www.mercadopago.cl")

st.divider()

# --- RESTRICCIÓN LÓGICA ---
# Esta casilla actúa como la "llave"
pago_confirmado = st.checkbox("✅ Ya realicé el pago y tengo mi comprobante")

if pago_confirmado:
    st.success("🔓 Formulario habilitado. Por favor, ingresa los detalles de la licitación.")
    
    # --- PASO 2: EL FORMULARIO (SOLO VISIBLE SI MARCÓ EL CHECKBOX) ---
    with st.form("registro", clear_on_submit=True):
        st.markdown("### Paso 2: Detalles de la Licitación")
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
                    st.success("📥 ¡Recibido! Tu analista experto ha sido notificado.")
                except:
                    st.error("Error al guardar. Intenta de nuevo.")
            else:
                st.warning("⚠️ Completa los campos para procesar el pedido.")
else:
    st.warning("🔒 El formulario de envío de datos está bloqueado hasta confirmar el pago.")

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.header("🔑 Admin")
    if st.text_input("Clave", type="password") == "bids2026":
        if os.path.exists(DB_FILE):
            st.dataframe(pd.read_csv(DB_FILE, sep=';'))




