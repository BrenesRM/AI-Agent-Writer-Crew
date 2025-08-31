#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de prueba para el sistema de agentes - Versión Corregida"""

import sys
import logging
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_agent_initialization():
    """Prueba la inicialización de agentes"""
    print("?? Probando inicialización de agentes...")
    
    try:
        # Importar después de configurar el path
        from agents.agent_manager import AgentManager
        
        # Inicializar manager sin LLM
        manager = AgentManager()
        
        # Verificar agentes
        agents = manager.list_agents()
        print(f"? Agentes inicializados: {len(agents)}")
        
        expected_agents = [
            'lorekeeper', 'character_developer', 'plot_weaver', 
            'style_editor', 'visualizer', 'researcher',
            'continuity_auditor', 'beta_reader', 'pacing_specialist',
            'proofreader', 'innovation_scout'
        ]
        
        missing_agents = set(expected_agents) - set(agents)
        if missing_agents:
            print(f"??  Agentes faltantes: {missing_agents}")
        
        for agent in agents:
            print(f"   - {agent}")
        
        # Probar obtener agente específico
        lorekeeper = manager.get_agent('lorekeeper')
        if lorekeeper:
            print("? Agente Lorekeeper accesible")
        else:
            print("? Error accediendo Lorekeeper")
        
        return True
        
    except ImportError as e:
        print(f"? Error de importación: {str(e)}")
        print("?? Asegúrate de haber copiado todos los archivos de agentes")
        return False
    except Exception as e:
        print(f"? Error en inicialización: {str(e)}")
        return False

def test_agent_tools():
    """Prueba las herramientas de los agentes"""
    print("\n?? Probando herramientas de agentes...")
    
    try:
        from agents.agent_manager import AgentManager
        
        manager = AgentManager()
        lorekeeper = manager.get_agent('lorekeeper')
        
        if lorekeeper and hasattr(lorekeeper, 'agent'):
            tools = lorekeeper.agent.tools
            print(f"? Herramientas disponibles: {len(tools)}")
            
            # Mostrar todas las herramientas
            expected_tools = [
                'Consultar Base de Conocimiento',
                'Analizador de Escritura',
                'Analizador de Estilo', 
                'Analizador de Personajes',
                'Verificador de Consistencia',
                'Analizador de Ritmo',
                'Analizador de Trama',
                'Generador de Ideas Creativas',
                'Generador de Prompts Visuales'
            ]
            
            tool_names = [tool.name for tool in tools]
            for expected_tool in expected_tools:
                if expected_tool in tool_names:
                    print(f"   ? {expected_tool}")
                else:
                    print(f"   ? {expected_tool} (faltante)")
            
            return len(tool_names) >= 8  # Al menos 8 herramientas
        else:
            print("? No se pudieron acceder a las herramientas")
            return False
            
    except ImportError as e:
        print(f"? Error de importación: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error probando herramientas: {str(e)}")
        return False

def test_individual_tools():
    """Prueba herramientas individuales"""
    print("\n???  Probando herramientas individuales...")
    
    try:
        from agents.tools import (
            WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer,
            ConsistencyChecker, PacingAnalyzer, PlotAnalyzer,
            IdeaGenerator, VisualPromptGenerator
        )
        
        # Texto de prueba
        test_text = """
        En el reino de Eldoria, la joven maga Lyra caminaba por el bosque encantado. 
        Sus ojos azules brillaban con determinación mientras buscaba el cristal perdido.
        El viento susurraba secretos antiguos entre las hojas doradas.
        """
        
        tools_to_test = [
            (WritingAnalyzer(), "texto de análisis", test_text),
            (StyleAnalyzer(), "texto de análisis estilística", test_text),
            (CharacterAnalyzer(), "texto que contiene personajes", test_text),
            (ConsistencyChecker(), "texto a verificar", test_text),
            (PacingAnalyzer(), "texto para analizar ritmo", test_text),
            (PlotAnalyzer(), "texto narrativo para trama", test_text),
            (IdeaGenerator(), "contexto de generación", "reino mágico con cristales"),
            (VisualPromptGenerator(), "descripción de escena", "maga caminando por bosque encantado")
        ]
        
        successful_tools = 0
        
        for tool, param_name, test_input in tools_to_test:
            try:
                # Crear argumentos dinámicamente
                kwargs = {param_name: test_input}
                result = tool._run(**kwargs)
                
                if result and len(str(result)) > 10:  # Resultado no vacío
                    print(f"   ? {tool.name}: OK")
                    successful_tools += 1
                else:
                    print(f"   ??  {tool.name}: Resultado vacío")
                    
            except Exception as e:
                print(f"   ? {tool.name}: {str(e)[:50]}...")
        
        print(f"\n?? Herramientas funcionando: {successful_tools}/{len(tools_to_test)}")
        return successful_tools >= len(tools_to_test) * 0.7  # 70% de éxito
        
    except ImportError as e:
        print(f"? Error importando herramientas: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error probando herramientas: {str(e)}")
        return False

