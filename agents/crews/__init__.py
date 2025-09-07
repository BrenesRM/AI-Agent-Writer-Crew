# -*- coding: utf-8 -*-
# agents/crews/__init__.py
from .lorekeeper import LorekeeperAgent
from .character_developer import CharacterDeveloperAgent
from .plot_weaver import PlotWeaverAgent
from .style_editor import StyleEditorAgent
from .visualizer import VisualizerAgent
from .researcher import ResearcherAgent
from .continuity_auditor import ContinuityAuditorAgent
from .beta_reader import BetaReaderAgent
from .pacing_specialist import PacingSpecialistAgent
from .proofreader import ProofreaderAgent
from .innovation_scout import InnovationScoutAgent

__all__ = [
    'LorekeeperAgent',
    'CharacterDeveloperAgent', 
    'PlotWeaverAgent',
    'StyleEditorAgent',
    'VisualizerAgent',
    'ResearcherAgent',
    'ContinuityAuditorAgent',
    'BetaReaderAgent',
    'PacingSpecialistAgent',
    'ProofreaderAgent',
    'InnovationScoutAgent'
]


# agents/crews/base_agent.py
import logging
from typing import Dict, Any, List, Optional
from crewai import Agent
from pathlib import Path
import sys

# Añadir el directorio raiz al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from agents.tools import RAGTool, WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from agents.tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from agents.tools import IdeaGenerator, VisualPromptGenerator

