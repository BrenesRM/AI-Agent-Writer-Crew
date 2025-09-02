# orchestrator/iteration_controller.py
"""
Controlador de ciclos iterativos del flujo de trabajo.
Gestiona cuándo continuar, detener o reiniciar iteraciones.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

class IterationStopReason(Enum):
    """Razones para detener iteraciones"""
    MAX_ITERATIONS = "max_iterations_reached"
    ALL_NODES_COMPLETED = "all_nodes_completed"
    QUALITY_THRESHOLD = "quality_threshold_met"
    TOO_MANY_FAILURES = "too_many_failures"
    TIMEOUT = "timeout_reached"
    USER_STOPPED = "user_stopped"
    ERROR_THRESHOLD = "error_threshold_exceeded"

class IterationController:
    """Controla el ciclo de iteraciones del workflow"""
    
    def __init__(
        self, 
        max_iterations: int = 5,
        quality_threshold: float = 0.8,
        failure_threshold: int = 3,
        timeout_minutes: int = 30
    ):
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.failure_threshold = failure_threshold
        self.timeout_duration = timedelta(minutes=timeout_minutes)
        
        self.logger = logging.getLogger(__name__)
        self.current_iteration = 0
        self.start_time = None
        self.stop_requested = False
        self.stop_reason = None
        
        self.logger.info(
            f"IterationController inicializado - Max: {max_iterations}, "
            f"Quality threshold: {quality_threshold}, Timeout: {timeout_minutes}min"
        )
    
    def should_continue(
        self, 
        state: Dict[str, Any], 
        iteration: int
    ) -> bool:
        """
        Determina si el flujo de trabajo debe continuar con otra iteración
        """
        
        self.current_iteration = iteration
        
        # Inicializar tiempo de inicio si es la primera iteración
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        
        # Verificar razones para detener
        stop_reason = self._evaluate_stop_conditions(state, iteration)
        
        if stop_reason:
            self.stop_reason = stop_reason
            self.logger.info(f"Deteniendo iteraciones - Razón: {stop_reason.value}")
            return False
        
        self.logger.info(f"Continuando con iteración {iteration + 1}")
        return True
    
    def _evaluate_stop_conditions(
        self, 
        state: Dict[str, Any], 
        iteration: int
    ) -> Optional[IterationStopReason]:
        """Evalúa todas las condiciones de parada"""
        
        # 1. Verificar si el usuario solicitó parada
        if self.stop_requested:
            return IterationStopReason.USER_STOPPED
        
        # 2. Verificar timeout
        if self._is_timeout_reached():
            return IterationStopReason.TIMEOUT
        
        # 3. Verificar máximo de iteraciones
        if iteration >= self.max_iterations:
            return IterationStopReason.MAX_ITERATIONS
        
        # 4. Verificar si todos los nodos requeridos se completaron
        if self._are_all_required_nodes_completed(state):
            return IterationStopReason.ALL_NODES_COMPLETED
        
        # 5. Verificar umbral de calidad
        if self._is_quality_threshold_met(state):
            return IterationStopReason.QUALITY_THRESHOLD
        
        # 6. Verificar demasiados fallos
        if self._too_many_failures(state):
            return IterationStopReason.TOO_MANY_FAILURES
        
        # 7. Verificar umbral de errores
        if self._error_threshold_exceeded(state):
            return IterationStopReason.ERROR_THRESHOLD
        
        return None
    
    def _is_timeout_reached(self) -> bool:
        """Verifica si se alcanzó el timeout"""
        if self.start_time is None:
            return False
        
        elapsed = datetime.utcnow() - self.start_time
        return elapsed > self.timeout_duration
    
    def _are_all_required_nodes_completed(self, state: Dict[str, Any]) -> bool:
        """Verifica si todos los nodos requeridos se completaron"""
        
        # Lista de nodos requeridos (los opcionales pueden fallar sin detener el workflow)
        required_nodes = [
            'lorekeeper_analysis',
            'character_development',
            'plot_analysis',
            'quality_assurance'  # Este es crítico
        ]
        
        completed_nodes = state.get('completed_nodes', [])
        
        return all(node in completed_nodes for node in required_nodes)
    
    def _is_quality_threshold_met(self, state: Dict[str, Any]) -> bool:
        """Verifica si se alcanzó el umbral de calidad"""
        
        analysis_results = state.get('analysis_results', {})
        
        # Verificar calidad específica del QA si existe
        qa_results = analysis_results.get('quality_assurance', {})
        if qa_results:
            overall_score = qa_results.get('overall_score', 0)
            if isinstance(overall_score, (int, float)):
                quality_ratio = overall_score / 100  # Convertir a ratio
                return quality_ratio >= self.quality_threshold
        
        # Calcular puntuación promedio de todos los análisis
        scores = []
        
        # Recopilar puntuaciones de diferentes análisis
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                # Buscar diferentes tipos de puntuaciones
                score_keys = [
                    'consistency_score', 'overall_score', 'structure_score',
                    'character_development_score', 'style_consistency', 'prose_quality'
                ]
                
                for key in score_keys:
                    if key in data and isinstance(data[key], (int, float)):
                        scores.append(data[key] / 100)  # Normalizar a ratio
        
        if scores:
            average_quality = sum(scores) / len(scores)
            return average_quality >= self.quality_threshold
        
        return False
    
    def _too_many_failures(self, state: Dict[str, Any]) -> bool:
        """Verifica si hay demasiados fallos de nodos"""
        
        failed_nodes = state.get('failed_nodes', [])
        return len(failed_nodes) >= self.failure_threshold
    
    def _error_threshold_exceeded(self, state: Dict[str, Any]) -> bool:
        """Verifica si se excedió el umbral de errores"""
        
        error_log = state.get('error_log', [])
        
        # Contar errores en las últimas 2 iteraciones
        current_iteration = state.get('iteration', 0)
        recent_errors = [
            error for error in error_log 
            if error.get('iteration', 0) >= current_iteration - 1
        ]
        
        # Si hay más de 5 errores en iteraciones recientes, detener
        return len(recent_errors) > 5
    
    def request_stop(self, reason: str = "User requested") -> None:
        """Solicita detener las iteraciones"""
        self.stop_requested = True
        self.logger.info(f"Parada solicitada: {reason}")
    
    def reset(self) -> None:
        """Reinicia el controlador para una nueva sesión"""
        self.current_iteration = 0
        self.start_time = None
        self.stop_requested = False
        self.stop_reason = None
        self.logger.info("IterationController reiniciado")
    
    def get_iteration_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene un resumen del estado de las iteraciones"""
        
        elapsed_time = None
        if self.start_time:
            elapsed_time = (datetime.utcnow() - self.start_time).total_seconds()
        
        # Calcular progreso
        completed_nodes = len(state.get('completed_nodes', []))
        failed_nodes = len(state.get('failed_nodes', []))
        total_nodes = 6  # Total de nodos en el workflow
        
        progress_percentage = (completed_nodes / total_nodes) * 100
        
        # Estimar tiempo restante basado en progreso
        estimated_remaining = None
        if elapsed_time and completed_nodes > 0:
            time_per_node = elapsed_time / completed_nodes
            remaining_nodes = total_nodes - completed_nodes
            estimated_remaining = time_per_node * remaining_nodes
        
        return {
            'current_iteration': self.current_iteration,
            'max_iterations': self.max_iterations,
            'elapsed_time_seconds': elapsed_time,
            'estimated_remaining_seconds': estimated_remaining,
            'progress_percentage': progress_percentage,
            'completed_nodes': completed_nodes,
            'failed_nodes': failed_nodes,
            'total_nodes': total_nodes,
            'stop_requested': self.stop_requested,
            'stop_reason': self.stop_reason.value if self.stop_reason else None,
            'can_continue': not self.stop_requested and self.current_iteration < self.max_iterations
        }
    
    def get_performance_metrics(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene métricas de rendimiento de las iteraciones"""
        
        action_history = state.get('action_history', [])
        
        # Calcular estadísticas por iteración
        iteration_stats = {}
        for action in action_history:
            iteration = action.get('iteration', 0)
            if iteration not in iteration_stats:
                iteration_stats[iteration] = {
                    'actions': 0,
                    'successes': 0,
                    'failures': 0,
                    'duration': 0
                }
            
            iteration_stats[iteration]['actions'] += 1
            if action.get('status') == 'completed':
                iteration_stats[iteration]['successes'] += 1
            elif action.get('status') == 'failed':
                iteration_stats[iteration]['failures'] += 1
        
        # Calcular métricas globales
        total_actions = len(action_history)
        successful_actions = len([a for a in action_history if a.get('status') == 'completed'])
        failed_actions = len([a for a in action_history if a.get('status') == 'failed'])
        
        success_rate = (successful_actions / total_actions) if total_actions > 0 else 0
        
        return {
            'total_actions': total_actions,
            'successful_actions': successful_actions,
            'failed_actions': failed_actions,
            'success_rate': success_rate,
            'iteration_stats': iteration_stats,
            'average_actions_per_iteration': total_actions / max(self.current_iteration, 1)
        }
    
    def should_retry_failed_nodes(self, state: Dict[str, Any]) -> bool:
        """Determina si se deben reintentar nodos fallidos"""
        
        failed_nodes = state.get('failed_nodes', [])
        
        # Solo reintentar si:
        # 1. Hay nodos fallidos
        # 2. No hemos excedido el máximo de iteraciones
        # 3. Los fallos no son críticos (menos del 50% de nodos)
        
        if not failed_nodes:
            return False
        
        if self.current_iteration >= self.max_iterations - 1:
            return False
        
        total_nodes = 6
        failure_rate = len(failed_nodes) / total_nodes
        
        # No reintentar si más del 50% de nodos fallaron
        return failure_rate <= 0.5
    
    def get_next_iteration_strategy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Sugiere estrategia para la próxima iteración"""
        
        completed_nodes = state.get('completed_nodes', [])
        failed_nodes = state.get('failed_nodes', [])
        error_log = state.get('error_log', [])
        
        strategy = {
            'focus_areas': [],
            'retry_nodes': [],
            'skip_nodes': [],
            'optimization_suggestions': []
        }
        
        # Determinar nodos para reintentar
        if self.should_retry_failed_nodes(state):
            strategy['retry_nodes'] = failed_nodes.copy()
        
        # Identificar áreas de enfoque basadas en errores recientes
        recent_errors = [e for e in error_log if e.get('iteration', 0) >= self.current_iteration - 1]
        error_patterns = {}
        
        for error in recent_errors:
            node_id = error.get('node_id', 'unknown')
            if node_id not in error_patterns:
                error_patterns[node_id] = 0
            error_patterns[node_id] += 1
        
        # Sugerir optimizaciones basadas en patrones de error
        for node_id, error_count in error_patterns.items():
            if error_count > 1:
                strategy['focus_areas'].append(f"Revisar configuración de {node_id}")
                strategy['optimization_suggestions'].append(
                    f"Considerar parámetros alternativos para {node_id}"
                )
        
        # Sugerir salto de nodos no críticos si hay muchos fallos
        if len(failed_nodes) > 2:
            optional_nodes = ['visual_generation', 'style_refinement']
            for node in optional_nodes:
                if node in failed_nodes:
                    strategy['skip_nodes'].append(node)
        
        return strategy
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del controlador"""
        
        return {
            'current_iteration': self.current_iteration,
            'max_iterations': self.max_iterations,
            'quality_threshold': self.quality_threshold,
            'failure_threshold': self.failure_threshold,
            'timeout_minutes': self.timeout_duration.total_seconds() / 60,
            'is_running': self.start_time is not None,
            'stop_requested': self.stop_requested,
            'stop_reason': self.stop_reason.value if self.stop_reason else None
        }