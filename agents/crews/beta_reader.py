# agents/crews/beta_reader.py
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
            backstory="""Eres un lector voraz con la habilidad única de adoptar diferentes 
            perspectivas de lectura. Puedes leer como un adolescente buscando aventura, 
            como un adulto buscando profundidad emocional, o como un crítico literario 
            buscando excelencia técnica.
            
            Tu valor radica en tu empatía lectora - puedes anticipar qué partes van 
            a enganchar a los lectores, qué secciones pueden resultar confusas, y 
            dónde la historia puede perder momentum. Has leído miles de historias 
            en múltiples géneros y entiendes qué funciona y qué no.
            
            Tu feedback es directo pero constructivo, siempre enfocado en mejorar 
            la experiencia del lector final."""
        )
    
    def provide_reader_feedback(self, manuscript: str, target_audience: str = "general") -> Dict[str, Any]:
        """Proporciona feedback desde la perspectiva del lector target"""
        task_description = f"""
        Lee y evalúa este manuscrito desde la perspectiva de {target_audience}:
        
        MANUSCRITO:
        {manuscript}
        
        AUDIENCIA TARGET: {target_audience}
        
        TAREAS A REALIZAR:
        1. Evalúa el engagement general y puntos donde puede perderse la atención
        2. Identifica momentos confusos o que requieren clarificación
        3. Analiza el appeal emocional y conexión con personajes
        4. Evalúa el ritmo desde la perspectiva del lector
        5. Sugiere mejoras para aumentar el appeal al público objetivo
        
        FORMATO DE SALIDA:
        - Evaluación general de engagement
        - Puntos de confusión identificados
        - Análisis de conexión emocional
        - Sugerencias de mejora específicas
        - Rating general como lector target
        """
        
        return {"task": task_description, "agent": "beta_reader"}
