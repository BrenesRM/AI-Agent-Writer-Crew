
# Estado del Proyecto: Sistema Multi-Agente para Novelas

## Avance actual: 85%

### Orquestación LangGraph
- El grafo de flujo de trabajo está completamente implementado y validado.
- Cada agente/nodo está encapsulado en su propia clase, facilitando la extensión y el mantenimiento.
- Tipos de nodos claros (análisis, generación, validación, consolidación) mediante Enum.
- Dependencias explícitas entre nodos, permitiendo ejecución secuencial y paralela.
- Validación de grafo: verificación de ciclos y dependencias inexistentes.
- Ejemplo de lógica de ejecución: cada nodo simula el análisis y retorna resultados estructurados, listos para integración con agentes reales.
- Gestión de grupos paralelos para optimizar la ejecución de nodos independientes.
- Logging y manejo de errores robusto.

#### Sugerencias menores
Las siguientes acciones optimizarán la orquestación y facilitarán la escalabilidad del sistema:
- Conecta los métodos `execute` de cada nodo con la lógica de los agentes reales para pasar de simulación a producción.
- Al agregar nuevos agentes, crea su clase correspondiente y añádela en la inicialización del grafo para integrarlos automáticamente al flujo.
- Si tu flujo requiere combinar resultados de varios agentes antes de la salida final, implementa nodos de consolidación para centralizar y procesar esos resultados.

---


# AI-Agent-Writer-Crew

## Descripción

**AI-Agent-Writer-Crew** es un sistema multi-agente modular diseñado para asistir en la escritura, análisis y mejora de novelas. Utiliza agentes especializados y herramientas avanzadas para automatizar tareas creativas y técnicas, permitiendo la generación iterativa de manuscritos de alta calidad.

## Características principales

- **Agentes especializados:**  
   11 agentes, cada uno enfocado en áreas clave como desarrollo de personajes, trama, estilo, visualización, investigación, auditoría de continuidad, ritmo, corrección, innovación y lore.

- **Herramientas integradas:**  
   Análisis de escritura, estilo, personajes, consistencia, ritmo, trama, generación de ideas, prompts visuales y búsqueda semántica (RAG).

- **Gestión centralizada:**  
   El `AgentManager` coordina la ejecución de los agentes y la agregación de resultados.

- **Orquestación avanzada:**  
   Flujo de trabajo definido con LangGraph, permitiendo ciclos iterativos de mejora y colaboración entre agentes.

- **Sistema RAG:**  
   Ingesta y búsqueda semántica de documentos para enriquecer el proceso creativo.

- **Integración con LLM locales:**  
   Soporte para modelos como Llama para generación y análisis de texto.

- **Frontend interactivo:**  
   Interfaz planeada con Streamlit o Gradio para facilitar la interacción con el sistema.

- **Generadores de salida:**  
   Producción de manuscritos, bibliotecas de lore, guías de personajes y prompts visuales.

## Estructura del proyecto

