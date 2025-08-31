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
            goal="""Realizar la corrección final del manuscrito, eliminando errores 
            gramaticales, ortográficos, de puntuación y formateo. Asegurar que el 
            texto final sea impecable desde el punto de vista técnico.""",
            backstory="""Eres un corrector profesional con décadas de experiencia 
            puliendo manuscritos para publicación. Tu ojo entrenado puede detectar 
            errores que otros pasan por alto, desde typos obvios hasta inconsistencias 
            sutiles en el uso de mayúsculas o puntuación.
            
            Entiendes que tu trabajo es el último filtro antes de que el texto llegue 
            a los lectores. Un error gramatical puede distraer de la historia más 
            hermosa, y una inconsistencia en el formateo puede afectar la experiencia 
            de lectura.
            
            Tu enfoque es meticuloso pero respetuoso del estilo del autor. Corriges 
            errores objetivos pero preservas las decisiones estilísticas intencionales."""
        )
    
    def proofread_manuscript(self, manuscript: str) -> Dict[str, Any]:
        """Realiza corrección final del manuscrito"""
        task_description = f"""
        Realiza una corrección completa del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Revisar ortografía y gramática
        2. Verificar puntuación y uso de mayúsculas
        3. Asegurar consistencia en formateo
        4. Detectar frases mal construidas o ambiguas
        5. Verificar coherencia en tiempo verbal y perspectiva
        6. Proporcionar versión corregida con explicaciones
        
        FORMATO DE SALIDA:
        - Lista de errores encontrados y corregidos
        - Explicación de correcciones importantes
        - Versión final corregida
        - Sugerencias de mejora menor
        """
        
        return {"task": task_description, "agent": "proofreader"}
