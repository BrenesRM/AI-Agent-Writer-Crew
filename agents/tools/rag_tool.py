# -*- coding: utf-8 -*-
# agents/tools/rag_tool.py
import logging
from typing import Dict, Any, Optional, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from rag.rag_manager import RAGManager

class RAGToolInput(BaseModel):
    query: str = Field(..., description="La consulta a realizar en la base de conocimiento")
    doc_type: Optional[str] = Field(None, description="Tipo de documento específico a buscar")
    k: int = Field(5, description="Número máximo de documentos relevantes a retornar")

class RAGTool(BaseTool):
    name: str = "Consultar Base de Conocimiento"
    description: str = """
    Herramienta para consultar la base de conocimiento RAG con documentos de referencia.
    Útil para obtener información sobre lore, personajes, reglas del mundo, referencias históricas,
    y cualquier otro contexto relevante para la historia.
    """
    args_schema: type[BaseModel] = RAGToolInput
    
    # Define as class attributes for Pydantic v2 compatibility
    rag_manager: Any = None
    logger: Any = None
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize RAG manager after parent initialization
        if self.rag_manager is None:
            self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize RAG manager after object creation"""
        try:
            self.rag_manager = RAGManager()
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            self.logger = logging.getLogger(__name__)
            self.logger.error(f"Failed to initialize RAG manager: {e}")
            self.rag_manager = None
    
    def _run(self, query: str, doc_type: Optional[str] = None, k: int = 5) -> str:
        """Ejecuta una consulta en el sistema RAG"""
        try:
            # Ensure RAG manager is initialized
            if self.rag_manager is None:
                self._initialize_rag()
                
            if self.rag_manager is None:
                return f"Error: Sistema RAG no disponible para la consulta: {query}"
            
            if self.logger:
                self.logger.info(f"Consultando RAG: {query}")
            
            result = self.rag_manager.query(query, k=k, doc_type=doc_type)
            
            if not result['context']:
                return f"No se encontró información relevante para: {query}"
            
            # Formatear respuesta
            response = f"INFORMACIÓN ENCONTRADA para '{query}':\n\n"
            response += result['context']
            response += f"\n\nFuentes consultadas: {result['num_sources']} documentos"
            
            return response
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en consulta RAG: {str(e)}")
            return f"Error consultando la base de conocimiento: {str(e)}"
