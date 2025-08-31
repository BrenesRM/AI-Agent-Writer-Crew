# agents/crews/plot_weaver.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class PlotWeaverAgent(BaseNovelAgent):
    """Agente Plot Weaver - Especialista en trama y estructura"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_plot_weaver()
    
    def _create_plot_weaver(self) -> Agent:
        return self.create_agent(
            role="Plot Weaver - Maestro de la Narrativa",
            goal="""Diseñar tramas cautivadoras y bien estructuradas. Organizar eventos 
            narrativos de manera que maximicen el impacto emocional y mantengan el 
            engagement del lector. Balancear tensión, ritmo y revelaciones.""",
            backstory="""Eres un maestro arquitecto de historias con un entendimiento 
            profundo de la estructura narrativa clásica y moderna. Has estudiado las 
            obras de los grandes narradores y entiendes los patrones que hacen que una 
            historia sea inolvidable.
            
            Tu especialidad es tejer múltiples hilos narrativos en una tapestry coherente 
            y emocionante. Sabes cuándo acelerar el ritmo, cuándo permitir momentos de 
            respiro, y cómo colocar revelaciones para máximo impacto.
            
            Entiendes que cada escena debe servir un propósito: avanzar la trama, 
            desarrollar personajes, o enriquecer el mundo. No toleras escenas innecesarias, 
            pero tampoco sacrificas momentos importantes por el sake de la eficiencia."""
        )
    
    def analyze_plot_structure(self, manuscript: str) -> Dict[str, Any]:
        """Analiza la estructura de la trama"""
        task_description = f"""
        Analiza la estructura narrativa del siguiente manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de trama para evaluar la estructura narrativa
        2. Usa el analizador de ritmo para evaluar el pacing
        3. Identifica los puntos clave de la trama (setup, inciting incident, plot points, climax, resolution)
        4. Evalúa la progresión y escalamiento de conflictos
        5. Identifica subtramas y su integración con la trama principal
        6. Sugiere mejoras estructurales y de ritmo
        
        FORMATO DE SALIDA:
        - Análisis de estructura narrativa
        - Evaluación del ritmo y pacing
        - Identificación de puntos débiles en la trama
        - Sugerencias de mejora estructural
        - Recomendaciones para subtramas
        """
        
        return {"task": task_description, "agent": "plot_weaver"}
    
    def suggest_plot_improvements(self, current_plot: str, issues: List[str]) -> str:
        """Sugiere mejoras específicas para la trama"""
        task_description = f"""
        Basándote en los siguientes problemas identificados en la trama:
        
        TRAMA ACTUAL:
        {current_plot}
        
        PROBLEMAS IDENTIFICADOS:
        {chr(10).join([f"- {issue}" for issue in issues])}
        
        Genera sugerencias específicas para resolver estos problemas y mejorar 
        la estructura narrativa general.
        """
        
        return task_description
