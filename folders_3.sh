#!/bin/bash

# Crear directorio principal del proyecto
mkdir -p ~/story-enhancer-ai
cd ~/story-enhancer-ai || exit

# Crear estructura modular de carpetas
mkdir -p {agents,rag,frontend,orchestrator,utils,data,outputs,tests,config}
mkdir -p data/{documents,manuscripts,processed}
mkdir -p outputs/{novels,libraries,characters,video_prompts}

# Crear archivos base
touch README.md .env .gitignore requirements.txt
touch config/{agent_configs.py,rag_config.py,app_config.py}
touch utils/{file_handlers.py,text_processors.py,validators.py}
