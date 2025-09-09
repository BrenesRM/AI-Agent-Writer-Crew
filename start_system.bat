@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo   AI Writer Crew - Sistema de Inicio
echo ===============================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar si Python está disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo 💡 Soluciones:
    echo    1. Instalar Python 3.8+ desde https://python.org
    echo    2. Agregar Python al PATH del sistema
    echo    3. Reiniciar el terminal después de la instalación
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python %PYTHON_VERSION% detectado

REM Verificar si existe entorno virtual
if exist "novel_env" (
    echo 📦 Activando entorno virtual...
    call novel_env\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo ⚠️  Error activando entorno virtual - usando Python del sistema
    ) else (
        echo ✅ Entorno virtual activado
    )
) else (
    echo ℹ️  No se encontró entorno virtual - usando Python del sistema
)

echo.
echo 🚀 Opciones disponibles:
echo ===============================================
echo 1. 🔧 Setup completo del sistema
echo 2. 🧪 Test rápido de verificación  
echo 3. 🧪 Test completo del sistema
echo 4. 🎭 Test específico de fases de agentes
echo 5. 🌐 Lanzar interfaz web moderna
echo 6. 📊 Lanzar interfaz Streamlit
echo 7. 🔄 Ejecutar orchestrator de prueba
echo 8. 📝 Ver estado del sistema
echo 9. ❌ Salir
echo ===============================================
echo.

:menu
set /p choice="🎯 Selecciona una opción (1-9): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto quicktest
if "%choice%"=="3" goto fulltest
if "%choice%"=="4" goto phasetest
if "%choice%"=="5" goto webinterface
if "%choice%"=="6" goto streamlit
if "%choice%"=="7" goto orchestrator
if "%choice%"=="8" goto status
if "%choice%"=="9" goto exit
echo ⚠️  Opción inválida. Por favor selecciona 1-9.
goto menu

:setup
echo.
echo 🔧 Ejecutando setup completo del sistema...
echo ===============================================
python setup_system.py
if %errorlevel% neq 0 (
    echo ❌ Setup falló con errores
) else (
    echo ✅ Setup completado exitosamente
)
echo.
pause
goto menu

:quicktest
echo.
echo ⚡ Ejecutando test rápido...
echo ===============================================
python test_system_complete.py --quick
if %errorlevel% neq 0 (
    echo ❌ Test rápido detectó problemas
) else (
    echo ✅ Test rápido pasado - sistema básico funcional
)
echo.
pause
goto menu

:fulltest
echo.
echo 🧪 Ejecutando test completo del sistema...
echo ===============================================
echo ⏱️  Esto puede tomar varios minutos...
python test_system_complete.py
if %errorlevel% neq 0 (
    echo ❌ Test completo detectó problemas
) else (
    echo ✅ Todos los tests pasaron - sistema completamente funcional
)
echo.
pause
goto menu

:phasetest
echo.
echo 🎭 Ejecutando test específico de fases de agentes...
echo ===============================================
python test_agent_phases.py
if %errorlevel% neq 0 (
    echo ❌ Test de fases detectó problemas
) else (
    echo ✅ Todas las fases funcionan correctamente
)
echo.
pause
goto menu

:webinterface
echo.
echo 🌐 Lanzando interfaz web moderna...
echo ===============================================
echo 💡 La interfaz se abrirá en tu navegador en http://localhost:8000
echo 🛑 Presiona Ctrl+C para detener el servidor
echo.
python launch_web_interface.py
echo.
echo 🛑 Interfaz web detenida
pause
goto menu

:streamlit
echo.
echo 📊 Lanzando interfaz Streamlit...
echo ===============================================
echo 💡 La interfaz se abrirá en tu navegador
echo 🛑 Presiona Ctrl+C para detener
echo.
if exist "frontend\app.py" (
    streamlit run frontend\app.py
) else (
    echo ❌ Archivo frontend\app.py no encontrado
    echo 🔧 Ejecuta primero el setup del sistema
)
echo.
echo 🛑 Interfaz Streamlit detenida
pause
goto menu

:orchestrator
echo.
echo 📊 Ejecutando prueba del orchestrator...
echo ===============================================
python test_orchestrator_complete.py
if %errorlevel% neq 0 (
    echo ❌ Test del orchestrator detectó problemas
) else (
    echo ✅ Orchestrator funcionando correctamente
)
echo.
pause
goto menu

:status
echo.
echo 📝 Verificando estado del sistema...
echo ===============================================

REM Verificar archivos críticos
echo 🔍 Verificando archivos críticos:
if exist "agents\agent_manager.py" (echo    ✅ AgentManager) else (echo    ❌ AgentManager)
if exist "orchestrator\coordinator.py" (echo    ✅ Orchestrator) else (echo    ❌ Orchestrator)
if exist "llm_local\llama_manager.py" (echo    ✅ LLM Manager) else (echo    ❌ LLM Manager)
if exist "rag\rag_manager.py" (echo    ✅ RAG Manager) else (echo    ❌ RAG Manager)
if exist "frontend\index.html" (echo    ✅ Interfaz Web) else (echo    ❌ Interfaz Web)

echo.
echo 🔍 Verificando directorios:
if exist "llm_local\models" (echo    ✅ Directorio de modelos LLM) else (echo    ❌ Directorio de modelos LLM)
if exist "data\reference_docs" (echo    ✅ Directorio de documentos) else (echo    ❌ Directorio de documentos)
if exist "rag\vectorstore" (echo    ✅ Directorio de vectorstore) else (echo    ❌ Directorio de vectorstore)

echo.
echo 🔍 Verificando modelos:
set /a model_count=0
if exist "llm_local\models\*.gguf" (
    for %%f in ("llm_local\models\*.gguf") do (
        set /a model_count+=1
        echo    📁 %%~nxf
    )
) 
if !model_count!==0 (
    echo    ⚠️  No se encontraron modelos LLM (.gguf)
    echo    💡 Descarga un modelo de https://huggingface.co/models?search=gguf
)

echo.
echo 🔍 Verificando documentos RAG:
set /a doc_count=0
if exist "data\reference_docs\*.*" (
    for %%f in ("data\reference_docs\*.*") do (
        set /a doc_count+=1
    )
)
if !doc_count! gtr 0 (
    echo    ✅ !doc_count! documento(s) encontrado(s)
) else (
    echo    ⚠️  No se encontraron documentos de referencia
    echo    💡 Agrega archivos .txt, .docx, .pdf a data\reference_docs\
)

echo.
echo 🔍 Verificando dependencias Python críticas:
python -c "import sys; deps=['crewai','langchain','fastapi','streamlit']; [print(f'    ✅ {d}') if __import__(d.replace('-','_')) or True else print(f'    ❌ {d}') for d in deps]" 2>nul
if %errorlevel% neq 0 (
    echo    ⚠️  Error verificando dependencias
    echo    🔧 Ejecuta: pip install -r requirements.txt
)

echo.
pause
goto menu

:exit
echo.
echo 👋 ¡Gracias por usar AI Writer Crew!
echo.
echo 💡 Recursos útiles:
echo    📚 Documentación: README.md
echo    🌐 Interfaz web: python launch_web_interface.py
echo    🧪 Tests: python test_system_complete.py
echo.
exit /b 0

:error
echo ❌ Error ejecutando el comando
pause
goto menu