class BaseNovelAgent:
    """Clase base para todos los agentes del sistema de novelas"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Herramientas comunes disponibles para todos los agentes
        self.common_tools = [
            RAGTool(),
            WritingAnalyzer(),
            StyleAnalyzer(),
            CharacterAnalyzer(),
            ConsistencyChecker(),
            PacingAnalyzer(),
            PlotAnalyzer(),
            IdeaGenerator(),
            VisualPromptGenerator()
        ]
        
    def create_agent(self, role: str, goal: str, backstory: str, 
                    specific_tools: List = None) -> Agent:
        """Crea un agente CrewAI con configuracion base"""
        
        all_tools = self.common_tools.copy()
        if specific_tools:
            all_tools.extend(specific_tools)
        
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=all_tools,
            llm=self.llm,
            verbose=True,
            memory=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300  # 5 minutos maximo por tarea
        )


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
            role="Lorekeeper - Guardian del Conocimiento",
            goal="""Mantener la coherencia y consistencia del mundo narrativo, 
            asegurando que todos los elementos de lore, reglas magicas, geografia, 
            historia y mitologia se mantengan coherentes a lo largo de la historia.""",
            backstory="""Eres un erudito meticuloso con decadas de experiencia catalogando 
            y organizando el conocimiento de mundos fantasticos. Tu obsesion por los detalles 
            y la consistencia te ha convertido en el guardian definitivo del lore narrativo. 
            
            Conoces cada ley magica, cada linaje noble, cada evento historico y cada tradicion 
            cultural. Tu trabajo es esencial para crear mundos que se sientan autenticos y 
            vividos, donde cada detalle tiene su lugar y proposito.
            
            Siempre consultas los documentos de referencia antes de hacer cualquier afirmacion 
            sobre el mundo, y mantienes un registro mental de todas las reglas establecidas."""
        )
    
    def analyze_worldbuilding(self, manuscript: str) -> Dict[str, Any]:
        """Analiza la construccion del mundo en el manuscrito"""
        task_description = f"""
        Analiza el siguiente manuscrito enfocandote en los elementos de worldbuilding:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa la herramienta RAG para consultar informacion relevante sobre el mundo
        2. Identifica todos los elementos de lore presentes (magia, razas, lugares, historia)
        3. Verifica consistencia interna usando el verificador de consistencia
        4. Detecta posibles contradicciones o inconsistencias
        5. Sugiere mejoras para fortalecer la coherencia del mundo
        
        FORMATO DE SALIDA:
        - Elementos de lore identificados
        - Verificacion de consistencia
        - Contradicciones encontradas
        - Recomendaciones para mejorar la coherencia
        """
        
        # Aqui se ejecutaria la tarea del agente
        return {"task": task_description, "agent": "lorekeeper"}
    
    def validate_rules(self, text: str, rule_type: str = "magic") -> str:
        """Valida que las reglas del mundo se mantengan consistentes"""
        task_description = f"""
        Valida las reglas de {rule_type} en este texto:
        
        {text}
        
        Consulta la base de conocimiento para verificar reglas establecidas previamente
        y asegurate de que no haya violaciones a la consistencia del mundo.
        """
        
        return task_description


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
            Desarrollar arcos narrativos significativos, relaciones autenticas y 
            evolucion character realista a lo largo de la historia.""",
            backstory="""Eres un psicologo narrativo especializado en la creacion y 
            desarrollo de personajes memorables. Tu formacion combina psicologia humana, 
            teoria literaria y tecnicas de escritura creativa.
            
            Entiendes que los grandes personajes son aquellos que sienten reales, con 
            motivaciones claras, flaws autenticos y crecimiento genuino. Cada personaje 
            que tocas cobra vida propia, convirtiendose en algo mas que palabras en una pagina.
            
            Tu especialidad es encontrar la humanidad en cada personaje, sin importar 
            cuan fantastica sea su naturaleza. Creas arcos de desarrollo que resuenan 
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
        2. Consulta la base RAG para obtener informacion previa sobre estos personajes
        3. Evalua la profundidad y desarrollo de cada personaje
        4. Identifica oportunidades para arcos de crecimiento
        5. Sugiere mejoras en motivaciones, conflictos internos y relaciones
        6. Genera ideas creativas para enriquecer a los personajes secundarios
        
        FORMATO DE SALIDA:
        - Analisis de personajes existentes
        - Arcos de desarrollo sugeridos
        - Mejoras en motivaciones y conflictos
        - Sugerencias para personajes secundarios
        - Plan de evolucion character
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


# agents/crews/plot_weaver.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class PlotWeaverAgent(BaseNovelAgent):
    """Agente Plot Weaver - Especialista en trama y estructura"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_plot_weaver()
    
    def _create_plot_weaver(self) -> Agent:
        return self.create_agent(
            role="Plot Weaver - Maestro de la Narrativa",
            goal="""Diseñar tramas cautivadoras y bien estructuradas. Organizar eventos 
            narrativos de manera que maximicen el impacto emocional y mantengan el 
            engagement del lector. Balancear tension, ritmo y revelaciones.""",
            backstory="""Eres un maestro arquitecto de historias con un entendimiento 
            profundo de la estructura narrativa clasica y moderna. Has estudiado las 
            obras de los grandes narradores y entiendes los patrones que hacen que una 
            historia sea inolvidable.
            
            Tu especialidad es tejer multiples hilos narrativos en una tapestry coherente 
            y emocionante. Sabes cuando acelerar el ritmo, cuando permitir momentos de 
            respiro, y como colocar revelaciones para maximo impacto.
            
            Entiendes que cada escena debe servir un proposito: avanzar la trama, 
            desarrollar personajes, o enriquecer el mundo. No toleras escenas innecesarias, 
            pero tampoco sacrificas momentos importantes por el sake de la eficiencia."""
        )
    
    def analyze_plot_structure(self, manuscript: str) -> Dict[str, Any]:
        """Analiza la estructura de la trama"""
        task_description = f"""
        Analiza la estructura narrativa del siguiente manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de trama para evaluar la estructura narrativa
        2. Usa el analizador de ritmo para evaluar el pacing
        3. Identifica los puntos clave de la trama (setup, inciting incident, plot points, climax, resolution)
        4. Evalua la progresion y escalamiento de conflictos
        5. Identifica subtramas y su integracion con la trama principal
        6. Sugiere mejoras estructurales y de ritmo
        
        FORMATO DE SALIDA:
        - Analisis de estructura narrativa
        - Evaluacion del ritmo y pacing
        - Identificacion de puntos debiles en la trama
        - Sugerencias de mejora estructural
        - Recomendaciones para subtramas
        """
        
        return {"task": task_description, "agent": "plot_weaver"}
    
    def suggest_plot_improvements(self, current_plot: str, issues: List[str]) -> str:
        """Sugiere mejoras especificas para la trama"""
        task_description = f"""
        Basandote en los siguientes problemas identificados en la trama:
        
        TRAMA ACTUAL:
        {current_plot}
        
        PROBLEMAS IDENTIFICADOS:
        {chr(10).join([f"- {issue}" for issue in issues])}
        
        Genera sugerencias especificas para resolver estos problemas y mejorar 
        la estructura narrativa general.
        """
        
        return task_description