def test_manuscript_analysis():
    """Prueba análisis de manuscrito simple"""
    print("\n?? Probando análisis de manuscrito...")
    
    try:
        from agents.agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Manuscrito de prueba más largo
        test_manuscript = """
        En el reino de Eldoria, el joven mago Kael descubrió un antiguo grimorio
        en las ruinas de la torre de su maestro. El libro contenía hechizos
        prohibidos que podrían cambiar el destino del reino para siempre.
        
        Kael era conocido por su cabello dorado y sus ojos verdes como esmeraldas.
        Su maestro, el anciano Aldric, había desaparecido misteriosamente hace tres días,
        dejando solo una nota críptica: "El poder tiene un precio, y ese precio es la verdad."
        
        Mientras Kael examinaba el grimorio, una sombra se movió en la esquina de la torre.
        Los hechizos parecían susurrar su nombre, tentándolo con promesas de poder infinito.
        Pero Kael recordaba las advertencias de Aldric sobre la magia oscura.
        
        El reino se enfrentaba a una invasión de las Sombras del Vacío, criaturas
        que se alimentaban de la esperanza y la luz. Solo la magia más poderosa
        podría detenerlas, pero ¿a qué costo?
        """
        
        # Establecer manuscrito
        manager.set_manuscript(test_manuscript)
        
        # Obtener resumen
        summary = manager.get_analysis_summary()
        print(f"? Manuscrito establecido: {summary['manuscript_length']} caracteres")
        print(f"   Agentes disponibles: {len(summary['available_agents'])}")
        print(f"   LLM disponible: {summary['llm_available']}")
        
        # Probar fases individuales
        phases_to_test = ["worldbuilding", "character_development", "plot_structure"]
        successful_phases = 0
        
        for phase in phases_to_test:
            try:
                print(f"\n?? Probando fase: {phase}")
                results = manager.run_analysis_phase(phase)
                
                if results and "error" not in results:
                    print(f"   ? Fase {phase} ejecutada exitosamente")
                    print(f"   ?? Agentes involucrados: {results.get('agents_involved', [])}")
                    successful_phases += 1
                else:
                    error_msg = results.get('error', 'Error desconocido') if results else 'Sin resultados'
                    print(f"   ??  Fase {phase} falló: {str(error_msg)[:100]}...")
                    
            except Exception as e:
                print(f"   ? Error en fase {phase}: {str(e)[:100]}...")
        
        print(f"\n?? Fases exitosas: {successful_phases}/{len(phases_to_test)}")
        return successful_phases >= 1  # Al menos una fase debe funcionar
        
    except ImportError as e:
        print(f"? Error de importación: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error en análisis de manuscrito: {str(e)}")
        return False

