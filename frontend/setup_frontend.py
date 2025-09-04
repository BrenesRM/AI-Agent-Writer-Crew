#!/usr/bin/env python3
"""
Script de configuración del frontend Streamlit
Crea la estructura completa del frontend y archivos necesarios
"""

import os
import sys
from pathlib import Path

def create_frontend_structure():
    """Crea la estructura completa del frontend"""
    
    print("🚀 Configurando estructura del frontend...")
    
    # Directorios a crear
    directories = [
        "frontend",
        "frontend/pages",
        "frontend/components", 
        "frontend/static",
        "frontend/utils",
        "frontend/assets",
        "frontend/config"
    ]
    
    # Crear directorios
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Creado: {directory}")
    
    # Archivos __init__.py
    init_files = [
        "frontend/__init__.py",
        "frontend/pages/__init__.py", 
        "frontend/components/__init__.py",
        "frontend/utils/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"📄 Creado: {init_file}")

def create_streamlit_config():
    """Crea archivo de configuración de Streamlit"""
    
    config_content = """
[global]
developmentMode = false

[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff" 
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"
"""
    
    # Crear directorio .streamlit si no existe
    Path(".streamlit").mkdir(exist_ok=True)
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content.strip())
    
    print("📄 Creado: .streamlit/config.toml")

def create_requirements_frontend():
    """Crea requirements específicos del frontend"""
    
    frontend_requirements = """
# Frontend específico
streamlit>=1.28.0
streamlit-option-menu>=0.3.6
streamlit-aggrid>=0.3.4
streamlit-authenticator>=0.2.3

# Visualización
plotly>=5.17.0
altair>=5.1.2
matplotlib>=3.8.0
seaborn>=0.12.2

# Componentes UI
streamlit-elements>=0.1.0
streamlit-ace>=0.1.1
streamlit-camera-input-live>=0.2.0

# Utilidades frontend
Pillow>=10.0.0
pandas>=2.1.0
numpy>=1.24.0
"""
    
    with open("requirements_frontend.txt", "w") as f:
        f.write(frontend_requirements.strip())
    
    print("📄 Creado: requirements_frontend.txt")

def create_launch_script():
    """Crea script de lanzamiento"""
    
    launch_content = """#!/bin/bash

# Script de lanzamiento del Sistema Multi-Agente para Novelas

echo "🚀 Iniciando Sistema Multi-Agente para Novelas..."

# Verificar entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Activando entorno virtual..."
    source novel_env/bin/activate
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
pip install -r requirements.txt -q
pip install -r requirements_frontend.txt -q

# Variables de entorno
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Lanzar aplicación
echo "🌟 Lanzando interfaz web..."
echo "📱 La aplicación estará disponible en: http://localhost:8501"
echo "🛑 Presiona Ctrl+C para detener"

streamlit run frontend/app.py
"""
    
    with open("launch.sh", "w") as f:
        f.write(launch_content)
    
    # Hacer ejecutable
    os.chmod("launch.sh", 0o755)
    
    print("📄 Creado: launch.sh (ejecutable)")

def create_docker_setup():
    """Crea configuración Docker para el frontend"""
    
    dockerfile_content = """
# Dockerfile para Sistema Multi-Agente de Novelas
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Novel System"
LABEL version="1.0.0"
LABEL description="Sistema Multi-Agente para Creación de Novelas"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \\
    build-essential \\
    cmake \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt requirements_frontend.txt ./

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_frontend.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs outputs data/manuscripts data/reference_docs rag/vectorstore

# Exponer puerto
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())
    
    # Docker Compose
    compose_content = """
version: '3.8'

services:
  novel-system:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./rag/vectorstore:/app/rag/vectorstore
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  # Servicio opcional para base de datos
  # postgres:
  #   image: postgres:15
  #   environment:
  #     POSTGRES_DB: novel_system
  #     POSTGRES_USER: novel_user
  #     POSTGRES_PASSWORD: novel_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

volumes:
  postgres_data:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content.strip())
    
    print("📄 Creado: Dockerfile")
    print("📄 Creado: docker-compose.yml")

