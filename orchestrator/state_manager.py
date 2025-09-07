# -*- coding: utf-8 -*-
# orchestrator/state_manager.py
"""
Gestion del estado entre iteraciones del flujo de trabajo.
Mantiene el estado persistente y gestiona las transiciones de estado.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import pickle
import hashlib

class StateManager:
    """Gestor del estado del sistema multi-agente"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or "data/sessions")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self.current_state = {}
        self.state_history = []
        self.max_history = 50  # Maximo de estados en historial
        
        self.logger.info(f"StateManager inicializado - Storage: {self.storage_path}")
    
    async def initialize_state(
        self, 
        manuscript: str, 
        requirements: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Inicializa el estado para una nueva sesion de procesamiento
        """
        try:
            initial_state = {
                'session_id': session_id,
                'manuscript': manuscript,
                'manuscript_hash': self._calculate_hash(manuscript),
                'requirements': requirements,
                'start_time': datetime.utcnow().isoformat(),
                'iteration': 0,
                'completed_nodes': [],
                'failed_nodes': [],
                'analysis_results': {},
                'action_history': [],
                'consolidated_recommendations': [],
                'quality_metrics': {},
                'metadata': {
                    'manuscript_length': len(manuscript),
                    'word_count': len(manuscript.split()),
                    'created_at': datetime.utcnow().isoformat(),
                    'last_updated': datetime.utcnow().isoformat()
                },
                'processing_status': 'initialized',
                'error_log': []
            }
            
            # Guardar estado inicial
            await self._save_state(initial_state)
            
            self.current_state = initial_state
            self._add_to_history(initial_state)
            
            self.logger.info(f"Estado inicializado para sesion: {session_id}")
            return initial_state
            
        except Exception as e:
            self.logger.error(f"Error inicializando estado: {str(e)}")
            raise
    
    async def update_state(
        self, 
        current_state: Dict[str, Any], 
        action_results: Dict[str, Any],
        iteration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Actualiza el estado con los resultados de las acciones ejecutadas
        """
        try:
            # Crear nuevo estado basado en el actual
            new_state = current_state.copy()
            
            # Actualizar iteracion
            if iteration is not None:
                new_state['iteration'] = iteration
            
            # Actualizar timestamp
            new_state['metadata']['last_updated'] = datetime.utcnow().isoformat()
            
            # Procesar resultados de acciones
            for action_id, result in action_results.items():
                # Agregar a historial de acciones
                action_entry = {
                    'action_id': action_id,
                    'timestamp': result.get('timestamp', datetime.utcnow().isoformat()),
                    'status': result.get('status', 'unknown'),
                    'iteration': new_state['iteration']
                }
                new_state['action_history'].append(action_entry)
                
                # Actualizar nodos completados o fallidos
                if result.get('status') == 'completed':
                    node_id = result.get('result', {}).get('node_id')
                    if node_id and node_id not in new_state['completed_nodes']:
                        new_state['completed_nodes'].append(node_id)
                    
                    # Integrar resultados del analisis
                    await self._integrate_analysis_results(new_state, result)
                    
                elif result.get('status') == 'failed':
                    node_id = result.get('action', {}).get('type')
                    if node_id and node_id not in new_state['failed_nodes']:
                        new_state['failed_nodes'].append(node_id)
                    
                    # Registrar error
                    error_entry = {
                        'node_id': node_id,
                        'error': result.get('error', 'Unknown error'),
                        'timestamp': result.get('timestamp'),
                        'iteration': new_state['iteration']
                    }
                    new_state['error_log'].append(error_entry)
            
            # Actualizar estado de procesamiento
            await self._update_processing_status(new_state)
            
            # Consolidar recomendaciones
            await self._consolidate_recommendations(new_state)
            
            # Guardar estado actualizado
            await self._save_state(new_state)
            
            # Actualizar estado actual y historial
            self.current_state = new_state
            self._add_to_history(new_state)
            
            self.logger.info(f"Estado actualizado - Iteracion: {new_state['iteration']}")
            return new_state
            
        except Exception as e:
            self.logger.error(f"Error actualizando estado: {str(e)}")
            raise
    
    async def _integrate_analysis_results(
        self, 
        state: Dict[str, Any], 
        result: Dict[str, Any]
    ) -> None:
        """Integra los resultados de analisis en el estado"""
        
        result_data = result.get('result', {})
        node_id = result_data.get('node_id')
        
        if not node_id:
            return
        
        # Mapear resultados por tipo de analisis
        analysis_mapping = {
            'lorekeeper_analysis': 'worldbuilding',
            'character_development': 'character_development', 
            'plot_analysis': 'plot_structure',
            'style_refinement': 'style_refinement',
            'visual_generation': 'visual_content',
            'quality_assurance': 'quality_assurance'
        }
        
        analysis_category = analysis_mapping.get(node_id)
        
        if analysis_category:
            # Extraer datos relevantes del resultado
            if 'worldbuilding_analysis' in result_data:
                state['analysis_results'][analysis_category] = result_data['worldbuilding_analysis']
            elif 'character_analysis' in result_data:
                state['analysis_results'][analysis_category] = result_data['character_analysis']
            elif 'plot_analysis' in result_data:
                state['analysis_results'][analysis_category] = result_data['plot_analysis']
            elif 'style_analysis' in result_data:
                state['analysis_results'][analysis_category] = result_data['style_analysis']
            elif 'visual_content' in result_data:
                state['analysis_results'][analysis_category] = result_data['visual_content']
            elif 'quality_report' in result_data:
                state['analysis_results'][analysis_category] = result_data['quality_report']
    
    async def _update_processing_status(self, state: Dict[str, Any]) -> None:
        """Actualiza el estado de procesamiento basado en nodos completados"""
        
        total_nodes = 6  # Total de nodos en el workflow
        completed_count = len(state['completed_nodes'])
        failed_count = len(state['failed_nodes'])
        
        if failed_count > 0 and completed_count < total_nodes // 2:
            state['processing_status'] = 'failed'
        elif completed_count == total_nodes:
            state['processing_status'] = 'completed'
        elif completed_count > total_nodes // 2:
            state['processing_status'] = 'advanced'
        elif completed_count > 0:
            state['processing_status'] = 'in_progress'
        else:
            state['processing_status'] = 'initialized'
    
    async def _consolidate_recommendations(self, state: Dict[str, Any]) -> None:
        """Consolida recomendaciones de todos los analisis"""
        
        all_recommendations = []
        analysis_results = state.get('analysis_results', {})
        
        # Recopilar recomendaciones de cada analisis
        for category, data in analysis_results.items():
            if isinstance(data, dict) and 'recommendations' in data:
                category_recommendations = data['recommendations']
                for rec in category_recommendations:
                    all_recommendations.append({
                        'category': category,
                        'recommendation': rec,
                        'priority': self._calculate_priority(category, rec),
                        'timestamp': datetime.utcnow().isoformat()
                    })
        
        # Ordenar por prioridad y eliminar duplicados
        all_recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        # Deduplicar recomendaciones similares
        consolidated = []
        seen_recommendations = set()
        
        for rec in all_recommendations:
            rec_key = rec['recommendation'].lower().strip()
            if rec_key not in seen_recommendations:
                consolidated.append(rec)
                seen_recommendations.add(rec_key)
        
        state['consolidated_recommendations'] = consolidated[:10]  # Top 10 recomendaciones
    
    def _calculate_priority(self, category: str, recommendation: str) -> int:
        """Calcula la prioridad de una recomendacion"""
        
        # Prioridades por categoria
        category_priorities = {
            'quality_assurance': 100,
            'plot_structure': 90,
            'character_development': 80,
            'worldbuilding': 70,
            'style_refinement': 60,
            'visual_content': 50
        }
        
        base_priority = category_priorities.get(category, 50)
        
        # Ajustar prioridad basada en palabras clave
        high_priority_keywords = ['critical', 'error', 'inconsistency', 'plot hole']
        medium_priority_keywords = ['improve', 'enhance', 'develop', 'clarify']
        
        recommendation_lower = recommendation.lower()
        
        if any(keyword in recommendation_lower for keyword in high_priority_keywords):
            return base_priority + 20
        elif any(keyword in recommendation_lower for keyword in medium_priority_keywords):
            return base_priority + 10
        else:
            return base_priority
    
    async def _save_state(self, state: Dict[str, Any]) -> None:
        """Guarda el estado en almacenamiento persistente"""
        
        try:
            session_id = state.get('session_id')
            if not session_id:
                raise ValueError("Session ID requerido para guardar estado")
            
            # Crear archivo de estado
            state_file = self.storage_path / f"{session_id}_state.json"
            
            # Guardar estado como JSON
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            # Crear backup comprimido para estados grandes
            backup_file = self.storage_path / f"{session_id}_backup.pkl"
            with open(backup_file, 'wb') as f:
                pickle.dump(state, f)
            
            # Limpiar archivos antiguos (mas de 7 dias)
            await self._cleanup_old_files()
            
        except Exception as e:
            self.logger.error(f"Error guardando estado: {str(e)}")
            raise
    
    async def load_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Carga un estado desde almacenamiento"""
        
        try:
            state_file = self.storage_path / f"{session_id}_state.json"
            
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                self.current_state = state
                self.logger.info(f"Estado cargado para sesion: {session_id}")
                return state
            else:
                # Intentar cargar desde backup
                backup_file = self.storage_path / f"{session_id}_backup.pkl"
                if backup_file.exists():
                    with open(backup_file, 'rb') as f:
                        state = pickle.load(f)
                    
                    self.current_state = state
                    self.logger.info(f"Estado cargado desde backup: {session_id}")
                    return state
                else:
                    self.logger.warning(f"No se encontro estado para sesion: {session_id}")
                    return None
        
        except Exception as e:
            self.logger.error(f"Error cargando estado: {str(e)}")
            return None
    
    async def save_current_state(self) -> None:
        """Guarda el estado actual"""
        if self.current_state:
            await self._save_state(self.current_state)
    
    def _add_to_history(self, state: Dict[str, Any]) -> None:
        """Añade un estado al historial"""
        
        # Crear una copia ligera del estado para el historial
        history_entry = {
            'session_id': state.get('session_id'),
            'iteration': state.get('iteration', 0),
            'timestamp': state.get('metadata', {}).get('last_updated'),
            'completed_nodes': len(state.get('completed_nodes', [])),
            'failed_nodes': len(state.get('failed_nodes', [])),
            'processing_status': state.get('processing_status')
        }
        
        self.state_history.append(history_entry)
        
        # Mantener solo los ultimos estados
        if len(self.state_history) > self.max_history:
            self.state_history = self.state_history[-self.max_history:]
    
    def _calculate_hash(self, text: str) -> str:
        """Calcula hash MD5 de un texto"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    async def _cleanup_old_files(self) -> None:
        """Limpia archivos de estado antiguos"""
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=7)
            
            for file_path in self.storage_path.glob("*_state.json"):
                if file_path.stat().st_mtime < cutoff_date.timestamp():
                    file_path.unlink()
                    
                    # Eliminar backup correspondiente
                    backup_path = file_path.with_suffix('.pkl')
                    if backup_path.exists():
                        backup_path.unlink()
            
        except Exception as e:
            self.logger.warning(f"Error limpiando archivos antiguos: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del gestor"""
        
        return {
            'has_current_state': bool(self.current_state),
            'history_length': len(self.state_history),
            'storage_path': str(self.storage_path),
            'current_session': self.current_state.get('session_id') if self.current_state else None
        }
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Obtiene un resumen de una sesion especifica"""
        
        if self.current_state and self.current_state.get('session_id') == session_id:
            state = self.current_state
        else:
            state = asyncio.run(self.load_state(session_id))
        
        if not state:
            return {'error': 'Session not found'}
        
        return {
            'session_id': session_id,
            'status': state.get('processing_status'),
            'iteration': state.get('iteration', 0),
            'completed_nodes': len(state.get('completed_nodes', [])),
            'failed_nodes': len(state.get('failed_nodes', [])),
            'start_time': state.get('start_time'),
            'last_updated': state.get('metadata', {}).get('last_updated'),
            'word_count': state.get('metadata', {}).get('word_count', 0),
            'recommendations_count': len(state.get('consolidated_recommendations', []))
        }