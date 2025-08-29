#!/usr/bin/env python3
"""Script de prueba para el sistema RAG"""
import os
import sys
import json
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from rag.vector_store import VectorStore
from rag.document_ingestion import DocumentIngestion

def test_text_processing():
    """Probar procesamiento de texto básico"""
    print("🔍 Probando procesamiento de texto...")
    
    # Crear archivo de prueba
    test_file = Path("data/documents/test.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("""
Esta es una historia de prueba para el sistema RAG.

Capítulo 1: El Comienzo
En un reino lejano, había un joven aventurero llamado Alex.
Alex tenía el sueño de convertirse en un gran mago.

Capítulo 2: El Aprendizaje  
Alex comenzó a estudiar en la Academia de Magia.
Allí aprendió sobre hechizos, pociones y criaturas mágicas.

Capítulo 3: La Aventura
Un día, Alex recibió una misión especial del director.
Debía encontrar un artefacto perdido en el Bosque Oscuro.
        """.strip())
    
    print(f"✅ Archivo de prueba creado: {test_file}")
    return str(test_file)

def test_vector_store():
    """Probar el sistema de vector store"""
    print("\n🗄️  Probando Vector Store...")
    
    # Crear archivo de prueba
    test_file = test_text_processing()
    
    # Inicializar vector store
    vector_store = VectorStore("test_collection")
    
    # Agregar documento
    result = vector_store.add_document(test_file)
    print(f"Resultado de ingesta: {result}")
    
    # Probar búsqueda
    query = "Alex mago academia"
    results = vector_store.search(query, k=3)
    
    print(f"\n🔎 Búsqueda: '{query}'")
    print(f"Resultados encontrados: {len(results)}")
    
    for i, result in enumerate(results[:2]):  # Mostrar solo los primeros 2
        print(f"\nResultado {i+1}:")
        print(f"Similitud: {result['similarity']:.3f}")
        print(f"Contenido: {result['content'][:200]}...")
        print(f"Fuente: {result['source']}")
    
    # Mostrar estadísticas
    stats = vector_store.get_collection_stats()
    print(f"\n📊 Estadísticas de la colección:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return vector_store

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del sistema RAG")
    print("=" * 50)
    
    try:
        # Probar vector store básico
        vector_store = test_vector_store()
        
        print("\n" + "=" * 50)
        print("✅ Pruebas completadas exitosamente!")
        
        # Mostrar estadísticas finales
        final_stats = vector_store.get_collection_stats()
        print(f"\n📊 Estadísticas finales del sistema:")
        for key, value in final_stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
