cat > README.md << 'EOF'
# Story Enhancer AI

Sistema multi-agente para mejora iterativa de manuscritos usando CrewAI, LangGraph y RAG.

## Arquitectura

- **Agentes**: CrewAI para roles especializados
- **Orquestación**: LangGraph para flujo iterativo
- **RAG**: ChromaDB/Pinecone para documentos de referencia
- **Frontend**: Streamlit para interfaz interactiva
- **LLM**: Compatible con OpenAI API y modelos locales (Ollama)

## Estructura del Proyecto