```
agents/
   crews/                # Definición de agentes especializados
   tools/                # Herramientas de análisis y creatividad
   agent_manager.py      # Coordinador central de agentes
orchestrator/
   workflow_graph.py     # Orquestación del flujo de trabajo
rag/
   document_processor.py # Ingesta de documentos
   vector_store.py       # Almacenamiento vectorial
   rag_manager.py        # Gestión del sistema RAG
llm_local/
   llama_manager.py      # Integración con modelos LLM locales
frontend/               # Interfaz de usuario (Streamlit/Gradio)
outputs/
   generators/           # Generadores de manuscritos y recursos
README.md               # Documentación principal
```

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/AI-Agent-Writer-Crew.git
    ```
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Configura los agentes y herramientas según tus necesidades.
2. Ejecuta el flujo de trabajo principal desde el orquestador.
3. Accede a la interfaz frontend para interactuar con el sistema.

## Ejemplo de uso

1. **Preparar el manuscrito inicial:**  
    Coloca tu borrador o documento en la carpeta `inputs/`.

2. **Ejecutar el sistema multi-agente:**  
    Desde la terminal, ejecuta el orquestador principal:
    ```bash
    python orchestrator/workflow_graph.py
    ```

3. **Interactuar con los resultados:**  
    - Revisa los análisis y mejoras generados en la carpeta `outputs/`.
    - Accede a la interfaz gráfica (si está habilitada):
       ```bash
       streamlit run frontend/app.py
       ```
    - Explora los informes de agentes, guías de personajes, prompts visuales y manuscritos mejorados.

4. **Iterar y mejorar:**  
    Puedes ajustar los parámetros de los agentes en sus archivos de configuración y volver a ejecutar el flujo para obtener nuevas versiones y sugerencias.

---

Este ejemplo te guía para aprovechar el sistema desde la preparación del texto hasta la revisión de los resultados generados por los agentes.

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para sugerencias y mejoras.

## Licencia

Este proyecto está bajo la licencia MIT.
## ? ETAPA 2 COMPLETADA: Backend RAG

### Componentes Implementados:

#### ?? Procesador de Documentos (`rag/document_processor.py`)
- **Formatos soportados**: PDF, DOCX, TXT, MD, JSON, XLSX
- **Chunking inteligente**: RecursiveCharacterTextSplitter
- **Metadatos completos**: source, doc_type, chunk_index
- **Manejo de errores robusto**

#### ??? Vector Store (`rag/vector_store.py`)
- **ChromaDB**: Almacenamiento vectorial persistente
- **SentenceTransformers**: Embeddings locales (all-MiniLM-L6-v2)
- **Búsqueda por similitud**: Con filtros por tipo de documento
- **Gestión de colecciones**: CRUD completo

#### ?? RAG Manager (`rag/rag_manager.py`)
- **API unificada**: Interfaz simple para todo el sistema RAG
- **Ingesta individual y masiva**: Archivos y directorios
- **Consultas contextuales**: Retorna contexto + fuentes
- **Estadísticas**: Monitoreo del sistema

#### ?? LLM Local (`llm_local/llama_manager.py`)
- **llama.cpp integration**: Soporte para modelos GGUF
- **Chat completion**: API compatible con OpenAI
- **Contexto RAG**: Generación con documentos de referencia
- **Configuración flexible**: Temperatura, tokens, contexto

#### ?? Scripts de Prueba
- **`scripts/test_rag.py`**: Pruebas completas del sistema
- **`scripts/setup_env.py`**: Configuración automática del entorno
- **Documentos de prueba**: Generación automática

### Capacidades Actuales:
- ? Ingestar documentos de 7 formatos diferentes
- ? Búsqueda semántica en documentos
- ? Integración con modelos LLM locales
- ? Sistema de logging y monitoreo
- ? API completa para consultas RAG
- ? Persistencia de vector store

---

## ? ETAPA 3 COMPLETADA: Definición de Agentes CrewAI

### ??? Sistema de Herramientas (`agents/tools/`)

#### Herramientas RAG y Análisis:
- **RAGTool**: Consultas a la base de conocimiento
- **WritingAnalyzer**: Estadísticas de escritura y métricas
- **StyleAnalyzer**: Análisis de tono, perspectiva y estilo
- **CharacterAnalyzer**: Identificación y análisis de personajes

#### Herramientas de Verificación:
- **ConsistencyChecker**: Detecta contradicciones e inconsistencias
- **PacingAnalyzer**: Evalúa ritmo y flujo narrativo
- **PlotAnalyzer**: Analiza estructura de trama y elementos narrativos

#### Herramientas Creativas:
- **IdeaGenerator**: Genera ideas creativas contextuales para personajes, tramas y escenarios
- **VisualPromptGenerator**: Convierte escenas en prompts cinematográficos para video AI

### ?? Agentes Especializados (`agents/crews/`)

#### Agentes Principales:
1. **LorekeeperAgent** - Guardián del Conocimiento
   - Mantiene coherencia del mundo narrativo
   - Verifica reglas mágicas y lore
   - Consulta documentos de referencia

2. **CharacterDeveloperAgent** - Arquitecto de Personajes  
   - Desarrolla personajes tridimensionales
   - Crea arcos narrativos significativos
   - Analiza motivaciones y relaciones

3. **PlotWeaverAgent** - Maestro de la Narrativa
   - Diseña tramas cautivadoras
   - Optimiza estructura narrativa
   - Balancea tensión y ritmo

4. **StyleEditorAgent** - Maestro del Estilo Literario
   - Perfecciona voz narrativa
   - Mantiene consistencia tonal
   - Mejora fluidez de la prosa

5. **VisualizerAgent** - Director Cinematográfico Virtual
   - Crea prompts visuales detallados
   - Traduce escenas a descripciones cinematográficas
   - Optimiza para generación de video AI

#### Agentes Especializados:
6. **ResearcherAgent** - Investigador y Verificador
   - Busca información histórica y cultural
   - Enriquece narrativa con detalles auténticos
   - Verifica precisión de referencias

7. **ContinuityAuditorAgent** - Guardián de la Consistencia
   - Verifica continuidad narrativa completa
   - Detecta inconsistencias en timelines
   - Mantiene coherencia de personajes

8. **BetaReaderAgent** - Voz del Lector Target
   - Simula experiencia de diferentes lectores
   - Evalúa engagement y claridad
   - Proporciona feedback desde perspectiva del público

9. **PacingSpecialistAgent** - Maestro del Ritmo
   - Optimiza ritmo narrativo
   - Balancea acción, tensión y reflexión
   - Mejora flujo de lectura

10. **ProofreaderAgent** - Guardián de la Calidad Final
    - Corrección gramatical y ortográfica
    - Verificación de puntuación y formato
    - Asegura calidad técnica impecable

11. **InnovationScoutAgent** - Explorador de Fronteras Creativas
    - Identifica oportunidades de innovación
    - Sugiere giros creativos originales
    - Propone combinaciones de género únicas

### ?? Sistema de Gestión (`agents/agent_manager.py`)

#### Capacidades del AgentManager:
- **Inicialización automática**: 11 agentes especializados
- **Integración LLM**: Soporte para modelos locales
- **Fases de análisis**: 6 fases estructuradas de mejora
- **Análisis completo**: Pipeline automatizado end-to-end
- **Gestión de estado**: Tracking de progreso y resultados

#### Fases de Análisis Implementadas:
1. **Worldbuilding**: Lorekeeper + Researcher + Continuity Auditor
2. **Character Development**: Character Developer + Beta Reader  
3. **Plot Structure**: Plot Weaver + Pacing Specialist + Innovation Scout
4. **Style Refinement**: Style Editor + Beta Reader
5. **Visual Creation**: Visualizer
6. **Quality Assurance**: Proofreader + Continuity Auditor

### ?? Sistema de Pruebas (`agents/test_agents.py`)
- **Pruebas de inicialización**: Verificación de todos los agentes
- **Pruebas de herramientas**: Validación de funcionalidades
- **Pruebas de análisis**: Pipeline completo con manuscrito de ejemplo
- **Integración LLM**: Pruebas con modelo local cuando disponible

---

## ?? PRÓXIMAS ETAPAS

### ETAPA 4: Orquestación LangGraph
```
orchestrator/
+-- coordinator.py          # Coordinador principal
+-- workflow_graph.py       # Definición del grafo de flujo
+-- state_manager.py        # Gestión de estado entre iteraciones  
+-- iteration_controller.py # Control de ciclos iterativos
+-- decision_engine.py      # Motor de decisiones para flujo
```

### ETAPA 5: Frontend Streamlit/Gradio
```
frontend/
+-- app.py                  # Aplicación principal
+-- components/             # Componentes reutilizables
+-- pages/                  # Páginas de la aplicación
¦   +-- upload_docs.py      # Subida de documentos
¦   +-- manuscript_editor.py # Editor de manuscrito
¦   +-- agent_monitor.py    # Monitoreo de agentes
¦   +-- results_viewer.py   # Visualización de resultados
+-- static/                 # Recursos estáticos
```

### ETAPA 6: Generación de Outputs
```
outputs/
+-- generators/
¦   +-- novel_generator.py      # Generador de novela final
¦   +-- library_generator.py    # Biblioteca de lore
¦   +-- character_generator.py  # Guía de personajes
¦   +-- visual_generator.py     # Pack de prompts visuales
+-- templates/              # Plantillas de formato
+-- exporters/             # Exportadores (MD, DOCX, JSON)
```

---

## ?? Estructura Actual del Proyecto

```
multi_agent_novel_system/
+-- agents/                    # ? Completo
¦   +-- crews/                 # ? 11 agentes especializados
¦   +-- tools/                 # ? 9 herramientas integradas  
¦   +-- agent_manager.py       # ? Gestor central
¦   +-- test_agents.py         # ? Suite de pruebas
+-- config/                    # ? Completo
+-- data/                      # ? Completo
+-- frontend/                  # ?? Pendiente (Etapa 5)
+-- llm_local/                 # ? Completo
+-- orchestrator/              # ?? Pendiente (Etapa 4)
+-- outputs/                   # ? Estructura base
+-- rag/                       # ? Completo
+-- scripts/                   # ? Completo + scripts agentes
+-- utils/                     # ? Estructura
+-- novel_env/                 # ? Entorno virtual
+-- .env                       # ? Configuración
+-- requirements.txt           # ? Dependencias actualizadas
```

---

## ?? Comandos para Continuar

### Instalar Etapa 3:
```bash
cd ~/multi_agent_novel_system
source novel_env/bin/activate

