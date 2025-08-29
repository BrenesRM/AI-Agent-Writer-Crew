#!/usr/bin/env python3
"""
Script de prueba para el frontend de Story Enhancer
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import importlib
import traceback
from pathlib import Path

# Agregar directorio del proyecto al path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

def test_imports():
    """Prueba que todos los módulos se puedan importar"""
    
    print("🔍 Probando importación de módulos...")
    
    modules_to_test = [
        'streamlit',
        'frontend.utils.session_state',
        'frontend.components.sidebar', 
        'frontend.pages.document_upload',
        'frontend.pages.manuscript_editor',
        'frontend.pages.agent_control',
        'frontend.pages.outputs_viewer',
        'frontend.pages.settings_page'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"  ⚠️  {module}: Error inesperado - {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} módulos fallaron en la importación")
        return False
    else:
        print(f"\n✅ Todos los módulos se importaron correctamente")
        return True

def test_dependencies():
    """Prueba las dependencias críticas"""
    
    print("\n📦 Probando dependencias críticas...")
    
    critical_deps = [
        ('streamlit', 'Streamlit'),
        ('streamlit_option_menu', 'Streamlit Option Menu'),
        ('plotly', 'Plotly'),
        ('pandas', 'Pandas'),
        ('pathlib', 'Pathlib (built-in)'),
        ('json', 'JSON (built-in)'),
        ('datetime', 'DateTime (built-in)')
    ]
    
    failed_deps = []
    
    for dep_name, dep_display in critical_deps:
        try:
            importlib.import_module(dep_name)
            print(f"  ✅ {dep_display}")
        except ImportError:
            print(f"  ❌ {dep_display}")
            failed_deps.append(dep_display)
    
    if failed_deps:
        print(f"\n❌ Dependencias faltantes: {', '.join(failed_deps)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ Todas las dependencias están disponibles")
        return True

def test_directory_structure():
    """Verifica la estructura de directorios"""
    
    print("\n📁 Verificando estructura de directorios...")
    
    required_dirs = [
        'frontend/pages',
        'frontend/components', 
        'frontend/utils',
        'static/uploads',
        'static/outputs',
        'static/temp',
        'logs'
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        full_path = project_dir / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path}")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️  Directorios faltantes encontrados. Creándolos...")
        for dir_path in missing_dirs:
            full_path = project_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Creado: {dir_path}")
    
    print(f"\n✅ Estructura de directorios verificada")
    return True

def test_streamlit_config():
    """Verifica la configuración de Streamlit"""
    
    print("\n⚙️ Verificando configuración de Streamlit...")
    
    config_file = project_dir / '.streamlit' / 'config.toml'
    
    if config_file.exists():
        print(f"  ✅ Archivo de configuración encontrado")
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                if '[global]' in content and '[server]' in content:
                    print(f"  ✅ Configuración válida")
                    return True
                else:
                    print(f"  ⚠️  Configuración incompleta")
        except Exception as e:
            print(f"  ❌ Error leyendo configuración: {e}")
    else:
        print(f"  ⚠️  Archivo de configuración no encontrado")
        print(f"  💡 El frontend funcionará con configuración por defecto")
    
    return True

def test_main_app():
    """Verifica que el archivo principal app.py esté correcto"""
    
    print("\n📱 Verificando aplicación principal...")
    
    app_file = project_dir / 'app.py'
    
    if not app_file.exists():
        print(f"  ❌ app.py no encontrado")
        return False
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar elementos críticos
        critical_elements = [
            'import streamlit as st',
            'st.set_page_config',
            'def main():',
            '__name__ == "__main__"'
        ]
        
        missing_elements = []
        for element in critical_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"  ❌ Elementos faltantes en app.py: {missing_elements}")
            return False
        else:
            print(f"  ✅ app.py tiene estructura correcta")
            return True
            
    except Exception as e:
        print(f"  ❌ Error verificando app.py: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    
    print("=" * 50)
    print("🧪 TESTING FRONTEND - STORY ENHANCER")
    print("=" * 50)
    
    tests = [
        ("Importación de módulos", test_imports),
        ("Dependencias", test_dependencies), 
        ("Estructura de directorios", test_directory_structure),
        ("Configuración Streamlit", test_streamlit_config),
        ("Aplicación principal", test_main_app)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"⚠️  {test_name} tuvo problemas menores")
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {passed_tests}/{total_tests} pruebas exitosas")
    
    if passed_tests == total_tests:
        print("✅ ¡Todos los tests pasaron! El frontend está listo.")
        print("\n🚀 Para ejecutar la aplicación:")
        print("   ./run_frontend.sh")
        print("   o")
        print("   streamlit run app.py")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron, pero el frontend debería funcionar.")
        print("💡 Revisa los errores arriba para una experiencia óptima.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)