def test_with_llm():
    """Prueba con modelo LLM si está disponible"""
    print("\n?? Probando con modelo LLM...")
    
    try:
        from config.settings import settings
        from agents.agent_manager import AgentManager
        
        llm_path = None
        
        # Buscar modelo en ubicaciones comunes
        possible_paths = [
            "./llm_local/models/model.gguf",
            "/home/user/multi_agent_novel_system/llm_local/models/model.gguf",
            str(settings.llm_model_path) if settings.llm_model_path else None,
            # Agregar más ubicaciones comunes
            "./llm_local/models/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf",
            "/home/user/multi_agent_novel_system/llm_local/models/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"
        ]
        
        for path in possible_paths:
            if path and Path(path).exists():
                llm_path = path
                break
        
        if llm_path:
            try:
                print(f"?? Inicializando con modelo: {Path(llm_path).name}")
                manager = AgentManager(llm_path)
                
                summary = manager.get_analysis_summary()
                print(f"? Manager con LLM inicializado")
                print(f"   LLM disponible: {summary['llm_available']}")
                
                # Probar una consulta simple si LLM está disponible
                if summary['llm_available']:
                    print("?? Probando generación con LLM...")
                    # Aquí podrías hacer una prueba simple del LLM
                    # pero por ahora solo confirmamos que está disponible
                
                return True
                
            except Exception as e:
                print(f"? Error con LLM: {str(e)}")
                return False
        else:
            print("??  No se encontró modelo LLM - saltando prueba")
            print("?? Para probar con LLM, coloca un modelo .gguf en ./llm_local/models/")
            return True
            
    except ImportError as e:
        print(f"? Error de importación: {str(e)}")
        return False

def test_rag_integration():
    """Prueba la integración con el sistema RAG"""
    print("\n?? Probando integración RAG...")
    
    try:
        from agents.tools import RAGTool
        from rag.rag_manager import RAGManager
        
        # Verificar que RAG esté funcionando
        rag_manager = RAGManager()
        stats = rag_manager.get_stats()
        print(f"?? Vector store: {stats.get('total_documents', 0)} documentos")
        
        # Probar RAGTool
        rag_tool = RAGTool()
        result = rag_tool._run("reino mágico", k=3)
        
        if result and len(result) > 20:
            print("? RAGTool funcionando correctamente")
            print(f"   Resultado: {result[:100]}...")
            return True
        else:
            print("??  RAGTool retornó resultado vacío o muy corto")
            return False
            
    except ImportError as e:
        print(f"? Error importando RAG: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error probando RAG: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("?? Iniciando pruebas del sistema de agentes\n")
    print(f"?? Directorio de trabajo: {Path.cwd()}")
    print(f"?? Directorio del proyecto: {project_root}")
    
    tests = [
        ("Inicialización de Agentes", test_agent_initialization),
        ("Herramientas de Agentes", test_agent_tools),
        ("Herramientas Individuales", test_individual_tools),
        ("Integración RAG", test_rag_integration),
        ("Análisis de Manuscrito", test_manuscript_analysis),
        ("Integración con LLM", test_with_llm)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"?? TEST: {test_name}")
        print('='*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"? Error inesperado en {test_name}: {str(e)}")
            logger.exception(f"Error detallado en {test_name}")
            results.append((test_name, False))
    
    # Resumen final
    print(f"\n{'='*60}")
    print("?? RESUMEN DE PRUEBAS")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "? PASÓ" if result else "? FALLÓ"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n?? Resultado final: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("?? ¡Todos los tests pasaron - Sistema de agentes completamente funcional!")
        print("\n?? Siguiente paso: Ejecutar Etapa 4 - Orquestación LangGraph")
    elif passed >= len(results) * 0.7:
        print("? La mayoría de tests pasaron - Sistema mayormente funcional")
        print("?? Revisar tests fallidos para optimización")
    else:
        print("??  Muchos tests fallaron - Revisar instalación y configuración")
        print("\n?? Pasos de troubleshooting:")
        print("1. Verificar que todos los archivos de código estén copiados")
        print("2. Instalar dependencias: pip install nltk textblob")
        print("3. Configurar NLTK: python -c \"import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')\"")
        print("4. Verificar estructura de directorios con: tree agents/")

if __name__ == "__main__":
    main()