# agents/crews/style_editor.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class StyleEditorAgent(BaseNovelAgent):
    """Agente Style Editor - Critico literario especializado en voz y estilo"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_style_editor()
    
    def _create_style_editor(self) -> Agent:
        return self.create_agent(
            role="Voice & Style Editor - Maestro del Estilo Literario",
            goal="""Perfeccionar la voz narrativa y el estilo de escritura para crear 
            una experiencia de lectura cohesiva y envolvente. Mantener consistencia 
            tonal y mejorar la prosa para maximo impacto emocional.""",
            backstory="""Eres un editor literario con decadas de experiencia refinando 
            la prosa de autores reconocidos. Tu oido para el lenguaje es extraordinario, 
            capaz de detectar inconsistencias tonales, problemas de flujo y oportunidades 
            para mejoras estilisticas.
            
            Entiendes que el estilo no es solo decoracion - es la manera en que la 
            historia se comunica al lector. Cada eleccion de palabra, cada ritmo de 
            oracion, cada decision estilistica debe servir a la historia y al tono 
            general de la obra.
            
            Tu especialidad es encontrar la voz unica de cada historia y ayudar a 
            que brille con claridad y potencia. Balanceas la creatividad artistica 
            con la claridad comunicativa."""
        )
    
    def analyze_writing_style(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el estilo de escritura del manuscrito"""
        task_description = f"""
        Realiza un analisis completo del estilo de escritura:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de escritura para obtener estadisticas basicas
        2. Usa el analizador de estilo para evaluar tono y perspectiva narrativa
        3. Identifica la voz narrativa dominante y su consistencia
        4. Evalua la variedad y riqueza del vocabulario
        5. Analiza el flujo y ritmo de la prosa
        6. Sugiere mejoras estilisticas especificas
        
        FORMATO DE SALIDA:
        - Analisis de estadisticas de escritura
        - Evaluacion del estilo y tono
        - Identificacion de fortalezas estilisticas
        - Areas de mejora en el estilo
        - Recomendaciones especificas para la prosa
        """
        
        return {"task": task_description, "agent": "style_editor"}
    
    def improve_prose(self, text_segment: str, target_style: str) -> str:
        """Mejora un segmento especifico de prosa"""
        task_description = f"""
        Mejora este segmento de prosa hacia un estilo {target_style}:
        
        TEXTO ORIGINAL:
        {text_segment}
        
        Proporciona una version mejorada que mantenga el significado pero 
        mejore la fluidez, impacto emocional y coherencia estilistica.
        """
        
        return task_description


