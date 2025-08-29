#"""Configuración del sistema RAG"""
import os
from typing import List, Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class RAGConfig(BaseModel):
    """Configuración para el sistema RAG"""
    
    # Vector Database
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "chromadb")
    chromadb_path: str = os.getenv("CHROMADB_PATH", "./chromadb")
    
    # Embeddings
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embedding_dimension: int = 1536  # OpenAI text-embedding-3-small
    
    # Text Processing
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Search Parameters
    similarity_threshold: float = 0.7
    max_results: int = 10
    
    # File Processing
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    allowed_extensions: List[str] = [
        "pdf", "docx", "txt", "json", "md", "xlsx"
    ]
    
    # Paths
    documents_path: str = "data/documents"
    processed_path: str = "data/processed"
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Configuración para OpenAI"""
        return {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": self.embedding_model
        }

# Instancia global de configuración
rag_config = RAGConfig()