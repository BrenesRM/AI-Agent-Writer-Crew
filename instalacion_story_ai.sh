#!/bin/bash
set -e

echo "=== Instalación de Story Enhancer AI ==="

sudo apt update
sudo apt install -y python3.12-venv


# 1. Directorio base del proyecto
PROYECTO="$HOME/story-enhancer-ai"
mkdir -p "$PROYECTO"
cd "$PROYECTO" || exit

echo "Directorio del proyecto: $PROYECTO"

# 2. Crear estructura modular de carpetas
mkdir -p agents rag frontend orchestrator utils data/{documents,manuscripts,processed} \
         outputs/{novels,libraries,characters,video_prompts} tests config

# 3. Crear archivos base
touch README.md .env .gitignore requirements.txt
touch config/{agent_configs.py,rag_config.py,app_config.py}
touch utils/{file_handlers.py,text_processors.py,validators.py}

# 4. Agregar .gitkeep en carpetas vacías
for dir in data/documents data/manuscripts data/processed \
           outputs/novels outputs/libraries outputs/characters outputs/video_prompts; do
    touch "$dir/.gitkeep"
done

# 5. Crear entorno virtual (usar python3.11 si existe)
if command -v python3.11 &>/dev/null; then
    PYTHON=python3.11
else
    PYTHON=python3
fi

echo "Usando intérprete: $($PYTHON --version)"
$PYTHON -m venv venv

# 6. Activar entorno virtual
source venv/bin/activate

# 7. Actualizar pip, setuptools y wheel (usar break-system-packages si hace falta)
pip install --upgrade pip setuptools wheel --break-system-packages || true

# 8. Verificación final
echo -e "\n=== Verificación del Entorno ==="
echo "Python: $(which python)"
python --version
echo "Pip: $(pip --version)"
echo "Virtual env: $VIRTUAL_ENV"

echo -e "\nEstructura del proyecto:"
tree -d -L 3 "$PROYECTO"

echo -e "\nArchivos de configuración:"
ls -l "$PROYECTO"/.env "$PROYECTO"/.gitignore
