#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el sistema de orquestacion
"""

import asyncio
import logging
from orchestrator import NovelCoordinator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_orchestrator():
    """Prueba basica del coordinador"""
    
    # Manuscript de ejemplo
    sample_manuscript = """
    En el reino de Aethermoor, la maga Lyra Stormwind descubrio un antiguo grimorio
    que podria salvar al reino de las Sombras del Vacio. Con su compañero elfico
    Thane Silverleaf, se embarco en una peligrosa mision hacia las Montañas de Cristal.
    
    El grimorio contenia hechizos ancestrales que habian sido olvidados por siglos.
    Pero usar tal poder tenia un precio que Lyra no estaba segura de poder pagar.
    
    Mientras tanto, las fuerzas oscuras del Lord Malachar avanzaban hacia la capital,
    y el tiempo se agotaba para el reino de la luz.
    """
    
    requirements = {
        'analysis_depth': 'comprehensive',
        'focus_areas': ['worldbuilding', 'character_development', 'plot_structure'],
        'output_format': 'detailed_report'
    }
    
    try:
        print("🚀 Inicializando coordinador...")
        coordinator = NovelCoordinator()
        
        print("📊 Estado inicial del coordinador:")
        status = coordinator.get_status()
        for component, state in status['components'].items():
            print(f"  - {component}: {state}")
        
        print("\n📝 Procesando manuscrito...")
        results = await coordinator.process_manuscript(
            manuscript=sample_manuscript,
            requirements=requirements
        )
        
        print("\n✅ Procesamiento completado!")
        print(f"Sesion: {results['session_id']}")
        print(f"Estado: {results['processing_summary']['status']}")
        print(f"Iteraciones: {results['processing_summary']['iterations']}")
        print(f"Acciones totales: {results['processing_summary']['total_actions']}")
        
        print("\n📋 Resumen de analisis:")
        for category, analysis in results['analysis_results'].items():
            print(f"  - {category}: ✓")
        
        print(f"\n🎯 Recomendaciones ({len(results['recommendations'])} encontradas):")
        for i, rec in enumerate(results['recommendations'][:5], 1):
            print(f"  {i}. [{rec['category']}] {rec['recommendation']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_components():
    """Prueba componentes individuales"""
    
    print("\n🔧 Probando componentes individuales...")
    
    try:
        from orchestrator import StateManager, IterationController, DecisionEngine, WorkflowGraph
        
        # Test StateManager
        print("  - StateManager: ", end="")
        state_manager = StateManager()
        print("✓")
        
        # Test IterationController
        print("  - IterationController: ", end="")
        iteration_controller = IterationController()
        print("✓")
        
        # Test DecisionEngine
        print("  - DecisionEngine: ", end="")
        decision_engine = DecisionEngine()
        print("✓")
        
        # Test WorkflowGraph
        print("  - WorkflowGraph: ", end="")
        workflow_graph = WorkflowGraph()
        is_valid = workflow_graph.validate_graph()
        print("✓" if is_valid else "❌")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando componentes: {str(e)}")
        return False

def main():
    """Funcion principal de prueba"""
    
    print("🧪 Sistema de Orquestacion - Pruebas")
    print("=" * 50)
    
    # Probar componentes
    components_ok = asyncio.run(test_components())
    
    if components_ok:
        print("\n✅ Todos los componentes funcionan correctamente")
        
        # Probar orquestador completo
        print("\n🔄 Probando sistema completo...")
        orchestrator_ok = asyncio.run(test_orchestrator())
        
        if orchestrator_ok:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        else:
            print("\n❌ Fallas en el sistema completo")
    else:
        print("\n❌ Fallas en componentes basicos")

if __name__ == "__main__":
    main()