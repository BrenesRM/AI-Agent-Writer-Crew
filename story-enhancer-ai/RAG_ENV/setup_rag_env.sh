#!/bin/bash
# =========================================
# Setup script for RAG_ENV - Story Enhancer AI
# =========================================

set -e

echo "=== Step 1: Update system packages ==="
sudo apt update
sudo apt install -y build-essential cmake git python3 python3-pip

echo "=== Step 2: Install pipx (optional for CLI tools) ==="
sudo apt install -y pipx
pipx ensurepath

echo "=== Step 3: Create virtual environment ==="
VENV_DIR="$HOME/llama-venv"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"


set -e

# 1️⃣ Define paths
PROJECT_DIR="$HOME/Documents/Aget-Writer/story-enhancer-ai/RAG_ENV"
VENV_DIR="$PROJECT_DIR/venv"

DATA_DIR="$PROJECT_DIR/data"
OUTPUTS_DIR="$PROJECT_DIR/outputs"
CONFIG_DIR="$PROJECT_DIR/config"

# 2️⃣ Update system packages and install Python venv tools
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# 3️⃣ Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at $VENV_DIR"
fi

# 4️⃣ Activate venv
source "$VENV_DIR/bin/activate"

# 5️⃣ Upgrade pip and install requirements
pip install --upgrade pip
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
    echo "Requirements installed."
else
    echo "WARNING: requirements.txt not found in $PROJECT_DIR"
fi

# 6️⃣ Export environment variables
export RAG_DATA_DIR="$DATA_DIR"
export RAG_OUTPUTS_DIR="$OUTPUTS_DIR"
export RAG_CONFIG_DIR="$CONFIG_DIR"

echo "Environment variables set:"
echo "RAG_DATA_DIR=$RAG_DATA_DIR"
echo "RAG_OUTPUTS_DIR=$RAG_OUTPUTS_DIR"
echo "RAG_CONFIG_DIR=$RAG_CONFIG_DIR"

echo "RAG_ENV is ready. To activate the environment later, run:"
echo "source $VENV_DIR/bin/activate"
