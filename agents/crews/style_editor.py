# agents/crews/style_editor.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class StyleEditorAgent(BaseNovelAgent):
    """Agente Style Editor - Crítico literario especializado en voz y estilo"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_style_editor()
    
    def _create_style_editor(self) -> Agent:
        return self.create_agent(
            role="Voice & Style Editor - Maestro del Estilo Literario",
            goal="""Perfeccionar la voz narrativa y el estilo de escritura para crear 
            una experiencia de lectura cohesiva y envolvente. Mantener consistencia 
            tonal y mejorar la prosa para máximo impacto emocional.""",
            backstory="""Eres un editor literario con décadas de experiencia refinando 
            la prosa de autores reconocidos. Tu oído para el lenguaje es extraordinario, 
            capaz de detectar inconsistencias tonales, problemas de flujo y oportunidades 
            para mejoras estilísticas.
            
            Entiendes que el estilo no es solo decoración - es la manera en que la 
            historia se comunica al lector. Cada elección de palabra, cada ritmo de 
            oración, cada decisión estilística debe servir a la historia y al tono 
            general de la obra.
            
            Tu especialidad es encontrar la voz única de cada historia y ayudar a 
            que brille con claridad y potencia. Balanceas la creatividad artística 
            con la claridad comunicativa."""
        )
    
    def analyze_writing_style(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el estilo de escritura del manuscrito"""
        task_description = f"""
        Realiza un análisis completo del estilo de escritura:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de escritura para obtener estadísticas básicas
        2. Usa el analizador de estilo para evaluar tono y perspectiva narrativa
        3. Identifica la voz narrativa dominante y su consistencia
        4. Evalúa la variedad y riqueza del vocabulario
        5. Analiza el flujo y ritmo de la prosa
        6. Sugiere mejoras estilísticas específicas
        
        FORMATO DE SALIDA:
        - Análisis de estadísticas de escritura
        - Evaluación del estilo y tono
        - Identificación de fortalezas estilísticas
        - Áreas de mejora en el estilo
        - Recomendaciones específicas para la prosa
        """
        
        return {"task": task_description, "agent": "style_editor"}
    
    def improve_prose(self, text_segment: str, target_style: str) -> str:
        """Mejora un segmento específico de prosa"""
        task_description = f"""
        Mejora este segmento de prosa hacia un estilo {target_style}:
        
        TEXTO ORIGINAL:
        {text_segment}
        
        Proporciona una versión mejorada que mantenga el significado pero 
        mejore la fluidez, impacto emocional y coherencia estilística.
        """
        
        return task_description
