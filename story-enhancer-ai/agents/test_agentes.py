#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para los agentes de CrewAI
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar paths necesarios
sys.path.append(str(Path(__file__).parent))

def test_tools():
    """Probar las herramientas base individualmente"""
    print("=== PROBANDO HERRAMIENTAS BASE ===\n")
    
    try:
        from agents.tools.base_tools import (
            RAGSearchTool, ManuscriptReaderTool, 
            StoryElementExtractorTool, OutputWriterTool
        )
        
        # Test 1: RAG Search Tool
        print("1. Probando RAGSearchTool...")
        rag_tool = RAGSearchTool()
        result = rag_tool._run("personajes principales")
        print(f"   Resultado: {result[:200]}...")
        print("   ✅ RAGSearchTool funciona\n")
        
        # Test 2: Manuscript Reader Tool
        print("2. Probando ManuscriptReaderTool...")
        manuscript_tool = ManuscriptReaderTool()
        result = manuscript_tool._run("summary")
        print(f"   Resultado: {result[:200]}...")
        print("   ✅ ManuscriptReaderTool funciona\n")
        
        # Test 3: Story Element Extractor Tool
        print("3. Probando StoryElementExtractorTool...")
        extractor_tool = StoryElementExtractorTool()
        sample_text = "En el reino de Eldoria, el príncipe Marcus luchó contra el dragón Pyrion cerca del castillo de Stonehaven."
        result = extractor_tool._run(sample_text, "characters")
        print(f"   Resultado: {result}")
        print("   ✅ StoryElementExtractorTool funciona\n")
        
        # Test 4: Output Writer Tool
        print("4. Probando OutputWriterTool...")
        output_tool = OutputWriterTool()
        result = output_tool._run("Contenido de prueba", "novel", "test_output.md")
        print(f"   Resultado: {result}")
        print("   ✅ OutputWriterTool funciona\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error probando herramientas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_agent():
    """Probar un solo agente para verificar funcionamiento básico"""
    print("=== PROBANDO AGENTE INDIVIDUAL ===\n")
    
    try:
        from agents.story_agents import StoryEnhancementAgents
        from crewai import Task
        
        # Crear instancia de agentes
        print("1. Inicializando agentes...")
        story_agents = StoryEnhancementAgents()
        print("   ✅ Agentes inicializados\n")
        
        # Probar un agente específico (Lorekeeper)
        print("2. Creando tarea para Lorekeeper...")
        lorekeeper = story_agents.agents['lorekeeper']
        
        # Crear una tarea simple
        test_task = Task(
            description=(
                "Analiza este fragmento de historia y identifica elementos de lore:\n\n"
                "En el reino de Aethermoor, la magia funciona a través de cristales elementales. "
                "Los magos deben canalizar energía de estos cristales para lanzar hechizos. "
                "La Orden de los Guardianes protege estos cristales de los Corruptores, "
                "quienes buscan usar la magia oscura para conquistar el reino."
            ),
            expected_output=(
                "Una lista de elementos de lore identificados en el fragmento, "
                "incluyendo sistemas mágicos, facciones, y conceptos del mundo."
            ),
            agent=lorekeeper
        )
        
        print("3. Ejecutando tarea...")
        # Nota: Para esta prueba, simularemos la ejecución sin usar crew.kickoff()
        print("   📝 Tarea creada exitosamente")
        print("   🤖 Agente: The Lorekeeper")
        print("   🎯 Objetivo: Analizar elementos de lore")
        print("   ✅ Configuración de agente completada\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error probando agente: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_creation():
    """Probar la creación de todos los agentes"""
    print("=== PROBANDO CREACIÓN DE TODOS LOS AGENTES ===\n")
    
    try:
        from agents.story_agents import StoryEnhancementAgents
        
        print("1. Creando instancia de StoryEnhancementAgents...")
        story_agents = StoryEnhancementAgents(
            model_name="gpt-3.5-turbo",  # Usar modelo más barato para pruebas
            temperature=0.7
        )
        
        print("2. Verificando agentes creados:")
        for name, agent in story_agents.agents.items():
            print(f"   ✅ {name}: {agent.role}")
            print(f"      Herramientas: {len(agent.tools)}")
            
        print(f"\n   📊 Total de agentes: {len(story_agents.agents)}")
        print("   ✅ Todos los agentes creados exitosamente\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creando agentes: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    print("=== VERIFICANDO DEPENDENCIAS ===\n")
    
    required_packages = [
        'crewai',
        'langchain',
        'langchain_openai',
        'chromadb',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("Instala con: pip install " + " ".join(missing_packages))
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas")
        return True

def check_environment():
    """Verificar configuración del entorno"""
    print("=== VERIFICANDO CONFIGURACIÓN ===\n")
    
    # Verificar API key de OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("   ✅ OPENAI_API_KEY configurada")
    else:
        print("   ⚠️  OPENAI_API_KEY no encontrada")
        print("       Los agentes intentarán usar modelo local si está disponible")
    
    # Verificar estructura de directorios
    required_dirs = ['data/documents', 'data/manuscripts', 'outputs', 'rag']
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ⚠️  {dir_path}/ - no existe")
    
    print()

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBAS DE AGENTES CREW AI")
    print("=" * 50)
    
    # 1. Verificar dependencias
    if not check_dependencies():
        print("❌ Faltan dependencias críticas. Instálalas antes de continuar.")
        return
    
    # 2. Verificar entorno
    check_environment()
    
    # 3. Probar herramientas
    if not test_tools():
        print("❌ Las herramientas base fallan. Revisa la configuración del RAG.")
        return
    
    # 4. Probar creación de agentes
    if not test_agent_creation():
        print("❌ Falla la creación de agentes. Revisa la configuración de LLM.")
        return
    
    # 5. Probar agente individual
    if not test_single_agent():
        print("❌ Falla la prueba de agente individual.")
        return
    
    print("🎉 TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 30)
    print("✅ Herramientas funcionan correctamente")
    print("✅ Agentes se crean sin problemas")
    print("✅ Configuración es válida")
    print("\n🚀 Los agentes están listos para usar!")
    print("\nPróximos pasos:")
    print("  1. Ejecuta 'python agents/story_agents.py' para análisis completo")
    print("  2. Procede a la Etapa 4: Orquestación con LangGraph")

if __name__ == "__main__":
    main()