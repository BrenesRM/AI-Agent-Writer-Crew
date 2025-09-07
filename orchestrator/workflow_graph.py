# -*- coding: utf-8 -*-
# orchestrator/workflow_graph.py
"""
Definicion del grafo de flujo de trabajo usando LangGraph.
Define los nodos, aristas y flujo del sistema multi-agente.
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio

class NodeType(Enum):
    """Tipos de nodos en el workflow"""
    ANALYSIS = "analysis"
    GENERATION = "generation" 
    VALIDATION = "validation"
    CONSOLIDATION = "consolidation"

@dataclass
class WorkflowNode:
    """Representacion de un nodo en el workflow"""
    id: str
    name: str
    node_type: NodeType
    agent_class: str
    dependencies: List[str]
    parallel_safe: bool = True
    required: bool = True
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta la logica del nodo"""
        # Esta sera implementada por cada nodo especifico
        pass

class LorekeeperNode(WorkflowNode):
    """Nodo para analisis de worldbuilding"""
    
    def __init__(self):
        super().__init__(
            id="lorekeeper_analysis",
            name="Analisis de Worldbuilding",
            node_type=NodeType.ANALYSIS,
            agent_class="LorekeeperAgent",
            dependencies=[],
            parallel_safe=True
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta analisis de lore y worldbuilding"""
        try:
            manuscript = state.get('manuscript', '')
            
            # Simulacion del analisis (se conectaria con el agente real)
            analysis = {
                'lore_elements': ['Magic System', 'Geography', 'History'],
                'consistency_score': 85,
                'recommendations': [
                    'Clarify magic system rules',
                    'Expand geographical descriptions'
                ],
                'detected_inconsistencies': [],
                'world_complexity': 'Medium'
            }
            
            return {
                'worldbuilding_analysis': analysis,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class CharacterDeveloperNode(WorkflowNode):
    """Nodo para desarrollo de personajes"""
    
    def __init__(self):
        super().__init__(
            id="character_development",
            name="Desarrollo de Personajes",
            node_type=NodeType.ANALYSIS,
            agent_class="CharacterDeveloperAgent",
            dependencies=[],
            parallel_safe=True
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta analisis y desarrollo de personajes"""
        try:
            manuscript = state.get('manuscript', '')
            
            analysis = {
                'characters_identified': ['Protagonist', 'Antagonist', 'Supporting Cast'],
                'character_development_score': 78,
                'arc_completeness': {
                    'protagonist': 90,
                    'antagonist': 65,
                    'supporting': 45
                },
                'relationships': ['Mentor-Student', 'Rivalry', 'Friendship'],
                'recommendations': [
                    'Develop antagonist motivation',
                    'Strengthen supporting character arcs'
                ]
            }
            
            return {
                'character_analysis': analysis,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class PlotWeaverNode(WorkflowNode):
    """Nodo para analisis de trama"""
    
    def __init__(self):
        super().__init__(
            id="plot_analysis",
            name="Analisis de Trama",
            node_type=NodeType.ANALYSIS,
            agent_class="PlotWeaverAgent",
            dependencies=["lorekeeper_analysis", "character_development"],
            parallel_safe=False
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta analisis de estructura narrativa"""
        try:
            manuscript = state.get('manuscript', '')
            worldbuilding = state.get('analysis_results', {}).get('worldbuilding', {})
            characters = state.get('analysis_results', {}).get('character_development', {})
            
            analysis = {
                'structure_score': 82,
                'pacing_rating': 'Good',
                'conflict_development': 75,
                'plot_holes': [],
                'narrative_tension': 'Adequate',
                'recommendations': [
                    'Intensify midpoint conflict',
                    'Clarify stakes in act 2'
                ],
                'three_act_structure': {
                    'act1': 85,
                    'act2': 70,
                    'act3': 90
                }
            }
            
            return {
                'plot_analysis': analysis,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class StyleEditorNode(WorkflowNode):
    """Nodo para refinamiento de estilo"""
    
    def __init__(self):
        super().__init__(
            id="style_refinement",
            name="Refinamiento de Estilo",
            node_type=NodeType.ANALYSIS,
            agent_class="StyleEditorAgent",
            dependencies=[],
            parallel_safe=True
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta analisis y refinamiento de estilo"""
        try:
            manuscript = state.get('manuscript', '')
            
            analysis = {
                'style_consistency': 88,
                'tone_analysis': 'Consistent Epic Fantasy',
                'voice_strength': 'Strong',
                'prose_quality': 80,
                'dialogue_quality': 75,
                'recommendations': [
                    'Vary sentence structure more',
                    'Strengthen character voices in dialogue'
                ],
                'readability_score': 82
            }
            
            return {
                'style_analysis': analysis,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class VisualizerNode(WorkflowNode):
    """Nodo para generacion de contenido visual"""
    
    def __init__(self):
        super().__init__(
            id="visual_generation",
            name="Generacion Visual",
            node_type=NodeType.GENERATION,
            agent_class="VisualizerAgent",
            dependencies=["lorekeeper_analysis", "character_development", "plot_analysis"],
            parallel_safe=False
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Genera prompts visuales basados en el analisis"""
        try:
            # Tomar datos de analisis previos
            worldbuilding = state.get('analysis_results', {}).get('worldbuilding', {})
            characters = state.get('analysis_results', {}).get('character_development', {})
            plot = state.get('analysis_results', {}).get('plot_analysis', {})
            
            visual_content = {
                'character_prompts': [
                    'Epic fantasy protagonist with determined expression',
                    'Dark sorcerer antagonist in mystical robes'
                ],
                'scene_prompts': [
                    'Ancient magical library with floating books',
                    'Battle scene in enchanted forest'
                ],
                'world_prompts': [
                    'Sweeping view of fantasy kingdom with twin moons',
                    'Underground dwarven city with crystal formations'
                ],
                'mood_boards': ['Epic Fantasy', 'Dark Magic', 'Heroic Journey']
            }
            
            return {
                'visual_content': visual_content,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class QualityAssuranceNode(WorkflowNode):
    """Nodo para control de calidad final"""
    
    def __init__(self):
        super().__init__(
            id="quality_assurance",
            name="Control de Calidad",
            node_type=NodeType.VALIDATION,
            agent_class="ProofreaderAgent",
            dependencies=["style_refinement", "plot_analysis"],
            parallel_safe=False,
            required=True
        )
    
    async def execute(self, state: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta control de calidad final"""
        try:
            manuscript = state.get('manuscript', '')
            
            # Consolidar todos los analisis previos
            all_analyses = state.get('analysis_results', {})
            
            quality_report = {
                'overall_score': 82,
                'technical_quality': 88,
                'narrative_quality': 80,
                'consistency_score': 85,
                'readiness': 'Good - Minor improvements recommended',
                'critical_issues': [],
                'improvement_areas': [
                    'Character development depth',
                    'Pacing in middle section'
                ],
                'strengths': [
                    'Strong worldbuilding',
                    'Consistent style',
                    'Clear narrative voice'
                ]
            }
            
            return {
                'quality_report': quality_report,
                'node_id': self.id,
                'status': 'completed'
            }
            
        except Exception as e:
            logging.error(f"Error en {self.name}: {str(e)}")
            return {
                'error': str(e),
                'node_id': self.id,
                'status': 'failed'
            }

class WorkflowGraph:
    """Grafo de flujo de trabajo que define la logica de ejecucion"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = {}
        self._initialize_graph()
    
    def _initialize_graph(self):
        """Inicializa el grafo con todos los nodos y conexiones"""
        
        # Crear nodos
        nodes = [
            LorekeeperNode(),
            CharacterDeveloperNode(),
            PlotWeaverNode(),
            StyleEditorNode(),
            VisualizerNode(),
            QualityAssuranceNode()
        ]
        
        # Registrar nodos
        for node in nodes:
            self.nodes[node.id] = node
        
        # Definir flujo de dependencias
        self._build_dependency_graph()
        
        self.logger.info(f"Grafo inicializado con {len(self.nodes)} nodos")
    
    def _build_dependency_graph(self):
        """Construye el grafo de dependencias basado en los nodos"""
        self.edges = {}
        
        for node_id, node in self.nodes.items():
            self.edges[node_id] = node.dependencies.copy()
        
        # Log del grafo para debugging
        self.logger.debug("Grafo de dependencias:")
        for node_id, deps in self.edges.items():
            self.logger.debug(f"  {node_id} -> {deps}")
    
    def get_executable_nodes(self, completed_nodes: List[str]) -> List[str]:
        """
        Obtiene los nodos que pueden ejecutarse basado en dependencias completadas
        """
        executable = []
        
        for node_id, dependencies in self.edges.items():
            # Si el nodo ya fue completado, saltar
            if node_id in completed_nodes:
                continue
            
            # Verificar si todas las dependencias estan completadas
            if all(dep in completed_nodes for dep in dependencies):
                executable.append(node_id)
        
        return executable
    
    def get_parallel_groups(self, executable_nodes: List[str]) -> List[List[str]]:
        """
        Agrupa nodos ejecutables en grupos que pueden ejecutarse en paralelo
        """
        parallel_groups = []
        sequential_nodes = []
        
        for node_id in executable_nodes:
            node = self.nodes[node_id]
            if node.parallel_safe:
                # Buscar si puede unirse a un grupo existente
                added_to_group = False
                for group in parallel_groups:
                    # Verificar que no haya dependencias cruzadas en el grupo
                    if not any(dep in group for dep in node.dependencies):
                        group.append(node_id)
                        added_to_group = True
                        break
                
                if not added_to_group:
                    parallel_groups.append([node_id])
            else:
                sequential_nodes.append([node_id])
        
        # Combinar grupos paralelos y secuenciales
        return parallel_groups + sequential_nodes
    
    def get_node(self, node_id: str) -> Optional[WorkflowNode]:
        """Obtiene un nodo por su ID"""
        return self.nodes.get(node_id)
    
    def validate_graph(self) -> bool:
        """Valida que el grafo sea valido (no tenga ciclos, etc.)"""
        try:
            # Verificar ciclos usando DFS
            visited = set()
            rec_stack = set()
            
            def has_cycle(node_id: str) -> bool:
                visited.add(node_id)
                rec_stack.add(node_id)
                
                for neighbor in self.edges.get(node_id, []):
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True
                
                rec_stack.remove(node_id)
                return False
            
            # Verificar cada nodo
            for node_id in self.nodes:
                if node_id not in visited:
                    if has_cycle(node_id):
                        self.logger.error(f"Ciclo detectado en el grafo que incluye: {node_id}")
                        return False
            
            # Verificar que todas las dependencias existan
            for node_id, dependencies in self.edges.items():
                for dep in dependencies:
                    if dep not in self.nodes:
                        self.logger.error(f"Dependencia inexistente: {dep} para nodo {node_id}")
                        return False
            
            self.logger.info("Grafo validado correctamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando grafo: {str(e)}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del grafo"""
        return {
            'nodes_count': len(self.nodes),
            'is_valid': self.validate_graph(),
            'node_types': {
                node_type.value: len([n for n in self.nodes.values() if n.node_type == node_type])
                for node_type in NodeType
            }
        }