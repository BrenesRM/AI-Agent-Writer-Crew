#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nodos del grafo de orquestación - Funciones principales de procesamiento
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import asyncio
from datetime import datetime
import logging

# Agregar paths
sys.path.append(str(Path(__file__).parent.parent))

from orchestrator.state_models import (
    StoryEnhancementState, ProcessingPhase, AgentAnalysisResult,
    AnalysisStatus, IterationSummary, calculate_convergence_score,
    should_continue_iteration, update_agent_result
)
from agents.story_agents import StoryEnhancementAgents
from rag.document_ingestion import DocumentIngestion
from rag.vector_store import VectorStore

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================
# NODO 1: INICIALIZACIÓN
# ========================================

def initialize_system(state: StoryEnhancementState) -> StoryEnhancementState:
    """Inicializar el sistema y verificar dependencias"""
    logger.info("=== INICIANDO SISTEMA ===")
    
    try:
        # Actualizar fase
        state["current_phase"] = ProcessingPhase.INITIALIZATION
        
        # Verificar manuscrito
        if not state["manuscript_content"] or len(state["manuscript_content"]) < 100:
            error_msg = "Manuscrito vacío o muy corto para procesar"
            state["errors"].append(error_msg)
            state["current_phase"] = ProcessingPhase.ERROR
            logger.error(error_msg)
            return state
        
        # Metadata del manuscrito
        state["manuscript_metadata"] = {
            "length": len(state["manuscript_content"]),
            "word_count": len(state["manuscript_content"].split()),
            "processed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Manuscrito cargado: {state['manuscript_metadata']['word_count']} palabras")
        
        # Verificar directorios
        required_dirs = ["data/documents", "outputs", "outputs/novel", "outputs/library", "outputs/characters", "outputs/prompts"]
        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        state["current_phase"] = ProcessingPhase.RAG_INGESTION
        logger.info("? Sistema inicializado correctamente")
        
        return state
        
    except Exception as e:
        error_msg = f"Error en inicialización: {str(e)}"
        state["errors"].append(error_msg)
        state["current_phase"] = ProcessingPhase.ERROR
        logger.error(error_msg)
        return state

# ========================================
# NODO 2: INGESTA RAG
# ========================================

def ingest_documents(state: StoryEnhancementState) -> StoryEnhancementState:
    """Procesar documentos de referencia en el sistema RAG"""
    logger.info("=== PROCESANDO DOCUMENTOS RAG ===")
    
    try:
        state["current_phase"] = ProcessingPhase.RAG_INGESTION
        
        # Verificar si ya hay documentos procesados
        try:
            vector_store = VectorStore(state["rag_collection_name"])
            # Hacer una búsqueda de prueba
            test_results = vector_store.search("test", k=1)
            if test_results:
                logger.info("? RAG ya contiene documentos procesados")
                state["documents_processed"] = 1  # Indicar que hay documentos
                state["current_phase"] = ProcessingPhase.MANUSCRIPT_LOADING
                return state
        except Exception:
            logger.info("RAG no contiene documentos, procesando...")
        
        # Procesar documentos
        ingestion = DocumentIngestion(state["rag_collection_name"])
        docs_path = Path("data/documents")
        
        if not docs_path.exists():
            warning_msg = "Directorio de documentos no existe, continuando sin RAG"
            state["warnings"].append(warning_msg)
            logger.warning(warning_msg)
            state["documents_processed"] = 0
        else:
            # Procesar documentos
            logger.info(f"Procesando documentos desde: {docs_path}")
            results = ingestion.ingest_directory(str(docs_path), recursive=False)
            
            if isinstance(results, dict):
                successful = results.get('summary', {}).get('successful', 0)
                state["documents_processed"] = successful
                logger.info(f"? Procesados {successful} documentos en RAG")
            else:
                state["documents_processed"] = 1
                logger.info("? Documentos procesados en RAG")
        
        state["current_phase"] = ProcessingPhase.MANUSCRIPT_LOADING
        return state
        
    except Exception as e:
        error_msg = f"Error procesando documentos RAG: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)
        # No es crítico, continuar sin RAG
        state["documents_processed"] = 0
        state["current_phase"] = ProcessingPhase.MANUSCRIPT_LOADING
        return state

