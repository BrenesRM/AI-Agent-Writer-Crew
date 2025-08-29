"""
Componente Sidebar para navegación y estado del sistema
"""

import streamlit as st
from streamlit_option_menu import option_menu
from frontend.utils.session_state import get_session_summary, save_session_state, load_session_state, clear_session_state

def render_sidebar():
    """Renderiza la barra lateral con navegación y estado"""
    
    with st.sidebar:
        st.title("📚 Story Enhancer")
        st.markdown("---")
        
        # Menú de navegación principal
        page = option_menu(
            "Navegación",
            ["📄 Documentos", "✍️ Manuscrito", "🤖 Agentes", "📊 Resultados", "⚙️ Configuración"],
            icons=['file-earmark-text', 'pencil-square', 'robot', 'bar-chart', 'gear'],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "#1f77b4", "font-size": "20px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#1f77b4"},
            }
        )
        
        st.markdown("---")
        
        # Estado del sistema
        st.subheader("📊 Estado del Sistema")
        summary = get_session_summary()
        
        # Indicadores de estado
        col1, col2 = st.columns(2)
        with col1:
            # Estado RAG
            if summary['rag_ready']:
                st.markdown("🟢 **RAG:** Listo")
            else:
                st.markdown("🔴 **RAG:** No configurado")
                
            # Estado manuscrito
            if summary['manuscript_loaded']:
                st.markdown("🟢 **Manuscrito:** Cargado")
            else:
                st.markdown("🔴 **Manuscrito:** Faltante")
        
        with col2:
            # Estado procesamiento
            status_icons = {
                'idle': '⚪',
                'running': '🔄',
                'completed': '✅',
                'error': '❌'
            }
            status_icon = status_icons.get(summary['processing_status'], '⚪')
            st.markdown(f"{status_icon} **Estado:** {summary['processing_status'].title()}")
            
            # Iteración actual
            st.markdown(f"🔄 **Iteración:** {summary['current_iteration']}")
        
        # Detalles adicionales
        st.markdown("**📄 Documentos procesados:** " + str(summary['documents_uploaded']))
        if summary['outputs_ready']:
            st.markdown("✅ **Outputs generados**")
        else:
            st.markdown("⏳ **Outputs pendientes**")
            
        st.markdown("---")
        
        # Controles de sesión
        st.subheader("💾 Gestión de Sesión")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar", help="Guardar estado actual"):
                if save_session_state():
                    st.success("Estado guardado")
                else:
                    st.error("Error al guardar")
        
        with col2:
            if st.button("📂 Cargar", help="Cargar estado guardado"):
                if load_session_state():
                    st.success("Estado cargado")
                    st.experimental_rerun()
                else:
                    st.warning("No hay estado guardado")
        
        if st.button("🗑️ Limpiar Todo", help="Reiniciar toda la sesión"):
            clear_session_state()
            st.success("Sesión reiniciada")
            st.experimental_rerun()
            
        st.markdown("---")
        
        # Logs recientes
        st.subheader("📝 Logs Recientes")
        if hasattr(st.session_state, 'agent_logs') and st.session_state.agent_logs:
            # Mostrar los últimos 5 logs
            recent_logs = st.session_state.agent_logs[-5:]
            for log in reversed(recent_logs):
                level_icons = {
                    'info': 'ℹ️',
                    'warning': '⚠️',
                    'error': '❌',
                    'success': '✅'
                }
                icon = level_icons.get(log['level'], 'ℹ️')
                timestamp = log['timestamp'].split('T')[1][:5]  # Solo HH:MM
                st.text(f"{icon} {timestamp} {log['agent'][:8]}: {log['message'][:30]}...")
        else:
            st.text("No hay logs disponibles")
            
        # Botón para ver logs completos
        if st.button("Ver Logs Completos"):
            st.session_state.show_full_logs = True
            
        st.markdown("---")
        
        # Información del sistema
        st.subheader("🔧 Sistema")
        st.text(f"LLM: {st.session_state.get('llm_provider', 'local')}")
        st.text(f"Embeddings: {st.session_state.get('embeddings_provider', 'local')}")
        
        # Información de versión
        st.markdown("---")
        st.caption("Story Enhancer v1.0")
        st.caption("Powered by CrewAI + LangGraph")
    
    return page

def show_status_indicator(status: str, label: str):
    """Muestra un indicador de estado con color"""
    status_colors = {
        'success': 'green',
        'warning': 'orange',
        'error': 'red',
        'info': 'blue',
        'idle': 'gray'
    }
    
    color = status_colors.get(status, 'gray')
    st.markdown(f":{color}[●] **{label}**")

def render_progress_bar(current: int, total: int, label: str = "Progreso"):
    """Renderiza una barra de progreso con etiqueta"""
    progress = current / total if total > 0 else 0
    st.progress(progress)
    st.text(f"{label}: {current}/{total} ({progress:.1%})")