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
pip install langchain langchain-community langchain-openai
#pip install chromadb sentence-transformers

# Instalar LangGraph
echo "🔄 Instalando LangGraph..."
pip install langgraph

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
