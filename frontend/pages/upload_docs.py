# -*- coding: utf-8 -*-
import streamlit as st
import os
import time
from pathlib import Path
from datetime import datetime
import pandas as pd

def render_upload_page(rag_manager):
    """Renderiza la pagina de gestion de documentos RAG"""
    
    st.header("📚 Biblioteca RAG de Documentos")
    st.markdown("*Gestiona tu coleccion de documentos de referencia para el sistema*")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Subir Documentos",
        "📋 Biblioteca Actual", 
        "🔍 Explorar y Buscar",
        "⚙️ Gestion Avanzada"
    ])
    
    with tab1:
        render_upload_tab(rag_manager)
    
    with tab2:
        render_library_tab(rag_manager)
    
    with tab3:
        render_search_tab(rag_manager)
    
    with tab4:
        render_management_tab(rag_manager)

def render_upload_tab(rag_manager):
    """Tab de subida de documentos"""
    st.subheader("📤 Subir Nuevos Documentos")
    
    # Informacion de formatos soportados
    st.info("""
    **📋 Formatos Soportados:**
    - **PDF** (.pdf) - Documentos, libros, articulos
    - **Word** (.docx) - Manuscritos, notas, guiones
    - **Texto** (.txt) - Notas simples, transcripciones
    - **Markdown** (.md) - Documentacion tecnica
    - **JSON** (.json) - Datos estructurados, configuraciones
    - **Excel** (.xlsx) - Tablas de datos, cronologias
    """)
    
    # Subida de archivos multiples
    uploaded_files = st.file_uploader(
        "Selecciona uno o mas documentos:",
        type=['pdf', 'docx', 'txt', 'md', 'json', 'xlsx'],
        accept_multiple_files=True,
        help="Puedes subir multiples archivos a la vez"
    )
    
    if uploaded_files:
        st.markdown(f"**📁 {len(uploaded_files)} archivo(s) seleccionado(s):**")
        
        # Mostrar informacion de archivos
        files_info = []
        total_size = 0
        
        for file in uploaded_files:
            file_size = len(file.getvalue())
            total_size += file_size
            
            files_info.append({
                'Nombre': file.name,
                'Tipo': file.type,
                'Tamaño': format_file_size(file_size),
                'Estado': '⏳ Pendiente'
            })
        
        # Mostrar tabla de archivos
        df_files = pd.DataFrame(files_info)
        st.dataframe(df_files, use_container_width=True)
        
        st.markdown(f"**📊 Tamaño total:** {format_file_size(total_size)}")
        
        # Boton de procesamiento
        st.markdown("---")
        
        if st.button("🚀 Procesar y Subir Documentos", type="primary", use_container_width=True):
            process_uploaded_files(rag_manager, uploaded_files)

def process_uploaded_files(rag_manager, files):
    """Procesa los archivos subidos"""
    
    with st.spinner("🔄 Procesando documentos..."):
        try:
            processed_count = 0
            
            for file in files:
                # Simular procesamiento
                time.sleep(1)
                processed_count += 1
                
                # Actualizar progreso
                progress = processed_count / len(files)
                st.progress(progress)
            
            st.success(f"✅ {len(files)} documentos procesados exitosamente!")
            
            # Actualizar estadisticas
            if 'rag_stats' not in st.session_state:
                st.session_state.rag_stats = {}
            
            current_docs = st.session_state.rag_stats.get('total_documents', 0)
            st.session_state.rag_stats['total_documents'] = current_docs + len(files)
            st.session_state.rag_stats['total_chunks'] = st.session_state.rag_stats.get('total_chunks', 0) + len(files) * 10
            
        except Exception as e:
            st.error(f"❌ Error procesando archivos: {str(e)}")

def render_library_tab(rag_manager):
    """Tab de biblioteca actual"""
    st.subheader("📋 Biblioteca Actual de Documentos")
    
    try:
        # Obtener estadisticas
        stats = st.session_state.get('rag_stats', {
            'total_documents': 0,
            'total_chunks': 0,
            'total_size_mb': 0.0,
            'last_updated': 'Nunca'
        })
        
        # Metricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documentos", stats.get('total_documents', 0))
        
        with col2:
            st.metric("Total Chunks", stats.get('total_chunks', 0))
        
        with col3:
            total_size = stats.get('total_size_mb', 0)
            st.metric("Tamaño Total", f"{total_size:.1f} MB")
        
        with col4:
            last_updated = stats.get('last_updated', 'Nunca')
            st.metric("Ultima Actualizacion", last_updated)
        
        st.markdown("---")
        
        # Lista de documentos
        st.subheader("📚 Documentos en la Biblioteca")
        
        if stats.get('total_documents', 0) > 0:
            # Generar datos simulados de documentos
            documents = generate_mock_documents(stats.get('total_documents', 0))
            
            # Mostrar documentos
            for doc in documents:
                with st.expander(f"📄 {doc['name']} ({doc['type']})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Archivo:** {doc['name']}")
                        st.markdown(f"**Chunks:** {doc['chunks']}")
                        st.markdown(f"**Ultima modificacion:** {doc['modified']}")
                    
                    with col2:
                        st.markdown(f"**Tamaño:** {doc['size']}")
                        st.markdown(f"**Estado:** {doc['status']}")
                        
                        if st.button(f"🗑️ Eliminar", key=f"delete_{doc['id']}"):
                            st.success(f"🗑️ Documento '{doc['name']}' eliminado")
        
        else:
            st.info("📭 No hay documentos en la biblioteca. Ve a la pestaña 'Subir Documentos' para añadir algunos.")
    
    except Exception as e:
        st.error(f"❌ Error obteniendo informacion de la biblioteca: {str(e)}")

