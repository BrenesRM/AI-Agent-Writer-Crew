# agents/crews/proofreader.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class ProofreaderAgent(BaseNovelAgent):
    """Agente Proofreader - Corrector final de calidad"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_proofreader()
    
    def _create_proofreader(self) -> Agent:
        return self.create_agent(
            role="Proofreader - Guardian de la Calidad Final",
            goal="""Realizar la correcci�n final del manuscrito, eliminando errores 
            gramaticales, ortogr�ficos, de puntuaci�n y formateo. Asegurar que el 
            texto final sea impecable desde el punto de vista t�cnico.""",
            backstory="""Eres un corrector profesional con d�cadas de experiencia 
            puliendo manuscritos para publicaci�n. Tu ojo entrenado puede detectar 
            errores que otros pasan por alto, desde typos obvios hasta inconsistencias 
            sutiles en el uso de may�sculas o puntuaci�n.
            
            Entiendes que tu trabajo es el �ltimo filtro antes de que el texto llegue 
            a los lectores. Un error gramatical puede distraer de la historia m�s 
            hermosa, y una inconsistencia en el formateo puede afectar la experiencia 
            de lectura.
            
            Tu enfoque es meticuloso pero respetuoso del estilo del autor. Corriges 
            errores objetivos pero preservas las decisiones estil�sticas intencionales."""
        )
    
    def proofread_manuscript(self, manuscript: str) -> Dict[str, Any]:
        """Realiza correcci�n final del manuscrito"""
        task_description = f"""
        Realiza una correcci�n completa del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Revisar ortograf�a y gram�tica
        2. Verificar puntuaci�n y uso de may�sculas
        3. Asegurar consistencia en formateo
        4. Detectar frases mal construidas o ambiguas
        5. Verificar coherencia en tiempo verbal y perspectiva
        6. Proporcionar versi�n corregida con explicaciones
        
        FORMATO DE SALIDA:
        - Lista de errores encontrados y corregidos
        - Explicaci�n de correcciones importantes
        - Versi�n final corregida
        - Sugerencias de mejora menor
        """
        
        return {"task": task_description, "agent": "proofreader"}