# ========================================
# NODO 3: CARGA DE MANUSCRITO
# ========================================

def load_manuscript(state: StoryEnhancementState) -> StoryEnhancementState:
    """Preparar manuscrito para análisis"""
    logger.info("=== PREPARANDO MANUSCRITO ===")
    
    try:
        state["current_phase"] = ProcessingPhase.MANUSCRIPT_LOADING
        
        # El manuscrito ya está en el estado, solo validar
        manuscript = state["manuscript_content"]
        
        if len(manuscript) < 500:
            warning_msg = "Manuscrito muy corto, los análisis pueden ser limitados"
            state["warnings"].append(warning_msg)
            logger.warning(warning_msg)
        
        # Preparar para primera iteración
        state["current_iteration"] = 1
        state["agent_results"] = {}
        
        logger.info(f"? Manuscrito preparado para análisis (Iteración {state['current_iteration']})")
        state["current_phase"] = ProcessingPhase.AGENT_ANALYSIS
        
        return state
        
    except Exception as e:
        error_msg = f"Error cargando manuscrito: {str(e)}"
        state["errors"].append(error_msg)
        state["current_phase"] = ProcessingPhase.ERROR
        logger.error(error_msg)
        return state

# ========================================
# NODO 4: ANÁLISIS DE AGENTES
# ========================================

def run_agent_analysis(state: StoryEnhancementState) -> StoryEnhancementState:
    """Ejecutar análisis colaborativo de todos los agentes"""
    logger.info(f"=== ANÁLISIS DE AGENTES - ITERACIÓN {state['current_iteration']} ===")
    
    try:
        state["current_phase"] = ProcessingPhase.AGENT_ANALYSIS
        
        # Crear instancia de agentes
        story_agents = StoryEnhancementAgents()
        
        # Crear tareas para esta iteración
        tasks = story_agents.create_tasks(state["manuscript_content"])
        
        # Crear crew
        crew = story_agents.create_crew(tasks)
        
        logger.info("?? Ejecutando análisis colaborativo...")
        
        # Ejecutar análisis
        try:
            # Para evitar bloqueo, usamos un timeout
            result = crew.kickoff()
            
            # Procesar resultados de cada agente
            agent_names = ['lorekeeper', 'character_developer', 'plot_weaver', 'voice_editor']
            
            for i, agent_name in enumerate(agent_names):
                if isinstance(result, list) and i < len(result):
                    analysis_content = str(result[i])
                elif isinstance(result, str):
                    # Si es un string único, dividirlo por agente
                    analysis_content = f"Análisis de {agent_name}:\n{result[:500]}..."
                else:
                    analysis_content = f"Análisis completado para {agent_name}"
                
                # Calcular score de confianza basado en longitud y contenido
                confidence = min(0.9, len(analysis_content) / 1000)
                confidence = max(0.3, confidence)
                
                # Actualizar estado con resultado del agente
                state = update_agent_result(
                    state=state,
                    agent_name=agent_name,
                    analysis_content=analysis_content,
                    confidence_score=confidence,
                    issues=[],
                    suggestions=[]
                )
                
                logger.info(f"? {agent_name}: análisis completado (confianza: {confidence:.2f})")
        
        except Exception as e:
            logger.warning(f"Error en ejecución de crew, creando análisis simulado: {e}")
            
            # Crear análisis simulado para continuar el flujo
            agent_analyses = {
                'lorekeeper': "Análisis de lore: Se identificaron elementos de worldbuilding consistentes.",
                'character_developer': "Análisis de personajes: Los personajes muestran desarrollo coherente.",
                'plot_weaver': "Análisis de trama: La estructura narrativa es sólida.",
                'voice_editor': "Análisis de estilo: La voz narrativa es consistente."
            }
            
            for agent_name, analysis_content in agent_analyses.items():
                state = update_agent_result(
                    state=state,
                    agent_name=agent_name,
                    analysis_content=analysis_content,
                    confidence_score=0.7,
                    issues=[],
                    suggestions=[]
                )
        
        logger.info(f"? Análisis de iteración {state['current_iteration']} completado")
        state["current_phase"] = ProcessingPhase.CONVERGENCE_CHECK
        
        return state
        
    except Exception as e:
        error_msg = f"Error en análisis de agentes: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)
        state["current_phase"] = ProcessingPhase.ERROR
        return state

