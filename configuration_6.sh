# Crear .env con configuración base
cat > .env << 'EOF'
# LLM Configuration
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=deepseek-r1:8b

# RAG Configuration
VECTOR_DB_TYPE=chromadb
CHROMADB_PATH=./chromadb
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Agent Configuration
MAX_ITERATIONS=5
MIN_STABILITY_THRESHOLD=0.8

# Frontend Configuration
STREAMLIT_PORT=8501
DEBUG_MODE=true

# File Upload Configuration
MAX_FILE_SIZE_MB=100
ALLOWED_EXTENSIONS=pdf,docx,txt,json,md,xlsx

# Output Configuration
OUTPUT_FORMAT=markdown
EXPORT_JSON=true
EXPORT_DOCX=true
EOF