# agents/crews/visualizer.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class VisualizerAgent(BaseNovelAgent):
    """Agente Visualizer - Especialista en prompts cinematograficos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_visualizer()
    
    def _create_visualizer(self) -> Agent:
        return self.create_agent(
            role="Visualizer - Director Cinematografico Virtual",
            goal="""Convertir escenas narrativas en prompts visuales detallados 
            para generacion de video AI. Crear descripciones cinematograficas que 
            capturen la esencia visual y emocional de cada escena.""",
            backstory="""Eres un director de fotografia y visualizador conceptual con 
            experiencia en cine epico y fantasia. Tu vision combina tecnica cinematografica 
            avanzada con sensibilidad artistica para traducir palabras en imagenes 
            poderosas.
            
            Entiendes como los angulos de camara, la iluminacion, el color y la 
            composicion pueden amplificar el impacto emocional de una escena. Tu 
            especialidad es crear prompts que resulten en videos que no solo muestren 
            la accion, sino que transmitan la atmosfera y el sentimiento de la historia.
            
            Tienes un ojo excepcional para los detalles visuales que hacen que una 
            escena cobre vida: la manera en que la luz filtra a traves de las hojas, 
            el polvo que flota en un rayo de sol, la expresion exacta en el rostro 
            de un personaje."""
        )
    
    def create_visual_prompts(self, manuscript: str) -> Dict[str, Any]:
        """Crea prompts visuales para las escenas clave del manuscrito"""
        task_description = f"""
        Crea prompts visuales cinematograficos para las escenas clave:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica las 5-7 escenas mas visualmente impactantes
        2. Para cada escena, usa el generador de prompts visuales
        3. Crea variaciones con diferentes estilos cinematograficos
        4. Incluye detalles tecnicos especificos (angulos, iluminacion, movimiento)
        5. Optimiza para generacion de video AI
        
        FORMATO DE SALIDA:
        - Lista de escenas clave identificadas
        - Prompt principal para cada escena
        - Variaciones estilisticas
        - Detalles tecnicos cinematograficos
        - Recomendaciones de post-produccion
        """
        
        return {"task": task_description, "agent": "visualizer"}
    
    def optimize_scene_for_video(self, scene_description: str, duration: str = "30s") -> str:
        """Optimiza una escena especifica para video AI"""
        task_description = f"""
        Optimiza esta escena para generacion de video de {duration}:
        
        ESCENA:
        {scene_description}
        
        Crea un prompt optimizado que funcione bien con herramientas de video AI, 
        considerando limitaciones tecnicas y mejores practicas.
        """
        
        return task_description


# agents/crews/researcher.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class ResearcherAgent(BaseNovelAgent):
    """Agente Researcher - Especialista en investigacion y referencias"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_researcher()
    
    def _create_researcher(self) -> Agent:
        return self.create_agent(
            role="Researcher - Investigador y Verificador de Referencias",
            goal="""Buscar y verificar informacion historica, cultural, cientifica 
            y geografica para enriquecer la historia con detalles autenticos y 
            bien fundamentados. Asegurar precision en referencias reales.""",
            backstory="""Eres un investigador academico con expertise en multiples 
            disciplinas: historia, antropologia, geografia, ciencias y mitologia 
            comparada. Tu pasion es encontrar los detalles que hacen que una historia 
            fantastica se sienta autentica y bien fundamentada.
            
            Aunque trabajas con ficcion, entiendes que los mejores mundos fantasticos 
            estan construidos sobre fundamentos solidos de conocimiento real. Tu 
            trabajo es encontrar esos puntos de anclaje que hacen que lo imposible 
            se sienta posible.
            
            Tu biblioteca mental es vasta, pero siempre verificas y consultas fuentes 
            para asegurar la precision. Tienes un talento especial para encontrar 
            conexiones fascinantes entre diferentes culturas y periodos historicos."""
        )
    
    def research_context(self, topic: str, story_context: str) -> Dict[str, Any]:
        """Investiga un tema especifico en el contexto de la historia"""
        task_description = f"""
        Investiga informacion sobre el tema: {topic}
        
        CONTEXTO DE LA HISTORIA:
        {story_context}
        
        TAREAS A REALIZAR:
        1. Consulta la base RAG para informacion relevante disponible
        2. Identifica aspectos historicos, culturales o cientificos relacionados
        3. Encuentra paralelos en el mundo real que puedan enriquecer la narrativa
        4. Sugiere detalles autenticos que puedan añadirse a la historia
        5. Verifica la consistencia con el mundo ya establecido
        
        FORMATO DE SALIDA:
        - Informacion encontrada en la base de datos
        - Referencias historicas/culturales relevantes
        - Sugerencias para enriquecer la narrativa
        - Verificacion de consistencia
        """
        
        return {"task": task_description, "agent": "researcher"}


