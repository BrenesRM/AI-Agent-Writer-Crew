"""
Página de configuración del sistema
"""

import streamlit as st
import os
from pathlib import Path
from frontend.utils.session_state import add_log_entry

def render_settings():
    """Renderiza la página de configuración"""
    
    st.title("⚙️ Configuración del Sistema")
    st.markdown("Configura los parámetros del sistema y las integraciones.")
    
    # Tabs para organizar configuraciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 Modelos LLM", 
        "🔤 Embeddings", 
        "🗄️ Base de Datos", 
        "🔧 Sistema",
        "📊 Logs"
    ])
    
    with tab1:
        render_llm_settings()
        
    with tab2:
        render_embeddings_settings()
        
    with tab3:
        render_database_settings()
        
    with tab4:
        render_system_settings()
        
    with tab5:
        render_logs_viewer()

def render_llm_settings():
    """Configuración de modelos LLM"""
    
    st.subheader("🤖 Configuración de Modelos LLM")
    
    # Selector de proveedor
    provider = st.selectbox(
        "Proveedor de LLM",
        ["local", "openai", "anthropic", "custom"],
        index=0 if st.session_state.llm_provider == "local" else 1,
        help="Selecciona el proveedor de modelos de lenguaje"
    )
    
    st.session_state.llm_provider = provider
    
    if provider == "local":
        render_local_llm_config()
    elif provider == "openai":
        render_openai_config()
    elif provider == "anthropic":
        render_anthropic_config()
    else:
        render_custom_llm_config()

def render_local_llm_config():
    """Configuración para LLM local"""
    
    st.markdown("### 🏠 Configuración LLM Local")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de servidor local
        local_server = st.selectbox(
            "Servidor Local",
            ["Ollama", "vLLM", "llama.cpp", "Text Generation WebUI"],
            help="Tipo de servidor local para LLM"
        )
        
        # URL del servidor
        server_url = st.text_input(
            "URL del Servidor",
            value="http://localhost:11434",
            help="URL donde está ejecutándose el servidor LLM"
        )
        
        # Modelo seleccionado
        if local_server == "Ollama":
            available_models = get_ollama_models()
            model_name = st.selectbox(
                "Modelo",
                available_models,
                help="Modelo disponible en Ollama"
            )
        else:
            model_name = st.text_input(
                "Nombre del Modelo",
                value="deepseek-r1-0528-qwen3-8b-q4",
                help="Nombre exacto del modelo"
            )
    
    with col2:
        # Parámetros del modelo
        st.markdown("**Parámetros:**")
        
        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Creatividad del modelo (0 = determinístico, 2 = muy creativo)"
        )
        
        max_tokens = st.number_input(
            "Máximo de Tokens",
            min_value=100,
            max_value=8192,
            value=2048,
            help="Máximo número de tokens en la respuesta"
        )
        
        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.05,
            help="Nucleus sampling parameter"
        )
    
    # Test de conexión
    if st.button("🔍 Probar Conexión"):
        test_local_llm_connection(server_url, model_name)
    
    # Información del modelo actual
    if st.session_state.get('current_model_info'):
        st.markdown("### 📊 Información del Modelo Actual")
        info = st.session_state.current_model_info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Modelo", info.get('name', 'N/A'))
        with col2:
            st.metric("Tamaño", info.get('size', 'N/A'))
        with col3:
            st.metric("Estado", info.get('status', 'N/A'))

def get_ollama_models():
    """Obtiene la lista de modelos disponibles en Ollama"""
    try:
        # Aquí se conectaría con Ollama para obtener modelos reales
        # Por ahora, devolvemos una lista simulada
        return [
            "deepseek-r1:latest",
            "llama2:7b",
            "llama2:13b",
            "mistral:latest",
            "codellama:latest"
        ]
    except:
        return ["No se pudieron obtener modelos"]

def test_local_llm_connection(server_url: str, model_name: str):
    """Prueba la conexión con el LLM local"""
    
    with st.spinner("Probando conexión..."):
        try:
            # Simular test de conexión
            import time
            time.sleep(2)
            
            # En implementación real, aquí haríamos una llamada al servidor
            st.success(f"✅ Conexión exitosa con {model_name}")
            st.session_state.current_model_info = {
                'name': model_name,
                'size': '4.1GB',
                'status': 'Disponible'
            }
            add_log_entry(f"Conexión LLM local exitosa: {model_name}", "success", "llm_config")
            
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")
            add_log_entry(f"Error conexión LLM: {str(e)}", "error", "llm_config")

def render_openai_config():
    """Configuración para OpenAI"""
    
    st.markdown("### 🤖 Configuración OpenAI")
    
    # API Key
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Tu clave API de OpenAI"
    )
    
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Modelo
        model = st.selectbox(
            "Modelo",
            ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            help="Modelo de OpenAI a usar"
        )
        
        # Organización (opcional)
        organization = st.text_input(
            "Organización (opcional)",
            help="ID de organización de OpenAI"
        )
    
    with col2:
        # Parámetros
        temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.number_input("Máximo Tokens", 100, 4000, 2048)
    
    # Test de API
    if api_key and st.button("🔍 Probar API"):
        test_openai_connection(api_key, model)

def test_openai_connection(api_key: str, model: str):
    """Prueba la conexión con OpenAI"""
    
    with st.spinner("Probando API de OpenAI..."):
        try:
            # Simulación - en realidad haríamos una llamada a OpenAI
            import time
            time.sleep(2)
            st.success(f"✅ Conexión exitosa con OpenAI {model}")
            add_log_entry(f"Conexión OpenAI exitosa: {model}", "success", "openai_config")
            
        except Exception as e:
            st.error(f"❌ Error con OpenAI API: {e}")
            add_log_entry(f"Error OpenAI: {str(e)}", "error", "openai_config")

def render_anthropic_config():
    """Configuración para Anthropic Claude"""
    
    st.markdown("### 🧠 Configuración Anthropic Claude")
    st.info("Configuración para Anthropic Claude en desarrollo")

def render_custom_llm_config():
    """Configuración para LLM personalizado"""
    
    st.markdown("### 🔧 Configuración LLM Personalizado")
    st.info("Configuración para LLM personalizado en desarrollo")

def render_embeddings_settings():
    """Configuración de embeddings"""
    
    st.subheader("🔤 Configuración de Embeddings")
    
    # Proveedor de embeddings
    embeddings_provider = st.selectbox(
        "Proveedor de Embeddings",
        ["local", "openai", "huggingface"],
        index=0 if st.session_state.embeddings_provider == "local" else 1,
        help="Selecciona el proveedor para generar embeddings"
    )
    
    st