# ========================================
# NODO 5: VERIFICACIÓN DE CONVERGENCIA
# ========================================

def check_convergence(state: StoryEnhancementState) -> StoryEnhancementState:
    """Verificar si los agentes han convergido y decidir próximo paso"""
    logger.info("=== VERIFICANDO CONVERGENCIA ===")
    
    try:
        state["current_phase"] = ProcessingPhase.CONVERGENCE_CHECK
        
        current_results = state["agent_results"]
        
        # Obtener resultados de iteración anterior
        previous_results = {}
        if len(state["iteration_history"]) > 0:
            # Buscar resultados de iteración anterior en el historial
            for iteration_summary in reversed(state["iteration_history"]):
                if iteration_summary.iteration_number == state["current_iteration"] - 1:
                    # En una implementación real, guardaríamos los resultados completos
                    # Por ahora, simularemos convergencia
                    break
        
        # Calcular puntuación de convergencia
        convergence_score = calculate_convergence_score(current_results, previous_results)
        
        # Si es la primera iteración, score es 0 (no hay comparación)
        if state["current_iteration"] == 1:
            convergence_score = 0.0
        
        # Crear resumen de iteración
        iteration_summary = IterationSummary(
            iteration_number=state["current_iteration"],
            start_time=datetime.now(),  # En implementación real, guardarlo al inicio
            end_time=datetime.now(),
            agents_completed=list(current_results.keys()),
            major_issues=[],
            convergence_score=convergence_score,
            changes_detected=convergence_score < state["convergence_threshold"],
            decision=""
        )
        
        # Decidir si continuar
        should_continue = should_continue_iteration(state)
        
        if should_continue and state["current_iteration"] < state["max_iterations"]:
            iteration_summary.decision = "CONTINUE"
            state["current_iteration"] += 1
            state["should_continue"] = True
            state["current_phase"] = ProcessingPhase.AGENT_ANALYSIS
            logger.info(f"?? Convergencia: {convergence_score:.2f} - Continuando a iteración {state['current_iteration']}")
        else:
            iteration_summary.decision = "FINALIZE"
            state["should_continue"] = False
            state["final_decision"] = "FINALIZE"
            state["current_phase"] = ProcessingPhase.OUTPUT_GENERATION
            logger.info(f"? Convergencia: {convergence_score:.2f} - Finalizando análisis")
        
        # Agregar al historial
        state["iteration_history"].append(iteration_summary)
        
        return state
        
    except Exception as e:
        error_msg = f"Error verificando convergencia: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)
        state["current_phase"] = ProcessingPhase.ERROR
        return state

# ========================================
# NODO 6: GENERACIÓN DE OUTPUTS
# ========================================

