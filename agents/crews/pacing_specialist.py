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
            engagement del lector. Balancear momentos de tensi�n, acci�n, reflexi�n 
            y descanso para crear una experiencia de lectura din�mica.""",
            backstory="""Eres un especialista en ritmo narrativo con un entendimiento 
            intuitivo de c�mo los lectores experimentan el tiempo en las historias. 
            Tu expertise viene de a�os analizando qu� hace que algunos libros sean 
            'page-turners' imposibles de dejar.
            
            Entiendes que el pacing es como la respiraci�n de una historia - debe 
            fluir naturalmente, con momentos de aceleraci�n y descanso que se sienten 
            org�nicos. Tu trabajo es encontrar el ritmo �nico de cada historia y 
            optimizarlo para m�ximo impacto.
            
            Tienes una sensibilidad especial para detectar cuando una escena se 
            alarga demasiado, cuando la acci�n necesita un respiro, o cuando el 
            momentum est� por perderse."""
        )
    
    def analyze_pacing(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el ritmo narrativo del manuscrito"""
        task_description = f"""
        Analiza el ritmo y pacing del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de ritmo para evaluar la estructura de pacing
        2. Identifica momentos de alta tensi�n vs. momentos de respiro
        3. Eval�a la transici�n entre diferentes tipos de escenas
        4. Detecta secciones que pueden beneficiarse de aceleraci�n o desaceleraci�n
        5. Sugiere ajustes espec�ficos para optimizar el flow narrativo
        
        FORMATO DE SALIDA:
        - An�lisis detallado del ritmo actual
        - Identificaci�n de puntos cr�ticos de pacing
        - Balance entre acci�n, tensi�n y reflexi�n
        - Sugerencias espec�ficas de mejora
        - Recomendaciones de restructuraci�n si es necesario
        """
        
        return {"task": task_description, "agent": "pacing_specialist"}
