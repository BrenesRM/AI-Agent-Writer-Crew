# orchestrator/__init__.py
"""
Sistema de Orquestación LangGraph para el sistema multi-agente de novelas.

Este módulo implementa la orquestación completa del flujo de trabajo usando LangGraph,
coordinando la ejecución de múltiples agentes especializados en análisis y mejora
de manuscritos narrativos.

Componentes principales:
- NovelCoordinator: Coordinador principal del sistema
- WorkflowGraph: Definición del grafo de flujo de trabajo
- StateManager: Gestión del estado entre iteraciones
- IterationController: Control de ciclos iterativos
- DecisionEngine: Motor de decisiones para el flujo
"""

from .coordinator import NovelCoordinator
from .workflow_graph import WorkflowGraph, WorkflowNode, NodeType
from .state_manager import StateManager
from .iteration_controller import IterationController, IterationStopReason
from .decision_engine import DecisionEngine, ActionPriority, ActionType

__all__ = [
    'NovelCoordinator',
    'WorkflowGraph',
    'WorkflowNode', 
    'NodeType',
    'StateManager',
    'IterationController',
    'IterationStopReason',
    'DecisionEngine',
    'ActionPriority',
    'ActionType'
]

__version__ = "1.0.0"