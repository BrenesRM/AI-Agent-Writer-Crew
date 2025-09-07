# -*- coding: utf-8 -*-
# agents/crews/researcher.py
from typing import Any, Dict
from .base_agent import BaseNovelAgent
from crewai import Agent

class ResearcherAgent(BaseNovelAgent):
    """Agente Researcher - Especialista en investigacion y referencias"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_researcher()
    
    def _create_researcher(self) -> Agent:
        return self.create_agent(
            role="Researcher - Investigador y Verificador de Referencias",
            goal="""Buscar y verificar informacion historica, cultural, cientifica 
            y geografica para enriquecer la historia con detalles autenticos y 
            bien fundamentados. Asegurar precision en referencias reales.""",
            backstory="""Eres un investigador academico con expertise en multiples 
            disciplinas: historia, antropologia, geografia, ciencias y mitologia 
            comparada. Tu pasion es encontrar los detalles que hacen que una historia 
            fantastica se sienta autentica y bien fundamentada.
            
            Aunque trabajas con ficcion, entiendes que los mejores mundos fantasticos 
            estan construidos sobre fundamentos solidos de conocimiento real. Tu 
            trabajo es encontrar esos puntos de anclaje que hacen que lo imposible 
            se sienta posible.
            
            Tu biblioteca mental es vasta, pero siempre verificas y consultas fuentes 
            para asegurar la precision. Tienes un talento especial para encontrar 
            conexiones fascinantes entre diferentes culturas y periodos historicos."""
        )
    
    def research_context(self, topic: str, story_context: str) -> Dict[str, Any]:
        """Investiga un tema especifico en el contexto de la historia"""
        task_description = f"""
        Investiga informacion sobre el tema: {topic}
        
        CONTEXTO DE LA HISTORIA:
        {story_context}
        
        TAREAS A REALIZAR:
        1. Consulta la base RAG para informacion relevante disponible
        2. Identifica aspectos historicos, culturales o cientificos relacionados
        3. Encuentra paralelos en el mundo real que puedan enriquecer la narrativa
        4. Sugiere detalles autenticos que puedan añadirse a la historia
        5. Verifica la consistencia con el mundo ya establecido
        
        FORMATO DE SALIDA:
        - Informacion encontrada en la base de datos
        - Referencias historicas/culturales relevantes
        - Sugerencias para enriquecer la narrativa
        - Verificacion de consistencia
        """
        
        return {"task": task_description, "agent": "researcher"}
