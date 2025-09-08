'Strong' if style_consistency >= 80 else 'Developing',
            'prose_quality': prose_quality,
            'dialogue_quality': min(85, prose_quality - 5),  # Slightly lower than prose
            'average_sentence_length': round(avg_sentence_length, 1),
            'vocabulary_richness': round(vocabulary_richness, 1),
            'readability_score': min(90, int(prose_quality * 0.9)),
            'recommendations': [
                'Vary sentence structure for better rhythm' if avg_sentence_length < 10 or avg_sentence_length > 25 else 'Maintain current sentence variety',
                'Strengthen character voices in dialogue',
                'Consider more vivid and specific word choices'
            ][:2]
        }
        
        return {
            'style_analysis': analysis,
            'node_id': self.id,
            'status': 'completed'
        }

class VisualizerNode(BaseWorkflowNode):
    """Nodo para generación de contenido visual"""
    
    def __init__(self):
        super().__init__(
            node_id="visual_generation",
            name="Generación Visual",
            node_type=NodeType.GENERATION,
            dependencies=["lorekeeper_analysis", "character_development", "plot_analysis"],
            parallel_safe=False,
            timeout=120
        )
    
    async def _execute_logic(self, state: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Genera prompts visuales basados en el análisis"""
        # Obtener datos de análisis previos
        worldbuilding = self._get_dependency_data(state, 'lorekeeper_analysis')
        characters = self._get_dependency_data(state, 'character_development')
        plot = self._get_dependency_data(state, 'plot_analysis')
        
        await asyncio.sleep(0.8)
        
        # Generar prompts basados en análisis
        character_prompts = []
        scene_prompts = []
        world_prompts = []
        
        # Prompts de personajes basados en análisis
        if characters and characters.get('characters_identified'):
            for char in characters['characters_identified'][:3]:  # Limitar a 3 principales
                if char.lower() == 'protagonist':
                    character_prompts.append('Epic fantasy protagonist with determined expression, detailed character design')
                elif char.lower() == 'antagonist':
                    character_prompts.append('Dark fantasy antagonist with mysterious aura, intricate villain design')
                else:
                    character_prompts.append(f'{char} character with distinctive features, fantasy art style')
        
        # Prompts de mundo basados en worldbuilding
        if worldbuilding and worldbuilding.get('lore_elements'):
            for element in worldbuilding['lore_elements'][:3]:
                if element == 'Magic System':
                    world_prompts.append('Magical library with floating tomes and ethereal light')
                    scene_prompts.append('Wizard casting spell with glowing magical effects')
                elif element == 'Geography':
                    world_prompts.append('Sweeping fantasy landscape with mountains and mystical atmosphere')
                    scene_prompts.append('Fantasy kingdom vista from high vantage point')
                elif element == 'History':
                    world_prompts.append('Ancient ruins with historical significance and atmospheric lighting')
                    scene_prompts.append('Historical battle scene with epic scope')
        
        # Prompts por defecto si no hay suficiente análisis
        if not character_prompts:
            character_prompts = ['Fantasy protagonist with heroic bearing', 'Mysterious antagonist figure']
        
        if not scene_prompts:
            scene_prompts = ['Epic fantasy battle scene', 'Mystical forest encounter']
        
        if not world_prompts:
            world_prompts = ['Fantasy realm with twin moons', 'Enchanted castle on hillside']
        
        # Determinar mood boards basado en el tono
        mood_boards = ['Epic Fantasy', 'Heroic Adventure']
        if plot and 'dark' in str(plot).lower():
            mood_boards.append('Dark Fantasy')
        if worldbuilding and 'magic' in str(worldbuilding).lower():
            mood_boards.append('Magical Realism')
        
        visual_content = {
            'character_prompts': character_prompts[:4],  # Máximo 4
            'scene_prompts': scene_prompts[:4],
            'world_prompts': world_prompts[:4],
            'mood_boards': mood_boards[:4],
            'style_tags': ['fantasy art', 'detailed illustration', 'cinematic lighting'],
            'generation_metadata': {
                'based_on_worldbuilding': bool(worldbuilding),
                'based_on_characters': bool(characters),
                'based_on_plot': bool(plot),
                'total_prompts': len(character_prompts) + len(scene_prompts) + len(world_prompts)
            }
        }
        
        return {
            'visual_content': visual_content,
            'node_id': self.id,
            'status': 'completed'
        }

class QualityAssuranceNode(BaseWorkflowNode):
    """Nodo para control de calidad final"""
    
    def __init__(self):
        super().__init__(
            node_id="quality_assurance",
            name="Control de Calidad",
            node_type=NodeType.VALIDATION,
            dependencies=["style_refinement", "plot_analysis"],
            parallel_safe=False,
            required=True,
            timeout=180
        )
    
    async def _execute_logic(self, state: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta control de calidad final"""
        manuscript = state.get('manuscript', '')
        
        if not manuscript:
            raise ValueError("Manuscrito vacío para control de calidad")
        
        await asyncio.sleep(1.5)
        
        # Consolidar todos los análisis previos
        all_analyses = state.get('analysis_results', {})
        
        # Calcular puntuación general
        scores = []
        weights = {
            'worldbuilding': 0.2,
            'character_development': 0.25,
            'plot_structure': 0.3,
            'style_refinement': 0.25
        }
        
        weighted_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in all_analyses:
                analysis_data = all_analyses[category]
                # Buscar puntuación en el análisis
                score_keys = ['consistency_score', 'structure_score', 'character_development_score', 'style_consistency']
                for key in score_keys:
                    if key in analysis_data:
                        scores.append(analysis_data[key])
                        weighted_score += analysis_data[key] * weight
                        total_weight += weight
                        break
        
        # Calcular puntuación final
        if total_weight > 0:
            overall_score = int(weighted_score / total_weight)
        else:
            overall_score = 70  # Puntuación por defecto
        
        # Evaluación técnica (gramática, estructura, etc.)
        word_count = len(manuscript.split())
        technical_quality = min(95, 75 + (10 if word_count > 10000 else 5))
        
        # Evaluación narrativa basada en análisis disponibles
        narrative_quality = overall_score
        
        # Puntuación de consistencia
        consistency_scores = []
        for analysis in all_analyses.values():
            if isinstance(analysis, dict) and 'consistency_score' in analysis:
                consistency_scores.append(analysis['consistency_score'])
        
        consistency_score = sum(consistency_scores) // len(consistency_scores) if consistency_scores else 80
        
        # Determinar estado de preparación
        if overall_score >= 85:
            readiness = "Excellent - Ready for publication"
        elif overall_score >= 75:
            readiness = "Good - Minor improvements recommended"
        elif overall_score >= 65:
            readiness = "Acceptable - Some improvements needed"
        else:
            readiness = "Needs significant improvement"
        
        # Identificar problemas críticos
        critical_issues = []
        if overall_score < 60:
            critical_issues.append("Overall quality below acceptable threshold")
        if consistency_score < 70:
            critical_issues.append("Consistency issues detected")
        if word_count < 5000:
            critical_issues.append("Manuscript may be too short")
        
        # Areas de mejora basadas en análisis
        improvement_areas = []
        if 'character_development' in all_analyses:
            char_score = all_analyses['character_development'].get('character_development_score', 80)
            if char_score < 75:
                improvement_areas.append("Character development depth")
        
        if 'plot_structure' in all_analyses:
            plot_score = all_analyses['plot_structure'].get('structure_score', 80)
            if plot_score < 75:
                improvement_areas.append("Plot structure and pacing")
        
        if 'style_refinement' in all_analyses:
            style_score = all_analyses['style_refinement'].get('style_consistency', 80)
            if style_score < 75:
                improvement_areas.append("Writing style consistency")
        
        # Identificar fortalezas
        strengths = []
        if 'worldbuilding' in all_analyses:
            wb_score = all_analyses['worldbuilding'].get('consistency_score', 0)
            if wb_score >= 80:
                strengths.append("Strong worldbuilding foundation")
        
        if consistency_score >= 85:
            strengths.append("Excellent narrative consistency")
        
        if technical_quality >= 85:
            strengths.append("High technical writing quality")
        
        if not strengths:
            strengths = ["Solid narrative foundation", "Clear writing voice"]
        
        quality_report = {
            'overall_score': overall_score,
            'technical_quality': technical_quality,
            'narrative_quality': narrative_quality,
            'consistency_score': consistency_score,
            'readiness': readiness,
            'word_count': word_count,
            'analyses_reviewed': len(all_analyses),
            'critical_issues': critical_issues,
            'improvement_areas': improvement_areas[:4],  # Limitar a 4 principales
            'strengths': strengths[:4],  # Limitar a 4 principales
            'quality_breakdown': {
                'plot': all_analyses.get('plot_structure', {}).get('structure_score', 'N/A'),
                'characters': all_analyses.get('character_development', {}).get('character_development_score', 'N/A'),
                'worldbuilding': all_analyses.get('worldbuilding', {}).get('consistency_score', 'N/A'),
                'style': all_analyses.get('style_refinement', {}).get('style_consistency', 'N/A')
            }
        }
        
        return {
            'quality_report': quality_report,
            'node_id': self.id,
            'status': 'completed'
        }

class WorkflowGraph:
    """Grafo de flujo de trabajo que define la lógica de ejecución"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nodes: Dict[str, BaseWorkflowNode] = {}
        self.edges: Dict[str, List[str]] = {}
        self.execution_stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'avg_execution_time': 0
        }
        self._initialize_graph()
    
    def _initialize_graph(self):
        """Inicializa el grafo con todos los nodos y conexiones"""
        
        try:
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
            
            # Validar grafo
            if not self._validate_graph_integrity():
                raise ValueError("Grafo inválido detectado durante inicialización")
            
            self.logger.info(f"Grafo inicializado con {len(self.nodes)} nodos")
            
        except Exception as e:
            self.logger.error(f"Error inicializando grafo: {str(e)}")
            raise
    
    def _build_dependency_graph(self):
        """Construye el grafo de dependencias basado en los nodos"""
        self.edges = {}
        
        for node_id, node in self.nodes.items():
            self.edges[node_id] = node.dependencies.copy()
        
        # Log del grafo para debugging
        self.logger.debug("Grafo de dependencias construido:")
        for node_id, deps in self.edges.items():
            self.logger.debug(f"  {node_id} -> {deps}")
    
    def _validate_graph_integrity(self) -> bool:
        """Valida la integridad del grafo completo"""
        try:
            # Verificar que todos los nodos tengan IDs únicos
            node_ids = [node.id for node in self.nodes.values()]
            if len(node_ids) != len(set(node_ids)):
                self.logger.error("IDs de nodos duplicados detectados")
                return False
            
            # Verificar que todas las dependencias existan
            for node_id, dependencies in self.edges.items():
                for dep in dependencies:
                    if dep not in self.nodes:
                        self.logger.error(f"Dependencia inexistente: {dep} para nodo {node_id}")
                        return False
            
            # Verificar que no haya ciclos
            if self._has_cycles():
                self.logger.error("Ciclos detectados en el grafo")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando integridad del grafo: {str(e)}")
            return False
    
    def _has_cycles(self) -> bool:
        """Detecta ciclos en el grafo usando DFS"""
        visited = set()
        rec_stack = set()
        
        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for neighbor in self.edges.get(node_id, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node_id)
            return False
        
        for node_id in self.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    return True
        
        return False
    
    def get_executable_nodes(self, completed_nodes: List[str]) -> List[str]:
        """
        Obtiene los nodos que pueden ejecutarse basado en dependencias completadas
        """
        executable = []
        completed_set = set(completed_nodes)
        
        for node_id, dependencies in self.edges.items():
            # Si el nodo ya fue completado, saltar
            if node_id in completed_set:
                continue
            
            # Verificar si todas las dependencias están completadas
            if all(dep in completed_set for dep in dependencies):
                executable.append(node_id)
        
        return executable
    
    def get_parallel_groups(self, executable_nodes: List[str]) -> List[List[str]]:
        """
        Agrupa nodos ejecutables en grupos que pueden ejecutarse en paralelo
        """
        if not executable_nodes:
            return []
        
        parallel_groups = []
        sequential_nodes = []
        
        for node_id in executable_nodes:
            node = self.nodes.get(node_id)
            if not node:
                continue
                
            if node.parallel_safe:
                # Verificar que no haya dependencias cruzadas con otros nodos del grupo
                added_to_group = False
                for group in parallel_groups:
                    # Verificar compatibilidad con el grupo existente
                    if not any(dep in group for dep in node.dependencies):
                        # Verificar que ningún nodo del grupo dependa de este nodo
                        group_nodes = [self.nodes.get(gn) for gn in group]
                        if not any(gn and node_id in gn.dependencies for gn in group_nodes):
                            group.append(node_id)
                            added_to_group = True
                            break
                
                if not added_to_group:
                    parallel_groups.append([node_id])
            else:
                sequential_nodes.append([node_id])
        
        return parallel_groups + sequential_nodes
    
    def get_node(self, node_id: str) -> Optional[BaseWorkflowNode]:
        """Obtiene un nodo por su ID"""
        return self.nodes.get(node_id)
    
    def validate_graph(self) -> bool:
        """Valida que el grafo sea válido (método público)"""
        return self._validate_graph_integrity()
    
    def get_topology_sort(self) -> List[str]:
        """Obtiene ordenamiento topológico de los nodos"""
        in_degree = {node_id: 0 for node_id in self.nodes}
        
        # Calcular grados de entrada
        for node_id, dependencies in self.edges.items():
            for dep in dependencies:
                if dep in in_degree:
                    in_degree[node_id] += 1
        
        # Cola de nodos sin dependencias
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            # Reducir grado de entrada de nodos dependientes
            for node_id, dependencies in self.edges.items():
                if current in dependencies:
                    in_degree[node_id] -= 1
                    if in_degree[node_id] == 0:
                        queue.append(node_id)
        
        return result if len(result) == len(self.nodes) else []
    
    def get_critical_path(self) -> List[str]:
        """Obtiene el camino crítico basado en duración estimada"""
        # Implementación simplificada - en un caso real usaríamos algoritmo CPM
        topo_order = self.get_topology_sort()
        if not topo_order:
            return []
        
        # Calcular tiempo más largo a cada nodo
        longest_time = {}
        longest_path = {}
        
        for node_id in topo_order:
            node = self.nodes.get(node_id)
            if not node:
                continue
                
            node_duration = getattr(node, 'timeout', 300)  # Usar timeout como estimación
            
            if not node.dependencies:
                longest_time[node_id] = node_duration
                longest_path[node_id] = [node_id]
            else:
                max_prev_time = 0
                best_prev_node = None
                
                for dep in node.dependencies:
                    if dep in longest_time and longest_time[dep] > max_prev_time:
                        max_prev_time = longest_time[dep]
                        best_prev_node = dep
                
                longest_time[node_id] = max_prev_time + node_duration
                if best_prev_node:
                    longest_path[node_id] = longest_path[best_prev_node] + [node_id]
                else:
                    longest_path[node_id] = [node_id]
        
        # Encontrar el nodo con el tiempo más largo
        if longest_time:
            critical_node = max(longest_time.keys(), key=lambda x: longest_time[x])
            return longest_path.get(critical_node, [])
        
        return []
    
    def update_execution_stats(self, node_id: str, success: bool, execution_time: float):
        """Actualiza estadísticas de ejecución"""
        self.execution_stats['total_executions'] += 1
        
        if success:
            self.execution_stats['successful_executions'] += 1
        else:
            self.execution_stats['failed_executions'] += 1
        
        # Actualizar tiempo promedio
        total_time = (self.execution_stats['avg_execution_time'] * 
                     (self.execution_stats['total_executions'] - 1) + execution_time)
        self.execution_stats['avg_execution_time'] = total_time / self.execution_stats['total_executions']
    
    def reset_stats(self):
        """Reinicia las estadísticas de ejecución"""
        self.execution_stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'avg_execution_time': 0
        }
        self.logger.info("Estadísticas de ejecución reiniciadas")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del grafo"""
        success_rate = 0
        if self.execution_stats['total_executions'] > 0:
            success_rate = (self.execution_stats['successful_executions'] / 
                          self.execution_stats['total_executions'] * 100)
        
        critical_path = self.get_critical_path()
        
        return {
            'nodes_count': len(self.nodes),
            'is_valid': self.validate_graph(),
            'has_cycles': self._has_cycles(),
            'node_types': {
                node_type.value: len([n for n in self.nodes.values() if n.node_type == node_type])
                for node_type in NodeType
            },
            'execution_stats': self.execution_stats.copy(),
            'success_rate': round(success_rate, 2),
            'critical_path': critical_path,
            'critical_path_length': len(critical_path),
            'topology_valid': len(self.get_topology_sort()) == len(self.nodes)
        }
    
    def get_node_details(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene detalles de todos los nodos"""
        details = {}
        
        for node_id, node in self.nodes.items():
            details[node_id] = {
                'name': node.name,
                'type': node.node_type.value,
                'dependencies': node.dependencies,
                'parallel_safe': node.parallel_safe,
                'required': node.required,
                'timeout': node.timeout
            }
        
        return details
