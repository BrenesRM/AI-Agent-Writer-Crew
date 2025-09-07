# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Agregar el directorio raiz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Importar configuracion y managers
try:
    from config.settings import settings
    from rag.rag_manager import RAGManager
    from agents.agent_manager import AgentManager
except ImportError as e:
    st.error(f"❌ Error importando modulos: {str(e)}")
    st.stop()

# Importar paginas
from pages.upload_docs import render_upload_page
from pages.manuscript_editor import render_manuscript_page
from pages.agent_monitor import render_monitor_page
from pages.results_viewer import render_results_page
from pages.visual_prompts import render_visual_page

# Importar componentes
from components.sidebar import render_main_sidebar
from components.alerts import initialize_alerts_system, render_alert_notifications, check_and_create_alerts

# Configuracion de pagina
st.set_page_config(
    page_title="Sistema Multi-Agente para Novelas",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .status-success { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-error { color: #dc3545; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #f0f2f6;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class NovelSystemApp:
    """Aplicacion principal del Sistema Multi-Agente para Novelas"""
    
    def __init__(self):
        self.init_session_state()
        self.rag_manager = None
        self.agent_manager = None
        
        # Inicializar sistema de alertas
        initialize_alerts_system()
    
    def init_session_state(self):
        """Inicializa el estado de la sesion"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = False
            st.session_state.manuscript = ""
            st.session_state.analysis_results = {}
            st.session_state.visual_prompts = []
            st.session_state.rag_stats = {}
            st.session_state.processing = False
            st.session_state.current_phase = ""
            st.session_state.page_selector = "upload"
            st.session_state.system_start_time = datetime.now()
            st.session_state.session_start_time = datetime.now()
    
    def initialize_system(self):
        """Inicializa los sistemas RAG y de agentes"""
        if not st.session_state.initialized:
            with st.spinner("🚀 Inicializando sistema..."):
                try:
                    # Inicializar RAG Manager
                    self.rag_manager = RAGManager()
                    
                    # Obtener estadisticas iniciales
                    try:
                        st.session_state.rag_stats = self.rag_manager.get_stats()
                    except Exception as e:
                        st.session_state.rag_stats = {
                            'total_documents': 0,
                            'total_chunks': 0,
                            'total_size_mb': 0.0,
                            'last_updated': 'Nunca'
                        }
                    
                    # Inicializar Agent Manager
                    self.agent_manager = AgentManager()
                    
                    st.session_state.initialized = True
                    st.success("✅ Sistema inicializado correctamente")
                    
                except Exception as e:
                    st.error(f"❌ Error inicializando sistema: {str(e)}")
                    # Continuar con funcionalidad limitada
                    st.session_state.initialized = True
                    st.warning("⚠️ Sistema iniciado con funcionalidad limitada")
        
        else:
            # Recuperar instancias existentes
            try:
                self.rag_manager = RAGManager()
                self.agent_manager = AgentManager()
            except Exception as e:
                st.warning(f"⚠️ Error reconectando con sistemas: {str(e)}")
    
    def render_header(self):
        """Renderiza el encabezado principal"""
        st.markdown("""
        <div class="main-header">
            <h2>📖 Sistema Multi-Agente para Creacion de Novelas</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                🤖 Potenciado por IA • 📚 RAG Inteligente • ✨ Creatividad Aumentada
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_main_content(self, selected_page):
        """Renderiza el contenido principal basado en la pagina seleccionada"""
        
        # Verificar alertas criticas antes de mostrar contenido
        render_alert_notifications()
        
        try:
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
            
            else:
                st.error(f"❌ Pagina desconocida: {selected_page}")
        
        except Exception as e:
            st.error(f"❌ Error renderizando pagina {selected_page}: {str(e)}")
            st.markdown("""
            ### 🔧 Soluciones Posibles:
            - Recarga la pagina (F5)
            - Verifica que todos los componentes esten inicializados
            - Revisa la consola del navegador para mas detalles
            """)
    
    def render_footer(self):
        """Renderiza el pie de pagina"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown("**🔗 Enlaces Utiles:**")
            st.markdown("- [Documentacion](https://docs.anthropic.com)")
            st.markdown("- [GitHub](https://github.com/tu-repo)")
            st.markdown("- [Soporte](mailto:soporte@proyecto.com)")
        
        with col2:
            st.markdown("**📊 Estado:**")
            if st.session_state.initialized:
                st.markdown("🟢 Sistema Activo")
            else:
                st.markdown("🔴 Sistema Inactivo")
        
        with col3:
            st.markdown(
                f"<div style='text-align: right; color: #666; font-size: 0.8rem;'>"
                f"© 2025 Sistema Multi-Agente para Novelas<br>"
                f"Ultima actualizacion: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>"
                f"Version: 1.0.0"
                f"</div>",
                unsafe_allow_html=True
            )
    
    def run(self):
        """Ejecuta la aplicacion principal"""
        
        # Inicializar sistema
        self.initialize_system()
        
        # Verificar alertas automaticas
        check_and_create_alerts()
        
        # Renderizar barra lateral y obtener pagina seleccionada
        selected_page = render_main_sidebar(self.rag_manager, self.agent_manager)
        
        # Si no hay pagina seleccionada, usar la del session state
        if not selected_page:
            selected_page = st.session_state.get('page_selector', 'upload')
        else:
            st.session_state.page_selector = selected_page
        
        # Area principal
        self.render_header()
        
        # Renderizar pagina seleccionada
        self.render_main_content(selected_page)
        
        # Footer
        self.render_footer()
        
        # Debug info (solo en desarrollo)
        if st.sidebar.checkbox("🐛 Informacion de Debug", value=False):
            with st.sidebar.expander("Debug Info"):
                st.json({
                    "initialized": st.session_state.initialized,
                    "current_page": selected_page,
                    "manuscript_loaded": bool(st.session_state.manuscript),
                    "analysis_completed": bool(st.session_state.analysis_results),
                    "rag_stats": st.session_state.rag_stats,
                    "processing": st.session_state.processing
                })

def main():
    """Funcion principal de la aplicacion"""
    
    try:
        app = NovelSystemApp()
        app.run()
        
    except Exception as e:
        st.error("❌ Error critico en la aplicacion")
        st.exception(e)
        
        # Opciones de recuperacion
        st.markdown("### 🔧 Opciones de Recuperacion:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reiniciar Aplicacion"):
                # Limpiar session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🧹 Limpiar Cache"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ Cache limpiado")
        
        # Informacion adicional de debug
        with st.expander("📋 Informacion Tecnica"):
            st.code(f"""
Error: {str(e)}
Tipo: {type(e).__name__}
Hora: {datetime.now().isoformat()}
Python: {sys.version}
Streamlit: {st.__version__ if hasattr(st, '__version__') else 'Unknown'}
            """)

# Configuracion adicional
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ejecutar aplicacion
    main()
