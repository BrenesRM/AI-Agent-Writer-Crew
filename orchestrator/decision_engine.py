                                   if e.get('node_id') == action.type])
            if action_failures >= action.max_retries + 1:
                include_action = False
                self.logger.info(f"Saltando {action.id} - demasiados fallos previos")
            
            if include_action:
                filtered_actions.append(action)
        
        return filtered_actions
    
    def _optimize_execution_order(
        self, 
        actions: List[Action], 
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Optimiza el orden de ejecucion y paralelismo"""
        
        if not actions:
            return []
        
        # Convertir a formato de diccionario
        action_dicts = []
        
        # Ordenar por prioridad y dependencias
        actions.sort(key=lambda x: (x.priority.value, len(x.dependencies), x.retry_count))
        
        for action in actions:
            action_dict = {
                'id': action.id,
                'type': action.type,
                'agent': action.agent,
                'priority': action.priority.value,
                'dependencies': action.dependencies,
                'parallel': action.parallel,
                'params': action.params,
                'estimated_duration': action.estimated_duration,
                'retry_count': action.retry_count,
                'max_retries': action.max_retries
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
        
        if not actions:
            return []
        
        # Optimización 1: Agrupar acciones paralelas
        parallel_actions = [a for a in actions if a.get('parallel', True)]
        sequential_actions = [a for a in actions if not a.get('parallel', True)]
        
        # Optimización 2: Balancear carga por duración estimada
        if len(parallel_actions) > self.max_concurrent_actions:
            # Ordenar por duración y tomar los más eficientes
            parallel_actions.sort(key=lambda x: x['estimated_duration'])
            parallel_actions = parallel_actions[:self.max_concurrent_actions]
        
        # Optimización 3: Priorizar acciones que desbloquean otras
        def count_dependents(action_type: str) -> int:
            return sum(1 for other in actions 
                      if action_type in other.get('dependencies', []))
        
        # Ordenar acciones secuenciales por número de dependientes
        sequential_actions.sort(
            key=lambda x: (count_dependents(x['type']), -x['priority']), 
            reverse=True
        )
        
        # Optimización 4: Evitar reintentos consecutivos del mismo tipo
        retry_spacing = self._space_out_retries(actions)
        
        # Combinar en orden optimizado
        optimized = parallel_actions + sequential_actions
        
        # Aplicar espaciado de reintentos
        if retry_spacing:
            optimized = retry_spacing
        
        self.logger.debug(f"Orden optimizado: {[a['id'] for a in optimized]}")
        
        return optimized
    
    def _space_out_retries(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Espacía los reintentos para evitar sobrecargar el mismo componente"""
        
        retries = [a for a in actions if a.get('params', {}).get('is_retry', False)]
        non_retries = [a for a in actions if not a.get('params', {}).get('is_retry', False)]
        
        if len(retries) <= 1:
            return actions  # No hay necesidad de espaciado
        
        # Intercalar reintentos con acciones normales
        spaced_actions = []
        retry_index = 0
        
        for i, action in enumerate(non_retries):
            spaced_actions.append(action)
            # Insertar un reintento después de cada acción normal (si hay disponibles)
            if retry_index < len(retries):
                spaced_actions.append(retries[retry_index])
                retry_index += 1
        
        # Añadir reintentos restantes al final
        spaced_actions.extend(retries[retry_index:])
        
        return spaced_actions
    
    def _record_decision(
        self, 
        state: Dict[str, Any], 
        available_actions: List[Action], 
        selected_actions: List[Dict[str, Any]]
    ):
        """Registra la decisión para análisis posterior"""
        
        decision_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'iteration': state.get('iteration', 0),
            'available_count': len(available_actions),
            'selected_count': len(selected_actions),
            'selected_actions': [a['id'] for a in selected_actions],
            'decision_factors': {
                'completed_nodes': len(state.get('completed_nodes', [])),
                'failed_nodes': len(state.get('failed_nodes', [])),
                'recent_errors': len([e for e in state.get('error_log', []) 
                                    if e.get('iteration', 0) >= state.get('iteration', 0) - 1])
            }
        }
        
        self.decision_history.append(decision_record)
        
        # Mantener solo las últimas 50 decisiones
        if len(self.decision_history) > 50:
            self.decision_history = self.decision_history[-50:]
    
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
        
        # Verificar si hay acciones disponibles de alta prioridad
        available_actions = self._get_available_actions(completed_nodes, failed_nodes, state)
        
        high_priority_available = [
            a for a in available_actions 
            if a.priority in [ActionPriority.CRITICAL, ActionPriority.HIGH]
        ]
        
        # Calcular cobertura de análisis
        analysis_coverage = len(completed_nodes) / len(self.action_dependencies)
        
        # El workflow está completo si:
        # 1. Los nodos mínimos están completados
        # 2. No hay más acciones disponibles de alta prioridad O
        # 3. Tenemos buena cobertura de análisis (80%+)
        is_complete = (
            minimum_satisfied and 
            (len(high_priority_available) == 0 or analysis_coverage >= 0.8)
        )
        
        # También considerar completo si demasiados nodos han fallado
        failure_rate = len(failed_nodes) / len(self.action_dependencies)
        if failure_rate > 0.5:  # Más del 50% de nodos fallaron
            self.logger.warning("Marcando workflow como completo debido a alta tasa de fallos")
            is_complete = True
        
        if is_complete:
            self.logger.info("Workflow marcado como completo")
            self.logger.info(f"Nodos completados: {list(completed_nodes)}")
            self.logger.info(f"Nodos fallidos: {list(failed_nodes)}")
        
        return is_complete
    
    def get_completion_status(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene el estado de completitud del workflow"""
        
        completed_nodes = set(state.get('completed_nodes', []))
        failed_nodes = set(state.get('failed_nodes', []))
        total_nodes = len(self.action_dependencies)
        
        # Calcular métricas de completitud
        completion_percentage = len(completed_nodes) / total_nodes * 100 if total_nodes > 0 else 0
        failure_rate = len(failed_nodes) / total_nodes * 100 if total_nodes > 0 else 0
        
        # Determinar nodos pendientes
        all_nodes = set(self.action_dependencies.keys())
        pending_nodes = all_nodes - completed_nodes - failed_nodes
        
        # Evaluar calidad de la completitud
        critical_nodes = ['quality_assurance', 'plot_analysis']
        critical_completed = sum(1 for node in critical_nodes if node in completed_nodes)
        critical_completion = (critical_completed / len(critical_nodes) * 100) if critical_nodes else 100
        
        return {
            'completion_percentage': round(completion_percentage, 2),
            'failure_rate': round(failure_rate, 2),
            'critical_completion': round(critical_completion, 2),
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
        failed_nodes = set(state.get('failed_nodes', []))
        analysis_results = state.get('analysis_results', {})
        
        # Evaluar cobertura
        total_possible = len(self.action_dependencies)
        completed_count = len(completed_nodes)
        failed_count = len(failed_nodes)
        coverage = completed_count / total_possible if total_possible > 0 else 0
        
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
        
        # Penalizar por fallos
        failure_penalty = failed_count * 10  # 10 puntos de penalización por fallo
        adjusted_quality = max(0, avg_quality - failure_penalty)
        
        # Determinar calidad general
        if coverage >= 0.9 and adjusted_quality >= 80:
            return "Excellent"
        elif coverage >= 0.7 and adjusted_quality >= 70:
            return "Good"
        elif coverage >= 0.5 and adjusted_quality >= 60:
            return "Acceptable"
        elif coverage >= 0.3:
            return "Poor"
        else:
            return "Failed"
    
    def get_decision_analytics(self) -> Dict[str, Any]:
        """Obtiene analíticas de las decisiones tomadas"""
        
        if not self.decision_history:
            return {"message": "No hay historial de decisiones disponible"}
        
        total_decisions = len(self.decision_history)
        
        # Analizar patrones
        avg_actions_selected = sum(d['selected_count'] for d in self.decision_history) / total_decisions
        
        # Acciones más seleccionadas
        all_selected_actions = []
        for decision in self.decision_history:
            all_selected_actions.extend(decision['selected_actions'])
        
        from collections import Counter
        action_frequency = Counter(all_selected_actions)
        
        return {
            'total_decisions': total_decisions,
            'avg_actions_per_decision': round(avg_actions_selected, 2),
            'most_frequent_actions': action_frequency.most_common(5),
            'decision_timeline': [
                {
                    'iteration': d['iteration'],
                    'selected_count': d['selected_count'],
                    'timestamp': d['timestamp']
                }
                for d in self.decision_history[-10:]  # Últimas 10 decisiones
            ]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del motor de decisiones"""
        
        return {
            'total_action_types': len(self.action_dependencies),
            'max_concurrent_actions': self.max_concurrent_actions,
            'decision_history_length': len(self.decision_history),
            'agent_configs_loaded': len(self.agent_configs),
            'decision_rules_active': True,
            'optimization_enabled': True
        }
    
    def reset_decision_history(self):
        """Reinicia el historial de decisiones"""
        self.decision_history.clear()
        self.logger.info("Historial de decisiones reiniciado")
    
    def update_max_concurrent_actions(self, new_limit: int):
        """Actualiza el límite de acciones concurrentes"""
        if new_limit > 0:
            old_limit = self.max_concurrent_actions
            self.max_concurrent_actions = new_limit
            self.logger.info(f"Límite de acciones concurrentes actualizado de {old_limit} a {new_limit}")
        else:
            self.logger.warning("El límite de acciones concurrentes debe ser mayor a 0")
