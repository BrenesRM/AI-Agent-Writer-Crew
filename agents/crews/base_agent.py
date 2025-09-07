# -*- coding: utf-8 -*-
# agents/crews/base_agent.py
import logging
from typing import Dict, Any, List, Optional
from crewai import Agent
from pathlib import Path
import sys

# Añadir el directorio raiz al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from agents.tools import RAGTool, WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from agents.tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from agents.tools import IdeaGenerator, VisualPromptGenerator

class BaseNovelAgent:
    """Clase base para todos los agentes del sistema de novelas"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Herramientas comunes disponibles para todos los agentes
        self.common_tools = [
            RAGTool(),
            WritingAnalyzer(),
            StyleAnalyzer(),
            CharacterAnalyzer(),
            ConsistencyChecker(),
            PacingAnalyzer(),
            PlotAnalyzer(),
            IdeaGenerator(),
            VisualPromptGenerator()
        ]
        
    def create_agent(self, role: str, goal: str, backstory: str, 
                    specific_tools: List = None) -> Agent:
        """Crea un agente CrewAI con configuracion base"""
        
        all_tools = self.common_tools.copy()
        if specific_tools:
            all_tools.extend(specific_tools)
        
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=all_tools,
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300  # 5 minutos maximo por tarea
        )
