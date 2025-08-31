# agents/crews/researcher.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class ResearcherAgent(BaseNovelAgent):
    """Agente Researcher - Especialista en investigaci�n y referencias"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_researcher()
    
    def _create_researcher(self) -> Agent:
        return self.create_agent(
            role="Researcher - Investigador y Verificador de Referencias",
            goal="""Buscar y verificar informaci�n hist�rica, cultural, cient�fica 
            y geogr�fica para enriquecer la historia con detalles aut�nticos y 
            bien fundamentados. Asegurar precisi�n en referencias reales.""",
            backstory="""Eres un investigador acad�mico con expertise en m�ltiples 
            disciplinas: historia, antropolog�a, geograf�a, ciencias y mitolog�a 
            comparada. Tu pasi�n es encontrar los detalles que hacen que una historia 
            fant�stica se sienta aut�ntica y bien fundamentada.
            
            Aunque trabajas con ficci�n, entiendes que los mejores mundos fant�sticos 
            est�n construidos sobre fundamentos s�lidos de conocimiento real. Tu 
            trabajo es encontrar esos puntos de anclaje que hacen que lo imposible 
            se sienta posible.
            
            Tu biblioteca mental es vasta, pero siempre verificas y consultas fuentes 
            para asegurar la precisi�n. Tienes un talento especial para encontrar 
            conexiones fascinantes entre diferentes culturas y per�odos hist�ricos."""
        )
    
    def research_context(self, topic: str, story_context: str) -> Dict[str, Any]:
        """Investiga un tema espec�fico en el contexto de la historia"""
        task_description = f"""
        Investiga informaci�n sobre el tema: {topic}
        
        CONTEXTO DE LA HISTORIA:
        {story_context}
        
        TAREAS A REALIZAR:
        1. Consulta la base RAG para informaci�n relevante disponible
        2. Identifica aspectos hist�ricos, culturales o cient�ficos relacionados
        3. Encuentra paralelos en el mundo real que puedan enriquecer la narrativa
        4. Sugiere detalles aut�nticos que puedan a�adirse a la historia
        5. Verifica la consistencia con el mundo ya establecido
        
        FORMATO DE SALIDA:
        - Informaci�n encontrada en la base de datos
        - Referencias hist�ricas/culturales relevantes
        - Sugerencias para enriquecer la narrativa
        - Verificaci�n de consistencia
        """
        
        return {"task": task_description, "agent": "researcher"}
