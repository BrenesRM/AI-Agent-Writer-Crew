# Actualizar repositorios y paquetes del sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias esenciales
sudo apt install -y build-essential curl wget git vim tree htop
sudo apt install -y software-properties-common apt-transport-https ca-certificates
sudo apt install -y libssl-dev libffi-dev libbz2-dev libreadline-dev libsqlite3-dev
sudo apt install -y python3-dev python3-pip python3-venv python3-setuptools
sudo apt install -y pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev