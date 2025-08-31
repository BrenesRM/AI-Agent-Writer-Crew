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
            backstory="""Eres un lector voraz con la habilidad �nica de adoptar diferentes 
            perspectivas de lectura. Puedes leer como un adolescente buscando aventura, 
            como un adulto buscando profundidad emocional, o como un cr�tico literario 
            buscando excelencia t�cnica.
            
            Tu valor radica en tu empat�a lectora - puedes anticipar qu� partes van 
            a enganchar a los lectores, qu� secciones pueden resultar confusas, y 
            d�nde la historia puede perder momentum. Has le�do miles de historias 
            en m�ltiples g�neros y entiendes qu� funciona y qu� no.
            
            Tu feedback es directo pero constructivo, siempre enfocado en mejorar 
            la experiencia del lector final."""
        )
    
    def provide_reader_feedback(self, manuscript: str, target_audience: str = "general") -> Dict[str, Any]:
        """Proporciona feedback desde la perspectiva del lector target"""
        task_description = f"""
        Lee y eval�a este manuscrito desde la perspectiva de {target_audience}:
        
        MANUSCRITO:
        {manuscript}
        
        AUDIENCIA TARGET: {target_audience}
        
        TAREAS A REALIZAR:
        1. Eval�a el engagement general y puntos donde puede perderse la atenci�n
        2. Identifica momentos confusos o que requieren clarificaci�n
        3. Analiza el appeal emocional y conexi�n con personajes
        4. Eval�a el ritmo desde la perspectiva del lector
        5. Sugiere mejoras para aumentar el appeal al p�blico objetivo
        
        FORMATO DE SALIDA:
        - Evaluaci�n general de engagement
        - Puntos de confusi�n identificados
        - An�lisis de conexi�n emocional
        - Sugerencias de mejora espec�ficas
        - Rating general como lector target
        """
        
        return {"task": task_description, "agent": "beta_reader"}
