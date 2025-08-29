#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de debug para identificar problemas de Unicode - VERSION LIMPIA"""
import sys
import traceback
from pathlib import Path

def test_imports():
    """Probar las importaciones una por una"""
    print("=== PROBANDO IMPORTACIONES ===")
    
    try:
        print("1. Agregando path...")
        sys.path.append(str(Path(__file__).parent))
        print("   [OK] Path agregado")
    except Exception as e:
        print(f"   [ERROR] Error en path: {e}")
        return False
    
    try:
        print("2. Importando VectorStore...")
        from rag.vector_store import VectorStore
        print("   [OK] VectorStore importado")
    except Exception as e:
        print(f"   [ERROR] Error en VectorStore: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("3. Importando DocumentIngestion...")
        from rag.document_ingestion import DocumentIngestion
        print("   [OK] DocumentIngestion importado")
    except Exception as e:
        print(f"   [ERROR] Error en DocumentIngestion: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_file_encodings():
    """Revisar encodings de archivos en el directorio rag/"""
    print("\n=== REVISANDO ENCODINGS DE ARCHIVOS RAG ===")
    
    rag_dir = Path("rag")
    if not rag_dir.exists():
        print("   [WARNING] Directorio rag/ no existe")
        return
    
    for py_file in rag_dir.glob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   [OK] {py_file.name}: UTF-8 OK ({len(content)} chars)")
        except UnicodeDecodeError as e:
            print(f"   [ERROR] {py_file.name}: Error UTF-8 - {e}")
            print(f"          Posicion del error: {e.start}-{e.end}")
            print(f"          Bytes problematicos: {e.object[e.start:e.end]}")
        except Exception as e:
            print(f"   [?] {py_file.name}: Otro error - {e}")

def test_documents_directory():
    """Revisar el directorio de documentos"""
    print("\n=== REVISANDO DIRECTORIO DE DOCUMENTOS ===")
    
    docs_path = Path("../data/documents")
    if not docs_path.exists():
        print(f"   [WARNING] No existe: {docs_path.absolute()}")
        return
    
    print(f"   [OK] Directorio existe: {docs_path.absolute()}")
    
    # Contar archivos con extension completa
    archivos = []
    extensiones = ['*.txt', '*.docx', '*.md', '*.json']
    for ext in extensiones:
        archivos.extend(list(docs_path.glob(ext)))
    
    print(f"   [INFO] Encontrados {len(archivos)} archivos")
    
    if len(archivos) == 0:
        print("   [WARNING] No se encontraron archivos con extensiones:")
        for ext in extensiones:
            print(f"             {ext}")
        print("   [INFO] Listando TODOS los archivos:")
        for item in docs_path.iterdir():
            if item.is_file():
                print(f"             {item.name}")
    
    # Probar encoding de archivos txt
    txt_files = [f for f in archivos if f.suffix == '.txt']
    if txt_files:
        print(f"   [INFO] Probando encoding de {len(txt_files)} archivos .txt:")
        for archivo in txt_files:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    content = f.read(100)  # Solo primeros 100 chars
                print(f"     [OK] {archivo.name}: UTF-8 OK")
            except UnicodeDecodeError as e:
                print(f"     [ERROR] {archivo.name}: Error UTF-8 - {e}")
                # Intentar con diferentes encodings
                for enc in ['latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        with open(archivo, 'r', encoding=enc) as f:
                            content = f.read(100)
                        print(f"     [FIX] {archivo.name}: Funciona con {enc}")
                        break
                    except:
                        continue
            except Exception as e:
                print(f"     [?] {archivo.name}: Otro error - {e}")

def main():
    """Funcion principal de debug"""
    print("DIAGNOSTICO DE PROBLEMAS UNICODE")
    print("=" * 50)
    
    # Test 1: Importaciones
    if not test_imports():
        print("\n[ERROR] Las importaciones fallan. El problema esta en los modulos rag/")
        test_file_encodings()
        return
    
    print("\n[SUCCESS] Importaciones exitosas")
    
    # Test 2: Directorio de documentos
    test_documents_directory()
    
    # Test 3: Instanciacion basica
    print("\n=== PROBANDO INSTANCIACION ===")
    try:
        from rag.vector_store import VectorStore
        from rag.document_ingestion import DocumentIngestion
        
        print("   Creando DocumentIngestion...")
        ingestion = DocumentIngestion("test_debug")
        print("   [OK] DocumentIngestion creado")
        
        print("   Creando VectorStore...")
        vector_store = VectorStore("test_debug")
        print("   [OK] VectorStore creado")
        
    except Exception as e:
        print(f"   [ERROR] Error en instanciacion: {e}")
        traceback.print_exc()
    
    print("\n[INFO] Diagnostico completado")

if __name__ == "__main__":
    main()