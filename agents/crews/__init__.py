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

# Añadir el directorio raíz al path
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
        """Crea un agente CrewAI con configuración base"""
        
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
            max_execution_time=300  # 5 minutos máximo por tarea
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
            role="Lorekeeper - Guardián del Conocimiento",
            goal="""Mantener la coherencia y consistencia del mundo narrativo, 
            asegurando que todos los elementos de lore, reglas mágicas, geografía, 
            historia y mitología se mantengan coherentes a lo largo de la historia.""",
            backstory="""Eres un erudito meticuloso con décadas de experiencia catalogando 
            y organizando el conocimiento de mundos fantásticos. Tu obsesión por los detalles 
            y la consistencia te ha convertido en el guardián definitivo del lore narrativo. 
            
            Conoces cada ley mágica, cada linaje noble, cada evento histórico y cada tradición 
            cultural. Tu trabajo es esencial para crear mundos que se sientan auténticos y 
            vividos, donde cada detalle tiene su lugar y propósito.
            
            Siempre consultas los documentos de referencia antes de hacer cualquier afirmación 
            sobre el mundo, y mantienes un registro mental de todas las reglas establecidas."""
        )
    
    def analyze_worldbuilding(self, manuscript: str) -> Dict[str, Any]:
        """Analiza la construcción del mundo en el manuscrito"""
        task_description = f"""
        Analiza el siguiente manuscrito enfocándote en los elementos de worldbuilding:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa la herramienta RAG para consultar información relevante sobre el mundo
        2. Identifica todos los elementos de lore presentes (magia, razas, lugares, historia)
        3. Verifica consistencia interna usando el verificador de consistencia
        4. Detecta posibles contradicciones o inconsistencias
        5. Sugiere mejoras para fortalecer la coherencia del mundo
        
        FORMATO DE SALIDA:
        - Elementos de lore identificados
        - Verificación de consistencia
        - Contradicciones encontradas
        - Recomendaciones para mejorar la coherencia
        """
        
        # Aquí se ejecutaría la tarea del agente
        return {"task": task_description, "agent": "lorekeeper"}
    
    def validate_rules(self, text: str, rule_type: str = "magic") -> str:
        """Valida que las reglas del mundo se mantengan consistentes"""
        task_description = f"""
        Valida las reglas de {rule_type} en este texto:
        
        {text}
        
        Consulta la base de conocimiento para verificar reglas establecidas previamente
        y asegúrate de que no haya violaciones a la consistencia del mundo.
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
            engagement del lector. Balancear tensión, ritmo y revelaciones.""",
            backstory="""Eres un maestro arquitecto de historias con un entendimiento 
            profundo de la estructura narrativa clásica y moderna. Has estudiado las 
            obras de los grandes narradores y entiendes los patrones que hacen que una 
            historia sea inolvidable.
            
            Tu especialidad es tejer múltiples hilos narrativos en una tapestry coherente 
            y emocionante. Sabes cuándo acelerar el ritmo, cuándo permitir momentos de 
            respiro, y cómo colocar revelaciones para máximo impacto.
            
            Entiendes que cada escena debe servir un propósito: avanzar la trama, 
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
        4. Evalúa la progresión y escalamiento de conflictos
        5. Identifica subtramas y su integración con la trama principal
        6. Sugiere mejoras estructurales y de ritmo
        
        FORMATO DE SALIDA:
        - Análisis de estructura narrativa
        - Evaluación del ritmo y pacing
        - Identificación de puntos débiles en la trama
        - Sugerencias de mejora estructural
        - Recomendaciones para subtramas
        """
        
        return {"task": task_description, "agent": "plot_weaver"}
    
    def suggest_plot_improvements(self, current_plot: str, issues: List[str]) -> str:
        """Sugiere mejoras específicas para la trama"""
        task_description = f"""
        Basándote en los siguientes problemas identificados en la trama:
        
        TRAMA ACTUAL:
        {current_plot}
        
        PROBLEMAS IDENTIFICADOS:
        {chr(10).join([f"- {issue}" for issue in issues])}
        
        Genera sugerencias específicas para resolver estos problemas y mejorar 
        la estructura narrativa general.
        """
        
        return task_description


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


