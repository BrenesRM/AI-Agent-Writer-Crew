#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definición de agentes especializados para mejora de historias
"""
import os
from typing import List, Dict, Any
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from pathlib import Path
import sys

# Agregar path para importaciones
sys.path.append(str(Path(__file__).parent.parent))
from agents.tools.base_tools import RAGSearchTool, ManuscriptReaderTool, StoryElementExtractorTool, OutputWriterTool

class StoryEnhancementAgents:
    """Clase principal para gestionar todos los agentes del sistema"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """Inicializar agentes con configuración de LLM"""
        
        # Configurar LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=2000
        )
        
        # Inicializar herramientas compartidas
        self.rag_tool = RAGSearchTool()
        self.manuscript_tool = ManuscriptReaderTool()
        self.extractor_tool = StoryElementExtractorTool()
        self.output_tool = OutputWriterTool()
        
        # Crear agentes
        self.agents = self._create_agents()
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Crear todos los agentes especializados"""
        
        agents = {}
        
        # ========================================
        # THE LOREKEEPER - Analista de Lore y Reglas
        # ========================================
        agents['lorekeeper'] = Agent(
            role='The Lorekeeper',
            goal=(
                'Analizar y mantener la consistencia del lore, reglas del mundo, '
                'historia, mitología y elementos fantásticos de la narrativa.'
            ),
            backstory=(
                'Eres un erudito obsesionado con los detalles y la consistencia. '
                'Tu conocimiento abarca la historia completa del mundo, sus reglas '
                'mágicas, culturas, religiones y tradiciones. Detectas inconsistencias '
                'inmediatamente y propones soluciones que enriquecen el mundo narrativo.'
            ),
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=3,
            allow_delegation=False
        )
        
        # ========================================
        # THE CHARACTER DEVELOPER - Editor de Personajes
        # ========================================
        agents['character_developer'] = Agent(
            role='The Character Developer',
            goal=(
                'Desarrollar personajes profundos, auténticos y memorables '
                'con arcos narrativos coherentes, motivaciones claras y evolución natural.'
            ),
            backstory=(
                'Eres un psicólogo narrativo especializado en desarrollo de personajes. '
                'Entiendes las complejidades de la personalidad humana y cómo traducirlas '
                'a personajes ficticios convincentes. Cada personaje debe sentirse real, '
                'con defectos, fortalezas, miedos y deseos que impulsen la historia.'
            ),
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=3,
            allow_delegation=False
        )
        
        # ========================================
        # THE PLOT WEAVER - Especialista en Trama
        # ========================================
        agents['plot_weaver'] = Agent(
            role='The Plot Weaver',
            goal=(
                'Construir tramas sólidas, bien estructuradas y emocionalmente impactantes '
                'que mantengan al lector enganchado desde el primer capítulo hasta el final.'
            ),
            backstory=(
                'Eres un maestro de la narrativa con décadas de experiencia en estructura '
                'dramática. Conoces los secretos del ritmo, la tensión, los giros argumentales '
                'y cómo balancear múltiples subtramas. Tu especialidad es encontrar el corazón '
                'emocional de cada historia y construir todo alrededor de él.'
            ),
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=3,
            allow_delegation=False
        )
        
        # ========================================
        # THE VOICE & STYLE EDITOR - Crítico Literario
        # ========================================
        agents['voice_editor'] = Agent(
            role='The Voice & Style Editor',
            goal=(
                'Refinar la voz narrativa, el estilo de escritura y la prosa '
                'para crear una experiencia de lectura fluida, evocativa y memorable.'
            ),
            backstory=(
                'Eres un editor literario de élite con un oído perfecto para el lenguaje. '
                'Detectas inconsistencias en el tono, problemas de ritmo, redundancias '
                'y oportunidades para mejorar la prosa. Tu trabajo transforma buenas '
                'historias en obras maestras de la literatura.'
            ),
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=3,
            allow_delegation=False
        )
        
        # ========================================
        # THE VISUALIZER - Agente Cinematográfico
        # ========================================
        agents['visualizer'] = Agent(
            role='The Visualizer',
            goal=(
                'Crear descripciones cinematográficas detalladas y prompts visuales '
                'para las escenas clave, optimizados para generación de video AI.'
            ),
            backstory=(
                'Eres un director de cine visionario especializado en fantasía épica. '
                'Tu mente funciona en términos de encuadres, iluminación, composición '
                'y movimiento. Traducir escenas escritas a lenguaje cinematográfico '
                'es tu superpoder, creando prompts que generan imágenes impactantes.'
            ),
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool, self.output_tool],
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=3,
            allow_delegation=False
        )
        
        return agents
    
    def create_tasks(self, manuscript_content: str) -> List[Task]:
        """Crear tareas específicas para cada agente"""
        
        tasks = []
        
        # ========================================
        # TASK 1: LORE ANALYSIS
        # ========================================
        lore_task = Task(
            description=(
                f"Analiza el siguiente manuscrito en busca de elementos de lore, "
                f"reglas del mundo y consistencia narrativa:\n\n{manuscript_content[:1000]}...\n\n"
                f"INSTRUCCIONES ESPECÍFICAS:\n"
                f"1. Identifica todos los elementos de worldbuilding presentes\n"
                f"2. Busca información adicional en los documentos de referencia usando RAG\n"
                f"3. Detecta inconsistencias o elementos que necesiten desarrollo\n"
                f"4. Propón mejoras para enriquecer el lore\n"
                f"5. Asegúrate de que las reglas del mundo sean coherentes"
            ),
            expected_output=(
                "Un análisis completo de lore que incluya:\n"
                "- Lista de elementos de worldbuilding identificados\n"
                "- Inconsistencias encontradas (si las hay)\n"
                "- Recomendaciones específicas para mejorar el lore\n"
                "- Referencias a material de apoyo encontrado en RAG"
            ),
            agent=self.agents['lorekeeper'],
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool]
        )
        tasks.append(lore_task)
        
        # ========================================
        # TASK 2: CHARACTER DEVELOPMENT
        # ========================================
        character_task = Task(
            description=(
                f"Analiza y desarrolla los personajes del manuscrito:\n\n{manuscript_content[:1000]}...\n\n"
                f"ENFÓCATE EN:\n"
                f"1. Identificar todos los personajes principales y secundarios\n"
                f"2. Evaluar sus arcos narrativos y desarrollo\n"
                f"3. Analizar motivaciones, conflictos internos y crecimiento\n"
                f"4. Buscar información adicional sobre los personajes en RAG\n"
                f"5. Proponer mejoras para hacer los personajes más profundos y creíbles"
            ),
            expected_output=(
                "Un análisis de personajes que incluya:\n"
                "- Perfil completo de cada personaje principal\n"
                "- Evaluación de arcos narrativos\n"
                "- Identificación de fortalezas y debilidades en desarrollo\n"
                "- Recomendaciones específicas para mejorar caracterización"
            ),
            agent=self.agents['character_developer'],
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool]
        )
        tasks.append(character_task)
        
        # ========================================
        # TASK 3: PLOT ANALYSIS
        # ========================================
        plot_task = Task(
            description=(
                f"Evalúa la estructura narrativa y trama del manuscrito:\n\n{manuscript_content[:1000]}...\n\n"
                f"ANALIZA:\n"
                f"1. Estructura general de la trama (inicio, desarrollo, clímax, resolución)\n"
                f"2. Ritmo narrativo y puntos de tensión\n"
                f"3. Subtramas y su integración con la trama principal\n"
                f"4. Coherencia temporal y causal de los eventos\n"
                f"5. Oportunidades para mejorar el impacto dramático"
            ),
            expected_output=(
                "Un análisis de trama que incluya:\n"
                "- Evaluación de la estructura narrativa\n"
                "- Identificación de puntos fuertes y débiles\n"
                "- Análisis del ritmo y tensión dramática\n"
                "- Recomendaciones para mejorar la trama"
            ),
            agent=self.agents['plot_weaver'],
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool]
        )
        tasks.append(plot_task)
        
        # ========================================
        # TASK 4: STYLE & VOICE REFINEMENT
        # ========================================
        style_task = Task(
            description=(
                f"Evalúa y refina el estilo de escritura del manuscrito:\n\n{manuscript_content[:1000]}...\n\n"
                f"EXAMINA:\n"
                f"1. Consistencia de la voz narrativa\n"
                f"2. Calidad de la prosa y fluidez del texto\n"
                f"3. Uso efectivo de descripciones y diálogos\n"
                f"4. Tono apropiado para el género fantástico\n"
                f"5. Oportunidades para mejorar el impacto emocional"
            ),
            expected_output=(
                "Un análisis de estilo que incluya:\n"
                "- Evaluación de la voz narrativa\n"
                "- Identificación de fortalezas y debilidades estilísticas\n"
                "- Sugerencias específicas de mejora\n"
                "- Ejemplos de reformulaciones cuando sea necesario"
            ),
            agent=self.agents['voice_editor'],
            tools=[self.rag_tool, self.manuscript_tool, self.extractor_tool]
        )
        tasks.append(style_task)
        
        return tasks
    
    def create_crew(self, tasks: List[Task]) -> Crew:
        """Crear el crew con todos los agentes y tareas"""
        
        return Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            verbose=True,
            process="sequential",  # Procesamiento secuencial para esta iteración
            memory=True,
            max_rpm=10  # Límite de requests por minuto
        )

