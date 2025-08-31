#!/bin/bash
# =====================================================
# ETAPA 1: PREPARACI�N DEL ENTORNO CON ANSIBLE
# =====================================================

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_FILE="$SCRIPT_DIR/setup_project.yml"

echo "Starting environment setup with Ansible..."
echo "Script directory: $SCRIPT_DIR"

# 1. Instalar Ansible en Ubuntu
echo "Updating packages and installing Ansible..."
sudo apt update
sudo apt install -y ansible

# 2. Crear directorio temporal para el playbook
echo "Creating temporary directory for Ansible setup..."
mkdir -p ~/ansible_setup
cd ~/ansible_setup

# 3. Crear el archivo inventory.yml
echo "Creating inventory file..."
cat > inventory.yml << EOF
[local]
localhost ansible_connection=local ansible_user=$USER
EOF

# 4. Copiar el playbook de Ansible al directorio temporal
echo "Copying setup_project.yml to temporary directory..."
echo "Looking for setup file at: $SETUP_FILE"

if [ -f "$SETUP_FILE" ]; then
    cp "$SETUP_FILE" ./setup_project.yml
    echo "setup_project.yml copied successfully."
else
    echo "ERROR: setup_project.yml not found at $SETUP_FILE!"
    echo "Current directory contents:"
    ls -la "$SCRIPT_DIR/"
    exit 1
fi

# 5. Ejecutar el playbook de Ansible
echo "Running Ansible playbook..."
ansible-playbook -i ./inventory.yml ./setup_project.yml --ask-become-pass

# 6. Verificar la instalaci�n
echo "Verifying installation..."
ls -la ~/multi_agent_novel_system/

echo "Setup completed successfully!"


# =====================================================
# ETAPA 2: INSTALACIÓN DE DEPENDENCIAS Y BACKEND RAG  
# =====================================================

# 1. Navegar al directorio del proyecto
cd ~/multi_agent_novel_system

# 2. Activar el entorno virtual
source novel_env/bin/activate

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias principales
pip install -r requirements.txt

# 5. Copiar archivo de configuración
cp .env.example .env

# 6. Editar configuración (ajustar rutas según tu sistema)
nano .env

# 7. Crear los archivos Python del sistema RAG
# (Copiar el contenido del artifact rag_implementation)

# Estructura de archivos a crear:
# rag/__init__.py (vacío)
# rag/document_processor.py
# rag/vector_store.py  
# rag/rag_manager.py
# llm_local/__init__.py (vacío)
# llm_local/llama_manager.py
# scripts/setup_env.py
# scripts/test_rag.py

# 8. Ejecutar configuración del entorno
python scripts/setup_env.py

# 9. Instalar modelo de embeddings (primera ejecución)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# 10. Probar el sistema RAG básico
python scripts/test_rag.py

# =====================================================
# COMANDOS DE VERIFICACI�N
# =====================================================

echo "=== Verificaci�n de la instalaci�n ==="

# Verificar estructura del proyecto (instalar tree si no existe)
if ! command -v tree &> /dev/null; then
    echo "Instalando tree para visualizaci�n de directorios..."
    sudo apt install -y tree
fi

echo "Estructura del proyecto:"
tree ~/multi_agent_novel_system -L 3 || ls -la ~/multi_agent_novel_system

