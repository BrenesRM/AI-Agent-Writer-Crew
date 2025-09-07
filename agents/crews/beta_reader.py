# -*- coding: utf-8 -*-
# agents/crews/beta_reader.py
from typing import Any, Dict
from .base_agent import BaseNovelAgent
from crewai import Agent

class BetaReaderAgent(BaseNovelAgent):
    """Agente Beta Reader - Simula diferentes tipos de lectores"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_beta_reader()
    
    def _create_beta_reader(self) -> Agent:
        return self.create_agent(
            role="Beta Reader - Voz del Lector Target",
            goal="""Simular la experiencia de diferentes tipos de lectores target, 
            proporcionando feedback desde perspectivas variadas sobre engagement, 
            claridad, ritmo y appeal emocional de la historia.""",
            backstory="""Eres un lector voraz con la habilidad unica de adoptar diferentes 
            perspectivas de lectura. Puedes leer como un adolescente buscando aventura, 
            como un adulto buscando profundidad emocional, o como un critico literario 
            buscando excelencia tecnica.
            
            Tu valor radica en tu empatia lectora - puedes anticipar que partes van 
            a enganchar a los lectores, que secciones pueden resultar confusas, y 
            donde la historia puede perder momentum. Has leido miles de historias 
            en multiples generos y entiendes que funciona y que no.
            
            Tu feedback es directo pero constructivo, siempre enfocado en mejorar 
            la experiencia del lector final."""
        )
    
    def provide_reader_feedback(self, manuscript: str, target_audience: str = "general") -> Dict[str, Any]:
        """Proporciona feedback desde la perspectiva del lector target"""
        task_description = f"""
        Lee y evalua este manuscrito desde la perspectiva de {target_audience}:
        
        MANUSCRITO:
        {manuscript}
        
        AUDIENCIA TARGET: {target_audience}
        
        TAREAS A REALIZAR:
        1. Evalua el engagement general y puntos donde puede perderse la atencion
        2. Identifica momentos confusos o que requieren clarificacion
        3. Analiza el appeal emocional y conexion con personajes
        4. Evalua el ritmo desde la perspectiva del lector
        5. Sugiere mejoras para aumentar el appeal al publico objetivo
        
        FORMATO DE SALIDA:
        - Evaluacion general de engagement
        - Puntos de confusion identificados
        - Analisis de conexion emocional
        - Sugerencias de mejora especificas
        - Rating general como lector target
        """
        
        return {"task": task_description, "agent": "beta_reader"}
