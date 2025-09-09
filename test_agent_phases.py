
        agent_manager.set_manuscript(character_manuscript)
        
        print("📝 Probando desarrollo de personajes con manuscrito específico...")
        
        # Test directo del método que estaba faltando
        try:
            result = await agent_manager.run_analysis_phase_async("character_development")
            
            if result.get('success', False):
                print("✅ Desarrollo de personajes ejecutado exitosamente")
                
                # Analizar resultados específicos
                if 'results' in result:
                    results = result['results']
                    
                    # Verificar análisis de personajes
                    if 'character_development' in results:
                        char_data = results['character_development']
                        print(f"   🎭 Datos de personajes encontrados")
                        
                        if isinstance(char_data, dict):
                            for key, value in char_data.items():
                                if isinstance(value, (str, int, float)):
                                    print(f"      - {key}: {value}")
                    
                    # Verificar feedback del beta reader
                    if 'reader_feedback' in results:
                        print(f"   📖 Feedback de beta reader disponible")
                    
                    # Verificar consistencia de personajes
                    if 'character_consistency' in results:
                        print(f"   🔍 Análisis de consistencia realizado")
                
                print(f"   🤖 Agentes involucrados: {result.get('agents_involved', [])}")
                
                return True
            else:
                error = result.get('error', 'Error desconocido')
                print(f"❌ Error en desarrollo de personajes: {error}")
                return False
                
        except Exception as e:
            print(f"💥 Excepción en desarrollo de personajes: {str(e)}")
            # Mostrar más detalles del error
            import traceback
            traceback.print_exc()
            return False
    
    except Exception as e:
        print(f"💥 Error inicializando test de personajes: {str(e)}")
        return False

def create_agent_diagnostic():
    """Crea un diagnóstico detallado de los agentes"""
    
    print("\n🔬 DIAGNÓSTICO DETALLADO DE AGENTES")
    print("=" * 50)
    
    try:
        from agents.agent_manager import AgentManager
        from agents.crews import (
            LorekeeperAgent, CharacterDeveloperAgent, PlotWeaverAgent,
            StyleEditorAgent, VisualizerAgent, ResearcherAgent,
            ContinuityAuditorAgent, BetaReaderAgent, PacingSpecialistAgent,
            ProofreaderAgent, InnovationScoutAgent
        )
        
        print("📦 Verificando importaciones de agentes...")
        
        agent_classes = {
            'LorekeeperAgent': LorekeeperAgent,
            'CharacterDeveloperAgent': CharacterDeveloperAgent,
            'PlotWeaverAgent': PlotWeaverAgent,
            'StyleEditorAgent': StyleEditorAgent,
            'VisualizerAgent': VisualizerAgent,
            'ResearcherAgent': ResearcherAgent,
            'ContinuityAuditorAgent': ContinuityAuditorAgent,
            'BetaReaderAgent': BetaReaderAgent,
            'PacingSpecialistAgent': PacingSpecialistAgent,
            'ProofreaderAgent': ProofreaderAgent,
            'InnovationScoutAgent': InnovationScoutAgent
        }
        
        successful_imports = 0
        for name, agent_class in agent_classes.items():
            try:
                # Verificar que la clase existe y es importable
                assert callable(agent_class)
                print(f"   ✅ {name}")
                successful_imports += 1
            except Exception as e:
                print(f"   ❌ {name}: {e}")
        
        print(f"\n📊 Clases importadas: {successful_imports}/{len(agent_classes)}")
        
        # Test de inicialización individual
        print("\n🧪 Probando inicialización individual de agentes...")
        
        initialization_results = {}
        
        for name, agent_class in agent_classes.items():
            try:
                agent = agent_class(llm=None)  # Sin LLM para test
                print(f"   ✅ {name}: Inicializado correctamente")
                initialization_results[name] = True
                
                # Verificar métodos disponibles
                methods = [method for method in dir(agent) if not method.startswith('_')]
                print(f"      📋 Métodos disponibles: {len(methods)}")
                
            except Exception as e:
                print(f"   ❌ {name}: Error - {str(e)}")
                initialization_results[name] = False
        
        successful_init = sum(initialization_results.values())
        print(f"\n📊 Agentes inicializados: {successful_init}/{len(agent_classes)}")
        
        # Test de AgentManager
        print("\n🏗️ Probando AgentManager...")
        
        try:
            agent_manager = AgentManager()
            agents_list = agent_manager.list_agents()
            agent_status = agent_manager.get_agent_status()
            
            print(f"   ✅ AgentManager inicializado")
            print(f"   📊 Agentes en manager: {len(agents_list)}")
            
            # Detalles de cada agente en el manager
            for agent_name in agents_list:
                agent = agent_manager.get_agent(agent_name)
                status = agent_status.get(agent_name, False)
                status_icon = "✅" if status else "❌"
                
                print(f"      {status_icon} {agent_name}: {'Disponible' if status else 'Mock/Error'}")
                
                # Si es mock, mostrar el error
                if hasattr(agent, 'error'):
                    print(f"         ⚠️  Error: {agent.error}")
            
            return successful_init >= len(agent_classes) * 0.7  # 70% éxito mínimo
            
        except Exception as e:
            print(f"   ❌ Error en AgentManager: {str(e)}")
            return False
    
    except Exception as e:
        print(f"💥 Error en diagnóstico: {str(e)}")
        return False

