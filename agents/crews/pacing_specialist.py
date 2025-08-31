# agents/crews/pacing_specialist.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class PacingSpecialistAgent(BaseNovelAgent):
    """Agente Pacing Specialist - Especialista en ritmo narrativo"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_pacing_specialist()
    
    def _create_pacing_specialist(self) -> Agent:
        return self.create_agent(
            role="Pacing Specialist - Maestro del Ritmo Narrativo",
            goal="""Optimizar el ritmo y flujo de la narrativa para mantener el 
            engagement del lector. Balancear momentos de tensión, acción, reflexión 
            y descanso para crear una experiencia de lectura dinámica.""",
            backstory="""Eres un especialista en ritmo narrativo con un entendimiento 
            intuitivo de cómo los lectores experimentan el tiempo en las historias. 
            Tu expertise viene de años analizando qué hace que algunos libros sean 
            'page-turners' imposibles de dejar.
            
            Entiendes que el pacing es como la respiración de una historia - debe 
            fluir naturalmente, con momentos de aceleración y descanso que se sienten 
            orgánicos. Tu trabajo es encontrar el ritmo único de cada historia y 
            optimizarlo para máximo impacto.
            
            Tienes una sensibilidad especial para detectar cuando una escena se 
            alarga demasiado, cuando la acción necesita un respiro, o cuando el 
            momentum está por perderse."""
        )
    
    def analyze_pacing(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el ritmo narrativo del manuscrito"""
        task_description = f"""
        Analiza el ritmo y pacing del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de ritmo para evaluar la estructura de pacing
        2. Identifica momentos de alta tensión vs. momentos de respiro
        3. Evalúa la transición entre diferentes tipos de escenas
        4. Detecta secciones que pueden beneficiarse de aceleración o desaceleración
        5. Sugiere ajustes específicos para optimizar el flow narrativo
        
        FORMATO DE SALIDA:
        - Análisis detallado del ritmo actual
        - Identificación de puntos críticos de pacing
        - Balance entre acción, tensión y reflexión
        - Sugerencias específicas de mejora
        - Recomendaciones de restructuración si es necesario
        """
        
        return {"task": task_description, "agent": "pacing_specialist"}
