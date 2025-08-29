#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos de estado y datos para el grafo de orquestación
"""
from typing import Dict, List, Any, Optional, TypedDict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ProcessingPhase(Enum):
    """Fases del procesamiento de historia"""
    INITIALIZATION = "initialization"
    RAG_INGESTION = "rag_ingestion"
    MANUSCRIPT_LOADING = "manuscript_loading"
    AGENT_ANALYSIS = "agent_analysis"
    CONVERGENCE_CHECK = "convergence_check"
    OUTPUT_GENERATION = "output_generation"
    COMPLETED = "completed"
    ERROR = "error"

class AnalysisStatus(Enum):
    """Estado de análisis de cada agente"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"
    REQUIRES_REVISION = "requires_revision"

class AgentAnalysisResult(BaseModel):
    """Resultado de análisis de un agente individual"""
    agent_name: str
    status: AnalysisStatus
    analysis_content: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    iteration: int
    timestamp: datetime
    issues_found: List[str] = []
    suggestions: List[str] = []
    metadata: Dict[str, Any] = {}

class IterationSummary(BaseModel):
    """Resumen de una iteración completa"""
    iteration_number: int
    start_time: datetime
    end_time: Optional[datetime] = None
    agents_completed: List[str] = []
    major_issues: List[str] = []
    convergence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    changes_detected: bool = True
    decision: str = ""  # CONTINUE o FINALIZE

class StoryEnhancementState(TypedDict):
    """Estado global del grafo de mejora de historia"""
    
    # === INFORMACIÓN BÁSICA ===
    session_id: str
    start_time: datetime
    current_phase: ProcessingPhase
    
    # === MANUSCRITO ===
    manuscript_content: str
    manuscript_metadata: Dict[str, Any]
    
    # === RAG ===
    documents_processed: int
    rag_collection_name: str
    
    # === AGENTES Y ANÁLISIS ===
    current_iteration: int
    max_iterations: int
    agent_results: Dict[str, AgentAnalysisResult]
    iteration_history: List[IterationSummary]
    
    # === CONVERGENCIA ===
    convergence_threshold: float
    stability_window: int
    
    # === OUTPUTS FINALES ===
    enhanced_novel: str
    story_library: Dict[str, Any]
    character_guide: str
    video_prompts: List[Dict[str, Any]]
    
    # === CONTROL DE FLUJO ===
    errors: List[str]
    warnings: List[str]
    should_continue: bool
    final_decision: str

class ConvergenceAnalysis(BaseModel):
    """Análisis de convergencia entre iteraciones"""
    current_iteration: int
    previous_iteration: int
    
    # Comparación por agente
    lorekeeper_similarity: float
    character_dev_similarity: float
    plot_weaver_similarity: float
    voice_editor_similarity: float
    
    # Métricas globales
    overall_similarity: float
    significant_changes: bool
    stability_score: float
    
    # Decisión
    recommendation: str  # CONTINUE, FINALIZE, or REVIEW
    reasoning: str

class OutputGenerationRequest(BaseModel):
    """Request para generación de outputs finales"""
    state: StoryEnhancementState
    output_types: List[str]  # ['novel', 'library', 'characters', 'prompts']
    format_preferences: Dict[str, str] = {}
    custom_instructions: str = ""

# ========================================
# UTILIDADES DE ESTADO
# ========================================

def create_initial_state(
    manuscript_content: str,
    session_id: str = None,
    max_iterations: int = 5,
    convergence_threshold: float = 0.85
) -> StoryEnhancementState:
    """Crear estado inicial del grafo"""
    
    if not session_id:
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return StoryEnhancementState(
        session_id=session_id,
        start_time=datetime.now(),
        current_phase=ProcessingPhase.INITIALIZATION,
        
        # Manuscrito
        manuscript_content=manuscript_content,
        manuscript_metadata={},
        
        # RAG
        documents_processed=0,
        rag_collection_name="documentos_procesados",
        
        # Iteraciones
        current_iteration=0,
        max_iterations=max_iterations,
        agent_results={},
        iteration_history=[],
        
        # Convergencia
        convergence_threshold=convergence_threshold,
        stability_window=2,
        
        # Outputs
        enhanced_novel="",
        story_library={},
        character_guide="",
        video_prompts=[],
        
        # Control
        errors=[],
        warnings=[],
        should_continue=True,
        final_decision=""
    )

