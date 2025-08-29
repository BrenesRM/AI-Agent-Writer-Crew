#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el coordinador con LangGraph
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# Agregar paths
sys.path.append(str(Path(__file__).parent))

def test_coordinator_creation():
    """Probar la creación del coordinador"""
    print("=== PROBANDO CREACIÓN DEL COORDINADOR ===\n")
    
    try:
        from orchestrator.story_coordinator import StoryEnhancementCoordinator
        
        print("1. Creando coordinador básico...")
        coordinator = StoryEnhancementCoordinator(
            max_iterations=2,
            convergence_threshold=0.8,
            enable_checkpoints=False  # Deshabilitado para pruebas simples
        )
        print("   ? Coordinador creado exitosamente")
        
        print("2. Verificando configuración...")
        print(f"   Max iteraciones: {coordinator.max_iterations}")
        print(f"   Umbral convergencia: {coordinator.convergence_threshold}")
        print(f"   Checkpoints: {'Habilitados' if coordinator.enable_checkpoints else 'Deshabilitados'}")
        
        print("3. Verificando grafo...")
        if coordinator.graph:
            print("   ? Grafo creado correctamente")
            
            # Intentar obtener visualización
            try:
                viz = coordinator.get_graph_visualization()
                print(f"   ?? Visualización disponible: {len(viz)} caracteres")
            except Exception as e:
                print(f"   ?? Visualización no disponible: {e}")
        else:
            print("   ? Grafo no creado")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ? Error creando coordinador: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_state_models():
    """Probar los modelos de estado"""
    print("=== PROBANDO MODELOS DE ESTADO ===\n")
    
    try:
        from orchestrator.state_models import (
            create_initial_state, StoryEnhancementState, 
            ProcessingPhase, get_state_summary
        )
        
        print("1. Creando estado inicial...")
        test_manuscript = "Había una vez en un reino lejano..."
        
        state = create_initial_state(
            manuscript_content=test_manuscript,
            session_id="test_session",
            max_iterations=3
        )
        
        print(f"   ? Estado creado con session_id: {state['session_id']}")
        print(f"   ?? Manuscrito: {len(state['manuscript_content'])} caracteres")
        print(f"   ?? Max iteraciones: {state['max_iterations']}")
        
        print("2. Verificando estructura del estado...")
        required_keys = [
            'session_id', 'current_phase', 'manuscript_content',
            'current_iteration', 'agent_results', 'should_continue'
        ]
        
        for key in required_keys:
            if key in state:
                print(f"   ? {key}")
            else:
                print(f"   ? {key} - FALTANTE")
        
        print("3. Probando resumen del estado...")
        summary = get_state_summary(state)
        print("   ?? Resumen generado:")
        print("   " + "\n   ".join(summary.split('\n')[:5]))
        
        return True
        
    except Exception as e:
        print(f"   ? Error probando modelos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_nodes():
    """Probar nodos individuales del grafo"""
    print("=== PROBANDO NODOS INDIVIDUALES ===\n")
    
    try:
        from orchestrator.state_models import create_initial_state
        from orchestrator.graph_nodes import (
            initialize_system, ingest_documents, load_manuscript
        )
        
        # Crear estado de prueba
        test_manuscript = """
        En el reino de Aethermoor, la magia es poder y el poder es responsabilidad.
        El príncipe Marcus debe aprender esta lección antes de que sea demasiado tarde.
        Los Corruptores acechan en las sombras, esperando su momento.
        """
        
        state = create_initial_state(
            manuscript_content=test_manuscript,
            session_id="node_test",
            max_iterations=2
        )
        
        print("1. Probando nodo de inicialización...")
        state = initialize_system(state)
        if state["current_phase"].value == "initialization" or state["current_phase"].value == "rag_ingestion":
            print("   ? Inicialización exitosa")
        else:
            print(f"   ?? Fase inesperada: {state['current_phase'].value}")
        
        print("2. Probando nodo de ingesta RAG...")
        state = ingest_documents(state)
        if "rag_ingestion" in str(state["current_phase"].value) or "manuscript_loading" in str(state["current_phase"].value):
            print("   ? Ingesta completada")
            print(f"   ?? Documentos procesados: {state['documents_processed']}")
        else:
            print(f"   ?? Fase inesperada: {state['current_phase'].value}")
        
        print("3. Probando carga de manuscrito...")
        state = load_manuscript(state)
        if state["current_phase"].value == "agent_analysis":
            print("   ? Manuscrito cargado, listo para análisis")
            print(f"   ?? Iteración actual: {state['current_iteration']}")
        else:
            print(f"   ?? Fase inesperada: {state['current_phase'].value}")
        
        return True
        
    except Exception as e:
        print(f"   ? Error probando nodos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_workflow():
    """Probar flujo completo con manuscrito simple"""
    print("=== PROBANDO FLUJO COMPLETO ===\n")
    
    try:
        from orchestrator.story_coordinator import enhance_story_simple
        
        # Manuscrito de prueba
        test_manuscript = """
        # El Reino Perdido
        
        En las tierras de Valdris, donde los dragones una vez surcaron los cielos,
        una joven llamada Elara descubrió un secreto que cambiaría su destino.
        
        El amuleto de su abuela brillaba con una luz extraña cada vez que la luna
        estaba llena. Esa noche, siguiendo su resplandor, Elara se adentró en el
        bosque prohibido.
        
        Allí encontró las ruinas de un antiguo templo, donde una voz le susurró
        al oído: "Eres la elegida, la última guardiana de la magia ancestral."
        
        Pero los Cazadores de Sombras ya habían detectado el despertar de su poder.
        La cacería había comenzado.
        """
        
        print("?? Procesando manuscrito de prueba...")
        print(f"   ?? Longitud: {len(test_manuscript)} caracteres")
        print(f"   ?? Palabras: {len(test_manuscript.split())} aproximadamente")
        
        print("\n?? Iniciando procesamiento completo...")
        results = enhance_story_simple(
            manuscript_content=test_manuscript,
            max_iterations=2  # Solo 2 iteraciones para prueba rápida
        )
        
        print("\n?? RESULTADOS DEL PROCESAMIENTO:")
        print("=" * 40)
        
        if results["success"]:
            print("? PROCESAMIENTO EXITOSO")
            
            stats = results["processing_stats"]
            print(f"\n?? ESTADÍSTICAS:")
            print(f"   Iteraciones completadas: {stats['total_iterations']}")
            print(f"   Documentos procesados: {stats['documents_processed']}")
            print(f"   Agentes ejecutados: {stats['agents_executed']}")
            print(f"   Fase final: {stats['final_phase']}")
            print(f"   Convergencia: {'Sí' if stats['convergence_achieved'] else 'No'}")
            
            print(f"\n?? ANÁLISIS DE AGENTES:")
            for agent, analysis in results["agent_analyses"].items():
                print(f"   {agent}:")
                print(f"     Estado: {analysis['status']}")
                print(f"     Confianza: {analysis['confidence_score']:.2f}")
                print(f"     Contenido: {analysis['content_length']} caracteres")
            
            print(f"\n?? ARCHIVOS GENERADOS ({len(results['generated_files'])}):")
            for file_path in results["generated_files"]:
                if Path(file_path).exists():
                    size = Path(file_path).stat().st_size
                    print(f"   ? {file_path} ({size} bytes)")
                else:
                    print(f"   ? {file_path} - NO ENCONTRADO")
            
            if results["convergence_history"]:
                print(f"\n?? HISTORIAL DE CONVERGENCIA:")
                for conv in results["convergence_history"]:
                    print(f"   Iteración {conv['iteration']}: {conv['score']:.2f} ? {conv['decision']}")
            
        else:
            print("? PROCESAMIENTO FALLÓ")
            print(f"Error: {results.get('error', 'No especificado')}")
        
        # Mostrar errores y advertencias
        if results.get("errors"):
            print(f"\n?? ERRORES ({len(results['errors'])}):")
            for error in results["errors"]:
                print(f"   • {error}")
        
        if results.get("warnings"):
            print(f"\n?? ADVERTENCIAS ({len(results['warnings'])}):")
            for warning in results["warnings"]:
                print(f"   • {warning}")
        
        return results["success"]
        
    except Exception as e:
        print(f"   ? Error en flujo completo: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Verificar dependencias específicas para LangGraph"""
    print("=== VERIFICANDO DEPENDENCIAS LANGGRAPH ===\n")
    
    required_packages = [
        ('langgraph', 'LangGraph para orquestación'),
        ('langsmith', 'LangSmith para trazabilidad'),
        ('sqlite3', 'SQLite para checkpoints'),
        ('crewai', 'CrewAI para agentes'),
        ('langchain', 'LangChain base'),
        ('chromadb', 'ChromaDB para RAG')
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                __import__(package.replace('-', '_'))
            print(f"   ? {package} - {description}")
        except ImportError:
            print(f"   ? {package} - {description} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n?? Paquetes faltantes: {', '.join(missing_packages)}")
        print("Instala con:")
        print("pip install " + " ".join(missing_packages))
        return False
    else:
        print("\n? Todas las dependencias están disponibles")
        return True

def test_checkpoint_functionality():
    """Probar funcionalidad de checkpoints"""
    print("=== PROBANDO CHECKPOINTS ===\n")
    
    try:
        from orchestrator.graph_nodes import create_state_checkpoint
        from orchestrator.state_models import create_initial_state
        
        # Crear estado de prueba
        state = create_initial_state("Manuscrito de prueba", "checkpoint_test")
        
        print("1. Creando checkpoint...")
        create_state_checkpoint(state, "test_checkpoint")
        
        # Verificar que se creó el archivo
        checkpoint_file = Path("outputs/checkpoints/test_checkpoint.json")
        if checkpoint_file.exists():
            print("   ? Archivo de checkpoint creado")
            
            # Leer y verificar contenido
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            print(f"   ?? Session ID: {checkpoint_data['session_id']}")
            print(f"   ?? Timestamp: {checkpoint_data['timestamp']}")
            print(f"   ?? Manuscrito: {checkpoint_data['manuscript_length']} caracteres")
            
            return True
        else:
            print("   ? Archivo de checkpoint no encontrado")
            return False
            
    except Exception as e:
        print(f"   ? Error probando checkpoints: {e}")
        return False

def clean_test_outputs():
    """Limpiar archivos de prueba"""
    print("=== LIMPIANDO ARCHIVOS DE PRUEBA ===\n")
    
    test_files = [
        "outputs/novel/enhanced_story.md",
        "outputs/library/story_library.json", 
        "outputs/characters/character_guide.md",
        "outputs/prompts/video_prompts.json",
        "outputs/error_report.md",
        "outputs/checkpoints/test_checkpoint.json",
        "outputs/checkpoints/initial_state.json",
        "outputs/checkpoints/final_state.json"
    ]
    
    removed_count = 0
    for file_path in test_files:
        path = Path(file_path)
        if path.exists():
            try:
                path.unlink()
                print(f"   ??? Eliminado: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"   ? No se pudo eliminar {file_path}: {e}")
    
    print(f"\n? Archivos eliminados: {removed_count}")

def main():
    """Función principal de prueba"""
    print("?? PRUEBAS DEL COORDINADOR LANGGRAPH")
    print("=" * 60)
    
    test_results = []
    
    # 1. Verificar dependencias
    print("1?? VERIFICANDO DEPENDENCIAS")
    deps_ok = check_dependencies()
    test_results.append(("Dependencias", deps_ok))
    
    if not deps_ok:
        print("\n? Dependencias faltantes. Instálalas antes de continuar.")
        return
    
    print("\n" + "="*60)
    
    # 2. Probar modelos de estado
    print("2?? PROBANDO MODELOS DE ESTADO")
    models_ok = test_state_models()
    test_results.append(("Modelos de Estado", models_ok))
    
    print("\n" + "="*60)
    
    # 3. Probar creación del coordinador
    print("3?? PROBANDO CREACIÓN DEL COORDINADOR")
    coordinator_ok = test_coordinator_creation()
    test_results.append(("Creación Coordinador", coordinator_ok))
    
    print("\n" + "="*60)
    
    # 4. Probar nodos individuales
    print("4?? PROBANDO NODOS INDIVIDUALES")
    nodes_ok = test_individual_nodes()
    test_results.append(("Nodos Individuales", nodes_ok))
    
    print("\n" + "="*60)
    
    # 5. Probar checkpoints
    print("5?? PROBANDO CHECKPOINTS")
    checkpoints_ok = test_checkpoint_functionality()
    test_results.append(("Checkpoints", checkpoints_ok))
    
    print("\n" + "="*60)
    
    # 6. Probar flujo completo
    print("6?? PROBANDO FLUJO COMPLETO")
    workflow_ok = test_full_workflow()
    test_results.append(("Flujo Completo", workflow_ok))
    
    # Resumen final
    print("\n" + "="*60)
    print("?? RESUMEN DE PRUEBAS")
    print("=" * 30)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "? PASÓ" if result else "? FALLÓ"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1
    
    print(f"\n?? RESULTADO FINAL: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("?? ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("\n?? El coordinador está listo para usar:")
        print("  python orchestrator/story_coordinator.py")
        print("\n?? Archivos generados disponibles en outputs/")
    else:
        print("?? Algunas pruebas fallaron. Revisa los errores anteriores.")
    
    # Preguntar si limpiar archivos de prueba
    print(f"\n?? ¿Limpiar archivos de prueba? (y/N): ", end="")
    try:
        response = input().strip().lower()
        if response in ['y', 'yes', 'sí', 's']:
            clean_test_outputs()
    except (EOFError, KeyboardInterrupt):
        print("\n?? Pruebas completadas")

if __name__ == "__main__":
    main()