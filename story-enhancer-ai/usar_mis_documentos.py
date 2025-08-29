#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script final para procesar documentos - SIN CARACTERES ESPECIALES"""
import sys
import traceback
from pathlib import Path

# Agregar path
sys.path.append(str(Path(__file__).parent))

def importar_modulos():
    """Importar modulos de forma segura"""
    try:
        from rag.vector_store import VectorStore
        from rag.document_ingestion import DocumentIngestion
        return VectorStore, DocumentIngestion
    except Exception as e:
        print(f"[ERROR] No se pueden importar modulos: {e}")
        return None, None

def encontrar_directorio_documentos():
    """Encontrar donde estan realmente los documentos"""
    print("Buscando directorio de documentos...")
    
    # Posibles ubicaciones
    ubicaciones = [
        Path("data/documents"),
        Path("../data/documents"),
        Path("./data/documents"),
        Path.cwd() / "data" / "documents",
        Path.cwd().parent / "data" / "documents"
    ]
    
    for ubicacion in ubicaciones:
        if ubicacion.exists():
            archivos = [f for f in ubicacion.iterdir() if f.is_file() and f.name != '.gitkeep']
            if archivos:
                print(f"[OK] Encontrado: {ubicacion.absolute()}")
                print(f"     {len(archivos)} archivos")
                return ubicacion
    
    print("[ERROR] No se encontro directorio con documentos")
    return None

def listar_archivos(directorio):
    """Listar archivos en el directorio"""
    if not directorio or not directorio.exists():
        return []
    
    print(f"\nArchivos en {directorio}:")
    archivos = []
    
    for archivo in directorio.iterdir():
        if archivo.is_file() and archivo.name != '.gitkeep':
            try:
                size_mb = archivo.stat().st_size / (1024 * 1024)
                print(f"  {archivo.name} ({size_mb:.2f} MB)")
                archivos.append(archivo)
            except Exception as e:
                print(f"  {archivo.name} (error: {e})")
    
    return archivos

def procesar_directorio(directorio_path, VectorStore, DocumentIngestion):
    """Procesar directorio de documentos"""
    print(f"\nProcesando directorio: {directorio_path}")
    
    try:
        # Crear ingestion
        ingestion = DocumentIngestion("documentos_procesados")
        
        # Procesar
        print("Ejecutando procesamiento...")
        resultados = ingestion.ingest_directory(str(directorio_path), recursive=False)
        
        # Mostrar resultados
        print("\nRESULTADOS:")
        if isinstance(resultados, dict):
            summary = resultados.get('summary', {})
            successful = summary.get('successful', 0)
            failed = summary.get('failed', 0)
            total_chunks = resultados.get('total_chunks', 0)
            
            print(f"  Exitosos: {successful}")
            print(f"  Fallidos: {failed}")
            print(f"  Chunks: {total_chunks}")
            
            if failed > 0 and 'errors' in resultados:
                print("  Errores:")
                for error in resultados['errors'][:3]:
                    print(f"    - {str(error)[:100]}")
                    
        elif isinstance(resultados, list):
            print(f"  Chunks procesados: {len(resultados)}")
        else:
            print(f"  Resultado: {type(resultados)}")
        
        return resultados is not None
        
    except Exception as e:
        print(f"[ERROR] Fallo en procesamiento: {e}")
        traceback.print_exc()
        return False

def probar_busquedas(VectorStore):
    """Probar busquedas simples"""
    print("\nProbando busquedas...")
    
    try:
        vector_store = VectorStore("documentos_procesados")
        
        # Busquedas simples sin caracteres especiales
        consultas = [
            "dos colmillos",
            "panteon",
            "mundo",
            "personajes",
            "politica",
            "caceria",
            "guerra",
            "iglesia"
        ]
        
        for consulta in consultas:
            try:
                resultados = vector_store.search(consulta, k=1)
                
                if resultados:
                    mejor = resultados[0]
                    similarity = mejor.get('similarity', 0)
                    source = mejor.get('source', 'desconocido')
                    content = mejor.get('content', '')[:80]
                    
                    if similarity > 0.3:  # Solo mostrar si hay similitud decente
                        print(f"  '{consulta}': {source} ({similarity:.3f})")
                        print(f"    {content}...")
                        
            except Exception as e:
                print(f"  '{consulta}': error - {e}")
                
    except Exception as e:
        print(f"[ERROR] Error en busquedas: {e}")

def main():
    """Funcion principal"""
    print("PROCESADOR DE DOCUMENTOS - VERSION FINAL")
    print("=" * 50)
    
    # 1. Importar modulos
    VectorStore, DocumentIngestion = importar_modulos()
    if not VectorStore:
        return
    
    # 2. Encontrar documentos
    directorio = encontrar_directorio_documentos()
    if not directorio:
        return
    
    # 3. Listar archivos
    archivos = listar_archivos(directorio)
    if not archivos:
        print("[ERROR] No hay archivos para procesar")
        return
    
    # 4. Procesar
    exito = procesar_directorio(directorio, VectorStore, DocumentIngestion)
    if not exito:
        print("[ERROR] Fallo el procesamiento")
        return
    
    # 5. Probar busquedas
    probar_busquedas(VectorStore)
    
    print("\n[SUCCESS] Proceso completado exitosamente")

if __name__ == "__main__":
    main()