# agents/crews/visualizer.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class VisualizerAgent(BaseNovelAgent):
    """Agente Visualizer - Especialista en prompts cinematográficos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_visualizer()
    
    def _create_visualizer(self) -> Agent:
        return self.create_agent(
            role="Visualizer - Director Cinematográfico Virtual",
            goal="""Convertir escenas narrativas en prompts visuales detallados 
            para generación de video AI. Crear descripciones cinematográficas que 
            capturen la esencia visual y emocional de cada escena.""",
            backstory="""Eres un director de fotografía y visualizador conceptual con 
            experiencia en cine épico y fantasía. Tu visión combina técnica cinematográfica 
            avanzada con sensibilidad artística para traducir palabras en imágenes 
            poderosas.
            
            Entiendes cómo los ángulos de cámara, la iluminación, el color y la 
            composición pueden amplificar el impacto emocional de una escena. Tu 
            especialidad es crear prompts que resulten en videos que no solo muestren 
            la acción, sino que transmitan la atmósfera y el sentimiento de la historia.
            
            Tienes un ojo excepcional para los detalles visuales que hacen que una 
            escena cobre vida: la manera en que la luz filtra a través de las hojas, 
            el polvo que flota en un rayo de sol, la expresión exacta en el rostro 
            de un personaje."""
        )
    
    def create_visual_prompts(self, manuscript: str) -> Dict[str, Any]:
        """Crea prompts visuales para las escenas clave del manuscrito"""
        task_description = f"""
        Crea prompts visuales cinematográficos para las escenas clave:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica las 5-7 escenas más visualmente impactantes
        2. Para cada escena, usa el generador de prompts visuales
        3. Crea variaciones con diferentes estilos cinematográficos
        4. Incluye detalles técnicos específicos (ángulos, iluminación, movimiento)
        5. Optimiza para generación de video AI
        
        FORMATO DE SALIDA:
        - Lista de escenas clave identificadas
        - Prompt principal para cada escena
        - Variaciones estilísticas
        - Detalles técnicos cinematográficos
        - Recomendaciones de post-producción
        """
        
        return {"task": task_description, "agent": "visualizer"}
    
    def optimize_scene_for_video(self, scene_description: str, duration: str = "30s") -> str:
        """Optimiza una escena específica para video AI"""
        task_description = f"""
        Optimiza esta escena para generación de video de {duration}:
        
        ESCENA:
        {scene_description}
        
        Crea un prompt optimizado que funcione bien con herramientas de video AI, 
        considerando limitaciones técnicas y mejores prácticas.
        """
        
        return task_description


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
            
            Tu obsesión por la consistencia viene de entender que los lectores notan 
            las inconsistencias, y que estas pueden romper la inmersión en la historia. 
            Un personaje que cambia de color de ojos, una fecha que no cuadra, o una 
            regla mágica que se viola sin explicación - nada escapa a tu atención.
            
            Trabajas sistemáticamente, creando timelines detallados, profiles de 
            personajes y registros de reglas del mundo. Tu trabajo es invisible cuando 
            está bien hecho, pero esencial para la credibilidad de la narrativa."""
        )
    
    def audit_continuity(self, manuscript: str, reference_materials: str = "") -> Dict[str, Any]:
        """Audita la continuidad del manuscrito completo"""
        task_description = f"""
        Realiza una auditoría completa de continuidad:
        
        MANUSCRITO:
        {manuscript}
        
        MATERIALES DE REFERENCIA:
        {reference_materials}
        
        TAREAS A REALIZAR:
        1. Usa el verificador de consistencia para detectar contradicciones
        2. Verifica consistencia de personajes (descripción física, personalidad, habilidades)
        3. Audita la timeline y secuencia de eventos
        4. Verifica reglas del mundo y su aplicación consistente
        5. Identifica discrepancias con materiales de referencia
        6. Crea un reporte detallado de problemas encontrados
        
        FORMATO DE SALIDA:
        - Reporte de consistencia general
        - Inconsistencias de personajes detectadas
        - Problemas de timeline identificados
        - Violaciones a reglas del mundo
        - Recomendaciones para corrección
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
            backstory="""Eres un lector voraz con la habilidad única de adoptar diferentes 
            perspectivas de lectura. Puedes leer como un adolescente buscando aventura, 
            como un adulto buscando profundidad emocional, o como un crítico literario 
            buscando excelencia técnica.
            
            Tu valor radica en tu empatía lectora - puedes anticipar qué partes van 
            a enganchar a los lectores, qué secciones pueden resultar confusas, y 
            dónde la historia puede perder momentum. Has leído miles de historias 
            en múltiples géneros y entiendes qué funciona y qué no.
            
            Tu feedback es directo pero constructivo, siempre enfocado en mejorar 
            la experiencia del lector final."""
        )
    
    def provide_reader_feedback(self, manuscript: str, target_audience: str = "general") -> Dict[str, Any]:
        """Proporciona feedback desde la perspectiva del lector target"""
        task_description = f"""
        Lee y evalúa este manuscrito desde la perspectiva de {target_audience}:
        
        MANUSCRITO:
        {manuscript}
        
        AUDIENCIA TARGET: {target_audience}
        
        TAREAS A REALIZAR:
        1. Evalúa el engagement general y puntos donde puede perderse la atención
        2. Identifica momentos confusos o que requieren clarificación
        3. Analiza el appeal emocional y conexión con personajes
        4. Evalúa el ritmo desde la perspectiva del lector
        5. Sugiere mejoras para aumentar el appeal al público objetivo
        
        FORMATO DE SALIDA:
        - Evaluación general de engagement
        - Puntos de confusión identificados
        - Análisis de conexión emocional
        - Sugerencias de mejora específicas
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
            engagement del lector. Balancear momentos de tensión, acción, reflexión 
            y descanso para crear una experiencia de lectura dinámica.""",
            backstory="""Eres un especialista en ritmo narrativo con un entendimiento 
            intuitivo de cómo los lectores experimentan el tiempo en las historias. 
            Tu expertise viene de años analizando qué hace que algunos libros sean 
            'page-turners' imposibles de dejar.
            
            Entiendes que el pacing es como la respiración de una historia - debe 
            fluir naturalmente, con momentos de aceleración y descanso que se sienten 
            orgánicos. Tu trabajo es encontrar el ritmo único de cada historia y 
            optimizarlo para máximo impacto.
            
            Tienes una sensibilidad especial para detectar cuando una escena se 
            alarga demasiado, cuando la acción necesita un respiro, o cuando el 
            momentum está por perderse."""
        )
    
    def analyze_pacing(self, manuscript: str) -> Dict[str, Any]:
        """Analiza el ritmo narrativo del manuscrito"""
        task_description = f"""
        Analiza el ritmo y pacing del manuscrito:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Usa el analizador de ritmo para evaluar la estructura de pacing
        2. Identifica momentos de alta tensión vs. momentos de respiro
        3. Evalúa la transición entre diferentes tipos de escenas
        4. Detecta secciones que pueden beneficiarse de aceleración o desaceleración
        5. Sugiere ajustes específicos para optimizar el flow narrativo
        
        FORMATO DE SALIDA:
        - Análisis detallado del ritmo actual
        - Identificación de puntos críticos de pacing
        - Balance entre acción, tensión y reflexión
        - Sugerencias específicas de mejora
        - Recomendaciones de restructuración si es necesario
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