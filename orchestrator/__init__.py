# -*- coding: utf-8 -*-
# orchestrator/__init__.py
"""
Sistema de Orquestacion LangGraph para el sistema multi-agente de novelas.

Este modulo implementa la orquestacion completa del flujo de trabajo usando LangGraph,
coordinando la ejecucion de multiples agentes especializados en analisis y mejora
de manuscritos narrativos.

Componentes principales:
- NovelCoordinator: Coordinador principal del sistema
- WorkflowGraph: Definicion del grafo de flujo de trabajo
- StateManager: Gestion del estado entre iteraciones
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