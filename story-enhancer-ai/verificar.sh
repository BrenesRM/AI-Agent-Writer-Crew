echo "🧪 Ejecutando verificaciones del sistema RAG..."

# Verificar instalación de dependencias
echo "Verificando dependencias críticas..."
python -c "
import langchain
import chromadb  
import openai
from sentence_transformers import SentenceTransformer
print('✅ Todas las dependencias principales están instaladas')
"

# Crear documentos de muestra y probar sistema
echo "Creando documentos de muestra..."
python create_samples.py

echo "Ejecutando pruebas del sistema RAG..."
python test_rag.py

echo "📊 Verificación de archivos creados:"
find data/ -type f -name "*.json" -o -name "*.md" -o -name "*.txt" | head -10