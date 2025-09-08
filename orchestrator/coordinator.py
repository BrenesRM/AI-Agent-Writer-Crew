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
        
        # Inicializar componentes con manejo de errores
        try:
            self.state_manager = StateManager()
            self.workflow_graph = WorkflowGraph()
            self.iteration_controller = IterationController(
                max_iterations=self.config.get('max_iterations', 5),
                quality_threshold=self.config.get('quality_threshold', 0.8)
            )
            self.decision_engine = DecisionEngine()
        except Exception as e:
            self.logger.error(f"Error inicializando componentes: {str(e)}")
            raise
        
        # Estado del sistema
        self.is_running = False
        self.current_session_id = None
        self._shutdown_requested = False
        
        # Validar configuración del grafo
        if not self.workflow_graph.validate_graph():
            raise ValueError("El grafo de workflow no es válido")
        
        self.logger.info("NovelCoordinator inicializado correctamente")
    
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
        if self.is_running:
            raise RuntimeError("Ya hay un procesamiento en curso")
            
        if not manuscript or not manuscript.strip():
            raise ValueError("El manuscrito no puede estar vacio")
        
        session_id = self._create_session_id()
        self.current_session_id = session_id
        self.is_running = True
        self._shutdown_requested = False
        
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
            # Intentar guardar el estado actual para recuperación
            try:
                if hasattr(self, 'state_manager') and self.state_manager.current_state:
                    await self.state_manager.save_current_state()
            except:
                pass
            raise
        finally:
            self.is_running = False
            self.current_session_id = None
            self._shutdown_requested = False
    
    async def _execute_workflow(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el flujo de trabajo principal"""
        current_state = initial_state
        iteration = 0
        
        # Reset del controlador de iteraciones
        self.iteration_controller.reset()
        
        # Ciclo principal de iteraciones
        while (self.iteration_controller.should_continue(current_state, iteration) and 
               not self._shutdown_requested):
            
            iteration += 1
            self.logger.info(f"Iniciando iteracion {iteration}")
            
            try:
                # Determinar proximas acciones
                next_actions = await self.decision_engine.get_next_actions(current_state)
                
                if not next_actions:
                    self.logger.info("No hay mas acciones disponibles")
                    break
                
                # Ejecutar acciones
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
                    
            except Exception as e:
                self.logger.error(f"Error en iteracion {iteration}: {str(e)}")
                # Registrar error en el estado
                error_entry = {
                    'iteration': iteration,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': 'workflow_error'
                }
                current_state.setdefault('error_log', []).append(error_entry)
                
                # Continuar con la siguiente iteración si no es un error crítico
                continue
                
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
        
        if not actions:
            return results
        
        # Separar acciones paralelas de secuenciales
        parallel_actions = [a for a in actions if a.get('parallel', True)]
        sequential_actions = [a for a in actions if not a.get('parallel', True)]
        
        # Ejecutar acciones paralelas con límite de concurrencia
        if parallel_actions:
            # Limitar concurrencia para evitar sobrecarga
            semaphore = asyncio.Semaphore(3)
            
            async def execute_with_semaphore(action):
                async with semaphore:
                    return await self._execute_single_action(action, state)
            
            try:
                parallel_results = await asyncio.gather(*[
                    execute_with_semaphore(action)
                    for action in parallel_actions
                ], return_exceptions=True)
                
                for i, result in enumerate(parallel_results):
                    if isinstance(result, Exception):
                        # Manejar excepciones en acciones paralelas
                        self.logger.error(f"Error en acción paralela {parallel_actions[i]['id']}: {str(result)}")
                        results[parallel_actions[i]['id']] = {
                            'status': 'error',
                            'error': str(result),
                            'action': parallel_actions[i],
                            'timestamp': datetime.utcnow().isoformat()
                        }
                    else:
                        results[parallel_actions[i]['id']] = result
            except Exception as e:
                self.logger.error(f"Error ejecutando acciones paralelas: {str(e)}")
        
        # Ejecutar acciones secuenciales
        for action in sequential_actions:
            try:
                result = await self._execute_single_action(action, state)
                results[action['id']] = result
                
                # Actualizar estado para próxima acción secuencial
                state = await self.state_manager.update_state(state, {action['id']: result})
            except Exception as e:
                self.logger.error(f"Error en acción secuencial {action['id']}: {str(e)}")
                results[action['id']] = {
                    'status': 'error',
                    'error': str(e),
                    'action': action,
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return results
    
    async def _execute_single_action(
        self, 
        action: Dict[str, Any], 
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta una accion individual"""
        action_start = datetime.utcnow()
        
        try:
            action_type = action.get('type')
            agent_name = action.get('agent')
            
            self.logger.info(f"Ejecutando accion: {action_type} con agente: {agent_name}")
            
            # Obtener nodo del workflow graph
            node = self.workflow_graph.get_node(action_type)
            if not node:
                raise ValueError(f"Nodo no encontrado para accion: {action_type}")
            
            # Ejecutar la accion con timeout
            try:
                result = await asyncio.wait_for(
                    node.execute(state, action.get('params', {})),
                    timeout=300  # 5 minutos timeout
                )
            except asyncio.TimeoutError:
                raise TimeoutError(f"Acción {action_type} excedió el tiempo límite")
            
            processing_time = (datetime.utcnow() - action_start).total_seconds()
            
            return {
                'status': 'success',
                'result': result,
                'action': action,
                'timestamp': datetime.utcnow().isoformat(),
                'processing_time': processing_time
            }
            
        except Exception as e:
            processing_time = (datetime.utcnow() - action_start).total_seconds()
            self.logger.error(f"Error ejecutando accion {action.get('type')}: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'action': action,
                'timestamp': datetime.utcnow().isoformat(),
                'processing_time': processing_time
            }
    
    async def _generate_final_results(self, final_state: Dict[str, Any]) -> Dict[str, Any]:
        """Genera los resultados finales del procesamiento"""
        processing_start = datetime.fromisoformat(final_state.get('start_time'))
        processing_end = datetime.utcnow()
        
        results = {
            'session_id': final_state.get('session_id'),
            'processing_summary': {
                'iterations': final_state.get('iteration', 0),
                'total_actions': len(final_state.get('action_history', [])),
                'completed_nodes': len(final_state.get('completed_nodes', [])),
                'failed_nodes': len(final_state.get('failed_nodes', [])),
                'start_time': final_state.get('start_time'),
                'end_time': processing_end.isoformat(),
                'total_duration_seconds': (processing_end - processing_start).total_seconds(),
                'status': final_state.get('processing_status', 'unknown')
            },
            'analysis_results': {},
            'recommendations': [],
            'generated_content': {},
            'quality_metrics': {},
            'errors': final_state.get('error_log', [])
        }
        
        # Extraer resultados por categoria de manera más robusta
        analysis_results = final_state.get('analysis_results', {})
        
        # Mapear resultados con validación
        result_mapping = {
            'worldbuilding': 'worldbuilding',
            'character_development': 'character_development',
            'plot_structure': 'plot_structure', 
            'style_refinement': 'style_refinement',
            'visual_content': 'visual_content',
            'quality_assurance': 'quality_assurance'
        }
        
        for key, target_key in result_mapping.items():
            if key in analysis_results and analysis_results[key]:
                results['analysis_results'][target_key] = analysis_results[key]
        
        # Generar métricas de calidad consolidadas
        results['quality_metrics'] = self._calculate_quality_metrics(final_state)
        
        # Generar recomendaciones consolidadas
        recommendations = final_state.get('consolidated_recommendations', [])
        results['recommendations'] = recommendations[:20]  # Limitar a top 20
        
        # Extraer contenido generado
        if 'visual_content' in analysis_results:
            results['generated_content']['visual_prompts'] = analysis_results['visual_content']
        
        return results
    
    def _calculate_quality_metrics(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas de calidad consolidadas"""
        analysis_results = state.get('analysis_results', {})
        
        scores = []
        detailed_scores = {}
        
        # Recopilar puntuaciones de cada análisis
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                score_keys = ['overall_score', 'consistency_score', 'quality_rating', 'structure_score']
                for key in score_keys:
                    if key in data and isinstance(data[key], (int, float)):
                        score_value = data[key]
                        scores.append(score_value)
                        detailed_scores[f"{category}_{key}"] = score_value
                        break
        
        # Calcular métricas generales
        overall_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'overall_score': round(overall_score, 2),
            'component_scores': detailed_scores,
            'completion_rate': len(state.get('completed_nodes', [])) / 6 * 100,  # 6 nodos total
            'error_rate': len(state.get('failed_nodes', [])) / 6 * 100,
            'analysis_depth': len(analysis_results),
            'recommendation_count': len(state.get('consolidated_recommendations', []))
        }
    
    def _create_session_id(self) -> str:
        """Genera un ID unico para la sesion"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"novel_session_{timestamp}"
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del coordinador"""
        return {
            'is_running': self.is_running,
            'current_session': self.current_session_id,
            'shutdown_requested': self._shutdown_requested,
            'components': {
                'state_manager': self.state_manager.get_status() if self.state_manager else None,
                'workflow_graph': self.workflow_graph.get_status() if self.workflow_graph else None,
                'iteration_controller': self.iteration_controller.get_status() if self.iteration_controller else None,
                'decision_engine': self.decision_engine.get_status() if self.decision_engine else None
            }
        }
    
    async def stop_processing(self) -> None:
        """Detiene el procesamiento actual de manera segura"""
        if self.is_running:
            self.logger.info("Solicitando parada del procesamiento...")
            self._shutdown_requested = True
            self.iteration_controller.request_stop("User requested shutdown")
            
            # Intentar guardar el estado actual
            try:
                await self.state_manager.save_current_state()
                self.logger.info("Estado guardado antes del shutdown")
            except Exception as e:
                self.logger.error(f"Error guardando estado durante shutdown: {str(e)}")
            
    async def resume_processing(self, session_id: str) -> Dict[str, Any]:
        """Reanuda una sesion de procesamiento"""
        if self.is_running:
            raise RuntimeError("Ya hay un procesamiento en curso")
            
        try:
            state = await self.state_manager.load_state(session_id)
            if not state:
                raise ValueError(f"No se pudo cargar el estado para la sesion: {session_id}")
            
            self.current_session_id = session_id
            self.is_running = True
            self._shutdown_requested = False
            
            # Continuar desde donde se quedó
            final_state = await self._execute_workflow(state)
            results = await self._generate_final_results(final_state)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error reanudando sesion {session_id}: {str(e)}")
            self.is_running = False
            self.current_session_id = None
            raise
        finally:
            if self.is_running:  # Solo si no hubo errores críticos
                self.is_running = False
                self.current_session_id = None

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Obtiene información sobre una sesión específica"""
        return self.state_manager.get_session_summary(session_id)
