@echo off
chcp 65001 >nul
cls

echo 🚀 AI Agent Writer Crew - Inicio del Sistema
echo =============================================

REM Verificar si Docker está ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está ejecutándose.
    echo Por favor inicia Docker Desktop e intenta nuevamente.
    pause
    exit /b 1
)

echo ✅ Docker está ejecutándose

REM Construir e iniciar los contenedores
echo 🔧 Construyendo e iniciando contenedores...
docker-compose down >nul 2>&1
docker-compose build

echo 🐳 Iniciando servicios...
docker-compose up -d

REM Esperar a que los servicios estén listos
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 10 /nobreak >nul

REM Verificar estado de los contenedores
echo.
echo 📋 Estado de los contenedores:
docker-compose ps

echo.
echo 🌐 Servicios disponibles:
echo    • Aplicación Principal: http://localhost:8501
echo    • Index HTML: %cd%\frontend\index.html
echo.

REM Verificar si Streamlit está respondiendo
echo 🔍 Verificando conectividad...
set /a "counter=0"
:check_loop
set /a "counter+=1"
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Streamlit está respondiendo en http://localhost:8501
    goto :success
)
if %counter% geq 30 (
    echo ⚠️  Streamlit aún no responde. Verifica los logs:
    echo    docker-compose logs frontend-streamlit
    goto :success
)
timeout /t 2 /nobreak >nul
goto :check_loop

:success
echo.
echo 🎯 Para acceder al sistema:
echo    1. Abre tu navegador
echo    2. Ve a: http://localhost:8501
echo.
echo 🔧 Comandos útiles:
echo    • Ver logs: docker-compose logs -f
echo    • Parar sistema: docker-compose down  
echo    • Reiniciar: docker-compose restart
echo.
echo 📖 ¡Sistema listo para crear novelas increíbles!
echo.

REM Preguntar si quiere abrir el navegador
set /p "open_browser=¿Quieres abrir el navegador automáticamente? (s/N): "
if /i "%open_browser%"=="s" (
    echo 🌐 Abriendo navegador...
    start http://localhost:8501
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
