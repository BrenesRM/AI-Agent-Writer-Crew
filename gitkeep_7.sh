#!/bin/bash
set -e

# Crear estructura de carpetas si no existe
mkdir -p data/documents
mkdir -p data/manuscripts
mkdir -p outputs/novels
mkdir -p outputs/libraries
mkdir -p outputs/characters
mkdir -p outputs/video_prompts

# Crear archivos .gitkeep en carpetas vacías
touch data/documents/.gitkeep
touch data/manuscripts/.gitkeep
touch outputs/novels/.gitkeep
touch outputs/libraries/.gitkeep
touch outputs/characters/.gitkeep
touch outputs/video_prompts/.gitkeep
