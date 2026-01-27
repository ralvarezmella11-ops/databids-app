import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="DataBids Pro", layout="centered")

st.title("📊 DataBids Pro")
st.subheader("Análisis Profesional de Licitaciones")

correo = st.text_input("Correo")
empresa = st.text_input("Empresa")
licitacion = st.text_input("ID Licitación")

if st.button("Enviar"):
    if correo and licitacion:
        token = "TU_TOKEN"
        chat_id = "TU_CHAT"

        msg = f"""
Nueva solicitud:
Empresa: {empresa}
Correo: {correo}
Licitación: {licitacion}
"""

        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": msg}
        )

        st.success("Solicitud enviada correctamente")
    else:
        st.warning("Completa los campos obligatorios")

