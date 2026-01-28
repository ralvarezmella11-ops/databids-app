# --- METODOLOGÍA ---
with st.container():
    # CAMBIO: Ahora son 4 columnas (antes eran 3)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">01. Admisibilidad</div>
            <div class="method-desc">Auditoría exhaustiva de requisitos mandatorios y formales para blindar la oferta ante rechazos administrativos.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">02. Evaluación y Estrategia</div>
            <div class="method-desc">Análisis inverso de las fórmulas de puntaje y diseño táctico de la oferta para maximizar la calificación técnica.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">03. Riesgos Críticos</div>
            <div class="method-desc">Detección temprana de multas desproporcionadas, cláusulas leoninas y riesgos operativos en las bases.</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">04. Viabilidad y Rec.</div>
            <div class="method-desc">Evaluación económica del contrato, proyección de flujo de caja y recomendación final (Go/No-Go).</div>
        </div>
        """, unsafe_allow_html=True)