# Verificar entorno virtual
echo "=== Verificando entorno virtual ==="
if [ -f ~/multi_agent_novel_system/novel_env/bin/activate ]; then
    source ~/multi_agent_novel_system/novel_env/bin/activate
    echo "Entorno virtual activado"
    
    # Verificar instalaci�n de dependencias
    echo "=== Verificando dependencias ==="
    pip list | grep -E "(langchain|chromadb|sentence-transformers|crewai|transformers|fastapi|uvicorn)" || echo "Algunas dependencias no encontradas"
    
    # Verificar ChromaDB
    echo "=== Verificando ChromaDB ==="
    python -c "import chromadb; print('ChromaDB OK')" || echo "ChromaDB no funciona"
    
    # Verificar sentence-transformers
    echo "=== Verificando SentenceTransformers ==="
    python -c "from sentence_transformers import SentenceTransformer; print('SentenceTransformers OK')" || echo "SentenceTransformers no funciona"
    
    # Verificar LangChain
    echo "=== Verificando LangChain ==="
    python -c "import langchain; print('LangChain OK')" || echo "LangChain no funciona"
    
    # Verificar CrewAI
    echo "=== Verificando CrewAI ==="
    python -c "import crewai; print('CrewAI OK')" || echo "CrewAI no funciona"
    
    deactivate
else
    echo "ERROR: Entorno virtual no encontrado en ~/multi_agent_novel_system/novel_env/"
    echo "Contenido del directorio:"
    ls -la ~/multi_agent_novel_system/
fi

echo "=== Verificaci�n completada ==="
# =====================================================
# INSTALACIÓN OPCIONAL: MODELO LLM LOCAL
# =====================================================

# Descargar modelo DeepSeek (ejemplo)
# mkdir -p ~/multi_agent_novel_system/llm_local/models
# cd ~/multi_agent_novel_system/llm_local/models

# Descargar modelo (ajustar URL según disponibilidad)
# wget https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf

# Actualizar .env con la ruta del modelo
echo "LLM_MODEL_PATH=./llm_local/models/Model.gguf" >> .env

# Probar con modelo LLM
python scripts/test_rag.py ./llm_local/models/model.gguf

# =====================================================
# ESTRUCTURA FINAL DEL PROYECTO
# =====================================================

# El proyecto debe tener esta estructura:
# multi_agent_novel_system/
# ├── agents/
# │   ├── __init__.py
# │   ├── crews/
# │   └── tools/
# ├── config/
# │   ├── __init__.py
# │   └── settings.py
# ├── data/
# │   ├── manuscripts/
# │   └── reference_docs/
# │       └── test_doc.txt
# ├── frontend/
# │   └── __init__.py
# ├── llm_local/
# │   ├── __init__.py
# │   ├── llama_manager.py
# │   └── models/ (opcional)
# ├── logs/
# ├── novel_env/ (entorno virtual)
# ├── orchestrator/
# │   └── __init__.py
# ├── outputs/
# │   ├── character_guide/
# │   ├── final_novel/
# │   ├── story_library/
# │   └── video_prompts/
# ├── rag/
# │   ├── __init__.py
# │   ├── document_processor.py
# │   ├── documents/
# │   ├── processed/
# │   ├── rag_manager.py
# │   ├── vector_store.py
# │   └── vectorstore/ (ChromaDB)
# ├── scripts/
# │   ├── setup_env.py
# │   └── test_rag.py
# ├── tests/
# ├── utils/
# │   └── __init__.py
# ├── .env
# ├── .env.example
# ├── activate_env.sh
# ├── README.md
# └── requirements.txt

# =====================================================
# COMANDOS DE TROUBLESHOOTING
# =====================================================

# Si hay problemas con ChromaDB:
pip uninstall chromadb
pip install chromadb==0.4.24

# Si hay problemas con llama-cpp-python:
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

# Para sistemas sin CUDA (solo CPU):
CMAKE_ARGS="-DLLAMA_CUDA=off" pip install llama-cpp-python --force-reinstall --no-cache-dir

