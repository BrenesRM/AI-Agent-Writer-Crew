# -*- coding: utf-8 -*-
"""
LLM Local Manager - Versión mejorada con mejor manejo de errores,
fallbacks y optimizaciones de rendimiento.
"""
import logging
import asyncio
import time
from typing import Dict, Any, Optional, List, Union
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

class LLMStatus(Enum):
    """Estados del LLM"""
    NOT_LOADED = "not_loaded"
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    BUSY = "busy"

@dataclass
class GenerationResult:
    """Resultado de una generación"""
    text: str
    success: bool
    processing_time: float
    tokens_generated: int
    error: Optional[str] = None
    cached: bool = False

class LlamaManager:
    """Gestor mejorado para modelos LLM locales usando llama.cpp"""
    
    def __init__(self, model_path: str = None, context_length: int = 4096,
                 max_tokens: int = 2048, temperature: float = 0.7,
                 enable_cache: bool = True, max_concurrent: int = 2):
        
        self.model_path = model_path
        self.context_length = context_length
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.enable_cache = enable_cache
        self.max_concurrent = max_concurrent
        
        self.model = None
        self.status = LLMStatus.NOT_LOADED
        self.logger = logging.getLogger(__name__)
        
        # Cache para respuestas
        self.response_cache = {} if enable_cache else None
        self.max_cache_size = 100
        
        # Control de concurrencia
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_generations = 0
        
        # Estadísticas
        self.stats = {
            'total_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'total_tokens_generated': 0,
            'total_processing_time': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Inicializar modelo si se proporciona ruta
        if model_path:
            self._initialize_model()
    
    def _initialize_model(self):
        """Inicializa el modelo LLM"""
        if not LLAMA_CPP_AVAILABLE:
            self.logger.error("llama-cpp-python no está instalado")
            self.status = LLMStatus.ERROR
            return False
        
        if not self.model_path or not Path(self.model_path).exists():
            self.logger.warning(f"Modelo no encontrado en: {self.model_path}")
            self.status = LLMStatus.NOT_LOADED
            return False
        
        try:
            self.status = LLMStatus.LOADING
            self.logger.info(f"Cargando modelo: {self.model_path}")
            
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=self.context_length,
                n_threads=min(os.cpu_count() or 4, 8),  # Limitar threads
                n_batch=512,
                verbose=False,
                use_mmap=True,
                use_mlock=False
            )
            
            self.status = LLMStatus.READY
            self.logger.info("Modelo cargado exitosamente")
            return True
            
        except Exception as e:
            self.status = LLMStatus.ERROR
            self.logger.error(f"Error cargando modelo: {str(e)}")
            return False
    
    def is_available(self) -> bool:
        """Verifica si el LLM está disponible para uso"""
        return (LLAMA_CPP_AVAILABLE and 
                self.status == LLMStatus.READY and 
                self.model is not None)
    
    def _get_cache_key(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Genera clave de cache para un prompt"""
        cache_data = f"{prompt}|{max_tokens}|{temperature}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Obtiene respuesta del cache"""
        if not self.response_cache or cache_key not in self.response_cache:
            self.stats['cache_misses'] += 1
            return None
        
        self.stats['cache_hits'] += 1
        return self.response_cache[cache_key]
    
    def _add_to_cache(self, cache_key: str, response: str):
        """Añade respuesta al cache"""
        if not self.response_cache:
            return
        
        # Limpiar cache si está lleno
        if len(self.response_cache) >= self.max_cache_size:
            # Eliminar el 20% de entradas más antiguas
            items_to_remove = list(self.response_cache.keys())[:self.max_cache_size // 5]
            for key in items_to_remove:
                del self.response_cache[key]
        
        self.response_cache[cache_key] = response
    
    async def generate_async(self, prompt: str, max_tokens: Optional[int] = None,
                           temperature: Optional[float] = None, 
                           use_cache: bool = True) -> GenerationResult:
        """Genera texto de forma asíncrona"""
        
        max_tokens = max_tokens or self.max_tokens
        temperature = temperature or self.temperature
        start_time = time.time()
        
        # Verificar disponibilidad
        if not self.is_available():
            return GenerationResult(
                text="",
                success=False,
                processing_time=0,
                tokens_generated=0,
                error="LLM no disponible"
            )
        
        # Verificar cache
        cache_key = None
        if use_cache and self.enable_cache:
            cache_key = self._get_cache_key(prompt, max_tokens, temperature)
            cached_response = self._get_from_cache(cache_key)
            if cached_response:
                return GenerationResult(
                    text=cached_response,
                    success=True,
                    processing_time=time.time() - start_time,
                    tokens_generated=len(cached_response.split()),
                    cached=True
                )
        
        # Control de concurrencia
        async with self.semaphore:
            self.active_generations += 1
            self.status = LLMStatus.BUSY
            
            try:
                # Ejecutar generación en thread pool para no bloquear
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, 
                    self._generate_sync, 
                    prompt, 
                    max_tokens, 
                    temperature
                )
                
                processing_time = time.time() - start_time
                tokens_generated = len(response.split()) if response else 0
                
                # Actualizar estadísticas
                self.stats['total_generations'] += 1
                self.stats['successful_generations'] += 1
                self.stats['total_tokens_generated'] += tokens_generated
                self.stats['total_processing_time'] += processing_time
                
                # Guardar en cache
                if cache_key and response:
                    self._add_to_cache(cache_key, response)
                
                return GenerationResult(
                    text=response,
                    success=True,
                    processing_time=processing_time,
                    tokens_generated=tokens_generated
                )
                
            except Exception as e:
                self.stats['total_generations'] += 1
                self.stats['failed_generations'] += 1
                
                return GenerationResult(
                    text="",
                    success=False,
                    processing_time=time.time() - start_time,
                    tokens_generated=0,
                    error=str(e)
                )
            
            finally:
                self.active_generations -= 1
                if self.active_generations == 0:
                    self.status = LLMStatus.READY
    
    def _generate_sync(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generación síncrona del modelo"""
        if not self.model:
            raise RuntimeError("Modelo no está cargado")
        
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "\n\n", "Human:", "Assistant:", "###"],
                echo=False,
                stream=False
            )
            
            if response and 'choices' in response and len(response['choices']) > 0:
                return response['choices'][0]['text'].strip()
            else:
                return ""
            
        except Exception as e:
            self.logger.error(f"Error en generación síncrona: {str(e)}")
            raise
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None,
                temperature: Optional[float] = None) -> str:
        """Genera texto de forma síncrona (wrapper para compatibilidad)"""
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # No hay loop, crear uno nuevo
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.generate_async(prompt, max_tokens, temperature)
                )
                return result.text if result.success else ""
            finally:
                loop.close()
        else:
            # Ya hay un loop, usar run_until_complete
            result = loop.run_until_complete(
                self.generate_async(prompt, max_tokens, temperature)
            )
            return result.text if result.success else ""
    
    async def generate_with_context_async(self, question: str, context: str,
                                        max_tokens: Optional[int] = None) -> GenerationResult:
        """Genera respuesta usando contexto RAG (versión async)"""
        
        prompt = f"""Contexto de referencia:
{context[:2000]}  # Limitar contexto para evitar overflow

Pregunta: {question}

Instrucciones: Responde basándote únicamente en el contexto proporcionado. Si la información no está en el contexto, indica que no tienes suficiente información.

Respuesta:"""
        
        return await self.generate_async(prompt, max_tokens)
    
    def generate_with_context(self, question: str, context: str,
                            max_tokens: Optional[int] = None) -> str:
        """Genera respuesta usando contexto RAG (versión sync)"""
        
        try:
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                self.generate_with_context_async(question, context, max_tokens)
            )
            return result.text if result.success else ""
        except RuntimeError:
            # No hay loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.generate_with_context_async(question, context, max_tokens)
                )
                return result.text if result.success else ""
            finally:
                loop.close()
    
    async def chat_completion_async(self, messages: List[Dict[str, str]]) -> GenerationResult:
        """Completado de chat estilo OpenAI (versión async)"""
        
        # Convertir mensajes a prompt único
        prompt = ""
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt += f"Sistema: {content}\n\n"
            elif role == "user":
                prompt += f"Usuario: {content}\n\n"
            elif role == "assistant":
                prompt += f"Asistente: {content}\n\n"
        
        prompt += "Asistente:"
        
        return await self.generate_async(prompt)
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Completado de chat estilo OpenAI (versión sync)"""
        
        try:
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                self.chat_completion_async(messages)
            )
            return result.text if result.success else ""
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.chat_completion_async(messages)
                )
                return result.text if result.success else ""
            finally:
                loop.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del LLM"""
        
        total_generations = self.stats['total_generations']
        success_rate = 0
        avg_processing_time = 0
        cache_hit_rate = 0
        
        if total_generations > 0:
            success_rate = (self.stats['successful_generations'] / total_generations) * 100
            avg_processing_time = self.stats['total_processing_time'] / total_generations
        
        total_cache_requests = self.stats['cache_hits'] + self.stats['cache_misses']
        if total_cache_requests > 0:
            cache_hit_rate = (self.stats['cache_hits'] / total_cache_requests) * 100
        
        return {
            'status': self.status.value,
            'model_loaded': self.model is not None,
            'model_path': self.model_path,
            'llama_cpp_available': LLAMA_CPP_AVAILABLE,
            'total_generations': total_generations,
            'successful_generations': self.stats['successful_generations'],
            'failed_generations': self.stats['failed_generations'],
            'success_rate': round(success_rate, 2),
            'total_tokens_generated': self.stats['total_tokens_generated'],
            'avg_processing_time': round(avg_processing_time, 2),
            'active_generations': self.active_generations,
            'cache_enabled': self.enable_cache,
            'cache_size': len(self.response_cache) if self.response_cache else 0,
            'cache_hit_rate': round(cache_hit_rate, 2),
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses']
        }
    
    def clear_cache(self):
        """Limpia el cache de respuestas"""
        if self.response_cache:
            self.response_cache.clear()
            self.logger.info("Cache de respuestas limpiado")
    
    def reload_model(self, new_model_path: str = None) -> bool:
        """Recarga el modelo"""
        if new_model_path:
            self.model_path = new_model_path
        
        # Limpiar modelo actual
        if self.model:
            del self.model
            self.model = None
        
        # Reinicializar
        return self._initialize_model()
    
    def get_fallback_response(self, prompt_type: str = "general") -> str:
        """Genera una respuesta de fallback cuando el LLM no está disponible"""
        
        fallback_responses = {
            "analysis": "Lo siento, no puedo realizar el análisis solicitado en este momento debido a que el modelo LLM local no está disponible. Por favor, verifica la configuración del modelo.",
            "generation": "No puedo generar contenido en este momento. El modelo de lenguaje local no está cargado o disponible.",
            "character": "Análisis de personajes no disponible sin modelo LLM. Por favor, carga un modelo compatible.",
            "plot": "Análisis de trama no disponible. Verifica que el modelo LLM esté correctamente configurado.",
            "style": "Análisis de estilo no disponible. Se requiere un modelo de lenguaje local funcional.",
            "worldbuilding": "Análisis de worldbuilding no disponible sin LLM local. Verifica la configuración.",
            "general": "El modelo de lenguaje local no está disponible en este momento. Por favor, verifica la configuración y que el archivo del modelo exista."
        }
        
        return fallback_responses.get(prompt_type, fallback_responses["general"])
    
    def __del__(self):
        """Cleanup al destruir la instancia"""
        if self.model:
            del self.model