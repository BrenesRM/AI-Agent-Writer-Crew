#"""Sistema de ingesta masiva de documentos"""
import os
from typing import List, Dict, Any
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from rag.vector_store import VectorStore
from config.rag_config import rag_config

class DocumentIngestion:
    """Sistema para ingestión masiva de documentos"""
    
    def __init__(self, collection_name: str = "story_documents"):
        self.vector_store = VectorStore(collection_name)
        self.config = rag_config
    
    def ingest_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, Any]:
        """Ingestar todos los documentos de un directorio"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            return {"status": "error", "message": f"Directorio no encontrado: {directory_path}"}
        
        # Encontrar todos los archivos soportados
        files_to_process = []
        
        if recursive:
            for ext in self.config.allowed_extensions:
                files_to_process.extend(directory_path.rglob(f"*.{ext}"))
        else:
            for ext in self.config.allowed_extensions:
                files_to_process.extend(directory_path.glob(f"*.{ext}"))
        
        if not files_to_process:
            return {
                "status": "warning", 
                "message": "No se encontraron archivos soportados",
                "supported_extensions": self.config.allowed_extensions
            }
        
        # Procesar archivos
        results = {
            "processed_files": [],
            "failed_files": [],
            "total_files": len(files_to_process),
            "total_chunks": 0
        }
        
        print(f"📁 Procesando {len(files_to_process)} archivos...")
        
        for file_path in tqdm(files_to_process, desc="Ingesta de documentos"):
            result = self.vector_store.add_document(str(file_path))
            
            if result["status"] == "success":
                results["processed_files"].append({
                    "file": result["document"],
                    "chunks": result["chunks_count"]
                })
                results["total_chunks"] += result["chunks_count"]
            else:
                results["failed_files"].append({
                    "file": str(file_path),
                    "error": result["message"]
                })
        
        # Resumen final
        success_count = len(results["processed_files"])
        failed_count = len(results["failed_files"])
        
        results["summary"] = {
            "successful": success_count,
            "failed": failed_count,
            "success_rate": f"{(success_count/len(files_to_process)*100):.1f}%"
        }
        
        return results
    
    def ingest_file_list(self, file_paths: List[str]) -> Dict[str, Any]:
        """Ingestar una lista específica de archivos"""
        results = {
            "processed_files": [],
            "failed_files": [],
            "total_files": len(file_paths),
            "total_chunks": 0
        }
        
        print(f"📄 Procesando {len(file_paths)} archivos específicos...")
        
        for file_path in tqdm(file_paths, desc="Ingesta de archivos"):
            if not Path(file_path).exists():
                results["failed_files"].append({
                    "file": file_path,
                    "error": "Archivo no encontrado"
                })
                continue
            
            result = self.vector_store.add_document(file_path)
            
            if result["status"] == "success":
                results["processed_files"].append({
                    "file": result["document"],
                    "chunks": result["chunks_count"]
                })
                results["total_chunks"] += result["chunks_count"]
            else:
                results["failed_files"].append({
                    "file": file_path,
                    "error": result["message"]
                })
        
        # Resumen final
        success_count = len(results["processed_files"])
        failed_count = len(results["failed_files"])
        
        results["summary"] = {
            "successful": success_count,
            "failed": failed_count,
            "success_rate": f"{(success_count/len(file_paths)*100):.1f}%"
        }
        
        return results
    
    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la ingesta"""
        return self.vector_store.get_collection_stats()
