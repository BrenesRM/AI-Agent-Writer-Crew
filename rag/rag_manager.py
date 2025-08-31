import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from .document_processor import DocumentProcessor, ProcessedDocument
from .vector_store import VectorStore

class RAGManager:
    """Gestor principal del sistema RAG"""
    
    def __init__(self, vector_store_path: str = "./rag/vectorstore",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore(vector_store_path, embedding_model)
        self.logger = logging.getLogger(__name__)
    
    def ingest_document(self, file_path: str) -> bool:
        """Ingesta un documento al sistema RAG"""
        try:
            self.logger.info(f"Procesando documento: {file_path}")
            
            # Procesar documento
            processed_docs = self.document_processor.process_document(file_path)
            
            if not processed_docs:
                self.logger.warning(f"No se pudo procesar el documento: {file_path}")
                return False
            
            # Añadir al vector store
            success = self.vector_store.add_documents(processed_docs)
            
            if success:
                self.logger.info(f"Documento ingresado exitosamente: {file_path}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error ingresando documento {file_path}: {str(e)}")
            return False
    
    def ingest_directory(self, directory_path: str) -> Dict[str, bool]:
        """Ingesta todos los documentos de un directorio"""
        directory = Path(directory_path)
        results = {}
        
        if not directory.exists():
            self.logger.error(f"El directorio {directory_path} no existe")
            return results
        
        # Extensiones soportadas
        supported_extensions = {'.pdf', '.docx', '.txt', '.md', '.json', '.xlsx', '.xls'}
        
        for file_path in directory.rglob("*"):
            if file_path.suffix.lower() in supported_extensions:
                results[str(file_path)] = self.ingest_document(str(file_path))
        
        successful = sum(1 for success in results.values() if success)
        self.logger.info(f"Ingresados {successful}/{len(results)} documentos del directorio")
        
        return results
    
    def query(self, question: str, k: int = 5, doc_type: Optional[str] = None) -> Dict[str, Any]:
        """Realiza una consulta al sistema RAG"""
        try:
            # Buscar documentos relevantes
            relevant_docs = self.vector_store.similarity_search(question, k, doc_type)
            
            if not relevant_docs:
                return {
                    "question": question,
                    "answer": "No se encontraron documentos relevantes para la consulta.",
                    "sources": [],
                    "context": ""
                }
            
            # Construir contexto
            context = "\n\n".join([
                f"Documento {i+1}:\n{doc['content']}"
                for i, doc in enumerate(relevant_docs)
            ])
            
            # Preparar fuentes
            sources = [
                {
                    "source": doc['metadata']['source'],
                    "doc_type": doc['metadata']['doc_type'],
                    "chunk_index": doc['metadata']['chunk_index'],
                    "distance": doc['distance']
                }
                for doc in relevant_docs
            ]
            
            return {
                "question": question,
                "context": context,
                "sources": sources,
                "num_sources": len(relevant_docs)
            }
            
        except Exception as e:
            self.logger.error(f"Error en consulta RAG: {str(e)}")
            return {
                "question": question,
                "answer": "Error procesando la consulta.",
                "sources": [],
                "context": ""
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema RAG"""
        return self.vector_store.get_collection_stats()
    
    def remove_document(self, file_path: str) -> bool:
        """Elimina un documento del sistema RAG"""
        return self.vector_store.delete_documents_by_source(file_path)
