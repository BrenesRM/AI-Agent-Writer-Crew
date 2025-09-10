#!/bin/bash

echo "🚀 AI Agent Writer Crew - Inicio del Sistema"
echo "============================================="

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose."
    echo "Por favor inicia Docker Desktop e intenta nuevamente."
    exit 1
fi

echo "✅ Docker está ejecutándose"

# Construir e iniciar los contenedores
echo "🔧 Construyendo e iniciando contenedores..."
docker-compose down > /dev/null 2>&1
docker-compose build

echo "🐳 Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los contenedores
echo ""
echo "📋 Estado de los contenedores:"
docker-compose ps

echo ""
echo "🌐 Servicios disponibles:"
echo "   • Aplicación Principal: http://localhost:8501"
echo "   • Index HTML: file://$(pwd)/frontend/index.html"
echo ""

# Verificar si Streamlit está respondiendo
echo "🔍 Verificando conectividad..."
for i in {1..30}; do
    if curl -s http://localhost:8501 > /dev/null; then
        echo "✅ Streamlit está respondiendo en http://localhost:8501"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  Streamlit aún no responde. Verifica los logs:"
        echo "   docker-compose logs frontend-streamlit"
    fi
    sleep 2
done

echo ""
echo "🎯 Para acceder al sistema:"
echo "   1. Abre tu navegador"
echo "   2. Ve a: http://localhost:8501"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs: docker-compose logs -f"
echo "   • Parar sistema: docker-compose down"
echo "   • Reiniciar: docker-compose restart"
echo ""
echo "📖 ¡Sistema listo para crear novelas increíbles!"
