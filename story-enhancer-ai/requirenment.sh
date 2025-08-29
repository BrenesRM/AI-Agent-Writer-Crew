# Solución de Errores - Etapa 2

## 🔧 Problema Identificado
- ❌ **Dependencias no instaladas**: falta langchain y otros módulos
- ❌ **Archivos mal creados**: test_rag.py tiene contenido de shell en lugar de Python
- ❌ **Scripts faltantes**: create_samples.py no existe

## Solución Paso a Paso

### Paso 1: Instalar Dependencias Correctamente

```bash
# Asegúrate de estar en el entorno virtual
cd ~/Documents/Aget-Writer/story-enhancer-ai
source venv/bin/activate

# Verificar que el entorno virtual está activo
echo "Entorno virtual: $VIRTUAL_ENV"

# Instalar dependencias una por una para detectar errores
echo "🔄 Instalando dependencias base..."
pip install --upgrade pip setuptools wheel

echo "🔄 Instalando utilidades básicas..."
pip install python-dotenv pydantic httpx aiofiles tenacity tqdm psutil

echo "🔄 Instalando procesadores de documentos..."
pip install pypdf2 python-docx openpyxl python-multipart markdown

echo "🔄 Instalando pandas y plotly..."
pip install pandas plotly

echo "🔄 Instalando LangChain..."
pip install langchain==0.1.20 langchain-community==0.0.38 langchain-openai==0.1.8

echo "🔄 Instalando LangGraph..."
pip install langgraph==0.0.55

echo "🔄 Instalando CrewAI..."
pip install crewai==0.28.8 crewai-tools==0.1.6

echo "🔄 Instalando ChromaDB..."
pip install chromadb==0.4.24

echo "🔄 Instalando OpenAI y embeddings..."
pip install openai==1.35.3 sentence-transformers==2.7.0

echo "🔄 Instalando Streamlit..."
pip install streamlit==1.34.0

echo "🔄 Instalando herramientas de desarrollo..."
pip install pytest black flake8 mypy

echo "✅ Instalación completada!"
```

### Paso 2: Corregir archivos dañados

#### 2.1 Recrear test_rag.py correctamente
```bash
# Eliminar archivo corrupto
rm test_rag.py

# Crear archivo Python correcto
cat > test_rag.py << 'EOF'
#!/usr/bin/env python3
"""Script de prueba para el sistema RAG"""
import os
import sys
import json
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from rag.vector_store import VectorStore
from rag.document_ingestion import DocumentIngestion

def test_text_processing():
    """Probar procesamiento de texto básico"""
    print("🔍 Probando procesamiento de texto...")
    
    # Crear archivo de prueba
    test_file = Path("data/documents/test.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("""
Esta es una historia de prueba para el sistema RAG.

Capítulo 1: El Comienzo
En un reino lejano, había un joven aventurero llamado Alex.
Alex tenía el sueño de convertirse en un gran mago.

Capítulo 2: El Aprendizaje  
Alex comenzó a estudiar en la Academia de Magia.
Allí aprendió sobre hechizos, pociones y criaturas mágicas.

Capítulo 3: La Aventura
Un día, Alex recibió una misión especial del director.
Debía encontrar un artefacto perdido en el Bosque Oscuro.
        """.strip())
    
    print(f"✅ Archivo de prueba creado: {test_file}")
    return str(test_file)

def test_vector_store():
    """Probar el sistema de vector store"""
    print("\n🗄️  Probando Vector Store...")
    
    # Crear archivo de prueba
    test_file = test_text_processing()
    
    # Inicializar vector store
    vector_store = VectorStore("test_collection")
    
    # Agregar documento
    result = vector_store.add_document(test_file)
    print(f"Resultado de ingesta: {result}")
    
    # Probar búsqueda
    query = "Alex mago academia"
    results = vector_store.search(query, k=3)
    
    print(f"\n🔎 Búsqueda: '{query}'")
    print(f"Resultados encontrados: {len(results)}")
    
    for i, result in enumerate(results[:2]):  # Mostrar solo los primeros 2
        print(f"\nResultado {i+1}:")
        print(f"Similitud: {result['similarity']:.3f}")
        print(f"Contenido: {result['content'][:200]}...")
        print(f"Fuente: {result['source']}")
    
    # Mostrar estadísticas
    stats = vector_store.get_collection_stats()
    print(f"\n📊 Estadísticas de la colección:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return vector_store

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del sistema RAG")
    print("=" * 50)
    
    try:
        # Probar vector store básico
        vector_store = test_vector_store()
        
        print("\n" + "=" * 50)
        print("✅ Pruebas completadas exitosamente!")
        
        # Mostrar estadísticas finales
        final_stats = vector_store.get_collection_stats()
        print(f"\n📊 Estadísticas finales del sistema:")
        for key, value in final_stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
EOF

chmod +x test_rag.py
```

