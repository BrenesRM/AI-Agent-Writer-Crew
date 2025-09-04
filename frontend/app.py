import streamlit as st
import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import settings
from rag.rag_manager import RAGManager
from agents.agent_manager import AgentManager

# Importar páginas
from pages.upload_docs import render_upload_page
from pages.manuscript_editor import render_manuscript_page
from pages.agent_monitor import render_monitor_page
from pages.results_viewer import render_results_page
from pages.visual_prompts import render_visual_page

# Configuración de página
st.set_page_config(
    page_title="Sistema Multi-Agente para Novelas",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class NovelSystemApp:
    """Aplicación principal del Sistema Multi-Agente para Novelas"""
    
    def __init__(self):
        self.init_session_state()
        self.rag_manager = None
        self.agent_manager = None
    
    def init_session_state(self):
        """Inicializa el estado de la sesión"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = False
            st.session_state.manuscript = ""
            st.session_state.analysis_results = {}
            st.session_state.visual_prompts = []
            st.session_state.rag_stats = {}
            st.session_state.processing = False
            st.session_state.current_phase = ""
    
    def initialize_system(self):
        """Inicializa los sistemas RAG y de agentes"""
        if not st.session_state.initialized:
            with st.spinner("Inicializando sistema..."):
                try:
                    # Inicializar RAG Manager
                    self.rag_manager = RAGManager()
                    st.session_state.rag_stats = self.rag_manager.get_stats()
                    
                    # Inicializar Agent Manager
                    self.agent_manager = AgentManager()
                    
                    st.session_state.initialized = True
                    st.success("✅ Sistema inicializado correctamente")
                    
                except Exception as e:
                    st.error(f"❌ Error inicializando sistema: {str(e)}")
                    st.stop()
        else:
            # Recuperar instancias
            self.rag_manager = RAGManager()
            self.agent_manager = AgentManager()
    
    def render_sidebar(self):
        """Renderiza la barra lateral"""
        with st.sidebar:
            st.title("📖 Sistema Multi-Agente")
            st.markdown("*Creación Inteligente de Novelas*")
            
            st.markdown("---")
            
            # Información del sistema
            if st.session_state.initialized:
                st.success("🟢 Sistema Activo")
                
                # Estadísticas RAG
                stats = st.session_state.rag_stats
                st.metric("Documentos RAG", stats.get('total_documents', 0))
                st.metric("Chunks Vectorizados", stats.get('total_chunks', 0))
                
                # Estado del manuscrito
                if st.session_state.manuscript:
                    word_count = len(st.session_state.manuscript.split())
                    st.metric("Palabras del Manuscrito", word_count)
                
                # Estado del procesamiento
                if st.session_state.processing:
                    st.warning(f"🔄 Procesando: {st.session_state.current_phase}")
            else:
                st.error("🔴 Sistema No Inicializado")
            
            st.markdown("---")
            
            # Navegación
            st.subheader("📑 Navegación")
            pages = [
                ("📚 Biblioteca RAG", "upload"),
                ("✍️ Editor de Manuscrito", "manuscript"),
                ("🤖 Monitor de Agentes", "monitor"),
                ("📊 Resultados", "results"),
                ("🎬 Prompts Visuales", "visual")
            ]
            
            selected_page = st.radio(
                "Selecciona una página:",
                options=[p[1] for p in pages],
                format_func=lambda x: next(p[0] for p in pages if p[1] == x),
                key="page_selector"
            )
            
            st.markdown("---")
            
            # Información del proyecto
            st.subheader("ℹ️ Información")
            st.caption(f"**Proyecto**: {settings.project_name}")
            st.caption(f"**Versión**: 1.0.0")
            st.caption(f"**Modelo LLM**: {'Configurado' if settings.llm_model_path else 'No configurado'}")
            
            return selected_page
    
    def render_header(self):
        """Renderiza el encabezado principal"""
        st.title("📖 Sistema Multi-Agente para Creación de Novelas")
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h3 style="margin: 0; text-align: center;">
                🤖 Potenciado por IA • 📚 RAG Inteligente • ✨ Creatividad Aumentada
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Inicializar sistema
        self.initialize_system()
        
        # Renderizar interfaz
        selected_page = self.render_sidebar()
        
        # Área principal
        self.render_header()
        
        # Renderizar página seleccionada
        if selected_page == "upload":
            render_upload_page(self.rag_manager)
        elif selected_page == "manuscript":
            render_manuscript_page(self.agent_manager)
        elif selected_page == "monitor":
            render_monitor_page(self.agent_manager)
        elif selected_page == "results":
            render_results_page()
        elif selected_page == "visual":
            render_visual_page()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
            f"© 2025 Sistema Multi-Agente para Novelas • "
            f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            "</div>",
            unsafe_allow_html=True
        )

def main():
    """Función principal"""
    app = NovelSystemApp()
    app.run()

if __name__ == "__main__":
    main()