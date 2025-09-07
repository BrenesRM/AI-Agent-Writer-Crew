# -*- coding: utf-8 -*-
# agents/crews/pacing_specialist.py
from .base_agent import BaseNovelAgent
from crewai import Agent
from typing import Dict, Any

class PacingSpecialistAgent(BaseNovelAgent):
    """Agente Pacing Specialist - Especialista en ritmo narrativo"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_pacing_specialist()
    
    def _create_pacing_specialist(self) -> Agent:
        return self.create_agent(
            role="Pacing Specialist - Maestro del Ritmo Narrativo",
            goal="""Optimizar el ritmo y flujo de la narrativa para mantener el 
            engagement del lector. Balancear momentos de tension, accion, reflexion 
            y descanso para crear una experiencia de lectura dinamica.""",
            backstory="""Eres un especialista en ritmo narrativo con un entendimiento 
            intuitivo de como los lectores experimentan el tiempo en las historias. 
            Tu expertise viene de años analizando que hace que algunos libros sean 
            'page-turners' imposibles de dejar.
            
            Entiendes que el pacing es como la respiracion de una historia - debe 
            fluir naturalmente, con momentos de aceleracion y descanso que se sienten 
            organicos. Tu trabajo es encontrar el ritmo unico de cada historia y 
            optimizarlo para maximo impacto.
            
            Tienes una sensibilidad especial para detectar cuando una escena se 
            alarga demasiado, cuando la accion necesita un respiro, o cuando el 
            momentum esta por perderse."""
        )
    
    def analyze_pacing(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el ritmo narrativo del manuscrito"""
        task_description = f"""
        Analiza el ritmo y pacing del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de ritmo para evaluar la estructura de pacing
        2. Identifica momentos de alta tension vs. momentos de respiro
        3. Evalua la transicion entre diferentes tipos de escenas
        4. Detecta secciones que pueden beneficiarse de aceleracion o desaceleracion
        5. Sugiere ajustes especificos para optimizar el flow narrativo
        
        FORMATO DE SALIDA:
        - Analisis detallado del ritmo actual
        - Identificacion de puntos criticos de pacing
        - Balance entre accion, tension y reflexion
        - Sugerencias especificas de mejora
        - Recomendaciones de reestructuracion si es necesario
        """
        
        return {"task": task_description, "agent": "pacing_specialist"}
