# agents/crews/researcher.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class ResearcherAgent(BaseNovelAgent):
    """Agente Researcher - Especialista en investigación y referencias"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_researcher()
    
    def _create_researcher(self) -> Agent:
        return self.create_agent(
            role="Researcher - Investigador y Verificador de Referencias",
            goal="""Buscar y verificar información histórica, cultural, científica 
            y geográfica para enriquecer la historia con detalles auténticos y 
            bien fundamentados. Asegurar precisión en referencias reales.""",
            backstory="""Eres un investigador académico con expertise en múltiples 
            disciplinas: historia, antropología, geografía, ciencias y mitología 
            comparada. Tu pasión es encontrar los detalles que hacen que una historia 
            fantástica se sienta auténtica y bien fundamentada.
            
            Aunque trabajas con ficción, entiendes que los mejores mundos fantásticos 
            están construidos sobre fundamentos sólidos de conocimiento real. Tu 
            trabajo es encontrar esos puntos de anclaje que hacen que lo imposible 
            se sienta posible.
            
            Tu biblioteca mental es vasta, pero siempre verificas y consultas fuentes 
            para asegurar la precisión. Tienes un talento especial para encontrar 
            conexiones fascinantes entre diferentes culturas y períodos históricos."""
        )
    
    def research_context(self, topic: str, story_context: str) -> Dict[str, Any]:
        """Investiga un tema específico en el contexto de la historia"""
        task_description = f"""
        Investiga información sobre el tema: {topic}
        
        CONTEXTO DE LA HISTORIA:
        {story_context}
        
        TAREAS A REALIZAR:
        1. Consulta la base RAG para información relevante disponible
        2. Identifica aspectos históricos, culturales o científicos relacionados
        3. Encuentra paralelos en el mundo real que puedan enriquecer la narrativa
        4. Sugiere detalles auténticos que puedan añadirse a la historia
        5. Verifica la consistencia con el mundo ya establecido
        
        FORMATO DE SALIDA:
        - Información encontrada en la base de datos
        - Referencias históricas/culturales relevantes
        - Sugerencias para enriquecer la narrativa
        - Verificación de consistencia
        """
        
        return {"task": task_description, "agent": "researcher"}
