# Verificar versión actual de Python
python3 --version

# Si la versión es menor a 3.11, instalar desde deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils

# Crear alias para python3.11 (opcional)
echo 'alias python311=/usr/bin/python3.11' >> ~/.bashrc
source ~/.bashrc