#!/bin/bash

# Script de ejecución del frontend de Story Enhancer
# Uso: ./run_frontend.sh [puerto]

# Configurar colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuración
DEFAULT_PORT=8501
PORT=${1:-$DEFAULT_PORT}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_DIR/venv"

log_info "=== Story Enhancer Frontend ==="
log_info "Directorio del proyecto: $PROJECT_DIR"
log_info "Puerto: $PORT"

# Verificar que estamos en el directorio correcto
if [[ ! -f "$PROJECT_DIR/app.py" ]]; then
    log_error "No se encontró app.py en el directorio actual"
    log_error "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar entorno virtual
if [[ ! -d "$VENV_PATH" ]]; then
    log_error "No se encontró el entorno virtual en: $VENV_PATH"
    log_info "Ejecuta primero: python3 -m venv venv"
    exit 1
fi

# Activar entorno virtual
log_info "Activando entorno virtual..."
source "$VENV_PATH/bin/activate"

if [[ $? -ne 0 ]]; then
    log_error "No se pudo activar el entorno virtual"
    exit 1
fi

log_success "Entorno virtual activado"

# Verificar instalación de Streamlit
if ! python -c "import streamlit" 2>/dev/null; then
    log_error "Streamlit no está instalado"
    log_info "Instalando dependencias..."
    pip install -r requirements.txt
    
    if [[ $? -ne 0 ]]; then
        log_error "Error instalando dependencias"
        exit 1
    fi
fi

# Crear directorios necesarios
log_info "Creando directorios necesarios..."
mkdir -p static/{uploads,outputs,temp}
mkdir -p logs
mkdir -p chroma_db

# Configurar variables de entorno
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Verificar puerto disponible
if command -v netstat >/dev/null 2>&1; then
    if netstat -tuln | grep ":$PORT " >/dev/null; then
        log_warning "El puerto $PORT está en uso"
        log_info "Intentando encontrar un puerto disponible..."
        
        for ((i=PORT+1; i<=PORT+10; i++)); do
            if ! netstat -tuln | grep ":$i " >/dev/null; then
                PORT=$i
                log_info "Usando puerto alternativo: $PORT"
                break
            fi
        done
    fi
fi

# Mensaje de información
log_info "Iniciando Story Enhancer..."
log_info "Interfaz web disponible en: http://localhost:$PORT"
log_info "Presiona Ctrl+C para detener el servidor"

echo ""
log_success "🚀 Lanzando aplicación..."
echo ""

# Ejecutar Streamlit
streamlit run app.py \
    --server.port=$PORT \
    --server.address=localhost \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --logger.level=info

log_info "Aplicación cerrada"