#!/bin/bash
# ============================
# Setup script for local LLaMA agent
# ============================

set -e

echo "=== Step 1: Update system packages ==="
sudo apt update
sudo apt install -y build-essential cmake git python3 python3-pip

echo "=== Step 2: Install pipx (optional for CLI tools) ==="
sudo apt install -y pipx
pipx ensurepath