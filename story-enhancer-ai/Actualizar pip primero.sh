# Actualizar pip primero
pip install --upgrade pip

# Instalar dependencias base
echo "Instalando dependencias base..."
pip install python-dotenv pydantic httpx aiofiles tenacity tqdm psutil

# Instalar procesamiento de documentos
echo "Instalando procesadores de documentos..."
pip install pypdf2 python-docx openpyxl unstructured markdown python-multipart

# Instalar pandas y plotly
echo "Instalando análisis de datos..."
pip install pandas plotly

# Instalar LangChain y componentes
echo "Instalando LangChain ecosystem..."
pip install langchain==0.1.20 langchain-community==0.0.38 langchain-openai==0.1.8

# Instalar LangGraph
echo "Instalando LangGraph..."
pip install langgraph==0.0.55

# Instalar CrewAI
echo "Instalando CrewAI..."
pip install crewai==0.28.8 crewai-tools==0.1.6

# Instalar vector databases
echo "Instalando bases de datos vectoriales..."
pip install chromadb==0.4.24

# Instalar OpenAI y embeddings
echo "Instalando OpenAI y embeddings..."
pip install openai==1.35.3 sentence-transformers==2.7.0

# Instalar frontend
echo "Instalando Streamlit..."
pip install streamlit==1.34.0

# Instalar herramientas de desarrollo
echo "Instalando herramientas de desarrollo..."
pip install pytest black flake8 mypy

echo "✅ Instalación de dependencias completada!"