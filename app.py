import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

# --- CONSTANTES Y CONFIGURACIÓN ---
PAGE_CONFIG = {
    "page_title": "DataBids | Inteligencia Estratégica",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

DATA_FILE = Path("ventas_databids.csv")
PRICE_CLP = 20000

# --- ESTILOS CSS (Inyectados dinámicamente) ---
CUSTOM_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; color: #111827; }
    h1 { color: #0070F3 !important; font-weight: 800; font-size: 3rem !important; text-align: center; line-height: 1.2; }
    .subtitle { text-align: center; color: #4B5563; font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem auto; }
    
    /* Cards */
    .feature-card, .section-card {
        background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .feature-card { padding: 2rem; height: 100%; }
    .section-card { padding: 2.5rem; }
    
    /* Typography & Icons */
    .feature-icon { color: #0070F3; font-size: 1.5rem; margin-bottom: 1rem; }
    .feature-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .feature-desc { color: #4B5563; font-size: 0.95rem; }
    .step-header { font-weight: 700; color: #4B5563; margin-top: 3rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.85rem;}
    
    /* Pricing */
    .price-tag { font-size: 2.5rem; font-weight: 800; color: #111827; }
    .price-currency { font-size: 1.5rem; color: #4B5563; }
    
    /* Buttons & Inputs */
    div.stButton > button, div.stLinkButton > a {
        background-color: #0070F3 !important; color: white !important; border: none !important;
        border-radius: 12px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important;
        width: 100%; transition: all 0.2s ease;
    }
    div.stButton > button:hover, div.stLinkButton > a:hover {
        background-color: #005bb5 !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,112,243,0.2);
    }
    .stTextInput input { border: 1px solid #D1D5DB !important; border-radius: 8px !important; padding: 0.75rem !important; }
    
    /* Utilities */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
"""

# --- CLASE DE GESTIÓN DE NEGOCIO (BACKEND) ---
class OrderManager:
    """Maneja la lógica de persistencia y notificaciones."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.filepath.exists():
            df = pd.DataFrame(columns=["Fecha", "Email", "Empresa", "ID_Lic", "Estado", "Monto"])
            df.to_csv(self.filepath, sep=';', index=False, encoding='utf-8-sig')

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    def save_order(self, email: str, company: str, lic_id: str) -> bool:
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        new_row = {
            "Fecha": timestamp,
            "Email": email,
            "Empresa": company,
            "ID_Lic": lic_id,
            "Estado": "SOLICITADO",
            "Monto": str(PRICE_CLP)
        }
        try:
            # Usamos lock file implícito al abrir en append, aunque pandas maneja bien CSVs simples
            # Para alta concurrencia se recomendaría SQLite
            df_new = pd.DataFrame([new_row])
            df_new.to_csv(self.filepath, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')
            return True
        except Exception as e:
            st.error(f"Error interno I/O: {e}")
            return False

    def notify_telegram(self, email: str, company: str, lic_id: str):
        # Recuperación segura de secretos
        try:
            token = st.secrets["telegram"]["token"]
            chat_id = st.secrets["telegram"]["chat_id"]
        except FileNotFoundError:
            # Fallback silencioso para desarrollo local sin secrets
            return 
        except KeyError:
             st.error("Configuración de secretos incompleta.")
             return

        msg = (
            f"🚀 *NUEVA ORDEN DATABIDS*\n\n"
            f"🏢 *Empresa:* {company}\n"
            f"🆔 *Licitación:* `{lic_id}`\n"
            f"📧 *Email:* {email}\n"
            f"💰 *Monto:* ${PRICE_CLP:,.0f} CLP"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
        except requests.RequestException:
            pass # No interrumpir el flujo de usuario si falla la API

# --- COMPONENTES DE UI ---
def render_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown("<h1>Informes y análisis estratégicos de licitaciones</h1>", unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Optimiza tu participación en Mercado Público con inteligencia de datos. '
        'Toma decisiones informadas y aumenta tus probabilidades de éxito.</p>', 
        unsafe_allow_html=True
    )
    st.info(f"💡 **Servicio Premium:** Análisis de competencia y factibilidad por **${PRICE_CLP:,.0f} CLP**.")

def render_features():
    col1, col2, col3 = st.columns(3)
    features = [
        {"icon": "📊", "title": "Análisis de Competencia", "desc": "Identifica competidores y sus estrategias de precios históricos."},
        {"icon": "🛡️", "title": "Evaluación de Riesgo", "desc": "Probabilidad de adjudicación basada en variables clave."},
        {"icon": "📄", "title": "Reportes Detallados", "desc": "Informe PDF completo con gráficos y recomendaciones accionables."}
    ]
    
    for col, feat in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{feat['icon']}</div>
                    <div class="feature-title">{feat['title']}</div>
                    <div class="feature-desc">{feat['desc']}</div>
                </div>
            """, unsafe_allow_html=True)

def render_payment_section():
    st.markdown('<div class="step-header">1. PASO INICIAL: PAGO</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Realiza tu pago seguro")
            st.markdown("""
                <ul style="list-style: none; padding: 0; color: #4B5563;">
                    <li style="margin-bottom: 0.5rem;">✅ Pago único por licitación</li>
                    <li style="margin-bottom: 0.5rem;">✅ Boleta o factura disponible</li>
                    <li style="margin-bottom: 0.5rem;">✅ Garantía de entrega en 24h</li>
                </ul>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="text-align: right;"><span class="price-tag">${PRICE_CLP:,.0f}</span> <span class="price-currency">CLP</span></div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align: right; font-size: 0.8rem; color: #6B7280;">Vía MercadoPago</div>', unsafe_allow_html=True)
        
        st.write("")
        st.link_button("💳 IR A PAGAR AHORA", "https://www.mercadopago.cl") 
        st.markdown('</div>', unsafe_allow_html=True)

def render_form_section(manager: OrderManager):
    st.markdown('<div class="step-header">2. PASO FINAL: ACTIVACIÓN</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Registra la Licitación")
        st.write("Ingresa los datos para generar tu reporte estratégico.")
        
        with st.form("registro_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                u_mail = st.text_input("Tu Correo Electrónico", placeholder="nombre@empresa.com")
            with col_b:
                u_emp = st.text_input("Nombre / Empresa", placeholder="Tu Empresa SpA")
            
            u_lic = st.text_input("ID de la Licitación (Mercado Público)", placeholder="Ej: 1234-56-LE24")
            
            submitted = st.form_submit_button("🚀 Confirmar y Solicitar Informe")
            
            if submitted:
                if not u_mail or not u_emp or not u_lic:
                    st.warning("⚠️ Todos los campos son obligatorios.")
                elif not manager.validate_email(u_mail):
                    st.error("❌ El correo electrónico ingresado no es válido.")
                else:
                    if manager.save_order(u_mail, u_emp, u_lic):
                        manager.notify_telegram(u_mail, u_emp, u_lic)
                        st.balloons()
                        st.success(f"✅ ¡Solicitud recibida correctamente! Hemos enviado una confirmación a **{u_mail}**.")
                    else:
                        st.error("❌ Hubo un error al procesar tu solicitud. Intenta nuevamente.")
        st.markdown('</div>', unsafe_allow_html=True)

def render_admin_panel(manager: OrderManager):
    with st.sidebar:
        st.divider()
        with st.expander("🔒 Acceso Administrativo"):
            pwd = st.text_input("Contraseña", type="password")
            
            # Verificación segura con secrets
            try:
                admin_pass = st.secrets["admin"]["password"]
            except KeyError:
                admin_pass = "admin" # Fallback NO recomendado en prod
            
            if pwd == admin_pass:
                st.success("Acceso Concedido")
                if manager.filepath.exists():
                    df = pd.read_csv(manager.filepath, sep=';', encoding='utf-8-sig')
                    st.dataframe(df)
                    
                    # Botón de descarga para el admin
                    csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name='ventas_databids.csv',
                        mime='text/csv',
                    )
                else:
                    st.info("Aún no hay ventas registradas.")
            elif pwd:
                st.error("Contraseña incorrecta")

# --- MAIN APP FLOW ---
def main():
    st.set_page_config(**PAGE_CONFIG)
    
    # Inicializar gestor
    manager = OrderManager(DATA_FILE)
    
    # Renderizar UI
    render_header()
    st.write("") # Spacer
    render_features()
    st.write("") # Spacer
    render_payment_section()
    render_form_section(manager)
    
    # Admin (oculto en sidebar)
    render_admin_panel(manager)

if __name__ == "__main__":
    main()
