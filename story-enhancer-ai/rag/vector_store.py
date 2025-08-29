"""Sistema de almacenamiento vectorial con ChromaDB"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from llama_cpp import Llama

import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

from config.rag_config import rag_config
from utils.text_processors import DocumentProcessor, TextChunker


# ======================
# Local LLM Initialization
# ======================
MODEL_PATH = "./models/llama-3.2-1b-instruct-q8_0.gguf"

# Create a single instance of Llama
llm = Llama(
    model_path=MODEL_PATH,
    n_threads=os.cpu_count() or 4,   # use all available threads if possible
    n_ctx=4096,                      # context window, adjust if model supports more
    verbose=False
)


def agente_query(prompt: str, max_tokens: int = 150) -> str:
    """
    Sends a prompt to the local LLaMA model and returns the response text.
    """
    try:
        result = llm.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95
        )
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"[LLM Error] {str(e)}"


class VectorStore:
    """Manejo del almac�n de vectores con ChromaDB"""

    def __init__(self, collection_name: str = "story_documents"):
        self.collection_name = collection_name
        self.config = rag_config

        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(
            path=self.config.chromadb_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Obtener o crear colecci�n
        try:
            self.collection = self.client.get_collection(
                name=collection_name
            )
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Story enhancement documents"}
            )

        # Inicializar modelo de embeddings
        self._init_embeddings()

        # Inicializar procesadores
        self.doc_processor = DocumentProcessor()
        self.text_chunker = TextChunker()

    def _init_embeddings(self):
        """Inicializar modelo de embeddings"""
        openai_key = os.getenv("OPENAI_API_KEY")

        if openai_key and openai_key != "your_openai_key_here":
            # Usar OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=openai_key,
                model=self.config.embedding_model
            )
            self.use_openai = True
        else:
            # Usar modelo local
            print("??  OpenAI API key no encontrada, usando modelo local...")
            self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_openai = False

    # --- the rest of VectorStore remains unchanged ---

    """Manejo del almacén de vectores con ChromaDB"""

    def add_document(self, file_path: str) -> Dict[str, Any]:
        """Agregar documento al vector store"""
        try:
            # Procesar documento
            doc_data = self.doc_processor.process_file(file_path)

            # Dividir en chunks
            chunks = self.text_chunker.chunk_text(
                doc_data['content'],
                doc_data['metadata']
            )

            if not chunks:
                return {"status": "error", "message": "No se pudieron extraer chunks del documento"}

            # Generar embeddings y agregar a ChromaDB
            texts = [chunk['text'] for chunk in chunks]
            metadatas = []
            ids = []

            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_data['filename']}_{i}_{str(uuid.uuid4())[:8]}"
                ids.append(chunk_id)

                # Preparar metadata para ChromaDB
                metadata = chunk['metadata'].copy()
                metadata['source_file'] = doc_data['filename']
                metadata['file_extension'] = doc_data['extension']

                # ChromaDB requiere que todos los valores de metadata sean strings, ints o floats
                clean_metadata = {}
                for key, value in metadata.items():
                    if isinstance(value, (str, int, float)):
                        clean_metadata[key] = value
                    else:
                        clean_metadata[key] = str(value)

                metadatas.append(clean_metadata)

            # Generar embeddings
            if self.use_openai:
                embeddings_list = self.embeddings.embed_documents(texts)
            else:
                embeddings_list = self.embeddings.encode(texts).tolist()

            # Agregar a ChromaDB
            self.collection.add(
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )

            return {
                "status": "success",
                "message": f"Documento procesado: {len(chunks)} chunks agregados",
                "document": doc_data['filename'],
                "chunks_count": len(chunks),
                "total_characters": len(doc_data['content'])
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error procesando documento: {str(e)}"
            }

    def search(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Buscar documentos similares"""
        k = k or self.config.max_results

        try:
            # Generar embedding de la query
            if self.use_openai:
                query_embedding = self.embeddings.embed_query(query)
            else:
                query_embedding = self.embeddings.encode([query])[0].tolist()

            # Buscar en ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=['documents', 'metadatas', 'distances']
            )

            # Formatear resultados
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity': 1 - results['distances'][0][i],  # Convertir distancia a similitud
                    'source': results['metadatas'][0][i].get('source_file', 'unknown')
                })

            # Filtrar por threshold de similitud
            filtered_results = [
                r for r in formatted_results
                if r['similarity'] >= self.config.similarity_threshold
            ]

            return filtered_results

        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            return []

    def get_collection_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la colección"""
        try:
            count = self.collection.count()

            # Obtener muestra de documentos para estadísticas
            if count > 0:
                sample = self.collection.get(limit=min(100, count), include=['metadatas'])

                # Contar documentos únicos
                unique_files = set()
                extensions = {}

                for metadata in sample['metadatas']:
                    if 'source_file' in metadata:
                        unique_files.add(metadata['source_file'])

                    if 'file_extension' in metadata:
                        ext = metadata['file_extension']
                        extensions[ext] = extensions.get(ext, 0) + 1

                return {
                    "total_chunks": count,
                    "unique_documents": len(unique_files),
                    "file_extensions": extensions,
                    "collection_name": self.collection_name,
                    "embedding_model": self.config.embedding_model
                }
            else:
                return {
                    "total_chunks": 0,
                    "unique_documents": 0,
                    "file_extensions": {},
                    "collection_name": self.collection_name,
                    "embedding_model": self.config.embedding_model
                }

        except Exception as e:
            return {"error": str(e)}

    def clear_collection(self):
        """Limpiar la colección (usar con cuidado)"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Story enhancement documents"}
            )
            return {"status": "success", "message": "Colección limpiada"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