def update_agent_result(
    state: StoryEnhancementState,
    agent_name: str,
    analysis_content: str,
    confidence_score: float,
    issues: List[str] = None,
    suggestions: List[str] = None
) -> StoryEnhancementState:
    """Actualizar resultado de un agente en el estado"""
    
    result = AgentAnalysisResult(
        agent_name=agent_name,
        status=AnalysisStatus.COMPLETED,
        analysis_content=analysis_content,
        confidence_score=confidence_score,
        iteration=state["current_iteration"],
        timestamp=datetime.now(),
        issues_found=issues or [],
        suggestions=suggestions or []
    )
    
    # Actualizar estado
    state["agent_results"][agent_name] = result
    
    return state

def calculate_convergence_score(
    current_results: Dict[str, AgentAnalysisResult],
    previous_results: Dict[str, AgentAnalysisResult]
) -> float:
    """Calcular score de convergencia entre dos iteraciones"""
    
    if not previous_results:
        return 0.0
    
    similarities = []
    
    for agent_name in current_results:
        if agent_name in previous_results:
            current_content = current_results[agent_name].analysis_content
            previous_content = previous_results[agent_name].analysis_content
            
            # Similaridad simple basada en longitud y contenido común
            # En implementación real usaríamos embeddings
            if len(current_content) == 0 and len(previous_content) == 0:
                similarity = 1.0
            elif len(current_content) == 0 or len(previous_content) == 0:
                similarity = 0.0
            else:
                # Similaridad básica - en producción usar embeddings
                common_words = set(current_content.lower().split()) & set(previous_content.lower().split())
                total_words = set(current_content.lower().split()) | set(previous_content.lower().split())
                similarity = len(common_words) / len(total_words) if total_words else 0.0
            
            similarities.append(similarity)
    
    return sum(similarities) / len(similarities) if similarities else 0.0

def should_continue_iteration(state: StoryEnhancementState) -> bool:
    """Determinar si debe continuar con otra iteración"""
    
    # Verificar límite máximo
    if state["current_iteration"] >= state["max_iterations"]:
        return False
    
    # Si no hay iteraciones previas, continuar
    if state["current_iteration"] <= 1:
        return True
    
    # Verificar convergencia en las últimas iteraciones
    if len(state["iteration_history"]) >= state["stability_window"]:
        recent_scores = [
            iteration.convergence_score 
            for iteration in state["iteration_history"][-state["stability_window"]:]
        ]
        
        # Si todas las puntuaciones recientes están por encima del umbral
        if all(score >= state["convergence_threshold"] for score in recent_scores):
            return False
    
    return True

def get_state_summary(state: StoryEnhancementState) -> str:
    """Obtener resumen legible del estado actual"""
    
    summary = f"""
=== ESTADO DEL PROCESAMIENTO ===
Session: {state['session_id']}
Fase: {state['current_phase'].value}
Iteración: {state['current_iteration']}/{state['max_iterations']}

=== AGENTES ===
"""
    
    for agent_name, result in state["agent_results"].items():
        summary += f"- {agent_name}: {result.status.value} (confianza: {result.confidence_score:.2f})\n"
    
    if state["iteration_history"]:
        last_iteration = state["iteration_history"][-1]
        summary += f"\nÚltima convergencia: {last_iteration.convergence_score:.2f}"
        summary += f"\nDecisión: {last_iteration.decision}"
    
    if state["errors"]:
        summary += f"\nErrores: {len(state['errors'])}"
    
    if state["warnings"]:
        summary += f"\nAdvertencias: {len(state['warnings'])}"
    
    return summary