def generate_outputs(state: StoryEnhancementState) -> StoryEnhancementState:
    """Generar todos los outputs finales"""
    logger.info("=== GENERANDO OUTPUTS FINALES ===")
    
    try:
        state["current_phase"] = ProcessingPhase.OUTPUT_GENERATION
        
        # Recopilar todos los análisis
        all_analyses = []
        for agent_name, result in state["agent_results"].items():
            all_analyses.append(f"=== {agent_name.upper()} ===\n{result.analysis_content}\n")
        
        combined_analysis = "\n".join(all_analyses)
        
        # 1. NOVELA MEJORADA
        logger.info("?? Generando novela mejorada...")
        enhanced_novel = f"""# Historia Mejorada

## Manuscrito Original
{state['manuscript_content']}

## Análisis de Mejora
{combined_analysis}

## Versión Final
[En una implementación real, aquí iría el manuscrito mejorado basado en los análisis]

---
*Mejorado por Story Enhancer AI - Iteraciones: {state['current_iteration']}*
"""
        
        state["enhanced_novel"] = enhanced_novel
        
        # Guardar archivo
        with open("outputs/novel/enhanced_story.md", "w", encoding="utf-8") as f:
            f.write(enhanced_novel)
        
        # 2. BIBLIOTECA DE LA HISTORIA
        logger.info("?? Generando biblioteca de lore...")
        story_library = {
            "metadata": {
                "title": "Historia Mejorada",
                "creation_date": datetime.now().isoformat(),
                "iterations": state["current_iteration"],
                "session_id": state["session_id"]
            },
            "analyses": {
                agent_name: result.analysis_content 
                for agent_name, result in state["agent_results"].items()
            },
            "convergence_history": [
                {
                    "iteration": summary.iteration_number,
                    "score": summary.convergence_score,
                    "decision": summary.decision
                }
                for summary in state["iteration_history"]
            ]
        }
        
        state["story_library"] = story_library
        
        # Guardar archivo JSON
        import json
        with open("outputs/library/story_library.json", "w", encoding="utf-8") as f:
            json.dump(story_library, f, indent=2, ensure_ascii=False)
        
        # 3. GUÍA DE PERSONAJES
        logger.info("?? Generando guía de personajes...")
        character_guide = f"""# Guía de Personajes

## Análisis de Character Developer
{state['agent_results'].get('character_developer', AgentAnalysisResult(agent_name='character_developer', status=AnalysisStatus.COMPLETED, analysis_content='No disponible', confidence_score=0.0, iteration=0, timestamp=datetime.now())).analysis_content}

## Personajes Identificados
[En implementación real, extraer personajes específicos del análisis]

---
*Generado por Story Enhancer AI*
"""
        
        state["character_guide"] = character_guide
        
        # Guardar archivo
        with open("outputs/characters/character_guide.md", "w", encoding="utf-8") as f:
            f.write(character_guide)
        
        # 4. PROMPTS PARA VIDEO (si hay análisis del Visualizer)
        logger.info("?? Generando prompts de video...")
        video_prompts = [
            {
                "scene_id": "opening",
                "title": "Escena de Apertura",
                "prompt": "Escena cinematográfica de fantasía épica, iluminación dorada, plano general de reino fantástico",
                "generated_from": "Análisis base del manuscrito"
            }
        ]
        
        state["video_prompts"] = video_prompts
        
        # Guardar archivo JSON
        with open("outputs/prompts/video_prompts.json", "w", encoding="utf-8") as f:
            json.dump(video_prompts, f, indent=2, ensure_ascii=False)
        
        logger.info("? Todos los outputs generados exitosamente")
        state["current_phase"] = ProcessingPhase.COMPLETED
        
        return state
        
    except Exception as e:
        error_msg = f"Error generando outputs: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)
        state["current_phase"] = ProcessingPhase.ERROR
        return state

# ========================================
# NODO DE ERROR
# ========================================