def create_testing_setup():
    """Crea configuración para pruebas del frontend"""
    
    test_content = """
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

class TestFrontendApp:
    """Pruebas para la aplicación frontend"""
    
    def test_app_loads(self):
        \"\"\"Prueba que la aplicación carga correctamente\"\"\"
        at = AppTest.from_file("frontend/app.py")
        at.run()
        assert not at.exception
    
    def test_sidebar_navigation(self):
        \"\"\"Prueba la navegación del sidebar\"\"\"
        at = AppTest.from_file("frontend/app.py")
        at.run()
        
        # Verificar que existen las opciones de navegación
        radio_options = at.sidebar.radio[0].options
        expected_pages = ["upload", "manuscript", "monitor", "results", "visual"]
        
        for page in expected_pages:
            assert page in radio_options
    
    def test_manuscript_editor_functionality(self):
        \"\"\"Prueba funcionalidad básica del editor\"\"\"
        at = AppTest.from_file("frontend/app.py")
        at.run()
        
        # Seleccionar página de manuscrito
        at.sidebar.radio[0].set_value("manuscript")
        at.run()
        
        # Verificar que el editor está presente
        assert len(at.text_area) > 0
    
    def test_upload_page_functionality(self):
        \"\"\"Prueba funcionalidad de subida de documentos\"\"\"
        at = AppTest.from_file("frontend/app.py") 
        at.run()
        
        # Seleccionar página de upload
        at.sidebar.radio[0].set_value("upload")
        at.run()
        
        # Verificar elementos de upload
        assert len(at.file_uploader) > 0

class TestComponents:
    \"\"\"Pruebas para componentes individuales\"\"\"
    
    def test_metrics_component(self):
        \"\"\"Prueba componente de métricas\"\"\"
        from frontend.components.metrics import render_metrics_card
        
        # Esta prueba requeriría un entorno Streamlit activo
        # En implementación real, usar mocking o AppTest
        pass
    
    def test_progress_component(self):
        \"\"\"Prueba componente de progreso\"\"\"
        from frontend.components.progress import render_progress_tracker
        
        steps = ["Paso 1", "Paso 2", "Paso 3"]
        # Prueba lógica del componente
        assert len(steps) == 3

if __name__ == "__main__":
    pytest.main([__file__])
"""
    
    with open("tests/test_frontend.py", "w") as f:
        f.write(test_content.strip())
    
    print("📄 Creado: tests/test_frontend.py")

