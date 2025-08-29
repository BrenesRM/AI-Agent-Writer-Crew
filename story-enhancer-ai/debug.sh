#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de debug para identificar problemas de Unicode"""
import sys
import traceback
from pathlib import Path

def test_imports():
    """Probar las importaciones una por una"""
    print("=== PROBANDO IMPORTACIONES ===")
    
    try:
        print("1. Agregando path...")
        sys.path.append(str(Path(__file__).parent))
        print("   ✓ Path agregado")
    except Exception as e:
        print(f"   ✗ Error en path: {e}")
        return False
    
    try:
        print("2. Importando VectorStore...")
        from rag.vector_store import VectorStore
        print("   ✓ VectorStore importado")
    except Exception as e:
        print(f"   ✗ Error en VectorStore: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("3. Importando DocumentIngestion...")
        from rag.document_ingestion import DocumentIngestion
        print("   ✓ DocumentIngestion importado")
    except Exception as e:
        print(f"   ✗ Error en DocumentIngestion: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_file_encodings():
    """Revisar encodings de archivos en el directorio rag/"""
    print("\n=== REVISANDO ENCODINGS DE ARCHIVOS RAG ===")
    
    rag_dir = Path("rag")
    if not rag_dir.exists():
        print("   ⚠ Directorio rag/ no existe")
        return
    
    for py_file in rag_dir.glob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   ✓ {py_file.name}: UTF-8 OK ({len(content)} chars)")
        except UnicodeDecodeError as e:
            print(f"   ✗ {py_file.name}: Error UTF-8 - {e}")
        except Exception as e:
            print(f"   ? {py_file.name}: Otro error - {e}")

def test_documents_directory():
    """Revisar el directorio de documentos"""
    print("\n=== REVISANDO DIRECTORIO DE DOCUMENTOS ===")
    
    docs_path = Path("../data/documents")
    if not docs_path.exists():
        print(f"   ⚠ No existe: {docs_path.absolute()}")
        return
    
    print(f"   ✓ Directorio existe: {docs_path.absolute()}")
    
    # Contar archivos
    archivos = []
    for ext in ['txt', 'docx']:
        archivos.extend(list(docs_path.glob(f"*.{ext}")))
    
    print(f"   📁 Encontrados {len(archivos)} archivos")
    
    # Probar encoding de archivos txt
    for archivo in archivos:
        if archivo.suffix == '.txt':
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    content = f.read(100)  # Solo primeros 100 chars
                print(f"   ✓ {archivo.name}: UTF-8 OK")
            except UnicodeDecodeError as e:
                print(f"   ✗ {archivo.name}: Error UTF-8 - {e}")
                # Intentar con diferentes encodings
                for enc in ['latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        with open(archivo, 'r', encoding=enc) as f:
                            content = f.read(100)
                        print(f"   💡 {archivo.name}: Funciona con {enc}")
                        break
                    except:
                        continue
            except Exception as e:
                print(f"   ? {archivo.name}: Otro error - {e}")

def main():
    """Función principal de debug"""
    print("🔍 DIAGNÓSTICO DE PROBLEMAS UNICODE")
    print("=" * 50)
    
    # Test 1: Importaciones
    if not test_imports():
        print("\n❌ Las importaciones fallan. El problema está en los módulos rag/")
        test_file_encodings()
        return
    
    print("\n✅ Importaciones exitosas")
    
    # Test 2: Directorio de documentos
    test_documents_directory()
    
    # Test 3: Instanciación básica
    print("\n=== PROBANDO INSTANCIACIÓN ===")
    try:
        from rag.vector_store import VectorStore
        from rag.document_ingestion import DocumentIngestion
        
        print("   Creando DocumentIngestion...")
        ingestion = DocumentIngestion("test_debug")
        print("   ✓ DocumentIngestion creado")
        
        print("   Creando VectorStore...")
        vector_store = VectorStore("test_debug")
        print("   ✓ VectorStore creado")
        
    except Exception as e:
        print(f"   ✗ Error en instanciación: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