#### 2.2 Crear create_samples.py
```bash
cat > create_samples.py << 'EOF'
#!/usr/bin/env python3
"""Crear documentos de muestra para pruebas"""
import json
from pathlib import Path

def create_sample_documents():
    """Crear documentos de muestra para pruebas"""
    documents_dir = Path("data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    
    # Documento de worldbuilding
    worldbuilding = """# Worldbuilding: Reino de Aetheria

## Geografía
El Reino de Aetheria se extiende por tres continentes principales:
- **Lumina**: Continente de la luz, hogar de la Academia de Magia
- **Umbra**: Continente de las sombras, territorio peligroso
- **Equilibrium**: Continente neutral, centro de comercio

## Sistema de Magia
La magia en Aetheria se basa en seis elementos fundamentales:
1. **Fuego**: Destructivo pero purificador
2. **Agua**: Sanador y adaptable  
3. **Tierra**: Estable y defensivo
4. **Aire**: Rápido y evasivo
5. **Luz**: Revelador y protector
6. **Sombra**: Oculto y manipulador

Los magos deben especializarse en máximo dos elementos complementarios.
"""
    
    with open(documents_dir / "worldbuilding_sample.md", "w", encoding="utf-8") as f:
        f.write(worldbuilding)
    
    # Guía de personajes
    characters = {
        "main_characters": {
            "Alex": {
                "full_name": "Alexander Brightward",
                "age": 18,
                "magic_affinity": ["Luz", "Fuego"],
                "personality": ["valiente", "curioso", "impulsivo"],
                "arc": "De novato inseguro a héroe confiado"
            }
        }
    }
    
    with open(documents_dir / "characters_sample.json", "w", encoding="utf-8") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)
    
    return {
        "created_files": [
            "worldbuilding_sample.md",
            "characters_sample.json"
        ],
        "location": str(documents_dir)
    }

if __name__ == "__main__":
    print("📝 Creando documentos de muestra...")
    result = create_sample_documents()
    print(f"✅ Creados {len(result['created_files'])} archivos en {result['location']}")
    for file in result['created_files']:
        print(f"  - {file}")
EOF

chmod +x create_samples.py
```

### Paso 3: Crear script de instalación completa
```bash
cat > instalar_completo.sh << 'EOF'
#!/bin/bash
echo "🚀 Instalación Completa del Sistema RAG"
echo "======================================"

# Verificar entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Entorno virtual no activo"
    echo "Ejecuta: source venv/bin/activate"
    exit 1
fi

echo "✅ Entorno virtual activo: $VIRTUAL_ENV"

# Actualizar pip
echo "🔄 Actualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias básicas
echo "🔄 Instalando dependencias básicas..."
pip install python-dotenv pydantic httpx aiofiles tenacity tqdm psutil

# Instalar procesadores de documentos
echo "🔄 Instalando procesadores de documentos..."
pip install pypdf2 python-docx openpyxl python-multipart markdown pandas plotly

# Instalar LangChain ecosystem
echo "🔄 Instalando LangChain..."
pip install langchain==0.1.20 langchain-community==0.0.38 langchain-openai==0.1.8

# Instalar LangGraph
echo "🔄 Instalando LangGraph..."
pip install langgraph==0.0.55

# Instalar CrewAI
echo "🔄 Instalando CrewAI..."
pip install crewai==0.28.8 crewai-tools==0.1.6

# Instalar ChromaDB
echo "🔄 Instalando ChromaDB..."
pip install chromadb==0.4.24

# Instalar OpenAI y embeddings
echo "🔄 Instalando OpenAI y embeddings..."
pip install openai==1.35.3 sentence-transformers==2.7.0

# Instalar Streamlit
echo "🔄 Instalando Streamlit..."
pip install streamlit==1.34.0

# Instalar herramientas de desarrollo
echo "🔄 Instalando herramientas de desarrollo..."
pip install pytest black flake8 mypy

echo "✅ Instalación completada!"

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "
try:
    import langchain
    import chromadb
    import openai
    from sentence_transformers import SentenceTransformer
    import crewai
    print('✅ Todas las dependencias están instaladas correctamente')
except ImportError as e:
    print(f'❌ Error de importación: {e}')
"

echo "🎉 Sistema RAG listo para usar!"
EOF

chmod +x instalar_completo.sh
```