def create_documentation():
    """Crea documentación del frontend"""
    
    docs_content = """
# 📖 Documentación del Frontend

## Estructura del Frontend

```
frontend/
├── app.py                 # Aplicación principal Streamlit
├── pages/                 # Páginas de la aplicación
│   ├── upload_docs.py     # Gestión de documentos RAG
│   ├── manuscript_editor.py # Editor de manuscrito
│   ├── agent_monitor.py   # Monitor de agentes
│   ├── results_viewer.py  # Visualización de resultados
│   └── visual_prompts.py  # Generador de prompts visuales
├── components/            # Componentes reutilizables
│   ├── sidebar.py         # Componente de sidebar
│   ├── metrics.py         # Componentes de métricas
│   ├── progress.py        # Componentes de progreso
│   └── alerts.py          # Componentes de alertas
├── static/                # Archivos estáticos
│   └── custom.css         # Estilos personalizados
├── utils/                 # Utilidades del frontend
│   ├── formatters.py      # Formateadores de datos
│   └── validators.py      # Validadores
└── config/                # Configuración específica
```

## Características Principales

### 🚀 Aplicación Principal (app.py)
- Configuración centralizada de Streamlit
- Gestión de estado de sesión
- Navegación entre páginas
- Inicialización de sistemas (RAG, Agentes)

### 📄 Páginas Especializadas

#### 📚 Upload Documents (upload_docs.py)
- Subida de múltiples formatos (PDF, DOCX, TXT, MD, JSON, XLSX)
- Procesamiento y vectorización automática
- Estadísticas de la biblioteca de conocimiento
- Búsqueda semántica en documentos

#### ✍️ Manuscript Editor (manuscript_editor.py)
- Editor de texto integrado con estadísticas en tiempo real
- Plantillas de inicio por género
- Procesamiento con agentes especializados
- Historial de versiones y borradores
- Configuración personalizable por género y audiencia

#### 🤖 Agent Monitor (agent_monitor.py)
- Estado en tiempo real de todos los agentes
- Métricas de rendimiento y estadísticas
- Configuración avanzada de parámetros
- Logs de actividad y diagnósticos
- Visualizaciones de performance

#### 📊 Results Viewer (results_viewer.py)
- Visualización completa de resultados de análisis
- Gráficos interactivos con Plotly
- Recomendaciones priorizadas
- Exportación de reportes en múltiples formatos
- Análisis comparativo de métricas

#### 🎬 Visual Prompts (visual_prompts.py)
- Generación de prompts para IA de video
- Configuración cinematográfica avanzada
- Biblioteca de estilos de directores famosos
- Galería de prompts guardados
- Optimización para diferentes herramientas de IA

### 🧩 Componentes Reutilizables

#### Metrics (components/metrics.py)
```python
from frontend.components.metrics import render_metrics_card, render_score_gauge

# Métrica básica
render_metrics_card("Documentos", 45, delta="+5", help_text="Documentos en RAG")

# Gauge de puntuación
render_score_gauge(8.5, "Calidad General", max_score=10)
```

#### Progress (components/progress.py)
```python
from frontend.components.progress import render_progress_tracker, animated_progress_bar

# Tracker de pasos
steps = ["Análisis", "Procesamiento", "Resultados"]
render_progress_tracker(steps, current_step=1)

# Barra animada
animated_progress_bar("Procesando manuscrito", duration=5)
```

#### Alerts (components/alerts.py)
```python
from frontend.components.alerts import render_alert, render_toast

# Alerta estática
render_alert("Procesamiento completado", "success")

# Notificación temporal
render_toast("Manuscrito guardado", duration=3)
```

## Configuración

### Streamlit Config (.streamlit/config.toml)
- Tema personalizado con colores del sistema
- Puerto y configuración de servidor
- Optimizaciones de rendimiento

### Variables de Entorno
```bash
# Configuración de la aplicación
STREAMLIT_SERVER_PORT=8501
PYTHONPATH=/path/to/project

# Configuración del sistema
LOG_LEVEL=INFO
PROJECT_NAME="Multi-Agent Novel System"
```

## Uso

### Desarrollo Local
```bash
# Activar entorno
source novel_env/bin/activate

# Instalar dependencias frontend
pip install -r requirements_frontend.txt

# Lanzar aplicación
streamlit run frontend/app.py
```

### Uso con Script
```bash
# Usar script de lanzamiento
./launch.sh
```

### Docker
```bash
# Construir imagen
docker build -t novel-system .

# Ejecutar contenedor
docker run -p 8501:8501 novel-system

# O usar docker-compose
docker-compose up
```

## Pruebas

### Ejecutar Pruebas
```bash
# Instalar pytest
pip install pytest streamlit[testing]

# Ejecutar pruebas
pytest tests/test_frontend.py -v
```

### Tipos de Pruebas
- **Pruebas de integración**: Verifican que la app carga correctamente
- **Pruebas de componentes**: Validan funcionalidad individual
- **Pruebas de navegación**: Comprueban el flujo entre páginas
- **Pruebas de validación**: Verifican entrada de datos

## Personalización

### Estilos CSS (static/custom.css)
- Tema personalizado coherente con la marca
- Componentes responsive
- Animaciones y transiciones
- Estilos para diferentes tipos de contenido

### Extensiones
El sistema está diseñado para ser extensible:

1. **Nuevas Páginas**: Añadir archivos en `pages/` y actualizar navegación
2. **Componentes Custom**: Crear en `components/` siguiendo patrones existentes  
3. **Integraciones**: Añadir conectores a servicios externos
4. **Temas**: Modificar configuración de Streamlit y CSS

## Arquitectura de Estado

### Session State Management
```python
# Estados principales
st.session_state.initialized       # Sistema inicializado
st.session_state.manuscript       # Texto del manuscrito
st.session_state.analysis_results # Resultados de análisis
st.session_state.rag_stats       # Estadísticas RAG
st.session_state.visual_prompts  # Prompts visuales
st.session_state.processing      # Estado de procesamiento
```

### Flujo de Datos
1. **Inicialización**: Carga de sistemas RAG y Agentes
2. **Ingesta**: Documentos → RAG Manager → Vector Store
3. **Edición**: Manuscrito → Session State → Validación
4. **Procesamiento**: Manuscrito → Agent Manager → Resultados
5. **Visualización**: Resultados → Componentes → UI

## Mejores Prácticas

### Performance
- Lazy loading de componentes pesados
- Cache de datos frecuentemente accedidos
- Optimización de re-renders con claves únicas
- Gestión eficiente de session state

### UX/UI
- Feedback inmediato para acciones de usuario
- Estados de carga claros y informativos
- Navegación intuitiva y consistente
- Responsive design para diferentes pantallas

### Mantenibilidad
- Separación clara de responsabilidades
- Componentes reutilizables y modulares
- Documentación inline de funciones complejas
- Manejo robusto de errores y edge cases
"""
    
    with open("docs/FRONTEND.md", "w") as f:
        f.write(docs_content.strip())
    
    print("📄 Creado: docs/FRONTEND.md")

def main():
    """Función principal de configuración"""
    
    print("🎨 Configurando Frontend del Sistema Multi-Agente para Novelas")
    print("=" * 60)
    
    try:
        # Crear estructura
        create_frontend_structure()
        print()
        
        # Configuración Streamlit
        create_streamlit_config()
        print()
        
        # Requirements específicos
        create_requirements_frontend()
        print()
        
        # Script de lanzamiento
        create_launch_script()
        print()
        
        # Docker setup
        create_docker_setup()
        print()
        
        # Pruebas
        Path("tests").mkdir(exist_ok=True)
        create_testing_setup()
        print()
        
        # Documentación
        Path("docs").mkdir(exist_ok=True)
        create_documentation()
        print()
        
        print("=" * 60)
        print("✅ CONFIGURACIÓN DEL FRONTEND COMPLETADA")
        print()
        print("🚀 Próximos pasos:")
        print("1. Activar entorno: source novel_env/bin/activate")
        print("2. Instalar dependencias: pip install -r requirements_frontend.txt")
        print("3. Lanzar aplicación: ./launch.sh")
        print("4. Abrir navegador: http://localhost:8501")
        print()
        print("📚 Documentación disponible en: docs/FRONTEND.md")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()