#!/bin/bash
# ==================================================
# Ollama Native Installer for Ubuntu (No Docker)
# ==================================================
# This script installs Ollama and sets up persistent
# directories for data & models.
# ==================================================

set -e

echo "=== Updating system packages ==="
sudo apt update && sudo apt upgrade -y
sudo apt install curl git unzip -y

echo "=== Downloading Ollama .deb ==="
curl -fsSL https://ollama.com/download/ollama-linux-amd64.deb -o /tmp/ollama.deb

echo "=== Installing Ollama ==="
sudo apt install /tmp/ollama.deb -y

echo "=== Creating persistent directories ==="
sudo mkdir -p /var/lib/ollama
sudo mkdir -p /opt/ollama-models
sudo chown -R $USER:$USER /var/lib/ollama /opt/ollama-models

echo "=== Configuring systemd environment ==="
SERVICE_OVERRIDE_DIR="/etc/systemd/system/ollama.service.d"
sudo mkdir -p $SERVICE_OVERRIDE_DIR

cat <<EOF | sudo tee $SERVICE_OVERRIDE_DIR/override.conf
[Service]
Environment="OLLAMA_HOME=/var/lib/ollama"
Environment="OLLAMA_MODELS=/opt/ollama-models"
EOF

echo "=== Reloading systemd and enabling service ==="
sudo systemctl daemon-reexec
sudo systemctl enable ollama
sudo systemctl restart ollama

echo "=== Checking Ollama service status ==="
systemctl --no-pager status ollama | grep Active

echo "=== Verifying Ollama installation ==="
ollama --version || { echo "Ollama installation failed!"; exit 1; }

echo "=== Running a test model (llama3) ==="
ollama run llama3 || echo "⚠️ Test model failed, but Ollama is installed. You can add your own models in /opt/ollama-models"

echo "✅ Installation complete! Ollama is running on port 11434"
echo "   Data path:   /var/lib/ollama"
echo "   Models path: /opt/ollama-models"