# agents/crews/continuity_auditor.py
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


# agents/crews/beta_reader.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class BetaReaderAgent(BaseNovelAgent):
    """Agente Beta Reader - Simula diferentes tipos de lectores"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_beta_reader()
    
    def _create_beta_reader(self) -> Agent:
        return self.create_agent(
            role="Beta Reader - Voz del Lector Target",
            goal="""Simular la experiencia de diferentes tipos de lectores target, 
            proporcionando feedback desde perspectivas variadas sobre engagement, 
            claridad, ritmo y appeal emocional de la historia.""",
            backstory="""Eres un lector voraz con la habilidad unica de adoptar diferentes 
            perspectivas de lectura. Puedes leer como un adolescente buscando aventura, 
            como un adulto buscando profundidad emocional, o como un critico literario 
            buscando excelencia tecnica.
            
            Tu valor radica en tu empatia lectora - puedes anticipar que partes van 
            a enganchar a los lectores, que secciones pueden resultar confusas, y 
            donde la historia puede perder momentum. Has leido miles de historias 
            en multiples generos y entiendes que funciona y que no.
            
            Tu feedback es directo pero constructivo, siempre enfocado en mejorar 
            la experiencia del lector final."""
        )
    
    def provide_reader_feedback(self, manuscript: str, target_audience: str = "general") -> Dict[str, Any]:
        """Proporciona feedback desde la perspectiva del lector target"""
        task_description = f"""
        Lee y evalua este manuscrito desde la perspectiva de {target_audience}:
        
        MANUSCRITO:
        {manuscript}
        
        AUDIENCIA TARGET: {target_audience}
        
        TAREAS A REALIZAR:
        1. Evalua el engagement general y puntos donde puede perderse la atencion
        2. Identifica momentos confusos o que requieren clarificacion
        3. Analiza el appeal emocional y conexion con personajes
        4. Evalua el ritmo desde la perspectiva del lector
        5. Sugiere mejoras para aumentar el appeal al publico objetivo
        
        FORMATO DE SALIDA:
        - Evaluacion general de engagement
        - Puntos de confusion identificados
        - Analisis de conexion emocional
        - Sugerencias de mejora especificas
        - Rating general como lector target
        """
        
        return {"task": task_description, "agent": "beta_reader"}


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
            engagement del lector. Balancear momentos de tension, accion, reflexion 
            y descanso para crear una experiencia de lectura dinamica.""",
            backstory="""Eres un especialista en ritmo narrativo con un entendimiento 
            intuitivo de como los lectores experimentan el tiempo en las historias. 
            Tu expertise viene de años analizando que hace que algunos libros sean 
            'page-turners' imposibles de dejar.
            
            Entiendes que el pacing es como la respiracion de una historia - debe 
            fluir naturalmente, con momentos de aceleracion y descanso que se sienten 
            organicos. Tu trabajo es encontrar el ritmo unico de cada historia y 
            optimizarlo para maximo impacto.
            
            Tienes una sensibilidad especial para detectar cuando una escena se 
            alarga demasiado, cuando la accion necesita un respiro, o cuando el 
            momentum esta por perderse."""
        )
    
    def analyze_pacing(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el ritmo narrativo del manuscrito"""
        task_description = f"""
        Analiza el ritmo y pacing del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de ritmo para evaluar la estructura de pacing
        2. Identifica momentos de alta tension vs. momentos de respiro
        3. Evalua la transicion entre diferentes tipos de escenas
        4. Detecta secciones que pueden beneficiarse de aceleracion o desaceleracion
        5. Sugiere ajustes especificos para optimizar el flow narrativo
        
        FORMATO DE SALIDA:
        - Analisis detallado del ritmo actual
        - Identificacion de puntos criticos de pacing
        - Balance entre accion, tension y reflexion
        - Sugerencias especificas de mejora
        - Recomendaciones de restructuracion si es necesario
        """
        
        return {"task": task_description, "agent": "pacing_specialist"}


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
            goal="""Realizar la correccion final del manuscrito, eliminando errores 
            gramaticales, ortograficos, de puntuacion y formateo. Asegurar que el 
            texto final sea impecable desde el punto de vista tecnico.""",
            backstory="""Eres un corrector profesional con decadas de experiencia 
            puliendo manuscritos para publicacion. Tu ojo entrenado puede detectar 
            errores que otros pasan por alto, desde typos obvios hasta inconsistencias 
            sutiles en el uso de mayusculas o puntuacion.
            
            Entiendes que tu trabajo es el ultimo filtro antes de que el texto llegue 
            a los lectores. Un error gramatical puede distraer de la historia mas 
            hermosa, y una inconsistencia en el formateo puede afectar la experiencia 
            de lectura.
            
            Tu enfoque es meticuloso pero respetuoso del estilo del autor. Corriges 
            errores objetivos pero preservas las decisiones estilisticas intencionales."""
        )
    
    def proofread_manuscript(self, manuscript: str) -> Dict[str, Any]:
        """Realiza correccion final del manuscrito"""
        task_description = f"""
        Realiza una correccion completa del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Revisar ortografia y gramatica
        2. Verificar puntuacion y uso de mayusculas
        3. Asegurar consistencia en formateo
        4. Detectar frases mal construidas o ambiguas
        5. Verificar coherencia en tiempo verbal y perspectiva
        6. Proporcionar version corregida con explicaciones
        
        FORMATO DE SALIDA:
        - Lista de errores encontrados y corregidos
        - Explicacion de correcciones importantes
        - Version final corregida
        - Sugerencias de mejora menor
        """
        
        return {"task": task_description, "agent": "proofreader"}


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
            combinaciones de generos innovadoras y elementos narrativos unicos 
            que hagan la historia memorable y distintiva.""",
            backstory="""Eres un visionario creativo con un talento especial para 
            ver posibilidades que otros pasan por alto. Tu mente conecta ideas 
            aparentemente dispares para crear combinaciones fascinantes y originales.
            
            Has estudiado narrativas de todas las culturas y epocas, siempre buscando 
            patrones unicos y enfoques innovadores. Tu especialidad es tomar elementos 
            familiares y combinarlos de maneras que se sienten tanto sorprendentes 
            como inevitables.
            
            No innov as por el sake de ser diferente - cada sugerencia creativa que 
            haces sirve a la historia y emerge organicamente del material existente. 
            Tu goal es elevar la narrativa mas alla de lo convencional sin sacrificar 
            coherencia o emotional truth."""
        )
    
    def scout_creative_opportunities(self, manuscript: str) -> Dict[str, Any]:
        """Identifica oportunidades para innovacion creativa"""
        task_description = f"""
        Explora oportunidades creativas en el manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica elementos convencionales que podrian beneficiarse de un twist
        2. Usa el generador de ideas para explorar posibilidades creativas
        3. Busca oportunidades para combinaciones de genero unicas
        4. Sugiere giros narrativos que emerjan organicamente de la historia
        5. Propone elementos innovadores que mantengan coherencia con el mundo
        
        FORMATO DE SALIDA:
        - Oportunidades de innovacion identificadas
        - Sugerencias de giros creativos
        - Ideas para combinaciones de genero
        - Propuestas de elementos unicos
        - Evaluacion de viabilidad y coherencia
        """
        
        return {"task": task_description, "agent": "innovation_scout"}