# Story Enhancer AI

Sistema modular para mejorar historias y gestionar documentos con RAG (Retrieval-Augmented Generation) usando Python y ChromaDB.

---

## 1. Requisitos Previos

- Ubuntu/Debian
- Python 3.11 o superior
- pip
- OpenSSH Server (opcional, para acceso remoto)

---

## 2. Instalación del Entorno

```bash
# Actualizar paquetes
sudo apt update

# Instalar OpenSSH Server
sudo apt install openssh-server -y

# Instalar herramientas de compatibilidad de scripts
sudo apt install dos2unix -y

# Verificar IP (opcional)
ip a
```

---

## 3. Preparar el Proyecto

```bash
# Descargar/extraer el proyecto
cd ~/Documents/Aget-Writer/story-enhancer-ai

# Dar permisos de ejecución a todos los scripts
sudo chmod +x *.sh
sudo dos2unix *.sh

# Instalar dependencias de Python
./Actualizar\ pip\ primero.sh
./requirenment.sh

# Crear estructura de carpetas y archivos
./folders_3.sh
./Entorno_Virtual_4.sh
./ConfiguracionGit_5.sh
./configuration_6.sh
./gitkeep_7.sh


Aget-Writer/story-enhancer-ai$
mkdir -p agents/{tools,prompts}
mkdir -p orchestrator
mkdir -p outputs/{novel,library,characters,prompts}
```

---

## 4. Crear y Activar Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

---

## 5. Instalación Completa del Proyecto

```bash
# Instalar todo de una vez
./instalar_completo.sh

# Verificar instalación
./verificar_mejorado.sh
```

---

## 6. Scripts de Prueba y Uso

- **Crear documentos de muestra**
```bash
python3 create_samples.py
```

- **Probar sistema RAG**
```bash
python3 test_rag.py
```

- **Procesar tus propios documentos**
```bash
python3 usar_mis_documentos.py
```

---

## 7. Notas

- Los documentos deben estar en `data/documents/` (soporte: `.txt` y `.docx`).  
- La carpeta `outputs/` contiene resultados de la ingesta y análisis de documentos.  
- Configura tu API key de OpenAI en `.env` si deseas usar embeddings de OpenAI, de lo contrario se usa modelo local.  

---

## 8. Estructura del Proyecto

```
story-enhancer-ai/
├── agents/
├── config/
│   ├── agent_configs.py
│   ├── app_config.py
│   └── rag_config.py
├── data/
│   ├── documents/
│   ├── manuscripts/
│   └── processed/
├── frontend/
├── orchestrator/
├── outputs/
│   ├── novels/
│   ├── libraries/
│   ├── characters/
│   └── video_prompts/
├── rag/
├── utils/
│   ├── file_handlers.py
│   ├── text_processors.py
│   └── validators.py
├── venv/
├── README.md
├── requirements.txt
└── varios scripts de instalación y prueba (.sh/.py)
```

---

## 9. Comandos Útiles

```bash
# Activar entorno virtual
source venv/bin/activate

# Listar documentos procesados
ls data/documents/

# Ejecutar pruebas
python3 test_rag.py
python3 usar_mis_documentos.py
```

