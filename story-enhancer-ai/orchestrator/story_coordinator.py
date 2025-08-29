#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinador principal usando LangGraph para orquestar el flujo de mejora de historias
"""
import sys
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime

# Agregar paths
sys.path.append(str(Path(__file__).parent.parent))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from orchestrator.state_models import (
    StoryEnhancementState, ProcessingPhase, create_initial_state, get_state_summary
)
from orchestrator.graph_nodes import (
    initialize_system, ingest_documents, load_manuscript, 
    run_agent_analysis, check_convergence, generate_outputs, handle_error,
    create_state_checkpoint, validate_state_integrity
)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StoryEnhancementCoordinator:
    """Coordinador principal que orquesta todo el flujo de mejora de historias"""
    
    def __init__(self, 
                 max_iterations: int = 5,
                 convergence_threshold: float = 0.85,
                 enable_checkpoints: bool = True):
        """
        Inicializar coordinador
        
        Args:
            max_iterations: Máximo número de iteraciones de agentes
            convergence_threshold: Umbral de convergencia (0.0-1.0)
            enable_checkpoints: Si habilitar checkpoints de estado
        """
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.enable_checkpoints = enable_checkpoints
        
        # Configurar persistencia si está habilitada
        self.checkpointer = None
        if enable_checkpoints:
            try:
                checkpoint_path = Path("outputs/graph_checkpoints.db")
                checkpoint_path.parent.mkdir(exist_ok=True)
                self.checkpointer = SqliteSaver.from_conn_string(str(checkpoint_path))
            except Exception as e:
                logger.warning(f"No se pudo configurar checkpointer: {e}")
        
        # Crear grafo
        self.graph = self._create_graph()
        logger.info("? Coordinador inicializado")
    
    def _create_graph(self) -> StateGraph:
        """Crear el grafo de estados con LangGraph"""
        
        # Crear grafo
        workflow = StateGraph(StoryEnhancementState)
        
        # ========================================
        # AGREGAR NODOS
        # ========================================
        
        workflow.add_node("initialize", initialize_system)
        workflow.add_node("ingest_documents", ingest_documents)
        workflow.add_node("load_manuscript", load_manuscript)
        workflow.add_node("agent_analysis", run_agent_analysis)
        workflow.add_node("check_convergence", check_convergence)
        workflow.add_node("generate_outputs", generate_outputs)
        workflow.add_node("handle_error", handle_error)
        
        # ========================================
        # DEFINIR FLUJO
        # ========================================
        
        # Punto de entrada
        workflow.set_entry_point("initialize")
        
        # Flujo principal
        workflow.add_edge("initialize", "ingest_documents")
        workflow.add_edge("ingest_documents", "load_manuscript")
        workflow.add_edge("load_manuscript", "agent_analysis")
        
        # Lógica de convergencia con condicional
        workflow.add_conditional_edges(
            "check_convergence",
            self._should_continue_or_finish,
            {
                "continue": "agent_analysis",
                "finish": "generate_outputs",
                "error": "handle_error"
            }
        )
        
        # Del análisis de agentes siempre ir a verificación de convergencia
        workflow.add_edge("agent_analysis", "check_convergence")
        
        # Terminaciones
        workflow.add_edge("generate_outputs", END)
        workflow.add_edge("handle_error", END)
        
        # Compilar grafo
        if self.checkpointer:
            return workflow.compile(checkpointer=self.checkpointer)
        else:
            return workflow.compile()
    
    def _should_continue_or_finish(self, state: StoryEnhancementState) -> str:
        """Función condicional para decidir próximo paso después de convergencia"""
        
        # Verificar errores críticos
        if state["current_phase"] == ProcessingPhase.ERROR:
            return "error"
        
        # Verificar si debe continuar iterando
        if state["should_continue"] and state["current_iteration"] <= state["max_iterations"]:
            logger.info(f"?? Continuando a iteración {state['current_iteration']}")
            return "continue"
        else:
            logger.info("? Finalizando y generando outputs")
            return "finish"
    
    def enhance_story(self, 
                     manuscript_content: str,
                     session_id: str = None) -> Dict[str, Any]:
        """
        Ejecutar el proceso completo de mejora de historia
        
        Args:
            manuscript_content: Contenido del manuscrito a mejorar
            session_id: ID de sesión opcional
            
        Returns:
            Dict con resultados del procesamiento
        """
        logger.info("?? INICIANDO PROCESO DE MEJORA DE HISTORIA")
        logger.info("=" * 60)
        
        try:
            # Crear estado inicial
            initial_state = create_initial_state(
                manuscript_content=manuscript_content,
                session_id=session_id,
                max_iterations=self.max_iterations,
                convergence_threshold=self.convergence_threshold
            )
            
            logger.info(f"?? Manuscrito: {len(manuscript_content)} caracteres")
            logger.info(f"?? Máximo iteraciones: {self.max_iterations}")
            logger.info(f"?? Umbral convergencia: {self.convergence_threshold}")
            
            # Crear checkpoint inicial si está habilitado
            if self.enable_checkpoints:
                create_state_checkpoint(initial_state, "initial_state")
            
            # Configuración de ejecución
            config = {"configurable": {"thread_id": initial_state["session_id"]}}
            
            # Ejecutar grafo
            logger.info("?? Iniciando procesamiento...")
            final_state = None
            
            for step, state in enumerate(self.graph.stream(initial_state, config=config)):
                current_phase = list(state.values())[0]["current_phase"]
                logger.info(f"Paso {step + 1}: {current_phase.value}")
                
                # Crear checkpoint en pasos críticos
                if self.enable_checkpoints and current_phase in [
                    ProcessingPhase.AGENT_ANALYSIS, 
                    ProcessingPhase.CONVERGENCE_CHECK
                ]:
                    create_state_checkpoint(
                        list(state.values())[0], 
                        f"step_{step + 1}_{current_phase.value}"
                    )
                
                final_state = list(state.values())[0]
            
            # Validar estado final
            issues = validate_state_integrity(final_state)
            if issues:
                logger.warning(f"?? Problemas de integridad: {', '.join(issues)}")
            
            # Crear resumen final
            logger.info("?? PROCESAMIENTO COMPLETADO")
            logger.info("=" * 40)
            logger.info(get_state_summary(final_state))
            
            # Crear checkpoint final
            if self.enable_checkpoints:
                create_state_checkpoint(final_state, "final_state")
            
            # Retornar resultados
            return self._create_results_summary(final_state)
            
        except Exception as e:
            logger.error(f"? Error crítico en coordinador: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id or "unknown",
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_results_summary(self, final_state: StoryEnhancementState) -> Dict[str, Any]:
        """Crear resumen de resultados del procesamiento"""
        
        success = final_state["current_phase"] == ProcessingPhase.COMPLETED
        
        results = {
            "success": success,
            "session_id": final_state["session_id"],
            "timestamp": datetime.now().isoformat(),
            
            # Estadísticas del procesamiento
            "processing_stats": {
                "total_iterations": len(final_state["iteration_history"]),
                "documents_processed": final_state["documents_processed"],
                "agents_executed": len(final_state["agent_results"]),
                "final_phase": final_state["current_phase"].value,
                "convergence_achieved": final_state["final_decision"] == "FINALIZE"
            },
            
            # Resultados por agente
            "agent_analyses": {
                name: {
                    "status": result.status.value,
                    "confidence_score": result.confidence_score,
                    "content_length": len(result.analysis_content),
                    "issues_found": len(result.issues_found),
                    "suggestions_count": len(result.suggestions)
                }
                for name, result in final_state["agent_results"].items()
            },
            
            # Historial de convergencia
            "convergence_history": [
                {
                    "iteration": summary.iteration_number,
                    "score": summary.convergence_score,
                    "decision": summary.decision,
                    "agents_completed": len(summary.agents_completed)
                }
                for summary in final_state["iteration_history"]
            ],
            
            # Archivos generados
            "generated_files": [],
            
            # Problemas encontrados
            "errors": final_state["errors"],
            "warnings": final_state["warnings"]
        }
        
        # Verificar archivos generados
        output_files = [
            "outputs/novel/enhanced_story.md",
            "outputs/library/story_library.json",
            "outputs/characters/character_guide.md",
            "outputs/prompts/video_prompts.json"
        ]
        
        for file_path in output_files:
            if Path(file_path).exists():
                results["generated_files"].append(file_path)
        
        return results
    
    def get_graph_visualization(self) -> str:
        """Obtener representación visual del grafo (para debugging)"""
        try:
            # Intentar generar visualización del grafo
            return str(self.graph.get_graph().draw_ascii())
        except Exception as e:
            return f"No se pudo generar visualización: {e}"

# ========================================
# FUNCIONES DE UTILIDAD PÚBLICAS
# ========================================

def create_coordinator(max_iterations: int = 5, 
                      convergence_threshold: float = 0.85,
                      enable_checkpoints: bool = True) -> StoryEnhancementCoordinator:
    """Crear una instancia del coordinador con configuración específica"""
    return StoryEnhancementCoordinator(
        max_iterations=max_iterations,
        convergence_threshold=convergence_threshold,
        enable_checkpoints=enable_checkpoints
    )

def enhance_story_simple(manuscript_content: str,
                        max_iterations: int = 3) -> Dict[str, Any]:
    """Función simplificada para mejorar una historia"""
    
    coordinator = create_coordinator(
        max_iterations=max_iterations,
        convergence_threshold=0.8,
        enable_checkpoints=False
    )
    
    return coordinator.enhance_story(manuscript_content)

# ========================================
# SCRIPT PRINCIPAL
# ========================================

if __name__ == "__main__":
    # Ejemplo de uso del coordinador
    
    # Manuscrito de ejemplo
    sample_manuscript = """
    En el reino de Aethermoor, donde la magia fluye como ríos de luz,
    el joven príncipe Marcus descubrió que su destino estaba ligado
    a un antiguo artefacto conocido como el Corazón de Dragón.
    
    Los Corruptores, una orden de magos oscuros, buscaban apoderarse
    del artefacto para plunger el reino en la oscuridad eterna.
    Marcus, junto con su compañera Lyra, una hechicera élfica,
    debía emprender una peligrosa misión para proteger su mundo.
    """
    
    print("?? PRUEBA DEL COORDINADOR")
    print("=" * 40)
    
    # Crear y ejecutar coordinador
    coordinator = create_coordinator(max_iterations=2, enable_checkpoints=False)
    
    results = coordinator.enhance_story(sample_manuscript)
    
    print("\n?? RESULTADOS:")
    print(f"Éxito: {results['success']}")
    print(f"Iteraciones: {results['processing_stats']['total_iterations']}")
    print(f"Agentes ejecutados: {results['processing_stats']['agents_executed']}")
    print(f"Archivos generados: {len(results['generated_files'])}")
    
    if results['generated_files']:
        print("Archivos creados:")
        for file_path in results['generated_files']:
            print(f"  - {file_path}")
    
    if results['errors']:
        print("Errores encontrados:")
        for error in results['errors']:
            print(f"  - {error}")
    
    print("\n? Prueba completada")