"""
Gestión del estado de sesión para Streamlit
"""

import streamlit as st
from typing import Dict, Any, List
from pathlib import Path
import json

def init_session_state():
    """Inicializa todas las variables de estado de sesión"""
    
    # Estado general de la aplicación
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
    # Documentos de referencia
    if 'uploaded_documents' not in st.session_state:
        st.session_state.uploaded_documents = []
        
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = []
        
    if 'rag_ready' not in st.session_state:
        st.session_state.rag_ready = False
        
    # Manuscrito
    if 'manuscript_content' not in st.session_state:
        st.session_state.manuscript_content = ""
        
    if 'manuscript_file' not in st.session_state:
        st.session_state.manuscript_file = None
        
    # Estado de agentes
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
        
    if 'current_iteration' not in st.session_state:
        st.session_state.current_iteration = 0
        
    if 'max_iterations' not in st.session_state:
        st.session_state.max_iterations = 3
        
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = "idle"  # idle, running, completed, error
        
    if 'agent_logs' not in st.session_state:
        st.session_state.agent_logs = []
        
    # Outputs finales
    if 'final_outputs' not in st.session_state:
        st.session_state.final_outputs = {
            'enhanced_story': None,
            'story_bible': None,
            'character_guide': None,
            'visual_prompts': None
        }
        
    # Configuraciones
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = "local"  # local, openai
        
    if 'embeddings_provider' not in st.session_state:
        st.session_state.embeddings_provider = "local"  # local, openai

def get_session_summary() -> Dict[str, Any]:
    """Retorna un resumen del estado actual de la sesión"""
    return {
        'documents_uploaded': len(st.session_state.uploaded_documents),
        'rag_ready': st.session_state.rag_ready,
        'manuscript_loaded': bool(st.session_state.manuscript_content),
        'current_iteration': st.session_state.current_iteration,
        'processing_status': st.session_state.processing_status,
        'outputs_ready': any(st.session_state.final_outputs.values())
    }

def save_session_state(filepath: str = "session_backup.json"):
    """Guarda el estado de sesión en un archivo"""
    try:
        # Crear un diccionario serializable
        state_to_save = {
            'uploaded_documents': st.session_state.uploaded_documents,
            'processed_documents': st.session_state.processed_documents,
            'rag_ready': st.session_state.rag_ready,
            'manuscript_content': st.session_state.manuscript_content,
            'current_iteration': st.session_state.current_iteration,
            'max_iterations': st.session_state.max_iterations,
            'processing_status': st.session_state.processing_status,
            'agent_logs': st.session_state.agent_logs,
            'final_outputs': st.session_state.final_outputs,
            'llm_provider': st.session_state.llm_provider,
            'embeddings_provider': st.session_state.embeddings_provider
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state_to_save, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        st.error(f"Error guardando estado de sesión: {e}")
        return False

def load_session_state(filepath: str = "session_backup.json"):
    """Carga el estado de sesión desde un archivo"""
    try:
        if not Path(filepath).exists():
            return False
            
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_state = json.load(f)
            
        # Cargar estado guardado
        for key, value in saved_state.items():
            st.session_state[key] = value
            
        return True
    except Exception as e:
        st.error(f"Error cargando estado de sesión: {e}")
        return False

def clear_session_state():
    """Limpia todo el estado de sesión"""
    keys_to_keep = ['initialized']  # Mantener algunas claves básicas
    
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    
    # Re-inicializar
    init_session_state()

def add_log_entry(message: str, level: str = "info", agent: str = "system"):
    """Agrega una entrada al log de la sesión"""
    from datetime import datetime
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'agent': agent,
        'message': message
    }
    
    st.session_state.agent_logs.append(log_entry)
    
    # Mantener solo los últimos 1000 logs
    if len(st.session_state.agent_logs) > 1000:
        st.session_state.agent_logs = st.session_state.agent_logs[-1000:]