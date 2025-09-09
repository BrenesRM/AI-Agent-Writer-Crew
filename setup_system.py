1. 🔧 Revisar problemas encontrados arriba")
            print("   2. 📦 Instalar dependencias faltantes")
            print("   3. 🧪 Ejecutar: python test_agent_phases.py")
            print("   4. 🔄 Re-ejecutar setup después de las correcciones")
        
        print("=" * 60)

def create_environment_file():
    """Crea archivo .env de ejemplo si no existe"""
    
    env_path = project_root / ".env"
    env_example_path = project_root / ".env.example"
    
    if not env_path.exists() and env_example_path.exists():
        try:
            import shutil
            shutil.copy(env_example_path, env_path)
            print("✅ Archivo .env creado desde .env.example")
            return True
        except Exception as e:
            print(f"⚠️  Error creando .env: {e}")
    
    return env_path.exists()

def install_optional_dependencies():
    """Instala dependencias opcionales para mejor rendimiento"""
    
    optional_deps = [
        'llama-cpp-python',  # LLM local
        'psutil',           # Monitoreo de sistema
        'rich',             # Output colorido
        'tqdm'              # Progress bars
    ]
    
    print("📦 INSTALACIÓN DE DEPENDENCIAS OPCIONALES")
    print("-" * 40)
    
    for dep in optional_deps:
        try:
            print(f"   📥 Instalando {dep}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {dep} instalado exitosamente")
        except subprocess.CalledProcessError:
            print(f"   ⚠️  Error instalando {dep} (opcional - continuando)")
        except Exception as e:
            print(f"   ⚠️  {dep}: {e}")

def create_quick_start_script():
    """Crea script de inicio rápido"""
    
    quick_start_content = '''@echo off
echo ===============================================
echo   AI Writer Crew - Quick Start
echo ===============================================
echo.

echo 🔍 Verificando sistema...
python test_system_complete.py --quick

echo.
echo 🚀 Iniciando interfaz web...
python launch_web_interface.py

pause
'''
    
    quick_start_path = project_root / "quick_start.bat"
    
    try:
        with open(quick_start_path, 'w', encoding='utf-8') as f:
            f.write(quick_start_content)
        print(f"✅ Script de inicio rápido creado: {quick_start_path}")
        return True
    except Exception as e:
        print(f"⚠️  Error creando quick start: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 INICIANDO SETUP COMPLETO DE AI WRITER CREW")
    print("=" * 70)
    
    try:
        # Setup principal
        setup = SystemSetup()
        success = setup.run_complete_setup()
        
        # Tareas adicionales
        print("\n🔧 TAREAS ADICIONALES")
        print("-" * 30)
        
        # Crear archivo .env
        create_environment_file()
        
        # Crear script de inicio rápido
        create_quick_start_script()
        
        # Preguntar por dependencias opcionales
        print("\n📦 ¿Instalar dependencias opcionales? (y/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['y', 'yes', 's', 'si']:
                install_optional_dependencies()
        except (EOFError, KeyboardInterrupt):
            print("Saltando dependencias opcionales...")
        
        # Resumen final y próximos pasos
        print("\n" + "=" * 70)
        print("🎯 SETUP COMPLETADO")
        print("=" * 70)
        
        if success:
            print("✅ Sistema configurado exitosamente!")
            print("\n🚀 PRÓXIMOS PASOS RECOMENDADOS:")
            print("   1. Ejecutar tests: python test_system_complete.py")
            print("   2. O test rápido: python test_system_complete.py --quick") 
            print("   3. Test de fases: python test_agent_phases.py")
            print("   4. Lanzar interfaz web: python launch_web_interface.py")
            print("   5. O usar quick start: quick_start.bat")
            
            print("\n📚 DOCUMENTACIÓN:")
            print("   - README.md: Información general del proyecto")
            print("   - ORCHESTRATOR_REFACTOR.md: Documentación del orchestrator")
            print("   - MODERN_WEB_INTERFACE.md: Guía de la interfaz web")
            
            print("\n💡 CONSEJOS:")
            print("   🧠 Para LLM local: Descarga modelo GGUF a llm_local/models/")
            print("   📚 Para RAG: Agrega documentos a data/reference_docs/")
            print("   🌐 Interfaz web disponible en http://localhost:8000")
            
        else:
            print("⚠️  Setup completado con problemas")
            print("\n🔧 ACCIONES REQUERIDAS:")
            print("   1. Revisar errores mostrados arriba")
            print("   2. Instalar dependencias faltantes")
            print("   3. Ejecutar nuevamente: python setup_system.py")
            print("   4. O ejecutar test diagnóstico: python test_agent_phases.py")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"\n💥 Error crítico en setup: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        
        print(f"\n{'='*50}")
        print("🏁 Setup terminado")
        print(f"{'='*50}")
        
        input("\nPresiona Enter para continuar...")
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"\n💥 Error ejecutando setup: {e}")
        input("\nPresiona Enter para continuar...")
        sys.exit(1)
