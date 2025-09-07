# -*- coding: utf-8 -*-
# agents/crews/innovation_scout.py
from typing import Any, Dict
from .base_agent import BaseNovelAgent
from crewai import Agent

class InnovationScoutAgent(BaseNovelAgent):
    """Agente Innovation Scout - Explorador de ideas creativas"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_innovation_scout()
    
    def _create_innovation_scout(self) -> Agent:
        return self.create_agent(
            role="Innovation Scout - Explorador de Fronteras Creativas",
            goal="""Identificar oportunidades para giros creativos originales, 
            combinaciones de generos innovadoras y elementos narrativos unicos 
            que hagan la historia memorable y distintiva.""",
            backstory="""Eres un visionario creativo con un talento especial para 
            ver posibilidades que otros pasan por alto. Tu mente conecta ideas 
            aparentemente dispares para crear combinaciones fascinantes y originales.
            
            Has estudiado narrativas de todas las culturas y epocas, siempre buscando 
            patrones unicos y enfoques innovadores. Tu especialidad es tomar elementos 
            familiares y combinarlos de maneras que se sienten tanto sorprendentes 
            como inevitables.
            
            No innov as por el sake de ser diferente - cada sugerencia creativa que 
            haces sirve a la historia y emerge organicamente del material existente. 
            Tu goal es elevar la narrativa mas alla de lo convencional sin sacrificar 
            coherencia o emotional truth."""
        )
    
    def scout_creative_opportunities(self, manuscript: str) -> Dict[str, Any]:
        """Identifica oportunidades para innovacion creativa"""
        task_description = f"""
        Explora oportunidades creativas en el manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica elementos convencionales que podrian beneficiarse de un twist
        2. Usa el generador de ideas para explorar posibilidades creativas
        3. Busca oportunidades para combinaciones de genero unicas
        4. Sugiere giros narrativos que emerjan organicamente de la historia
        5. Propone elementos innovadores que mantengan coherencia con el mundo
        
        FORMATO DE SALIDA:
        - Oportunidades de innovacion identificadas
        - Sugerencias de giros creativos
        - Ideas para combinaciones de genero
        - Propuestas de elementos unicos
        - Evaluacion de viabilidad y coherencia
        """
        
        return {"task": task_description, "agent": "innovation_scout"}