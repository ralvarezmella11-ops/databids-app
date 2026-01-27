import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- CONFIGURACIÓN ESTRUCTURAL ---
def init_app():
    st.set_page_config(
        page_title="DataBids | Inteligencia Estratégica",
        page_icon="📈",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

# --- ESTILOS DE ALTO NIVEL (CSS) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        /* Reset y Fondo */
        .stApp {
            background: linear-gradient(180deg, #001220 0%, #001F33 100%);
            font-family: 'Inter', sans-serif;
        }

        /* Contenedores Estilo Card (No cuadrados) */
        .main-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(12px);
        }

        /* Botón de Pago Pro */
        .stLinkButton > a {
            background: linear-gradient(90deg, #0061FF 0%, #60EFFF 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease !important;
            text-align: center;
            display: block;
        }

        .stLinkButton > a:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 97, 255, 0.4);
        }

        /* Inputs Modernos */
        .stTextInput input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            color: #fff !important;
            padding: 12px !important;
        }

        /* Títulos */
        h1 { color: #FFFFFF; font-weight: 800; font-size: 2.5rem !important; margin-bottom: 0.5rem; }
        h3 { color: #60EFFF; font-weight: 400; }
        
        /* Ocultar barra de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NEGOCIO (BACKEND) ---
def notify_telegram(email, empresa, id_lic):
    token = "8501600446:AAHmnOJGs0QIRgDRw---f4-fWMf7xP7Moz0"
    chat_id = "7619400780"
    msg = f"🛎️ *NUEVO PEDIDO DATABIDS*\n\n🏢 *Empresa:* {empresa}\n🆔 *Licitación:* {id_lic}\n📧 *Email:* {email}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except Exception as e:
        st.error(f"Error de notificación: {e}")

def save_transaction(email, empresa, id_lic):
    db_file = "registro_ventas.csv"
    data = {
        "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Email": [email],
        "Empresa": [empresa],
        "ID_Licitacion": [id_lic],
        "Estado": ["Pagado"],
        "Monto": ["20000"]
    }
    df = pd.DataFrame(data)
    try:
        if os.path.exists(db_file):
            df.to_csv(db_file, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
        else:
            df.to_csv(db_file, index=False, sep=';', encoding='utf-8-sig')
        return True
    except PermissionError:
        st.error("⚠️ Error: El archivo Excel está abierto. Ciérralo para procesar.")
        return False

# --- COMPONENTES DE INTERFAZ ---
def main():
    init_app()
    apply_custom_styles()

    # Header con Logo
    col_logo, _ = st.columns([1, 2])
    with col_logo:
        st.image("https://i.ibb.co/276P7mP/fdwwXykc.jpg", width=140)

    st.markdown("<h1>DataBids Insights</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Consultoría estratégica de licitaciones</h3>", unsafe_allow_html=True)

    # Hero Section
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("### 🚀 Asegura tu adjudicación")
        st.write("Analizamos tu competencia y optimizamos tu oferta técnica/económica para Mercado Público.")
        st.write("")
        st.link_button("💳 PAGAR ANÁLISIS ($20.000 CLP)", "https://www.mercadopago.cl")
        st.markdown('</div>', unsafe_allow_html=True)

    # Formulario
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.write("#### 📝 Registro de Solicitud")
        with st.form("pro_form", clear_on_submit=True):
            email = st.text_input("Correo electrónico corporativo")
            empresa = st.text_input("Razón Social / Nombre")
            licitacion = st.text_input("ID de Licitación (Ej: 1234-56-L123)")
            
            submit = st.form_submit_button("CONFIRMAR Y ENVIAR")
            
            if submit:
                if email and licitacion:
                    if save_transaction(email, empresa, licitacion):
                        notify_telegram(email, empresa, licitacion)
                        st.balloons()
                        st.success("✅ ¡Éxito! Tu analista ha sido notificado. Recibirás el informe en 24 hrs.")
                else:
                    st.warning("⚠️ Completa los campos obligatorios para continuar.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Admin
    with st.sidebar:
        st.title("🔐 Admin")
        pwd = st.text_input("Acceso", type="password")
        if pwd == "bids2026":
            if os.path.exists("registro_ventas.csv"):
                df_view = pd.read_csv("registro_ventas.csv", sep=';', encoding='utf-8-sig')
                st.dataframe(df_view)
                st.download_button("📥 Exportar CSV", data=df_view.to_csv(sep=';', index=False).encode('utf-8-sig'), file_name="ventas.csv")

if __name__ == "__main__":
    main()


