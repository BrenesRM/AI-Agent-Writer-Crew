# -*- coding: utf-8 -*-
import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain.schema import Document

class VectorStore:
    """Gestor del almacen vectorial con ChromaDB"""
    
    def __init__(self, persist_directory: str = "./rag/vectorstore", 
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model
        self.logger = logging.getLogger(__name__)
        
        # Crear directorio si no existe
        os.makedirs(persist_directory, exist_ok=True)
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Cargar modelo de embeddings
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Coleccion principal
        self.collection_name = "novel_documents"
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Obtiene o crea la coleccion principal"""
        try:
            return self.client.get_collection(name=self.collection_name)
        except Exception:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos para sistema multi-agente de novelas"}
            )
    
    def add_documents(self, processed_docs: List[Any]) -> bool:
        """Añade documentos procesados al vector store"""
        try:
            if not processed_docs:
                self.logger.warning("No hay documentos para añadir")
                return False
            
            # Preparar datos para ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(processed_docs):
                documents.append(doc.content)
                metadatas.append(doc.metadata)
                ids.append(f"{doc.source}_{doc.metadata.get('chunk_index', i)}")
            
            # Generar embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Añadir a ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
            self.logger.info(f"Añadidos {len(documents)} chunks al vector store")
            return True
            
        except Exception as e:
            self.logger.error(f"Error añadiendo documentos: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 5, 
                         doc_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Busqueda por similitud en el vector store"""
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Preparar filtros
            where_clause = {}
            if doc_type:
                where_clause["doc_type"] = doc_type
            
            # Realizar busqueda
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=where_clause if where_clause else None,
                include=["documents", "metadatas", "distances"]
            )
            
            # Formatear resultados
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error en busqueda: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Obtiene estadisticas de la coleccion"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "embedding_model": self.embedding_model_name,
                "collection_name": self.collection_name
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo estadisticas: {str(e)}")
            return {}
    
    def delete_documents_by_source(self, source: str) -> bool:
        """Elimina documentos por fuente"""
        try:
            # Obtener IDs de documentos de la fuente
            results = self.collection.get(
                where={"source": source},
                include=["documents"]
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                self.logger.info(f"Eliminados {len(results['ids'])} documentos de {source}")
                return True
            else:
                self.logger.info(f"No se encontraron documentos de {source}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error eliminando documentos: {str(e)}")
            return False
