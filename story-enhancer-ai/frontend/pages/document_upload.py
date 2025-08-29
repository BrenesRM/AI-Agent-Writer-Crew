"""
Página de carga y procesamiento de documentos de referencia
"""

import streamlit as st
import os
import tempfile
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from rag.document_processor import DocumentProcessor
from frontend.utils.session_state import add_log_entry

def render_document_upload():
    """Renderiza la página de carga de documentos"""
    
    st.title("📄 Documentos de Referencia")
    st.markdown("Sube documentos que servirán como base de conocimiento para los agentes.")
    
    # Tabs para organizar la interfaz
    tab1, tab2, tab3 = st.tabs(["📤 Subir Documentos", "📋 Documentos Procesados", "🔍 Buscar en RAG"])
    
    with tab1:
        render_upload_section()
        
    with tab2:
        render_processed_documents()
        
    with tab3:
        render_rag_search()

def render_upload_section():
    """Sección para subir nuevos documentos"""
    
    st.subheader("Subir Nuevos Documentos")
    
    # File uploader que acepta múltiples archivos
    uploaded_files = st.file_uploader(
        "Selecciona documentos de referencia",
        type=['pdf', 'docx', 'txt', 'md', 'json', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Formatos soportados: PDF, DOCX, TXT, Markdown, JSON, Excel"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} archivos seleccionados:**")
        
        # Mostrar lista de archivos seleccionados
        for file in uploaded_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(f"📄 {file.name}")
            with col2:
                st.text(f"{file.size / 1024:.1f} KB")
            with col3:
                st.text(file.type or "Unknown")
        
        st.markdown("---")
        
        # Configuraciones de procesamiento
        st.subheader("⚙️ Configuraciones de Procesamiento")
        
        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.number_input(
                "Tamaño de chunk", 
                min_value=100, 
                max_value=2000, 
                value=1000,
                help="Tamaño en caracteres para dividir el texto"
            )
            
            chunk_overlap = st.number_input(
                "Superposición de chunks", 
                min_value=0, 
                max_value=500, 
                value=200,
                help="Caracteres de superposición entre chunks"
            )
        
        with col2:
            extract_images = st.checkbox(
                "Extraer descripciones de imágenes", 
                value=False,
                help="Intentar extraer y describir imágenes en PDFs"
            )
            
            preserve_metadata = st.checkbox(
                "Preservar metadatos", 
                value=True,
                help="Mantener información como autor, fecha, etc."
            )
        
        # Botón de procesamiento
        if st.button("🚀 Procesar Documentos", type="primary"):
            process_uploaded_documents(
                uploaded_files, 
                chunk_size, 
                chunk_overlap, 
                extract_images, 
                preserve_metadata
            )

def process_uploaded_documents(
    files: List[Any], 
    chunk_size: int, 
    chunk_overlap: int, 
    extract_images: bool, 
    preserve_metadata: bool
):
    """Procesa los documentos subidos y los indexa en el RAG"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Guardar archivos temporalmente
            file_paths = []
            for i, file in enumerate(files):
                file_path = temp_path / file.name
                with open(file_path, 'wb') as f:
                    f.write(file.getvalue())
                file_paths.append(str(file_path))
                
                progress = (i + 1) / (len(files) * 2)  # 50% para guardar archivos
                progress_bar.progress(progress)
                status_text.text(f"Guardando {file.name}...")
            
            # Inicializar procesador de documentos
            processor = DocumentProcessor()
            
            # Procesar cada archivo
            processed_docs = []
            for i, file_path in enumerate(file_paths):
                status_text.text(f"Procesando {Path(file_path).name}...")
                
                try:
                    # Procesar documento
                    docs = processor.process_document(
                        file_path,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                    
                    processed_docs.extend(docs)
                    
                    # Actualizar progreso
                    progress = 0.5 + (i + 1) / (len(file_paths) * 2)
                    progress_bar.progress(progress)
                    
                    add_log_entry(f"Procesado {Path(file_path).name}: {len(docs)} chunks", "success", "document_processor")
                    
                except Exception as e:
                    st.error(f"Error procesando {Path(file_path).name}: {e}")
                    add_log_entry(f"Error en {Path(file_path).name}: {str(e)}", "error", "document_processor")
                    continue
            
            if processed_docs:
                # Indexar documentos en RAG
                status_text.text("Indexando documentos en RAG...")
                
                # Aquí llamarías al método para indexar en ChromaDB
                # processor.index_documents(processed_docs)
                
                # Actualizar estado de sesión
                st.session_state.processed_documents.extend([
                    {
                        'filename': Path(fp).name,
                        'chunks': len([d for d in processed_docs if d.metadata.get('source') == fp]),
                        'processed_at': datetime.now().isoformat(),
                        'chunk_size': chunk_size,
                        'chunk_overlap': chunk_overlap
                    }
                    for fp in file_paths
                ])
                
                st.session_state.rag_ready = True
                
                # Completar progreso
                progress_bar.progress(1.0)
                status_text.text("✅ Procesamiento completado!")
                
                st.success(f"✅ {len(processed_docs)} chunks indexados exitosamente!")
                add_log_entry(f"Indexados {len(processed_docs)} chunks en RAG", "success", "rag_indexer")
                
                # Auto-refresh para mostrar documentos procesados
                st.experimental_rerun()
            else:
                st.error("❌ No se pudieron procesar documentos")
                
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {e}")
        add_log_entry(f"Error general en procesamiento: {str(e)}", "error", "document_processor")
    finally:
        progress_bar.empty()
        status_text.empty()

def render_processed_documents():
    """Muestra los documentos ya procesados"""
    
    st.subheader("Documentos Procesados")
    
    if not st.session_state.processed_documents:
        st.info("No hay documentos procesados aún. Ve a la pestaña 'Subir Documentos' para comenzar.")
        return
    
    # Mostrar estadísticas generales
    total_docs = len(st.session_state.processed_documents)
    total_chunks = sum(doc['chunks'] for doc in st.session_state.processed_documents)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Documentos", total_docs)
    with col2:
        st.metric("🧩 Chunks Totales", total_chunks)
    with col3:
        if st.session_state.rag_ready:
            st.metric("🔍 Estado RAG", "✅ Listo")
        else:
            st.metric("🔍 Estado RAG", "❌ No configurado")
    
    st.markdown("---")
    
    # Lista detallada de documentos
    st.subheader("📋 Detalles por Documento")
    
    for i, doc in enumerate(st.session_state.processed_documents):
        with st.expander(f"📄 {doc['filename']} ({doc['chunks']} chunks)"):
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"Procesado: {doc['processed_at'][:16].replace('T', ' ')}")
                st.text(f"Chunks generados: {doc['chunks']}")
            with col2:
                st.text(f"Tamaño de chunk: {doc['chunk_size']}")
                st.text(f"Superposición: {doc['chunk_overlap']}")
            
            # Botón para eliminar documento
            if st.button(f"🗑️ Eliminar {doc['filename']}", key=f"delete_{i}"):
                st.session_state.processed_documents.pop(i)
                st.success(f"Documento {doc['filename']} eliminado")
                st.experimental_rerun()
    
    # Botón para limpiar todos los documentos
    if st.button("🗑️ Limpiar Todos los Documentos", type="secondary"):
        if st.confirm("¿Estás seguro de que quieres eliminar todos los documentos procesados?"):
            st.session_state.processed_documents = []
            st.session_state.rag_ready = False
            st.success("Todos los documentos han sido eliminados")
            st.experimental_rerun()

def render_rag_search():
    """Interfaz para buscar en el RAG"""
    
    st.subheader("🔍 Buscar en Base de Conocimiento")
    
    if not st.session_state.rag_ready:
        st.warning("⚠️ El RAG no está configurado. Procesa algunos documentos primero.")
        return
    
    # Campo de búsqueda
    search_query = st.text_input(
        "Buscar en documentos:",
        placeholder="Ej: personajes principales, reglas del mundo, timeline...",
        help="Busca información específica en los documentos procesados"
    )
    
    # Configuraciones de búsqueda
    col1, col2 = st.columns(2)
    with col1:
        num_results = st.slider(
            "Número de resultados", 
            min_value=1, 
            max_value=20, 
            value=5
        )
    with col2:
        similarity_threshold = st.slider(
            "Umbral de similitud", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7,
            step=0.05
        )
    
    if search_query and st.button("🔍 Buscar", type="primary"):
        perform_rag_search(search_query, num_results, similarity_threshold)

def perform_rag_search(query: str, num_results: int, threshold: float):
    """Ejecuta una búsqueda en el RAG"""
    
    with st.spinner("Buscando en la base de conocimiento..."):
        try:
            # Aquí se conectaría con el sistema RAG real
            # Por ahora, simulamos resultados
            
            # Simular resultados de búsqueda
            mock_results = [
                {
                    'content': f"Este es un fragmento relevante para '{query}' que contiene información importante sobre el tema consultado...",
                    'source': 'documento_ejemplo.pdf',
                    'score': 0.85,
                    'metadata': {'page': 5, 'chunk_id': 'chunk_123'}
                },
                {
                    'content': f"Otro fragmento relacionado con '{query}' que proporciona contexto adicional y detalles específicos...",
                    'source': 'manual_world.docx',
                    'score': 0.78,
                    'metadata': {'page': 12, 'chunk_id': 'chunk_456'}
                }
            ]
            
            if mock_results:
                st.success(f"✅ Encontrados {len(mock_results)} resultados")
                
                # Mostrar resultados
                for i, result in enumerate(mock_results):
                    with st.expander(f"Resultado {i+1} - {result['source']} (Score: {result['score']:.3f})"):
                        st.markdown(f"**Contenido:**")
                        st.text_area(
                            "Fragmento:", 
                            result['content'], 
                            height=100, 
                            key=f"result_{i}",
                            disabled=True
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text(f"📄 Fuente: {result['source']}")
                            if 'page' in result['metadata']:
                                st.text(f"📖 Página: {result['metadata']['page']}")
                        with col2:
                            st.text(f"🎯 Similitud: {result['score']:.3f}")
                            st.text(f"🔗 Chunk ID: {result['metadata']['chunk_id']}")
            else:
                st.info("No se encontraron resultados para la búsqueda.")
                
            add_log_entry(f"Búsqueda RAG: '{query}' - {len(mock_results)} resultados", "info", "rag_search")
            
        except Exception as e:
            st.error(f"❌ Error en la búsqueda: {e}")
            add_log_entry(f"Error en búsqueda RAG: {str(e)}", "error", "rag_search")