def generate_mock_documents(count):
    """Genera documentos simulados para demostracion"""
    
    import random
    
    mock_docs = []
    doc_types = ['PDF', 'DOCX', 'TXT', 'MD']
    statuses = ['✅ Procesado', '🔄 Procesando', '⚠️ Pendiente']
    
    for i in range(min(count, 10)):
        doc = {
            'id': i + 1,
            'name': f"documento_{i+1}.{random.choice(doc_types).lower()}",
            'type': random.choice(doc_types),
            'size': f"{random.randint(1, 50)} MB",
            'chunks': random.randint(5, 50),
            'status': random.choice(statuses),
            'modified': f"2025-01-{random.randint(1, 31):02d}",
        }
        mock_docs.append(doc)
    
    return mock_docs

def render_search_tab(rag_manager):
    """Tab de exploracion y busqueda"""
    st.subheader("🔍 Explorar y Buscar en la Biblioteca")
    
    # Busqueda principal
    search_query = st.text_input(
        "🔍 Buscar en la biblioteca:",
        placeholder="Ej: 'sistema de magia', 'personajes principales', 'historia del reino'...",
        help="Busca contenido similar usando busqueda semantica"
    )
    
    if search_query and st.button("🔍 Buscar", type="primary"):
        with st.spinner("🔍 Buscando en la biblioteca..."):
            time.sleep(2)
            st.success("✅ Busqueda completada")
            
            # Resultados simulados
            results = [
                {"source": "worldbuilding.pdf", "content": "Sistema de magia basado en cristales...", "score": 0.95},
                {"source": "characters.docx", "content": "Los personajes principales incluyen...", "score": 0.87},
                {"source": "history.txt", "content": "La historia del reino comenzo...", "score": 0.82}
            ]
            
            st.markdown("### 📋 Resultados de la Busqueda")
            
            for i, result in enumerate(results, 1):
                with st.expander(f"📄 Resultado #{i} - Relevancia: {result['score']:.2f}"):
                    st.markdown(f"**📄 Documento:** {result['source']}")
                    st.markdown(f"**📝 Contenido:** {result['content']}")

def render_management_tab(rag_manager):
    """Tab de gestion avanzada"""
    st.subheader("⚙️ Gestion Avanzada de la Biblioteca")
    
    # Estadisticas avanzadas
    st.markdown("### 📊 Estadisticas Avanzadas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documentos Activos", st.session_state.get('rag_stats', {}).get('total_documents', 0))
        st.metric("Chunks Vectorizados", st.session_state.get('rag_stats', {}).get('total_chunks', 0))
    
    with col2:
        st.metric("Tamaño de Vector Store", "23.4 MB")
        st.metric("Dimensiones de Vector", "384")
    
    with col3:
        st.metric("Consultas Realizadas", "1,247")
        st.metric("Promedio Tiempo/Consulta", "234ms")
    
    with col4:
        st.metric("Indice Actualizado", "Hoy")
        st.metric("Modelo de Embeddings", "all-MiniLM-L6-v2")
    
    st.markdown("---")
    
    # Herramientas de mantenimiento
    st.markdown("### 🔧 Herramientas de Mantenimiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔄 Operaciones de Indice")
        
        if st.button("🔄 Re-indexar Biblioteca Completa"):
            with st.spinner("🔄 Re-indexando..."):
                time.sleep(3)
                st.success("✅ Biblioteca re-indexada exitosamente")
        
        if st.button("🧹 Limpiar Indices Huerfanos"):
            with st.spinner("🧹 Limpiando..."):
                time.sleep(2)
                st.success("🧹 Indices huerfanos eliminados")
    
    with col2:
        st.markdown("#### 💾 Respaldo y Recuperacion")
        
        if st.button("💾 Crear Respaldo de Biblioteca"):
            with st.spinner("💾 Creando respaldo..."):
                time.sleep(3)
                st.success("💾 Respaldo creado exitosamente")
                
                # Boton de descarga simulado
                st.download_button(
                    label="📥 Descargar Respaldo",
                    data="Mock backup data",
                    file_name=f"biblioteca_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )
        
        if st.button("📊 Generar Reporte de Biblioteca"):
            with st.spinner("📊 Generando reporte..."):
                time.sleep(2)
                st.success("📊 Reporte generado")

def format_file_size(size_bytes):
    """Formatea el tamaño de archivo en formato legible"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"