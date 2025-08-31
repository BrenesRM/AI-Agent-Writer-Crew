# agents/crews/character_developer.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class CharacterDeveloperAgent(BaseNovelAgent):
    """Agente Character Developer - Editor de personajes y arcos narrativos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_character_developer()
    
    def _create_character_developer(self) -> Agent:
        return self.create_agent(
            role="Character Developer - Arquitecto de Personajes",
            goal="""Crear personajes complejos, tridimensionales y convincentes. 
            Desarrollar arcos narrativos significativos, relaciones auténticas y 
            evolución character realista a lo largo de la historia.""",
            backstory="""Eres un psicólogo narrativo especializado en la creación y 
            desarrollo de personajes memorables. Tu formación combina psicología humana, 
            teoría literaria y técnicas de escritura creativa.
            
            Entiendes que los grandes personajes son aquellos que sienten reales, con 
            motivaciones claras, flaws auténticos y crecimiento genuino. Cada personaje 
            que tocas cobra vida propia, convirtiéndose en algo más que palabras en una página.
            
            Tu especialidad es encontrar la humanidad en cada personaje, sin importar 
            cuán fantástica sea su naturaleza. Creas arcos de desarrollo que resuenan 
            emocionalmente con los lectores y drive the story forward."""
        )
    
    def develop_characters(self, manuscript: str) -> Dict[str, Any]:
        """Desarrolla y mejora los personajes en el manuscrito"""
        task_description = f"""
        Analiza y desarrolla los personajes en el siguiente manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de personajes para identificar todos los personajes presentes
        2. Consulta la base RAG para obtener información previa sobre estos personajes
        3. Evalúa la profundidad y desarrollo de cada personaje
        4. Identifica oportunidades para arcos de crecimiento
        5. Sugiere mejoras en motivaciones, conflictos internos y relaciones
        6. Genera ideas creativas para enriquecer a los personajes secundarios
        
        FORMATO DE SALIDA:
        - Análisis de personajes existentes
        - Arcos de desarrollo sugeridos
        - Mejoras en motivaciones y conflictos
        - Sugerencias para personajes secundarios
        - Plan de evolución character
        """
        
        return {"task": task_description, "agent": "character_developer"}
    
    def create_character_profile(self, character_name: str, context: str) -> str:
        """Crea un perfil detallado para un personaje"""
        task_description = f"""
        Crea un perfil completo para el personaje {character_name} basado en este contexto:
        
        {context}
        
        Incluye: trasfondo, motivaciones, miedos, fortalezas, debilidades, 
        relaciones y arco de desarrollo potencial.
        """
        
        return task_description