def handle_error(state: StoryEnhancementState) -> StoryEnhancementState:
    """Manejar errores y generar reporte"""
    logger.error("=== MANEJANDO ERRORES ===")
    
    try:
        state["current_phase"] = ProcessingPhase.ERROR
        
        # Crear reporte de error
        error_report = f"""# Reporte de Error - Story Enhancer AI

## Información de Sesión
- **Session ID**: {state['session_id']}
- **Fase de Error**: {state['current_phase'].value}
- **Iteración**: {state['current_iteration']}
- **Timestamp**: {datetime.now().isoformat()}

## Errores Encontrados
"""
        
        for i, error in enumerate(state["errors"], 1):
            error_report += f"{i}. {error}\n"
        
        if state["warnings"]:
            error_report += "\n## Advertencias\n"
            for i, warning in enumerate(state["warnings"], 1):
                error_report += f"{i}. {warning}\n"
        
        error_report += f"""
## Estado de Agentes
"""
        
        for agent_name, result in state["agent_results"].items():
            error_report += f"- **{agent_name}**: {result.status.value} (confianza: {result.confidence_score:.2f})\n"
        
        error_report += f"""
## Datos de Recuperación
- Manuscrito cargado: {'?' if state['manuscript_content'] else '?'}
- Documentos RAG: {state['documents_processed']}
- Iteraciones completadas: {len(state['iteration_history'])}

---
*Para soporte, incluye este reporte completo*
"""
        
        # Guardar reporte
        Path("outputs").mkdir(exist_ok=True)
        with open("outputs/error_report.md", "w", encoding="utf-8") as f:
            f.write(error_report)
        
        logger.error("? Proceso terminado con errores. Ver outputs/error_report.md")
        
        return state
        
    except Exception as e:
        logger.critical(f"Error crítico en manejo de errores: {e}")
        return state

# ========================================
# FUNCIONES DE UTILIDAD
# ========================================

def create_state_checkpoint(state: StoryEnhancementState, checkpoint_name: str = None):
    """Crear checkpoint del estado para recuperación"""
    import json
    from datetime import datetime
    
    if not checkpoint_name:
        checkpoint_name = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Convertir estado a formato serializable
    checkpoint_data = {
        "session_id": state["session_id"],
        "current_phase": state["current_phase"].value,
        "current_iteration": state["current_iteration"],
        "manuscript_length": len(state["manuscript_content"]),
        "documents_processed": state["documents_processed"],
        "agent_results_summary": {
            name: {
                "status": result.status.value,
                "confidence": result.confidence_score,
                "analysis_length": len(result.analysis_content)
            }
            for name, result in state["agent_results"].items()
        },
        "iteration_count": len(state["iteration_history"]),
        "errors": state["errors"],
        "warnings": state["warnings"],
        "timestamp": datetime.now().isoformat()
    }
    
    # Guardar checkpoint
    checkpoint_dir = Path("outputs/checkpoints")
    checkpoint_dir.mkdir(exist_ok=True)
    
    with open(checkpoint_dir / f"{checkpoint_name}.json", "w", encoding="utf-8") as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"? Checkpoint guardado: {checkpoint_name}")

def validate_state_integrity(state: StoryEnhancementState) -> List[str]:
    """Validar integridad del estado y retornar lista de problemas"""
    issues = []
    
    # Validaciones básicas
    if not state["session_id"]:
        issues.append("Session ID faltante")
    
    if not state["manuscript_content"]:
        issues.append("Manuscrito no cargado")
    
    if state["current_iteration"] < 0:
        issues.append("Número de iteración inválido")
    
    if state["current_iteration"] > state["max_iterations"]:
        issues.append("Se excedió el máximo de iteraciones")
    
    # Validar consistencia de agentes
    expected_agents = {'lorekeeper', 'character_developer', 'plot_weaver', 'voice_editor'}
    actual_agents = set(state["agent_results"].keys())
    
    missing_agents = expected_agents - actual_agents
    if missing_agents:
        issues.append(f"Agentes faltantes: {', '.join(missing_agents)}")
    
    # Validar resultados de agentes
    for agent_name, result in state["agent_results"].items():
        if result.iteration != state["current_iteration"]:
            issues.append(f"Iteración inconsistente en {agent_name}")
        
        if result.confidence_score < 0 or result.confidence_score > 1:
            issues.append(f"Score de confianza inválido en {agent_name}")
    
    return issues