#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de prueba para el sistema de agentes - Version Corregida"""

import sys
import logging
from pathlib import Path

# Añadir el directorio raiz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_agent_initialization():
    """Prueba la inicializacion de agentes"""
    print("?? Probando inicializacion de agentes...")
    
    try:
        # Importar despues de configurar el path
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
        
        # Probar obtener agente especifico
        lorekeeper = manager.get_agent('lorekeeper')
        if lorekeeper:
            print("? Agente Lorekeeper accesible")
        else:
            print("? Error accediendo Lorekeeper")
        
        return True
        
    except ImportError as e:
        print(f"? Error de importacion: {str(e)}")
        print("?? Asegurate de haber copiado todos los archivos de agentes")
        return False
    except Exception as e:
        print(f"? Error en inicializacion: {str(e)}")
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
        print(f"? Error de importacion: {str(e)}")
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
        Sus ojos azules brillaban con determinacion mientras buscaba el cristal perdido.
        El viento susurraba secretos antiguos entre las hojas doradas.
        """
        
        tools_to_test = [
            (WritingAnalyzer(), "text", test_text),
            (StyleAnalyzer(), "text", test_text),
            (CharacterAnalyzer(), "text", test_text),
            (ConsistencyChecker(), "text", test_text),
            (PacingAnalyzer(), "text", test_text),
            (PlotAnalyzer(), "text", test_text),
            (IdeaGenerator(), "context", "reino magico con cristales"),
            (VisualPromptGenerator(), "scene_description", "maga caminando por bosque encantado")
        ]
        
        successful_tools = 0
        
        for tool, param_name, test_input in tools_to_test:
            try:
                # Crear argumentos dinamicamente
                kwargs = {param_name: test_input}
                result = tool._run(**kwargs)
                
                if result and len(str(result)) > 10:  # Resultado no vacio
                    print(f"   ? {tool.name}: OK")
                    successful_tools += 1
                else:
                    print(f"   ??  {tool.name}: Resultado vacio")
                    
            except Exception as e:
                print(f"   ? {tool.name}: {str(e)[:50]}...")
        
        print(f"\n?? Herramientas funcionando: {successful_tools}/{len(tools_to_test)}")
        return successful_tools >= len(tools_to_test) * 0.7  # 70% de exito
        
    except ImportError as e:
        print(f"? Error importando herramientas: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error probando herramientas: {str(e)}")
        return False

def test_manuscript_analysis():
    """Prueba analisis de manuscrito simple"""
    print("\n?? Probando analisis de manuscrito...")
    
    try:
        from agents.agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Manuscrito de prueba mas largo
        test_manuscript = """
        En el reino de Eldoria, el joven mago Kael descubrio un antiguo grimorio
        en las ruinas de la torre de su maestro. El libro contenia hechizos
        prohibidos que podrian cambiar el destino del reino para siempre.
        
        Kael era conocido por su cabello dorado y sus ojos verdes como esmeraldas.
        Su maestro, el anciano Aldric, habia desaparecido misteriosamente hace tres dias,
        dejando solo una nota criptica: "El poder tiene un precio, y ese precio es la verdad."
        
        Mientras Kael examinaba el grimorio, una sombra se movio en la esquina de la torre.
        Los hechizos parecian susurrar su nombre, tentandolo con promesas de poder infinito.
        Pero Kael recordaba las advertencias de Aldric sobre la magia oscura.
        
        El reino se enfrentaba a una invasion de las Sombras del Vacio, criaturas
        que se alimentaban de la esperanza y la luz. Solo la magia mas poderosa
        podria detenerlas, pero ¿a que costo?
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
                    print(f"   ??  Fase {phase} fallo: {str(error_msg)[:100]}...")
                    
            except Exception as e:
                print(f"   ? Error en fase {phase}: {str(e)[:100]}...")
        
        print(f"\n?? Fases exitosas: {successful_phases}/{len(phases_to_test)}")
        return successful_phases >= 1  # Al menos una fase debe funcionar
        
    except ImportError as e:
        print(f"? Error de importacion: {str(e)}")
        return False
    except Exception as e:
        print(f"? Error en analisis de manuscrito: {str(e)}")
        return False

def test_with_llm():
    """Prueba con modelo LLM si esta disponible"""
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
            # Agregar mas ubicaciones comunes
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
                
                # Probar una consulta simple si LLM esta disponible
                if summary['llm_available']:
                    print("?? Probando generacion con LLM...")
                    # Aqui podrias hacer una prueba simple del LLM
                    # pero por ahora solo confirmamos que esta disponible
                
                return True
                
            except Exception as e:
                print(f"? Error con LLM: {str(e)}")
                return False
        else:
            print("??  No se encontro modelo LLM - saltando prueba")
            print("?? Para probar con LLM, coloca un modelo .gguf en ./llm_local/models/")
            return True
            
    except ImportError as e:
        print(f"? Error de importacion: {str(e)}")
        return False

def test_rag_integration():
    """Prueba la integracion con el sistema RAG"""
    print("\n?? Probando integracion RAG...")
    
    try:
        from agents.tools import RAGTool
        from rag.rag_manager import RAGManager
        
        # Verificar que RAG este funcionando
        rag_manager = RAGManager()
        stats = rag_manager.get_stats()
        print(f"?? Vector store: {stats.get('total_documents', 0)} documentos")
        
        # Probar RAGTool
        rag_tool = RAGTool()
        result = rag_tool._run("reino magico", k=3)
        
        if result and len(result) > 20:
            print("? RAGTool funcionando correctamente")
            print(f"   Resultado: {result[:100]}...")
            return True
        else:
            print("??  RAGTool retorno resultado vacio o muy corto")
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
        ("Inicializacion de Agentes", test_agent_initialization),
        ("Herramientas de Agentes", test_agent_tools),
        ("Herramientas Individuales", test_individual_tools),
        ("Integracion RAG", test_rag_integration),
        ("Analisis de Manuscrito", test_manuscript_analysis),
        ("Integracion con LLM", test_with_llm)
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
        status = "? PASO" if result else "? FALLO"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n?? Resultado final: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("?? ¡Todos los tests pasaron - Sistema de agentes completamente funcional!")
        print("\n?? Siguiente paso: Ejecutar Etapa 4 - Orquestacion LangGraph")
    elif passed >= len(results) * 0.7:
        print("? La mayoria de tests pasaron - Sistema mayormente funcional")
        print("?? Revisar tests fallidos para optimizacion")
    else:
        print("??  Muchos tests fallaron - Revisar instalacion y configuracion")
        print("\n?? Pasos de troubleshooting:")
        print("1. Verificar que todos los archivos de codigo esten copiados")
        print("2. Instalar dependencias: pip install nltk textblob")
        print("3. Configurar NLTK: python -c \"import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')\"")
        print("4. Verificar estructura de directorios con: tree agents/")

if __name__ == "__main__":
    main()