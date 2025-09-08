velCoordinator({
            'max_iterations': 3,
            'quality_threshold': 0.75
        })
        
        # Verificar inicialización
        status = coordinator.get_status()
        assert not status['is_running']
        assert status['components']['workflow_graph']['is_valid']
        print(f"   ✅ Coordinator inicializado correctamente")
        
        # Test procesamiento completo (simulado)
        test_manuscript = """
        En el reino de Eldoria, donde la magia fluye como ríos de luz dorada, 
        un joven héroe llamado Aiden debe enfrentar al malvado hechicero Malachar.
        
        Los dragones antiguos han despertado, y solo el elegido puede reunir 
        las tres piedras del poder para restaurar el equilibrio.
        
        Con su fiel compañera Lyra y el sabio mago Eldrin, Aiden emprende 
        una épica aventura que pondrá a prueba su valor y determinación.
        
        Las fuerzas del mal se congregan en la Torre Negra, mientras que 
        nuestros héroes deben superar pruebas mortales y descubrir secretos 
        ancestrales que cambiarán el destino del reino para siempre.
        """
        
        test_requirements = {
            'genre': 'epic_fantasy',
            'target_audience': 'young_adult',
            'target_length': 80000,
            'themes': ['heroism', 'friendship', 'good_vs_evil']
        }
        
        # Ejecutar procesamiento (esto debería completarse con simulaciones)
        results = await coordinator.process_manuscript(
            manuscript=test_manuscript,
            requirements=test_requirements
        )
        
        # Verificar resultados
        assert 'session_id' in results
        assert 'processing_summary' in results
        assert 'analysis_results' in results
        assert results['processing_summary']['status'] in ['completed', 'partial_completion']
        
        print(f"   ✅ Procesamiento completado:")
        print(f"      - Sesión: {results['session_id']}")
        print(f"      - Iteraciones: {results['processing_summary']['iterations']}")
        print(f"      - Nodos completados: {results['processing_summary']['completed_nodes']}")
        print(f"      - Estado: {results['processing_summary']['status']}")
        
        # Verificar análisis generados
        if results['analysis_results']:
            print(f"      - Análisis disponibles: {list(results['analysis_results'].keys())}")
        
        # Verificar recomendaciones
        if results['recommendations']:
            print(f"      - Recomendaciones: {len(results['recommendations'])}")
        
        print(f"   ✅ Integración completa funcionando")
        
    except Exception as e:
        print(f"   ❌ Error en Coordinator: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Node Execution
    print("\n🔧 Probando Ejecución de Nodos...")
    try:
        # Test nodo individual
        from orchestrator.workflow_graph import LorekeeperNode
        
        lorekeeper = LorekeeperNode()
        test_state = {
            'manuscript': test_manuscript,
            'completed_nodes': []
        }
        
        result = await lorekeeper.execute(test_state, {})
        
        assert result.status == 'completed'
        assert 'worldbuilding_analysis' in result.data
        assert result.processing_time > 0
        
        analysis = result.data['worldbuilding_analysis']
        assert 'lore_elements' in analysis
        assert 'consistency_score' in analysis
        assert isinstance(analysis['consistency_score'], int)
        
        print(f"   ✅ Nodo Lorekeeper ejecutado correctamente")
        print(f"      - Elementos: {analysis['lore_elements']}")
        print(f"      - Puntuación: {analysis['consistency_score']}")
        print(f"      - Tiempo: {result.processing_time:.2f}s")
        
        # Test nodo con dependencias
        from orchestrator.workflow_graph import PlotWeaverNode
        
        plot_weaver = PlotWeaverNode()
        state_with_deps = {
            'manuscript': test_manuscript,
            'completed_nodes': ['lorekeeper_analysis', 'character_development'],
            'analysis_results': {
                'worldbuilding': analysis,
                'character_development': {'character_development_score': 80}
            }
        }
        
        plot_result = await plot_weaver.execute(state_with_deps, {})
        
        assert plot_result.status == 'completed'
        assert 'plot_analysis' in plot_result.data
        
        plot_analysis = plot_result.data['plot_analysis']
        assert 'structure_score' in plot_analysis
        
        print(f"   ✅ Nodo Plot Weaver ejecutado correctamente")
        print(f"      - Estructura: {plot_analysis['structure_score']}")
        print(f"      - Ritmo: {plot_analysis['pacing_rating']}")
        
    except Exception as e:
        print(f"   ❌ Error ejecutando nodos: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 7: Error Handling
    print("\n⚠️  Probando Manejo de Errores...")
    try:
        # Test con manuscrito vacío
        try:
            await coordinator.process_manuscript("", {})
            print(f"   ❌ Debería fallar con manuscrito vacío")
            return False
        except ValueError:
            print(f"   ✅ Error capturado correctamente para manuscrito vacío")
        
        # Test nodo con datos faltantes
        broken_state = {'manuscript': ''}
        result = await lorekeeper.execute(broken_state, {})
        assert result.status == 'failed'
        assert result.error is not None
        print(f"   ✅ Error de nodo manejado correctamente")
        
        # Test límite de tiempo
        from orchestrator.workflow_graph import BaseWorkflowNode, NodeType
        
        class SlowNode(BaseWorkflowNode):
            def __init__(self):
                super().__init__("test_slow", "Slow Node", NodeType.ANALYSIS, [], timeout=1)
            
            async def _execute_logic(self, state, params):
                await asyncio.sleep(2)  # Más tiempo que el timeout
                return {'data': 'should_not_reach'}
        
        slow_node = SlowNode()
        timeout_result = await slow_node.execute({'manuscript': 'test'}, {})
        assert timeout_result.status == 'timeout'
        print(f"   ✅ Timeout manejado correctamente")
        
    except Exception as e:
        print(f"   ❌ Error probando manejo de errores: {e}")
        return False
    
    # Test 8: Performance and Scalability
    print("\n⚡ Probando Rendimiento...")
    try:
        import time
        
        # Test múltiples ejecuciones
        start_time = time.time()
        
        tasks = []
        for i in range(3):
            task = lorekeeper.execute({
                'manuscript': f"Test manuscript {i} with magic and dragons",
                'completed_nodes': []
            }, {})
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        successful = sum(1 for r in results if r.status == 'completed')
        total_time = end_time - start_time
        
        print(f"   ✅ Ejecuciones paralelas completadas:")
        print(f"      - Total: {len(results)}")
        print(f"      - Exitosas: {successful}")
        print(f"      - Tiempo total: {total_time:.2f}s")
        print(f"      - Promedio por ejecución: {total_time/len(results):.2f}s")
        
        # Verificar que el paralelismo funcionó (debería ser más rápido que secuencial)
        assert total_time < sum(r.processing_time for r in results), "Paralelismo no está funcionando"
        print(f"   ✅ Paralelismo funcionando correctamente")
        
    except Exception as e:
        print(f"   ❌ Error probando rendimiento: {e}")
        return False
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    test_results = {
        'Workflow Graph': '✅ PASS',
        'State Manager': '✅ PASS',
        'Decision Engine': '✅ PASS',
        'Iteration Controller': '✅ PASS',
        'Coordinator Integration': '✅ PASS',
        'Node Execution': '✅ PASS',
        'Error Handling': '✅ PASS',
        'Performance': '✅ PASS'
    }
    
    for test_name, result in test_results.items():
        print(f"{test_name:<25} {result}")
    
    print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("🚀 El sistema orchestrator está listo para uso en producción")
    
    return True

async def test_individual_components():
    """Pruebas individuales detalladas"""
    
    print("\n🔬 PRUEBAS DETALLADAS DE COMPONENTES")
    print("=" * 50)
    
    # Test Decision Engine en detalle
    print("\n🤖 Análisis Detallado del Decision Engine...")
    
    from orchestrator.decision_engine import DecisionEngine, ActionPriority
    
    engine = DecisionEngine()
    
    # Escenario 1: Inicio limpio
    clean_state = {
        'iteration': 0,
        'completed_nodes': [],
        'failed_nodes': [],
        'analysis_results': {},
        'error_log': []
    }
    
    actions = await engine.get_next_actions(clean_state)
    print(f"   Inicio limpio: {len(actions)} acciones")
    for action in actions:
        print(f"     - {action['id']} (prioridad: {action['priority']})")
    
    # Escenario 2: Algunas completadas
    partial_state = {
        'iteration': 1,
        'completed_nodes': ['lorekeeper_analysis', 'character_development'],
        'failed_nodes': [],
        'analysis_results': {
            'worldbuilding': {'consistency_score': 85},
            'character_development': {'character_development_score': 78}
        },
        'error_log': []
    }
    
    actions = await engine.get_next_actions(partial_state)
    print(f"   Estado parcial: {len(actions)} acciones")
    for action in actions:
        print(f"     - {action['id']} (prioridad: {action['priority']})")
    
    # Escenario 3: Con errores
    error_state = {
        'iteration': 2,
        'completed_nodes': ['lorekeeper_analysis'],
        'failed_nodes': ['character_development'],
        'analysis_results': {'worldbuilding': {'consistency_score': 85}},
        'error_log': [
            {'node_id': 'character_development', 'iteration': 1},
            {'node_id': 'character_development', 'iteration': 2}
        ]
    }
    
    actions = await engine.get_next_actions(error_state)
    print(f"   Estado con errores: {len(actions)} acciones")
    for action in actions:
        retry_info = " (RETRY)" if action['params'].get('is_retry') else ""
        print(f"     - {action['id']}{retry_info} (prioridad: {action['priority']})")
    
    # Test Workflow Graph en detalle
    print("\n📊 Análisis Detallado del Workflow Graph...")
    
    from orchestrator.workflow_graph import WorkflowGraph
    
    graph = WorkflowGraph()
    
    # Análisis de dependencias
    print("   Dependencias por nodo:")
    for node_id, node in graph.nodes.items():
        deps = ", ".join(node.dependencies) if node.dependencies else "Ninguna"
        print(f"     - {node_id}: {deps}")
    
    # Análisis de paralelismo
    all_nodes = list(graph.nodes.keys())
    parallel_groups = graph.get_parallel_groups(all_nodes)
    print(f"   Grupos de paralelismo: {len(parallel_groups)}")
    for i, group in enumerate(parallel_groups):
        print(f"     - Grupo {i+1}: {group}")
    
    # Camino crítico
    critical_path = graph.get_critical_path()
    print(f"   Camino crítico: {' -> '.join(critical_path)}")
    
    # Estadísticas de nodos
    node_details = graph.get_node_details()
    print("   Detalles de nodos:")
    for node_id, details in node_details.items():
        parallel = "Sí" if details['parallel_safe'] else "No"
        required = "Sí" if details['required'] else "No"
        print(f"     - {details['name']}:")
        print(f"       * Tipo: {details['type']}")
        print(f"       * Paralelo: {parallel}")
        print(f"       * Requerido: {required}")
        print(f"       * Timeout: {details['timeout']}s")

def main():
    """Función principal"""
    print("🔧 Iniciando pruebas del sistema Orchestrator...")
    
    try:
        # Ejecutar pruebas principales
        success = asyncio.run(test_orchestrator())
        
        if success:
            # Ejecutar pruebas detalladas
            asyncio.run(test_individual_components())
            
            print("\n" + "=" * 70)
            print("🏆 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
            print("📈 Sistema Orchestrator validado y listo para producción")
            print("=" * 70)
            return 0
        else:
            print("\n❌ ALGUNAS PRUEBAS FALLARON")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Pruebas interrumpidas por el usuario")
        return 1
    except Exception as e:
        print(f"\n💥 Error crítico en pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPresiona Enter para continuar...")
    sys.exit(exit_code)
