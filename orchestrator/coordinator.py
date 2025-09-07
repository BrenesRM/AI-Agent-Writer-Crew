# -*- coding: utf-8 -*-
# orchestrator/coordinator.py
"""
Coordinador principal del sistema multi-agente para novelas.
Gestiona la orquestacion completa del flujo de trabajo.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from .workflow_graph import WorkflowGraph
from .state_manager import StateManager
from .iteration_controller import IterationController
from .decision_engine import DecisionEngine

class NovelCoordinator:
    """Coordinador principal que orquesta todos los componentes del sistema"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Inicializar componentes
        self.state_manager = StateManager()
        self.workflow_graph = WorkflowGraph()
        self.iteration_controller = IterationController(max_iterations=5)
        self.decision_engine = DecisionEngine()
        
        # Estado del sistema
        self.is_running = False
        self.current_session_id = None
        
        self.logger.info("NovelCoordinator inicializado")
    
    async def process_manuscript(
        self, 
        manuscript: str, 
        requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Procesa un manuscrito completo a traves del sistema multi-agente
        
        Args:
            manuscript: El texto del manuscrito a procesar
            requirements: Requisitos especificos del procesamiento
            
        Returns:
            Dict con los resultados del procesamiento
        """
        session_id = self._create_session_id()
        self.current_session_id = session_id
        self.is_running = True
        
        try:
            self.logger.info(f"Iniciando procesamiento de manuscrito - Sesion: {session_id}")
            
            # 1. Inicializar estado
            initial_state = await self.state_manager.initialize_state(
                manuscript=manuscript,
                requirements=requirements or {},
                session_id=session_id
            )
            
            # 2. Ejecutar flujo de trabajo
            final_state = await self._execute_workflow(initial_state)
            
            # 3. Generar resultados finales
            results = await self._generate_final_results(final_state)
            
            self.logger.info(f"Procesamiento completado - Sesion: {session_id}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error en procesamiento: {str(e)}")
            raise
        finally:
            self.is_running = False
            self.current_session_id = None
    
    async def _execute_workflow(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el flujo de trabajo principal"""
        current_state = initial_state
        iteration = 0
        
        # Ciclo principal de iteraciones
        while self.iteration_controller.should_continue(current_state, iteration):
            iteration += 1
            self.logger.info(f"Iniciando iteracion {iteration}")
            
            # Determinar proximas acciones
            next_actions = await self.decision_engine.get_next_actions(current_state)
            
            # Ejecutar acciones en paralelo cuando sea posible
            action_results = await self._execute_actions(next_actions, current_state)
            
            # Actualizar estado
            current_state = await self.state_manager.update_state(
                current_state, 
                action_results,
                iteration
            )
            
            # Evaluar si necesitamos continuar
            if await self.decision_engine.is_workflow_complete(current_state):
                self.logger.info("Flujo de trabajo completado satisfactoriamente")
                break
                
        return current_state
    
    async def _execute_actions(
        self, 
        actions: List[Dict[str, Any]], 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ejecuta un conjunto de acciones, optimizando paralelismo cuando es posible
        """
        results = {}
        
        # Separar acciones paralelas de secuenciales
        parallel_actions = [a for a in actions if a.get('parallel', True)]
        sequential_actions = [a for a in actions if not a.get('parallel', True)]
        
        # Ejecutar acciones paralelas
        if parallel_actions:
            parallel_results = await asyncio.gather(*[
                self._execute_single_action(action, state)
                for action in parallel_actions
            ])
            
            for i, result in enumerate(parallel_results):
                results[parallel_actions[i]['id']] = result
        
        # Ejecutar acciones secuenciales
        for action in sequential_actions:
            result = await self._execute_single_action(action, state)
            results[action['id']] = result
            
            # Actualizar estado para proxima accion secuencial
            state = await self.state_manager.update_state(state, {action['id']: result})
        
        return results
    
    async def _execute_single_action(
        self, 
        action: Dict[str, Any], 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta una accion individual"""
        try:
            action_type = action.get('type')
            agent_name = action.get('agent')
            
            self.logger.info(f"Ejecutando accion: {action_type} con agente: {agent_name}")
            
            # Obtener nodo del workflow graph
            node = self.workflow_graph.get_node(action_type)
            if not node:
                raise ValueError(f"Nodo no encontrado para accion: {action_type}")
            
            # Ejecutar la accion
            result = await node.execute(state, action.get('params', {}))
            
            return {
                'status': 'success',
                'result': result,
                'action': action,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error ejecutando accion {action.get('type')}: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'action': action,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def _generate_final_results(self, final_state: Dict[str, Any]) -> Dict[str, Any]:
        """Genera los resultados finales del procesamiento"""
        results = {
            'session_id': final_state.get('session_id'),
            'processing_summary': {
                'iterations': final_state.get('iteration', 0),
                'total_actions': len(final_state.get('action_history', [])),
                'start_time': final_state.get('start_time'),
                'end_time': datetime.utcnow().isoformat(),
                'status': 'completed'
            },
            'analysis_results': {},
            'recommendations': [],
            'generated_content': {},
            'quality_metrics': {}
        }
        
        # Extraer resultados por categoria
        analysis_results = final_state.get('analysis_results', {})
        
        # Analisis de worldbuilding
        if 'worldbuilding' in analysis_results:
            results['analysis_results']['worldbuilding'] = analysis_results['worldbuilding']
        
        # Desarrollo de personajes
        if 'character_development' in analysis_results:
            results['analysis_results']['character_development'] = analysis_results['character_development']
        
        # Estructura de trama
        if 'plot_structure' in analysis_results:
            results['analysis_results']['plot_structure'] = analysis_results['plot_structure']
        
        # Refinamiento de estilo
        if 'style_refinement' in analysis_results:
            results['analysis_results']['style_refinement'] = analysis_results['style_refinement']
        
        # Contenido visual
        if 'visual_content' in analysis_results:
            results['generated_content']['visual_prompts'] = analysis_results['visual_content']
        
        # Aseguramiento de calidad
        if 'quality_assurance' in analysis_results:
            results['quality_metrics'] = analysis_results['quality_assurance']
        
        # Generar recomendaciones consolidadas
        recommendations = final_state.get('consolidated_recommendations', [])
        results['recommendations'] = recommendations
        
        return results
    
    def _create_session_id(self) -> str:
        """Genera un ID unico para la sesion"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"novel_session_{timestamp}"
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del coordinador"""
        return {
            'is_running': self.is_running,
            'current_session': self.current_session_id,
            'components': {
                'state_manager': self.state_manager.get_status(),
                'workflow_graph': self.workflow_graph.get_status(),
                'iteration_controller': self.iteration_controller.get_status(),
                'decision_engine': self.decision_engine.get_status()
            }
        }
    
    async def stop_processing(self) -> None:
        """Detiene el procesamiento actual de manera segura"""
        if self.is_running:
            self.logger.info("Deteniendo procesamiento...")
            self.is_running = False
            await self.state_manager.save_current_state()
            
    async def resume_processing(self, session_id: str) -> Dict[str, Any]:
        """Reanuda una sesion de procesamiento"""
        try:
            state = await self.state_manager.load_state(session_id)
            if state:
                self.current_session_id = session_id
                return await self._execute_workflow(state)
            else:
                raise ValueError(f"No se pudo cargar el estado para la sesion: {session_id}")
        except Exception as e:
            self.logger.error(f"Error reanudando sesion {session_id}: {str(e)}")
            raise