#!/usr/bin/env python3
"""
Story Enhancer - Aplicación Principal Streamlit
Sistema multi-agente para mejora de historias con RAG
"""

import streamlit as st
import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

# Importar módulos locales
from config.settings import settings
from frontend.utils.session_state import init_session_state
from frontend.components.sidebar import render_sidebar
from frontend.pages.document_upload import render_document_upload
from frontend.pages.manuscript_editor import render_manuscript_editor
from frontend.pages.agent_control import render_agent_control
from frontend.pages.outputs_viewer import render_outputs_viewer
from frontend.pages.settings_page import render_settings
from orchestrator.main_orchestrator import MainOrchestrator
from rag.document_processor import DocumentProcessor

# Configuración de página
st.set_page_config(
    page_title="Story Enhancer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .status-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .agent-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Inicializar estado de sesión
    init_session_state()
    
    # Header principal
    st.markdown('<h1 class="main-header">📚 Story Enhancer</h1>', unsafe_allow_html=True)
    st.markdown("### Sistema Multi-Agente para Mejora de Historias")
    
    # Sidebar para navegación
    page = render_sidebar()
    
    # Contenido principal basado en la página seleccionada
    if page == "📄 Documentos":
        render_document_upload()
    elif page == "✍️ Manuscrito":
        render_manuscript_editor()
    elif page == "🤖 Agentes":
        render_agent_control()
    elif page == "📊 Resultados":
        render_outputs_viewer()
    elif page == "⚙️ Configuración":
        render_settings()

if __name__ == "__main__":
    main()