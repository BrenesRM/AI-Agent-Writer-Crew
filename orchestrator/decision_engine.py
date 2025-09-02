# orchestrator/decision_engine.py
"""
Motor de decisiones para el flujo de trabajo.
Determina qué acciones ejecutar basado en el estado actual y las reglas de negocio.
"""

import logging
from typing import Dict, Any, List, Optional, Set
from enum import Enum
from dataclasses import dataclass

class ActionPriority(Enum):
    """Prioridades de las acciones"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class ActionType(Enum):
    """Tipos de acciones disponibles"""
    ANALYSIS = "analysis"
    VALIDATION = "validation"
    GENERATION = "generation"
    OPTIMIZATION = "optimization"
    RETRY = "retry"

@dataclass
class Action:
    """Representación de una acción a ejecutar"""
    id: str
    type: str
    agent: str
    priority: ActionPriority
    dependencies: List[str]
    parallel: bool = True
    params: Dict[str, Any] = None
    estimated_duration: int = 60  # segundos
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}

class DecisionEngine:
    """Motor de decisiones que determina qué acciones ejecutar"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Definir el grafo de dependencias de acciones
        self.action_dependencies = {
            'lorekeeper_analysis': [],
            'character_development': [],
            'style_refinement': [],
            'plot_analysis': ['lorekeeper_analysis', 'character_development'],
            'visual_generation': ['lorekeeper_analysis', 'character_development', 'plot_analysis'],
            'quality_assurance': ['style_refinement', 'plot_analysis']
        }
        
        # Definir reglas de ejecución
        self.parallel_groups = [
            ['lorekeeper_analysis', 'character_development', 'style_refinement'],
            ['plot_analysis'],
            ['visual_generation', 'quality_assurance']
        ]
        
        self.logger.info("DecisionEngine inicializado")
    
    async def get_next_actions(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Determina las próximas acciones a ejecutar basado en el estado actual
        """
        try:
            completed_nodes = set(state.get('completed_nodes', []))
            failed_nodes = set(state.get('failed_nodes', []))
            iteration = state.get('iteration', 0)
            
            # Determinar acciones disponibles
            available_actions = self._get_available_actions(completed_nodes, failed_nodes)
            
            # Aplicar reglas de decisión
            selected_actions = await self._apply_decision_rules(
                available_actions, state, iteration
            )
            
            # Optimizar orden y paralelismo
            optimized_actions = self._optimize_execution_order(selected_actions, state)
            
            self.logger.info(f"Determinadas {len(optimized_actions)} acciones para ejecutar")
            
            return optimized_actions
            
        except Exception as e:
            self.logger.error(f"Error determinando próximas acciones: {str(e)}")
            return []
    
    def _get_available_actions(
        self, 
        completed_nodes: Set[str], 
        failed_nodes: Set[str]
    ) -> List[Action]:
        """Obtiene las acciones disponibles basadas en dependencias"""
        
        available = []
        
        for action_id, dependencies in self.action_dependencies.items():
            # Saltar si ya está completado
            if action_id in completed_nodes:
                continue
            
            # Verificar si las dependencias están satisfechas
            deps_satisfied = all(dep in completed_nodes for dep in dependencies)
            
            if deps_satisfied:
                # Determinar si es un reintento
                is_retry = action_id in failed_nodes
                
                action = self._create_action(action_id, is_retry)
                available.append(action)
        
        return available
    
    def _create_action(self, action_id: str, is_retry: bool = False) -> Action:
        """Crea un objeto Action basado en el ID"""
        
        # Configuraciones específicas por tipo de acción
        action_configs = {
            'lorekeeper_analysis': {
                'agent': 'LorekeeperAgent',
                'priority': ActionPriority.HIGH,
                'parallel': True,
                'duration': 120
            },
            'character_development': {
                'agent': 'CharacterDeveloperAgent',
                'priority': ActionPriority.HIGH,
                'parallel': True,
                'duration': 150
            },
            'plot_analysis': {
                'agent': 'PlotWeaverAgent',
                'priority': ActionPriority.CRITICAL,
                'parallel': False,
                'duration': 180
            },
            'style_refinement': {
                'agent': 'StyleEditorAgent',
                'priority': ActionPriority.MEDIUM,
                'parallel': True,
                'duration': 100
            },
            'visual_generation': {
                'agent': 'VisualizerAgent',
                'priority': ActionPriority.LOW,
                'parallel': False,
                'duration': 90
            },
            'quality_assurance': {
                'agent': 'ProofreaderAgent',
                'priority': ActionPriority.CRITICAL,
                'parallel': False,
                'duration': 120
            }
        }
        
        config = action_configs.get(action_id, {
            'agent': 'UnknownAgent',
            'priority': ActionPriority.MEDIUM,
            'parallel': True,
            'duration': 60
        })
        
        # Ajustar ID si es reintento
        display_id = f"{action_id}_retry" if is_retry else action_id
        
        return Action(
            id=display_id,
            type=action_id,
            agent=config['agent'],
            priority=config['priority'],
            dependencies=self.action_dependencies.get(action_id, []),
            parallel=config['parallel'],
            estimated_duration=config['duration'],
            params={'is_retry': is_retry}
        )
    
    async def _apply_decision_rules(
        self, 
        available_actions: List[Action], 
        state: Dict[str, Any],
        iteration: int
    ) -> List[Action]:
        """Aplica reglas de decisión para filtrar y priorizar acciones"""
        
        selected_actions = []
        
        # Regla 1: Siempre ejecutar acciones críticas si están disponibles
        critical_actions = [a for a in available_actions if a.priority == ActionPriority.CRITICAL]
        selected_actions.extend(critical_actions)
        
        # Regla 2: En iteraciones tempranas, priorizar análisis base
        if iteration <= 1:
            early_actions = [
                a for a in available_actions 
                if a.type in ['lorekeeper_analysis', 'character_development', 'style_refinement']
                and a not in selected_actions
            ]
            selected_actions.extend(early_actions)
        
        # Regla 3: Ejecutar acciones de alta prioridad si hay recursos
        if len(selected_actions) < 3:  # Límite de acciones concurrentes
            high_priority_actions = [
                a for a in available_actions 
                if a.priority == ActionPriority.HIGH and a not in selected_actions
            ]
            selected_actions.extend(high_priority_actions[:3 - len(selected_actions)])
        
        # Regla 4: Limitar reintentos para evitar bucles infinitos
        retry_actions = [a for a in selected_actions if a.params.get('is_retry', False)]
        if len(retry_actions) > 2:
            # Mantener solo los 2 reintentos de mayor prioridad
            retry_actions.sort(key=lambda x: x.priority.value)
            selected_actions = [a for a in selected_actions if not a.params.get('is_retry', False)]
            selected_actions.extend(retry_actions[:2])
        
        # Regla 5: Evitar sobrecargar el sistema en iteraciones avanzadas
        if iteration >= 3:
            # Reducir número de acciones concurrentes
            selected_actions = selected_actions[:2]
        
        # Regla 6: Aplicar filtros basados en estado del sistema
        selected_actions = await self._apply_state_based_filters(selected_actions, state)
        
        return selected_actions
    
    async def _apply_state_based_filters(
        self, 
        actions: List[Action], 
        state: Dict[str, Any]
    ) -> List[Action]:
        """Aplica filtros basados en el estado actual del sistema"""
        
        filtered_actions = []
        
        # Obtener información del estado
        analysis_results = state.get('analysis_results', {})
        error_log = state.get('error_log', [])
        processing_status = state.get('processing_status', 'initialized')
        
        for action in actions:
            include_action = True
            
            # Filtro 1: Evitar acciones que dependen de análisis fallidos
            if action.dependencies:
                for dep in action.dependencies:
                    dep_errors = [e for e in error_log if e.get('node_id') == dep]
                    if len(dep_errors) > 2:  # Demasiados errores en la dependencia
                        include_action = False
                        self.logger.warning(f"Saltando {action.id} debido a errores en dependencia {dep}")
                        break
            
            # Filtro 2: No ejecutar generación visual si falta análisis base
            if action.type == 'visual_generation':
                required_analyses = ['worldbuilding', 'character_development']
                if not all(analysis in analysis_results for analysis in required_analyses):
                    include_action = False
                    self.logger.info("Saltando generación visual - análisis base incompleto")
            
            # Filtro 3: Solo ejecutar QA si hay suficiente análisis completado
            if action.type == 'quality_assurance':
                completed_analyses = len(analysis_results)
                if completed_analyses < 2:
                    include_action = False
                    self.logger.info("Saltando QA - análisis insuficiente")
            
            # Filtro 4: Limitar acciones costosas si hay muchos errores
            recent_errors = [e for e in error_log if e.get('iteration', 0) >= state.get('iteration', 0) - 1]
            if len(recent_errors) > 3 and action.estimated_duration > 120:
                include_action = False
                self.logger.info(f"Saltando {action.id} - demasiados errores recientes")
            
            if include_action:
                filtered_actions.append(action)
        
        return filtered_actions
    
    def _optimize_execution_order(
        self, 
        actions: List[Action], 
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Optimiza el orden de ejecución y paralelismo"""
        
        # Convertir a formato de diccionario
        action_dicts = []
        
        # Ordenar por prioridad y dependencias
        actions.sort(key=lambda x: (x.priority.value, len(x.dependencies)))
        
        for action in actions:
            action_dict = {
                'id': action.id,
                'type': action.type,
                'agent': action.agent,
                'priority': action.priority.value,
                'dependencies': action.dependencies,
                'parallel': action.parallel,
                'params': action.params,
                'estimated_duration': action.estimated_duration
            }
            action_dicts.append(action_dict)
        
        # Aplicar optimizaciones específicas
        optimized = self._apply_execution_optimizations(action_dicts, state)
        
        return optimized
    
    def _apply_execution_optimizations(
        self, 
        actions: List[Dict[str, Any]], 
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Aplica optimizaciones específicas al orden de ejecución"""
        
        # Optimización 1: Ejecutar análisis paralelos primero
        parallel_analyses = [a for a in actions if a.get('parallel', True) and 'analysis' in a['type']]
        sequential_actions = [a for a in actions if not a.get('parallel', True)]
        other_actions = [a for a in actions if a not in parallel_analyses and a not in sequential_actions]
        
        # Optimización 2: Balancear carga basada en duración estimada
        if len(parallel_analyses) > 3:
            # Dividir en grupos balanceados por duración
            parallel_analyses.sort(key=lambda x: x['estimated_duration'])
            # Mantener solo los más eficientes si hay muchos
            parallel_analyses = parallel_analyses[:3]
        
        # Optimización 3: Priorizar acciones que desbloquean otras
        high_dependency_actions = []
        for action in sequential_actions + other_actions:
            action_type = action['type']
            # Contar cuántas otras acciones dependen de esta
            dependents = sum(1 for other in actions if action_type in other.get('dependencies', []))
            if dependents > 0:
                high_dependency_actions.append((action, dependents))
        
        # Ordenar por número de dependientes
        high_dependency_actions.sort(key=lambda x: x[1], reverse=True)
        prioritized_sequential = [action for action, _ in high_dependency_actions]
        
        # Combinar en orden optimizado
        optimized = parallel_analyses + prioritized_sequential
        
        # Agregar acciones restantes
        remaining = [a for a in actions if a not in optimized]
        optimized.extend(remaining)
        
        self.logger.debug(f"Orden optimizado: {[a['id'] for a in optimized]}")
        
        return optimized
    
    async def is_workflow_complete(self, state: Dict[str, Any]) -> bool:
        """Determina si el workflow está completo"""
        
        completed_nodes = set(state.get('completed_nodes', []))
        failed_nodes = set(state.get('failed_nodes', []))
        
        # Nodos mínimos requeridos para completar
        minimum_required = {'lorekeeper_analysis', 'character_development', 'quality_assurance'}
        
        # Verificar si los nodos mínimos están completados
        minimum_satisfied = minimum_required.issubset(completed_nodes)
        
        if not minimum_satisfied:
            return False
        
        # Verificar si hay acciones disponibles
        available_actions = self._get_available_actions(completed_nodes, failed_nodes)
        
        # El workflow está completo si:
        # 1. Los nodos mínimos están completados
        # 2. No hay más acciones disponibles de alta prioridad
        # 3. O si tenemos buena cobertura de análisis
        
        high_priority_available = [
            a for a in available_actions 
            if a.priority in [ActionPriority.CRITICAL, ActionPriority.HIGH]
        ]
        
        analysis_coverage = len(completed_nodes) / len(self.action_dependencies)
        
        is_complete = (
            minimum_satisfied and 
            (len(high_priority_available) == 0 or analysis_coverage >= 0.8)
        )
        
        if is_complete:
            self.logger.info("Workflow marcado como completo")
        
        return is_complete
    
    def get_completion_status(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene el estado de completitud del workflow"""
        
        completed_nodes = set(state.get('completed_nodes', []))
        failed_nodes = set(state.get('failed_nodes', []))
        total_nodes = len(self.action_dependencies)
        
        # Calcular métricas de completitud
        completion_percentage = len(completed_nodes) / total_nodes * 100
        failure_rate = len(failed_nodes) / total_nodes * 100
        
        # Determinar nodos pendientes
        all_nodes = set(self.action_dependencies.keys())
        pending_nodes = all_nodes - completed_nodes - failed_nodes
        
        # Evaluar calidad de la completitud
        critical_nodes = ['quality_assurance', 'plot_analysis']
        critical_completed = sum(1 for node in critical_nodes if node in completed_nodes)
        critical_completion = critical_completed / len(critical_nodes) * 100
        
        return {
            'completion_percentage': completion_percentage,
            'failure_rate': failure_rate,
            'critical_completion': critical_completion,
            'completed_nodes': list(completed_nodes),
            'failed_nodes': list(failed_nodes),
            'pending_nodes': list(pending_nodes),
            'total_nodes': total_nodes,
            'is_minimum_satisfied': self._is_minimum_requirements_satisfied(completed_nodes),
            'quality_assessment': self._assess_completion_quality(state)
        }
    
    def _is_minimum_requirements_satisfied(self, completed_nodes: Set[str]) -> bool:
        """Verifica si se satisfacen los requisitos mínimos"""
        minimum_required = {'lorekeeper_analysis', 'character_development', 'quality_assurance'}
        return minimum_required.issubset(completed_nodes)
    
    def _assess_completion_quality(self, state: Dict[str, Any]) -> str:
        """Evalúa la calidad de la completitud del workflow"""
        
        completed_nodes = set(state.get('completed_nodes', []))
        analysis_results = state.get('analysis_results', {})
        
        # Evaluar cobertura
        total_possible = len(self.action_dependencies)
        completed_count = len(completed_nodes)
        coverage = completed_count / total_possible
        
        # Evaluar calidad de resultados
        quality_scores = []
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                # Buscar puntuaciones de calidad
                score_keys = ['overall_score', 'consistency_score', 'quality_rating']
                for key in score_keys:
                    if key in data and isinstance(data[key], (int, float)):
                        quality_scores.append(data[key])
                        break
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 50
        
        # Determinar calidad general
        if coverage >= 0.9 and avg_quality >= 85:
            return "Excellent"
        elif coverage >= 0.7 and avg_quality >= 75:
            return "Good"
        elif coverage >= 0.5 and avg_quality >= 60:
            return "Acceptable"
        else:
            return "Poor"
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del motor de decisiones"""
        
        return {
            'total_action_types': len(self.action_dependencies),
            'parallel_groups': len(self.parallel_groups),
            'decision_rules_active': True,
            'optimization_enabled': True
        }