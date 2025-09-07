# -*- coding: utf-8 -*-

# scripts/setup_env.py
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def setup_environment():
    """Configura el entorno del proyecto"""
    
    # Verificar Python
    if sys.version_info < (3, 11):
        print("Error: Se requiere Python 3.11 o superior")
        sys.exit(1)
    
    # Directorio del proyecto
    project_root = Path(__file__).parent.parent
    
    print(f"Configurando entorno en: {project_root}")
    
    # Crear directorios faltantes
    directories = [
        "rag/vectorstore",
        "rag/documents", 
        "rag/processed",
        "data/manuscripts",
        "data/reference_docs",
        "logs"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directorio creado: {directory}")
    
    # Verificar archivo .env
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("⚠️  Copiando .env.example a .env")
        env_file.write_text(env_example.read_text())
        print("📝 Edita el archivo .env con tus configuraciones")
    
    print("\n✅ Entorno configurado correctamente")
    print("\nProximos pasos:")
    print("1. Activar entorno: source novel_env/bin/activate")
    print("2. Instalar dependencias: pip install -r requirements.txt")
    print("3. Configurar archivo .env")
    print("4. Ejecutar tests: python -m pytest tests/")

if __name__ == "__main__":
    setup_environment()