def main():
    """Función principal del test de fases"""
    
    print("🚀 INICIANDO TEST ESPECÍFICO DE FASES DE AGENTES")
    print("=" * 70)
    
    try:
        # 1. Diagnóstico de agentes
        print("PASO 1: Diagnóstico de agentes")
        diagnostic_success = create_agent_diagnostic()
        
        if not diagnostic_success:
            print("⚠️  Problemas detectados en agentes - continuando con tests limitados")
        
        # 2. Test específico de desarrollo de personajes
        print("\nPASO 2: Test específico de desarrollo de personajes")
        character_success = asyncio.run(test_character_development_specific())
        
        # 3. Test completo de todas las fases
        print("\nPASO 3: Test completo de fases")
        phases_success = asyncio.run(test_agent_phases())
        
        # Resumen final
        print("\n" + "=" * 70)
        print("🏁 RESUMEN FINAL")
        print("=" * 70)
        
        tests = [
            ("Diagnóstico de Agentes", diagnostic_success),
            ("Desarrollo de Personajes", character_success), 
            ("Test Completo de Fases", phases_success)
        ]
        
        passed_tests = sum(1 for _, success in tests if success)
        total_tests = len(tests)
        
        for test_name, success in tests:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{status} {test_name}")
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"\n📊 RESULTADO: {passed_tests}/{total_tests} tests pasados ({success_rate:.1f}%)")
        
        if success_rate >= 100:
            print("🎉 ¡PERFECTO! Todas las fases funcionan correctamente")
            print("🚀 Sistema listo para uso en producción")
        elif success_rate >= 66:
            print("✅ ¡BUENO! Sistema mayormente funcional")
            print("🎯 Listo para uso con limitaciones menores")
        elif success_rate >= 33:
            print("⚠️  REGULAR - Sistema parcialmente funcional")
            print("🔧 Requiere correcciones para uso completo")
        else:
            print("❌ CRÍTICO - Sistema requiere atención inmediata")
            print("🛠️  Revisar configuración y dependencias")
        
        # Recomendaciones finales
        print(f"\n💡 RECOMENDACIONES FINALES:")
        
        if not diagnostic_success:
            print("   🔧 Revisar inicialización de agentes individuales")
            print("   📦 Verificar dependencias de CrewAI y herramientas")
        
        if not character_success:
            print("   🎭 Revisar método _run_character_analysis en AgentManager")
            print("   🔍 Verificar integración de CharacterDeveloperAgent")
        
        if not phases_success:
            print("   📊 Revisar ejecución asíncrona de fases")
            print("   ⏱️  Optimizar timeouts y manejo de errores")
        
        if all(success for _, success in tests):
            print("   🎯 Sistema funcionando perfectamente")
            print("   🚀 Proceder con uso completo del sistema")
        
        return success_rate >= 66
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n💥 Error crítico en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        
        print(f"\n{'='*50}")
        print("🏁 Test de fases completado")
        print(f"{'='*50}")
        
        input("\nPresiona Enter para continuar...")
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"\n💥 Error ejecutando test: {e}")
        input("\nPresiona Enter para continuar...")
        sys.exit(1)
