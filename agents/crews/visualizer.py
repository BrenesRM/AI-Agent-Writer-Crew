# -*- coding: utf-8 -*-
# agents/crews/visualizer.py
from .base_agent import BaseNovelAgent
from crewai import Agent
from typing import Dict, Any

class VisualizerAgent(BaseNovelAgent):
    """Agente Visualizer - Especialista en prompts cinematograficos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_visualizer()
    
    def _create_visualizer(self) -> Agent:
        return self.create_agent(
            role="Visualizer - Director Cinematografico Virtual",
            goal="""Convertir escenas narrativas en prompts visuales detallados 
            para generacion de video AI. Crear descripciones cinematograficas que 
            capturen la esencia visual y emocional de cada escena.""",
            backstory="""Eres un director de fotografia y visualizador conceptual con 
            experiencia en cine epico y fantasia. Tu vision combina tecnica cinematografica 
            avanzada con sensibilidad artistica para traducir palabras en imagenes 
            poderosas.
            
            Entiendes como los angulos de camara, la iluminacion, el color y la 
            composicion pueden amplificar el impacto emocional de una escena. Tu 
            especialidad es crear prompts que resulten en videos que no solo muestren 
            la accion, sino que transmitan la atmosfera y el sentimiento de la historia.
            
            Tienes un ojo excepcional para los detalles visuales que hacen que una 
            escena cobre vida: la manera en que la luz filtra a traves de las hojas, 
            el polvo que flota en un rayo de sol, la expresion exacta en el rostro 
            de un personaje."""
        )
    
    def create_visual_prompts(self, manuscript: str) -> Dict[str, Any]:
        """Crea prompts visuales para las escenas clave del manuscrito"""
        task_description = f"""
        Crea prompts visuales cinematograficos para las escenas clave:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica las 5-7 escenas mas visualmente impactantes
        2. Para cada escena, usa el generador de prompts visuales
        3. Crea variaciones con diferentes estilos cinematograficos
        4. Incluye detalles tecnicos especificos (angulos, iluminacion, movimiento)
        5. Optimiza para generacion de video AI
        
        FORMATO DE SALIDA:
        - Lista de escenas clave identificadas
        - Prompt principal para cada escena
        - Variaciones estilisticas
        - Detalles tecnicos cinematograficos
        - Recomendaciones de post-produccion
        """
        
        return {"task": task_description, "agent": "visualizer"}
    
    def optimize_scene_for_video(self, scene_description: str, duration: str = "30s") -> str:
        """Optimiza una escena especifica para video AI"""
        task_description = f"""
        Optimiza esta escena para generacion de video de {duration}:
        
        ESCENA:
        {scene_description}
        
        Crea un prompt optimizado que funcione bien con herramientas de video AI, 
        considerando limitaciones tecnicas y mejores practicas.
        """
        
        return task_description
