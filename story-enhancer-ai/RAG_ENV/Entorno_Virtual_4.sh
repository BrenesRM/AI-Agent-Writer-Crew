#!/bin/bash
set -e

# Usar Python 3.11 si está disponible, sino python3
if command -v python3.11 &>/dev/null; then
    PYTHON=python3.11
else
    PYTHON=python3
fi

# Crear entorno virtual
$PYTHON -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar herramientas base dentro del venv
pip install --upgrade pip setuptools wheel --break-system-packages || true

# Verificar que estamos en el entorno correcto
which python
python --version
