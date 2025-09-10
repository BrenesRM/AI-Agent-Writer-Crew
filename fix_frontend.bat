@echo off
chcp 65001 >nul
cls

echo 🔧 AI Agent Writer Crew - Fix Frontend
echo ========================================

echo 📍 Reiniciando el contenedor frontend...
docker-compose restart frontend-streamlit

echo ⏳ Esperando 10 segundos...
timeout /t 10 /nobreak >nul

echo 📋 Estado actual:
docker-compose ps frontend-streamlit

echo.
echo 🔍 Verificando conectividad...
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend funcionando correctamente
    echo 🌐 Disponible en: http://localhost:8501
) else (
    echo ❌ Frontend no responde
    echo 📝 Ver logs: docker-compose logs frontend-streamlit
)

echo.
pause