### Paso 4: Script de verificación mejorado
```bash
cat > verificar_mejorado.sh << 'EOF'
#!/bin/bash
echo "🔍 Verificación Mejorada del Sistema RAG"
echo "======================================"

# Verificar entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Entorno virtual no activo"
    echo "Ejecuta: source venv/bin/activate"
else
    echo "✅ Entorno virtual activo: $VIRTUAL_ENV"
fi

# Verificar dependencias críticas
echo "🔍 Verificando dependencias críticas..."
python -c "
import sys
try:
    import langchain
    print('✅ langchain: OK')
except ImportError:
    print('❌ langchain: FALTA')

try:
    import chromadb
    print('✅ chromadb: OK')
except ImportError:
    print('❌ chromadb: FALTA')

try:
    import openai
    print('✅ openai: OK')
except ImportError:
    print('❌ openai: FALTA')

try:
    from sentence_transformers import SentenceTransformer
    print('✅ sentence-transformers: OK')
except ImportError:
    print('❌ sentence-transformers: FALTA')

try:
    import crewai
    print('✅ crewai: OK')
except ImportError:
    print('❌ crewai: FALTA')
"

# Verificar estructura de archivos
echo ""
echo "📁 Verificando estructura de archivos..."
echo "Archivos Python principales:"
ls -la *.py 2>/dev/null || echo "No se encontraron archivos .py en el directorio raíz"

echo ""
echo "Configuración:"
ls -la config/ 2>/dev/null || echo "Directorio config/ no encontrado"

echo ""
echo "Módulos RAG:"
ls -la rag/ 2>/dev/null || echo "Directorio rag/ no encontrado"

echo ""
echo "Utilidades:"
ls -la utils/ 2>/dev/null || echo "Directorio utils/ no encontrado"

echo ""
echo "📄 Documentos disponibles:"
find ../data/documents -name "*.txt" -o -name "*.docx" -o -name "*.json" -o -name "*.md" 2>/dev/null | head -5

echo ""
echo "✅ Verificación completada"
EOF

chmod +x verificar_mejorado.sh
```

## Paso 5: Ejecutar la solución

### 5.1 Instalar todo
```bash
# Ejecutar instalación completa
./instalar_completo.sh
```

### 5.2 Verificar instalación
```bash
# Ejecutar verificación mejorada
./verificar_mejorado.sh
```

### 5.3 Probar sistema básico
```bash
# Crear documentos de muestra
python create_samples.py

# Probar sistema RAG
python test_rag.py
```

## Paso 6: Una vez que funcione, usar tus documentos reales

```bash
# Crear el script de uso práctico para tus documentos
cat > usar_mis_documentos.py << 'EOF'
#!/usr/bin/env python3
"""Script para procesar TUS documentos reales"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from rag.vector_store import VectorStore
from rag.document_ingestion import DocumentIngestion

def procesar_documentos_reales():
    """Procesar tus documentos reales"""
    print("📚 Procesando tus documentos reales...")
    
    # Ruta a tus documentos
    docs_path = Path("../data/documents")
    
    if not docs_path.exists():
        print(f"❌ No se encuentra: {docs_path}")
        return
    
    # Contar archivos
    archivos = []
    for ext in ['txt', 'docx']:  # Solo TXT y DOCX por ahora
        archivos.extend(list(docs_path.glob(f"*.{ext}")))
    
    print(f"📄 Encontrados {len(archivos)} archivos:")
    for archivo in archivos[:10]:  # Mostrar primeros 10
        size_mb = archivo.stat().st_size / (1024 * 1024)
        print(f"  - {archivo.name} ({size_mb:.1f}MB)")
    
    if len(archivos) > 10:
        print(f"  ... y {len(archivos) - 10} más")
    
    # Procesar
    print("\n🔄 Procesando documentos...")
    ingestion = DocumentIngestion("mis_documentos")
    resultados = ingestion.ingest_directory(str(docs_path), recursive=False)
    
    print(f"\n✅ RESULTADOS:")
    print(f"  📊 Procesados: {resultados['summary']['successful']}")
    print(f"  📝 Total chunks: {resultados['total_chunks']}")
    print(f"  ❌ Errores: {resultados['summary']['failed']}")
    
    return resultados

def probar_busquedas():
    """Probar búsquedas en tus documentos"""
    print("\n🔍 Probando búsquedas en tus documentos...")
    
    vector_store = VectorStore("mis_documentos")
    
    consultas = [
        "dos colmillos personaje principal",
        "panteón inquisición",
        "construcción mundo",
        "personajes principales",
        "política intriga"
    ]
    
    for consulta in consultas:
        print(f"\n➤ '{consulta}':")
        resultados = vector_store.search(consulta, k=2)
        
        if resultados:
            mejor = resultados[0]
            print(f"  📄 {mejor['source']} (similitud: {mejor['similarity']:.3f})")
            print(f"  📝 {mejor['content'][:150]}...")
        else:
            print("  ❌ Sin resultados")

if __name__ == "__main__":
    procesar_documentos_reales()
    probar_busquedas()
EOF

chmod +x usar_mis_documentos.py
```

## 🎯 Orden de Ejecución

1. **Instalar dependencias**: `./instalar_completo.sh`
2. **Verificar instalación**: `./verificar_mejorado.sh`  
3. **Probar sistema**: `python test_rag.py`
4. **Usar tus documentos**: `python usar_mis_documentos.py`

¡Una vez que esto funcione, tu sistema RAG estará listo para los agentes CrewAI! 🚀