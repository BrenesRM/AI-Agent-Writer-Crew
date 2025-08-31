#!/usr/bin/env python3
"""Script de prueba para el sistema RAG"""

import sys
import logging
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rag.rag_manager import RAGManager
from llm_local.llama_manager import LlamaManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rag_basic():
    """Prueba básica del sistema RAG"""
    print("🧪 Iniciando pruebas del sistema RAG...")
    
    # Inicializar RAG
    rag = RAGManager()
    
    # Obtener estadísticas
    stats = rag.get_stats()
    print(f"📊 Estadísticas del vector store: {stats}")
    
    # Crear documento de prueba
    test_doc_path = project_root / "data" / "reference_docs" / "test_doc.txt"
    test_doc_path.parent.mkdir(parents=True, exist_ok=True)
    
    test_content = """
    Esta es una historia sobre un reino mágico llamado Aethermoor.
    
    El reino está habitado por elfos, enanos y humanos que conviven en armonía.
    La capital del reino es la ciudad de Luminar, construida sobre cristales flotantes.
    
    El rey actual es Aldrin Goldenheart, un sabio líder élfico que ha gobernado por 200 años.
    
    Personajes principales:
    - Lyra Stormwind: Una maga humana especialista en magia elemental
    - Thorin Ironbeard: Un guerrero enano guardián del reino
    - Zephyr: Un dragón ancestral que protege los cristales de poder
    
    El reino enfrenta una amenaza: las Sombras del Vacío que buscan consumir toda la magia.
    """
    
    with open(test_doc_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"📄 Documento de prueba creado: {test_doc_path}")
    
    # Ingerir documento
    success = rag.ingest_document(str(test_doc_path))
    print(f"✅ Documento ingresado: {success}")
    
    # Realizar consultas de prueba
    queries = [
        "¿Quién es el rey del reino?",
        "¿Cuáles son las razas que habitan Aethermoor?",
        "¿Cómo se llama la capital?",
        "¿Quién es Lyra Stormwind?",
        "¿Cuál es la amenaza que enfrenta el reino?"
    ]
    
    print("\n🔍 Realizando consultas de prueba...")
    for query in queries:
        result = rag.query(query, k=3)
        print(f"\nPregunta: {query}")
        print(f"Fuentes encontradas: {result['num_sources']}")
        print(f"Contexto: {result['context'][:200]}...")
    
    print("\n✅ Pruebas RAG completadas")

def test_llm_integration(model_path: str = ""):
    """Prueba la integración con LLM local"""
    if not model_path or not Path(model_path).exists():
        print("⚠️  Modelo LLM no encontrado, saltando pruebas de LLM")
        return
    
    print(f"\n🤖 Probando LLM local: {model_path}")
    
    try:
        # Inicializar LLM
        llm = LlamaManager(model_path)
        
        # Prueba básica de generación
        prompt = "Escribe una breve descripción de un reino mágico:"
        response = llm.generate(prompt, max_tokens=100)
        print(f"🎯 Respuesta del LLM: {response}")
        
        # Prueba con contexto RAG
        rag = RAGManager()
        rag_result = rag.query("Describe el reino de Aethermoor")
        
        if rag_result['context']:
            llm_response = llm.generate_with_context(
                "Describe las características principales de este reino",
                rag_result['context']
            )
            print(f"🔗 Respuesta con contexto RAG: {llm_response}")
        
        print("✅ Pruebas LLM completadas")
        
    except Exception as e:
        print(f"❌ Error en pruebas LLM: {str(e)}")

if __name__ == "__main__":
    test_rag_basic()
    
    # Intentar probar LLM si está configurado
    model_path = ""
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    
    test_llm_integration(model_path)