# Verificar logs si algo falla:
tail -f logs/*.log

# Limpiar y reinstalar dependencias:
pip freeze > installed_packages.txt
pip uninstall -y -r installed_packages.txt
pip install -r requirements.txt

# Segunda Parte ------------------------------------------

# =====================================================
# ETAPA 3: INSTALACI�N DE AGENTES CrewAI
# =====================================================

# 1. Navegar al proyecto y activar entorno
cd ~/multi_agent_novel_system
source novel_env/bin/activate

# 2. Instalar dependencias adicionales para agentes
pip install nltk textblob

# 3. Descargar recursos de NLTK (ejecutar en Python)
python -c "
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    print('punkt ya descargado')
except LookupError:
    nltk.download('punkt')
    print('punkt descargado')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
    print('averaged_perceptron_tagger ya descargado')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
    print('averaged_perceptron_tagger descargado')
"

# 4. Crear estructura de archivos para agentes
mkdir -p agents/crews agents/tools

# 5. Crear archivos __init__.py
touch agents/__init__.py
touch agents/crews/__init__.py
touch agents/tools/__init__.py

# 6. Crear archivos de herramientas
# Copiar el contenido de los artifacts en estos archivos:

cat > agents/tools/__init__.py << 'EOF'
from .rag_tool import RAGTool
from .writing_tools import WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from .analysis_tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from .creative_tools import IdeaGenerator, VisualPromptGenerator

__all__ = [
    'RAGTool',
    'WritingAnalyzer', 
    'StyleAnalyzer',
    'CharacterAnalyzer',
    'ConsistencyChecker',
    'PacingAnalyzer', 
    'PlotAnalyzer',
    'IdeaGenerator',
    'VisualPromptGenerator'
]
EOF

# [NOTA: Aqu� necesitas copiar el contenido de los artifacts en los archivos correspondientes]
# - agents/tools/rag_tool.py
# - agents/tools/writing_tools.py  
# - agents/tools/analysis_tools.py
# - agents/tools/creative_tools.py
# - agents/crews/base_agent.py
# - agents/crews/lorekeeper.py
# - agents/crews/character_developer.py
# - agents/crews/plot_weaver.py
# - agents/crews/style_editor.py
# - agents/crews/visualizer.py
# - agents/crews/researcher.py
# - agents/crews/continuity_auditor.py
# - agents/crews/beta_reader.py
# - agents/crews/pacing_specialist.py
# - agents/crews/proofreader.py
# - agents/crews/innovation_scout.py
# - agents/agent_manager.py
# - agents/test_agents.py

# 7. Crear script de instalaci�n automatizada
cat > scripts/install_agents.py << 'EOF'
#!/usr/bin/env python3
"""Script para instalar y configurar los agentes"""

import sys
import os
import subprocess
from pathlib import Path

def install_nltk_data():
    """Instala datos necesarios de NLTK"""
    try:
        import nltk
        
        # Descargar recursos necesarios
        resources = ['punkt', 'averaged_perceptron_tagger', 'stopwords']
        
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'taggers/{resource}' if 'perceptron' in resource else f'corpora/{resource}')
                print(f'? {resource} ya disponible')
            except LookupError:
                print(f'?? Descargando {resource}...')
                nltk.download(resource, quiet=True)
                print(f'? {resource} descargado')
                
    except ImportError:
        print('? NLTK no est� instalado')
        return False
    
    return True

def verify_agent_structure():
    """Verifica que la estructura de agentes est� completa"""
    
    required_files = [
        'agents/__init__.py',
        'agents/tools/__init__.py',
        'agents/crews/__init__.py',
        'agents/agent_manager.py',
        'agents/test_agents.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print('? Archivos faltantes:')
        for file in missing_files:
            print(f'   - {file}')
        return False
    
    print('? Estructura de agentes verificada')
    return True

def main():
    print('?? Instalando sistema de agentes...')
    
    # Verificar que estamos en el directorio correcto
    if not Path('agents').exists():
        os.makedirs('agents/tools', exist_ok=True)
        os.makedirs('agents/crews', exist_ok=True)
    
    # Instalar datos de NLTK
    if install_nltk_data():
        print('? Datos de NLTK instalados')
    
    # Verificar estructura
    if verify_agent_structure():
        print('? Sistema de agentes listo')
    else:
        print('?? Algunos archivos faltan - revisar instalaci�n')
    
    print('\n?? Pr�ximos pasos:')
    print('1. Copiar los archivos de c�digo de los agents')
    print('2. Ejecutar: python agents/test_agents.py')
    print('3. Verificar que todos los agentes funcionan')

if __name__ == '__main__':
    main()
EOF

chmod +x scripts/install_agents.py

# 8. Ejecutar instalaci�n
python scripts/install_agents.py

# 9. Probar los agentes (despu�s de copiar archivos)
python agents/test_agents.py

# 10. Probar con manuscrito de ejemplo
python -c "
from agents.agent_manager import AgentManager
import sys
sys.path.append('.')

# Crear manager
manager = AgentManager()

# Manuscrito de prueba
test_manuscript = '''
El reino de Aethermoor se alzaba majestuoso entre monta�as nevadas.
Lyra Stormwind, la joven maga de cabello plateado, caminaba por los 
pasillos de cristal del palacio real. Su misi�n era clara: encontrar 
el grimorio perdido antes de que las Sombras del Vac�o consumieran 
toda la magia del reino.

El rey Aldrin Goldenheart la hab�a convocado al amanecer. Sus ojos 
dorados mostraban preocupaci�n mientras le explicaba la gravedad de la situaci�n.
'''

# Establecer manuscrito
manager.set_manuscript(test_manuscript)

# Obtener resumen
summary = manager.get_analysis_summary()
print('?? Test b�sico del sistema de agentes:')
print(f'   Manuscrito: {summary[\"manuscript_length\"]} caracteres')
print(f'   Agentes disponibles: {len(summary[\"available_agents\"])}')
print(f'   LLM disponible: {summary[\"llm_available\"]}')
print('? Sistema b�sico funcionando')
"

# =====================================================
# VERIFICACI�N DE LA INSTALACI�N
# =====================================================

echo "?? Verificando instalaci�n de Etapa 3..."

# Verificar estructura de directorios
echo "?? Verificando estructura:"
ls -la agents/
ls -la agents/tools/
ls -la agents/crews/

# Verificar importaciones Python
echo "?? Verificando importaciones:"
python -c "
try:
    from agents.tools import RAGTool
    print('? RAGTool importado correctamente')
except Exception as e:
    print(f'? Error importando RAGTool: {e}')

try:
    from agents.agent_manager import AgentManager
    print('? AgentManager importado correctamente')
except Exception as e:
    print(f'? Error importando AgentManager: {e}')

try:
    import nltk
    from textblob import TextBlob
    print('? Dependencias de NLP disponibles')
except Exception as e:
    print(f'? Error con dependencias NLP: {e}')
"

# Verificar herramientas disponibles
echo "?? Verificando herramientas:"
python -c "
from agents.tools import WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from agents.tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from agents.tools import IdeaGenerator, VisualPromptGenerator

tools = [
    WritingAnalyzer(),
    StyleAnalyzer(), 
    CharacterAnalyzer(),
    ConsistencyChecker(),
    PacingAnalyzer(),
    PlotAnalyzer(),
    IdeaGenerator(),
    VisualPromptGenerator()
]

print(f'? {len(tools)} herramientas creadas exitosamente')
for tool in tools:
    print(f'   - {tool.name}')
"

echo "? Verificaci�n de Etapa 3 completada"

# =====================================================
# COMANDOS DE TROUBLESHOOTING
# =====================================================

echo "??? Comandos de troubleshooting si hay problemas:"

echo "
# Si hay errores con NLTK:
python -c \"
import nltk
nltk.download('all')
\"

# Si hay errores con TextBlob:
pip uninstall textblob
pip install textblob

# Si hay errores con crewai_tools:
pip install crewai[tools]

# Para reinstalar todo:
pip uninstall crewai langchain langgraph
pip install crewai>=0.28.0 langchain>=0.1.0 langgraph>=0.0.40

# Para verificar versiones:
pip list | grep -E '(crewai|langchain|langgraph|nltk|textblob)'
"