# ========================================
# FUNCIONES DE UTILIDAD
# ========================================

def load_manuscript_for_analysis() -> str:
    """Cargar manuscrito para análisis"""
    manuscript_tool = ManuscriptReaderTool()
    content = manuscript_tool._run(section="summary")
    return content

def run_story_analysis():
    """Ejecutar análisis completo de la historia"""
    print("=== INICIANDO ANÁLISIS DE HISTORIA ===")
    
    # Cargar manuscrito
    print("Cargando manuscrito...")
    manuscript_content = load_manuscript_for_analysis()
    
    if "Error" in manuscript_content:
        print(f"❌ {manuscript_content}")
        return None
    
    print(f"✅ Manuscrito cargado: {len(manuscript_content)} caracteres")
    
    # Crear agentes
    print("Inicializando agentes...")
    story_agents = StoryEnhancementAgents()
    
    # Crear tareas
    print("Creando tareas...")
    tasks = story_agents.create_tasks(manuscript_content)
    
    # Crear crew
    print("Formando equipo de agentes...")
    crew = story_agents.create_crew(tasks)
    
    # Ejecutar análisis
    print("🚀 Iniciando análisis colaborativo...")
    try:
        result = crew.kickoff()
        print("✅ Análisis completado exitosamente")
        return result
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return None

if __name__ == "__main__":
    # Test básico de los agentes
    result = run_story_analysis()
    if result:
        print("\n=== RESULTADO DEL ANÁLISIS ===")
        print(result)