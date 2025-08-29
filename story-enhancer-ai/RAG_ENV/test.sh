# Hacer ejecutable el script de prueba
chmod +x test_rag.py

# Crear documentos de muestra (opcional)
cat > create_samples.py << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.rag_utils import create_sample_documents

if __name__ == "__main__":
    print("📝 Creando documentos de muestra...")
    result = create_sample_documents()
    print(f"✅ Creados {len(result['created_files'])} archivos en {result['location']}")
    for file in result['created_files']:
        print(f"  - {file}")
EOF

chmod +x create_samples.py