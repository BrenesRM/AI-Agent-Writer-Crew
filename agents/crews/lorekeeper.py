# agents/crews/lorekeeper.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class LorekeeperAgent(BaseNovelAgent):
    """Agente Lorekeeper - Analista de lore y reglas del mundo"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_lorekeeper()
    
    def _create_lorekeeper(self) -> Agent:
        return self.create_agent(
            role="Lorekeeper - Guardi�n del Conocimiento",
            goal="""Mantener la coherencia y consistencia del mundo narrativo, 
            asegurando que todos los elementos de lore, reglas m�gicas, geograf�a, 
            historia y mitolog�a se mantengan coherentes a lo largo de la historia.""",
            backstory="""Eres un erudito meticuloso con d�cadas de experiencia catalogando 
            y organizando el conocimiento de mundos fant�sticos. Tu obsesi�n por los detalles 
            y la consistencia te ha convertido en el guardi�n definitivo del lore narrativo. 
            
            Conoces cada ley m�gica, cada linaje noble, cada evento hist�rico y cada tradici�n 
            cultural. Tu trabajo es esencial para crear mundos que se sientan aut�nticos y 
            vividos, donde cada detalle tiene su lugar y prop�sito.
            
            Siempre consultas los documentos de referencia antes de hacer cualquier afirmaci�n 
            sobre el mundo, y mantienes un registro mental de todas las reglas establecidas."""
        )
    
    def analyze_worldbuilding(self, manuscript: str) -> Dict[str, Any]:
        """Analiza la construcci�n del mundo en el manuscrito"""
        task_description = f"""
        Analiza el siguiente manuscrito enfoc�ndote en los elementos de worldbuilding:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa la herramienta RAG para consultar informaci�n relevante sobre el mundo
        2. Identifica todos los elementos de lore presentes (magia, razas, lugares, historia)
        3. Verifica consistencia interna usando el verificador de consistencia
        4. Detecta posibles contradicciones o inconsistencias
        5. Sugiere mejoras para fortalecer la coherencia del mundo
        
        FORMATO DE SALIDA:
        - Elementos de lore identificados
        - Verificaci�n de consistencia
        - Contradicciones encontradas
        - Recomendaciones para mejorar la coherencia
        """
        
        # Aqu� se ejecutar�a la tarea del agente
        return {"task": task_description, "agent": "lorekeeper"}
    
    def validate_rules(self, text: str, rule_type: str = "magic") -> str:
        """Valida que las reglas del mundo se mantengan consistentes"""
        task_description = f"""
        Valida las reglas de {rule_type} en este texto:
        
        {text}
        
        Consulta la base de conocimiento para verificar reglas establecidas previamente
        y aseg�rate de que no haya violaciones a la consistencia del mundo.
        """
        
        return task_description
