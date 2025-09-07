# -*- coding: utf-8 -*-
import logging
from typing import Dict, Any, Optional, List
import os
from pathlib import Path

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

class LlamaManager:
    """Gestor para modelos LLM locales usando llama.cpp"""
    
    def __init__(self, model_path: str, context_length: int = 4096,
                 max_tokens: int = 2048, temperature: float = 0.7):
        self.model_path = model_path
        self.context_length = context_length
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = None
        self.logger = logging.getLogger(__name__)
        
        if not LLAMA_CPP_AVAILABLE:
            raise ImportError("llama-cpp-python no esta instalado. Instalalo con: pip install llama-cpp-python")
        
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo LLM local"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Modelo no encontrado en: {self.model_path}")
            
            self.logger.info(f"Cargando modelo: {self.model_path}")
            
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=self.context_length,
                n_threads=os.cpu_count() or 4,
                verbose=False
            )
            
            self.logger.info("Modelo cargado exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error cargando modelo: {str(e)}")
            raise
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None,
                temperature: Optional[float] = None) -> str:
        """Genera texto usando el modelo local"""
        if not self.model:
            raise RuntimeError("El modelo no esta cargado")
        
        try:
            max_tokens = max_tokens or self.max_tokens
            temperature = temperature or self.temperature
            
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "\n\n", "Human:", "Assistant:"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            self.logger.error(f"Error generando texto: {str(e)}")
            return ""
    
    def generate_with_context(self, question: str, context: str,
                            max_tokens: Optional[int] = None) -> str:
        """Genera respuesta usando contexto RAG"""
        prompt = f"""Contexto de referencia:
{context}

Pregunta: {question}

Respuesta basada en el contexto:"""
        
        return self.generate(prompt, max_tokens)
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Simula completado de chat estilo OpenAI"""
        # Convertir mensajes a prompt unico
        prompt = ""
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"Human: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant:"
        
        return self.generate(prompt)
