#!/bin/bash
# ============================
# Setup script for local LLaMA agent
# After it finishes:
# source ~/llama-venv/bin/activate
# cd ~/Documents/Aget-Writer/story-enhancer-ai/models
# ./agent_example.py
# ============================

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

echo "=== Step 4: Upgrade pip and install llama-cpp-python ==="
pip install --upgrade pip
pip install llama-cpp-python

echo "=== Step 5: Prepare models directory ==="
MODEL_DIR="$HOME/Documents/Aget-Writer/story-enhancer-ai/models"
mkdir -p "$MODEL_DIR"

# Check if the model exists
if [ ! -f "$MODEL_DIR/llama-3.2-1b-instruct-q8_0.gguf" ]; then
    echo "WARNING: LLaMA model not found in $MODEL_DIR"
    echo "Please download llama-3.2-1b-instruct-q8_0.gguf and place it there."
else
    echo "Model found: $MODEL_DIR/llama-3.2-1b-instruct-q8_0.gguf"
fi

echo "=== Step 6: Copy example scripts ==="
cp ./test_llama.py "$MODEL_DIR/"
cp ./agent_example.py "$MODEL_DIR/"

echo "=== Setup complete! ==="
echo "To activate your environment and run the agent:"
echo "  source $VENV_DIR/bin/activate"
echo "  cd $MODEL_DIR"
echo "  ./agent_example.py"