# Instalar dependencias adicionales
pip install nltk textblob

# Configurar recursos NLP
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Crear archivos de agentes (copiar de artifacts)
# Ejecutar pruebas
python agents/test_agents.py
```

### Probar Sistema Completo:
```bash
# Test básico sin LLM
python -c "
from agents.agent_manager import AgentManager
manager = AgentManager()
print(f'Agentes disponibles: {len(manager.list_agents())}')
"

# Test con manuscrito
python -c "
from agents.agent_manager import AgentManager
manager = AgentManager()

manuscript = '''
En el reino de Aethermoor, la maga Lyra Stormwind descubrió un 
antiguo grimorio que podría salvar al reino de las Sombras del Vacío.
'''

manager.set_manuscript(manuscript)
summary = manager.get_analysis_summary()
print('Sistema funcionando:', summary)
"
```

---

## ?? Estado General: 50% Completado

- ? **Infraestructura**: 100%
- ? **Sistema RAG**: 100% 
- ? **LLM Local**: 100%
- ? **Agentes CrewAI**: 100%
- ?? **Orquestación**: 0% (Siguiente)
- ?? **Frontend**: 0%
- ?? **Outputs**: 20% (estructura)

**Total estimado para producción**: 7 etapas
**Completadas**: 3 etapas  
**Siguiente**: Etapa 4 - Orquestación con LangGraph

### ?? Logros de la Etapa 3:
- **11 agentes especializados** con roles únicos y expertise específico
- **9 herramientas integradas** para análisis completo de manuscritos
- **6 fases de análisis** estructuradas y automatizadas
- **Sistema de gestión unificado** con AgentManager
- **Pipeline completo** desde análisis hasta generación de recomendaciones
- **Integración RAG+LLM** en todas las herramientas de agentes
- **Suite de pruebas comprehensiva** para validación del sistema

El sistema ahora puede analizar manuscritos de forma inteligente usando múltiples perspectivas especializadas, desde coherencia de worldbuilding hasta optimización de ritmo narrativo.# Estado del Proyecto: Sistema Multi-Agente para Novelas

## ? ETAPA 1 COMPLETADA: Preparación del Entorno

### Componentes Implementados:
- **Ansible Playbook**: Automatización completa de instalación
- **Estructura de proyecto**: 15 directorios organizados modularmente
- **Configuración base**: `.env.example`, `requirements.txt`, `README.md`
- **Scripts de utilidad**: `activate_env.sh`, `setup_env.py`
- **Sistema de configuración**: `config/settings.py` con Pydantic

### Tecnologías Configuradas:
- ? Python 3.11+ 
- ? Entorno virtual automático
- ? Dependencias del sistema (build-essential, cmake, etc.)
- ? Estructura modular SOLID

---

## ? ETAPA 2 COMPLETADA: Backend RAG

### Componentes Implementados:

#### ?? Procesador de Documentos (`rag/document_processor.py`)
- **Formatos soportados**: PDF, DOCX, TXT, MD, JSON, XLSX
- **Chunking inteligente**: RecursiveCharacterTextSplitter
- **Metadatos completos**: source, doc_type, chunk_index
- **Manejo de errores robusto**

#### ??? Vector Store (`rag/vector_store.py`)
- **ChromaDB**: Almacenamiento vectorial persistente
- **SentenceTransformers**: Embeddings locales (all-MiniLM-L6-v2)
- **Búsqueda por similitud**: Con filtros por tipo de documento
- **Gestión de colecciones**: CRUD completo

#### ?? RAG Manager (`rag/rag_manager.py`)
- **API unificada**: Interfaz simple para todo el sistema RAG
- **Ingesta individual y masiva**: Archivos y directorios
- **Consultas contextuales**: Retorna contexto + fuentes
- **Estadísticas**: Monitoreo del sistema

#### ?? LLM Local (`llm_local/llama_manager.py`)
- **llama.cpp integration**: Soporte para modelos GGUF
- **Chat completion**: API compatible con OpenAI
- **Contexto RAG**: Generación con documentos de referencia
- **Configuración flexible**: Temperatura, tokens, contexto

#### ?? Scripts de Prueba
- **`scripts/test_rag.py`**: Pruebas completas del sistema
- **`scripts/setup_env.py`**: Configuración automática del entorno
- **Documentos de prueba**: Generación automática

### Capacidades Actuales:
- ? Ingestar documentos de 7 formatos diferentes
- ? Búsqueda semántica en documentos
- ? Integración con modelos LLM locales
- ? Sistema de logging y monitoreo
- ? API completa para consultas RAG
- ? Persistencia de vector store

---

## ?? PRÓXIMAS ETAPAS

### ETAPA 3: Definición de Agentes CrewAI
```
agents/
+-- crews/
¦   +-- lorekeeper.py
¦   +-- character_developer.py
¦   +-- plot_weaver.py
¦   +-- style_editor.py
¦   +-- visualizer.py
+-- tools/
¦   +-- rag_tool.py
¦   +-- writing_tools.py
¦   +-- analysis_tools.py
+-- base_agent.py
```

### ETAPA 4: Orquestación LangGraph
```
orchestrator/
+-- coordinator.py
+-- workflow_graph.py
+-- state_manager.py
+-- iteration_controller.py
```

### ETAPA 5: Frontend Streamlit/Gradio
```
frontend/
+-- app.py
+-- components/
+-- pages/
+-- static/
```

### ETAPA 6: Generación de Outputs
```
outputs/
+-- generators/
+-- templates/
+-- formatters/
```

---

## ?? Estructura Actual del Proyecto

```
multi_agent_novel_system/
+-- agents/                    # ?? Pendiente (Etapa 3)
+-- config/                    # ? Completo
+-- data/                      # ? Completo
+-- frontend/                  # ?? Pendiente (Etapa 5)
+-- llm_local/                 # ? Completo
+-- orchestrator/              # ?? Pendiente (Etapa 4)
+-- outputs/                   # ? Estructura
+-- rag/                       # ? Completo
+-- scripts/                   # ? Completo
+-- utils/                     # ? Estructura
+-- novel_env/                 # ? Entorno virtual
+-- .env                       # ? Configuración
+-- requirements.txt           # ? Dependencias
```

---

## ?? Comandos para Continuar

```bash
# Activar entorno
cd ~/multi_agent_novel_system
source novel_env/bin/activate

# Probar sistema actual
python scripts/test_rag.py

# Verificar vector store
python -c "from rag.rag_manager import RAGManager; rag = RAGManager(); print(rag.get_stats())"

# Añadir documentos de referencia
cp /ruta/a/tus/documentos/* data/reference_docs/
python -c "from rag.rag_manager import RAGManager; rag = RAGManager(); rag.ingest_directory('data/reference_docs')"
```

---

## ?? Estado General: 30% Completado

- ? **Infraestructura**: 100%
- ? **Sistema RAG**: 100% 
- ? **LLM Local**: 100%
- ?? **Agentes**: 0% (Siguiente)
- ?? **Orquestación**: 0%
- ?? **Frontend**: 0%
- ?? **Outputs**: 20% (estructura)

**Total estimado para producción**: 7 etapas
**Completadas**: 2 etapas
**Siguiente**: Etapa 3 - Definición de Agentes CrewAI