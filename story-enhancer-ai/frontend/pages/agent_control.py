"""
Página de control y monitoreo de agentes
"""

import streamlit as st
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List
from frontend.utils.session_state import add_log_entry

def render_agent_control():
    """Renderiza la página de control de agentes"""
    
    st.title("🤖 Control de Agentes")
    st.markdown("Controla el proceso iterativo de mejora de la historia usando agentes especializados.")
    
    # Verificar prerrequisitos
    if not check_prerequisites():
        return
    
    # Tabs para organizar la funcionalidad
    tab1, tab2, tab3, tab4 = st.tabs(["🎮 Control Principal", "👥 Configuración de Agentes", "📊 Monitoreo", "🔄 Historial"])
    
    with tab1:
        render_main_control()
        
    with tab2:
        render_agent_configuration()
        
    with tab3:
        render_agent_monitoring()
        
    with tab4:
        render_iteration_history()

def check_prerequisites():
    """Verifica que los prerrequisitos estén cumplidos"""
    
    issues = []
    
    if not st.session_state.rag_ready:
        issues.append("📄 RAG no configurado - Carga documentos de referencia primero")
    
    if not st.session_state.manuscript_content:
        issues.append("✍️ Manuscrito faltante - Carga tu historia base primero")
    
    if issues:
        st.error("❌ No se puede iniciar el proceso de agentes:")
        for issue in issues:
            st.write(f"• {issue}")
        
        st.markdown("---")
        st.info("💡 Ve a las páginas correspondientes para completar la configuración.")
        return False
    
    return True

def render_main_control():
    """Panel de control principal para ejecutar el proceso de agentes"""
    
    st.subheader("🎮 Control Principal")
    
    # Estado actual del proceso
    render_process_status()
    
    st.markdown("---")
    
    # Configuración del proceso
    col1, col2 = st.columns(2)
    
    with col1:
        max_iterations = st.number_input(
            "Máximo de iteraciones",
            min_value=1,
            max_value=10,
            value=st.session_state.max_iterations,
            help="Número máximo de ciclos de mejora"
        )
        st.session_state.max_iterations = max_iterations
        
        convergence_threshold = st.slider(
            "Umbral de convergencia",
            min_value=0.1,
            max_value=1.0,
            value=0.8,
            step=0.1,
            help="Si los cambios son menores a este umbral, el proceso se detiene"
        )
    
    with col2:
        auto_save = st.checkbox(
            "Guardar automáticamente",
            value=True,
            help="Guardar progreso después de cada iteración"
        )
        
        detailed_logging = st.checkbox(
            "Logging detallado",
            value=False,
            help="Registrar información detallada de cada agente"
        )
    
    st.markdown("---")
    
    # Controles de ejecución
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Iniciar Proceso", type="primary", disabled=st.session_state.processing_status == "running"):
            start_agent_process(max_iterations, convergence_threshold, auto_save, detailed_logging)
    
    with col2:
        if st.button("⏸️ Pausar", disabled=st.session_state.processing_status != "running"):
            pause_agent_process()
    
    with col3:
        if st.button("▶️ Reanudar", disabled=st.session_state.processing_status != "paused"):
            resume_agent_process()
    
    with col4:
        if st.button("🛑 Detener", disabled=st.session_state.processing_status == "idle"):
            stop_agent_process()

def render_process_status():
    """Muestra el estado actual del proceso"""
    
    st.subheader("📊 Estado del Proceso")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_icons = {
            'idle': '⚪',
            'running': '🔄',
            'paused': '⏸️',
            'completed': '✅',
            'error': '❌'
        }
        icon = status_icons.get(st.session_state.processing_status, '⚪')
        st.metric("Estado", f"{icon} {st.session_state.processing_status.title()}")
    
    with col2:
        st.metric("Iteración Actual", f"{st.session_state.current_iteration}/{st.session_state.max_iterations}")
    
    with col3:
        if st.session_state.processing_status == "running":
            st.metric("Progreso", f"{(st.session_state.current_iteration / st.session_state.max_iterations)