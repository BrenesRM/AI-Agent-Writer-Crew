# -*- coding: utf-8 -*-
# agents/crews/continuity_auditor.py
from typing import Any, Dict
from .base_agent import BaseNovelAgent
from crewai import Agent

class ContinuityAuditorAgent(BaseNovelAgent):
    """Agente Continuity Auditor - Especialista en consistencia narrativa"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_continuity_auditor()
    
    def _create_continuity_auditor(self) -> Agent:
        return self.create_agent(
            role="Continuity Auditor - Guardian de la Consistencia",
            goal="""Verificar y mantener la continuidad perfecta en todos los aspectos 
            de la narrativa: personajes, timeline, reglas del mundo y detalles 
            descriptivos. Eliminar inconsistencias y contradicciones.""",
            backstory="""Eres un auditor meticuloso especializado en continuity para 
            producciones complejas. Tu mente funciona como una base de datos viviente, 
            capaz de recordar y cross-referenciar cada detalle mencionado en una historia.
            
            Tu obsesion por la consistencia viene de entender que los lectores notan 
            las inconsistencias, y que estas pueden romper la inmersion en la historia. 
            Un personaje que cambia de color de ojos, una fecha que no cuadra, o una 
            regla magica que se viola sin explicacion - nada escapa a tu atencion.
            
            Trabajas sistematicamente, creando timelines detallados, profiles de 
            personajes y registros de reglas del mundo. Tu trabajo es invisible cuando 
            esta bien hecho, pero esencial para la credibilidad de la narrativa."""
        )
    
    def audit_continuity(self, manuscript: str, reference_materials: str = "") -> Dict[str, Any]:
        """Audita la continuidad del manuscrito completo"""
        task_description = f"""
        Realiza una auditoria completa de continuidad:
        
        MANUSCRITO:
        {manuscript}
        
        MATERIALES DE REFERENCIA:
        {reference_materials}
        
        TAREAS A REALIZAR:
        1. Usa el verificador de consistencia para detectar contradicciones
        2. Verifica consistencia de personajes (descripcion fisica, personalidad, habilidades)
        3. Audita la timeline y secuencia de eventos
        4. Verifica reglas del mundo y su aplicacion consistente
        5. Identifica discrepancias con materiales de referencia
        6. Crea un reporte detallado de problemas encontrados
        
        FORMATO DE SALIDA:
        - Reporte de consistencia general
        - Inconsistencias de personajes detectadas
        - Problemas de timeline identificados
        - Violaciones a reglas del mundo
        - Recomendaciones para correccion
        """
        
        return {"task": task_description, "agent": "continuity_auditor"}
