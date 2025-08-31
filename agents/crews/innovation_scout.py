# agents/crews/innovation_scout.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class InnovationScoutAgent(BaseNovelAgent):
    """Agente Innovation Scout - Explorador de ideas creativas"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_innovation_scout()
    
    def _create_innovation_scout(self) -> Agent:
        return self.create_agent(
            role="Innovation Scout - Explorador de Fronteras Creativas",
            goal="""Identificar oportunidades para giros creativos originales, 
            combinaciones de géneros innovadoras y elementos narrativos únicos 
            que hagan la historia memorable y distintiva.""",
            backstory="""Eres un visionario creativo con un talento especial para 
            ver posibilidades que otros pasan por alto. Tu mente conecta ideas 
            aparentemente dispares para crear combinaciones fascinantes y originales.
            
            Has estudiado narrativas de todas las culturas y épocas, siempre buscando 
            patrones únicos y enfoques innovadores. Tu especialidad es tomar elementos 
            familiares y combinarlos de maneras que se sienten tanto sorprendentes 
            como inevitables.
            
            No innov as por el sake de ser diferente - cada sugerencia creativa que 
            haces sirve a la historia y emerge orgánicamente del material existente. 
            Tu goal es elevar la narrativa más allá de lo convencional sin sacrificar 
            coherencia o emotional truth."""
        )
    
    def scout_creative_opportunities(self, manuscript: str) -> Dict[str, Any]:
        """Identifica oportunidades para innovación creativa"""
        task_description = f"""
        Explora oportunidades creativas en el manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica elementos convencionales que podrían beneficiarse de un twist
        2. Usa el generador de ideas para explorar posibilidades creativas
        3. Busca oportunidades para combinaciones de género únicas
        4. Sugiere giros narrativos que emerjan orgánicamente de la historia
        5. Propone elementos innovadores que mantengan coherencia con el mundo
        
        FORMATO DE SALIDA:
        - Oportunidades de innovación identificadas
        - Sugerencias de giros creativos
        - Ideas para combinaciones de género
        - Propuestas de elementos únicos
        - Evaluación de viabilidad y coherencia
        """
        
        return {"task": task_description, "agent": "innovation_scout"}