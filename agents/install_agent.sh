# =====================================================
# ETAPA 3: INSTALACIÓN DE AGENTES CrewAI
# =====================================================

# 1. Navegar al proyecto y activar entorno
cd ~/multi_agent_novel_system
source novel_env/bin/activate

# 2. Instalar dependencias adicionales para agentes
pip install nltk textblob

# 3. Descargar recursos de NLTK (ejecutar en Python)
python -c "
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    print('punkt ya descargado')
except LookupError:
    nltk.download('punkt')
    print('punkt descargado')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
    print('averaged_perceptron_tagger ya descargado')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
    print('averaged_perceptron_tagger descargado')
"

# 4. Crear estructura de archivos para agentes
mkdir -p agents/crews agents/tools

# 5. Crear archivos __init__.py
touch agents/__init__.py
touch agents/crews/__init__.py
touch agents/tools/__init__.py

# 6. Crear archivos de herramientas
# Copiar el contenido de los artifacts en estos archivos:

cat > agents/tools/__init__.py << 'EOF'
from .rag_tool import RAGTool
from .writing_tools import WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from .analysis_tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from .creative_tools import IdeaGenerator, VisualPromptGenerator

__all__ = [
    'RAGTool',
    'WritingAnalyzer', 
    'StyleAnalyzer',
    'CharacterAnalyzer',
    'ConsistencyChecker',
    'PacingAnalyzer', 
    'PlotAnalyzer',
    'IdeaGenerator',
    'VisualPromptGenerator'
]
EOF

# [NOTA: Aquí necesitas copiar el contenido de los artifacts en los archivos correspondientes]
# - agents/tools/rag_tool.py
# - agents/tools/writing_tools.py  
# - agents/tools/analysis_tools.py
# - agents/tools/creative_tools.py
# - agents/crews/base_agent.py
# - agents/crews/lorekeeper.py
# - agents/crews/character_developer.py
# - agents/crews/plot_weaver.py
# - agents/crews/style_editor.py
# - agents/crews/visualizer.py
# - agents/crews/researcher.py
# - agents/crews/continuity_auditor.py
# - agents/crews/beta_reader.py
# - agents/crews/pacing_specialist.py
# - agents/crews/proofreader.py
# - agents/crews/innovation_scout.py
# - agents/agent_manager.py
# - agents/test_agents.py

# 7. Crear script de instalación automatizada
cat > scripts/install_agents.py << 'EOF'
#!/usr/bin/env python3
"""Script para instalar y configurar los agentes"""

import sys
import os
import subprocess
from pathlib import Path

def install_nltk_data():
    """Instala datos necesarios de NLTK"""
    try:
        import nltk
        
        # Descargar recursos necesarios
        resources = ['punkt', 'averaged_perceptron_tagger', 'stopwords']
        
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'taggers/{resource}' if 'perceptron' in resource else f'corpora/{resource}')
                print(f'✅ {resource} ya disponible')
            except LookupError:
                print(f'📥 Descargando {resource}...')
                nltk.download(resource, quiet=True)
                print(f'✅ {resource} descargado')
                
    except ImportError:
        print('❌ NLTK no está instalado')
        return False
    
    return True

def verify_agent_structure():
    """Verifica que la estructura de agentes esté completa"""
    
    required_files = [
        'agents/__init__.py',
        'agents/tools/__init__.py',
        'agents/crews/__init__.py',
        'agents/agent_manager.py',
        'agents/test_agents.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print('❌ Archivos faltantes:')
        for file in missing_files:
            print(f'   - {file}')
        return False
    
    print('✅ Estructura de agentes verificada')
    return True

def main():
    print('🚀 Instalando sistema de agentes...')
    
    # Verificar que estamos en el directorio correcto
    if not Path('agents').exists():
        os.makedirs('agents/tools', exist_ok=True)
        os.makedirs('agents/crews', exist_ok=True)
    
    # Instalar datos de NLTK
    if install_nltk_data():
        print('✅ Datos de NLTK instalados')
    
    # Verificar estructura
    if verify_agent_structure():
        print('✅ Sistema de agentes listo')
    else:
        print('⚠️ Algunos archivos faltan - revisar instalación')
    
    print('\n🎯 Próximos pasos:')
    print('1. Copiar los archivos de código de los agents')
    print('2. Ejecutar: python agents/test_agents.py')
    print('3. Verificar que todos los agentes funcionan')

if __name__ == '__main__':
    main()
EOF

chmod +x scripts/install_agents.py

# 8. Ejecutar instalación
python scripts/install_agents.py

# 9. Probar los agentes (después de copiar archivos)
python agents/test_agents.py

# 10. Probar con manuscrito de ejemplo
python -c "
from agents.agent_manager import AgentManager
import sys
sys.path.append('.')

# Crear manager
manager = AgentManager()

# Manuscrito de prueba
test_manuscript = '''
El reino de Aethermoor se alzaba majestuoso entre montañas nevadas.
Lyra Stormwind, la joven maga de cabello plateado, caminaba por los 
pasillos de cristal del palacio real. Su misión era clara: encontrar 
el grimorio perdido antes de que las Sombras del Vacío consumieran 
toda la magia del reino.

El rey Aldrin Goldenheart la había convocado al amanecer. Sus ojos 
dorados mostraban preocupación mientras le explicaba la gravedad de la situación.
'''

# Establecer manuscrito
manager.set_manuscript(test_manuscript)

# Obtener resumen
summary = manager.get_analysis_summary()
print('🧪 Test básico del sistema de agentes:')
print(f'   Manuscrito: {summary[\"manuscript_length\"]} caracteres')
print(f'   Agentes disponibles: {len(summary[\"available_agents\"])}')
print(f'   LLM disponible: {summary[\"llm_available\"]}')
print('✅ Sistema básico funcionando')
"

# =====================================================
# VERIFICACIÓN DE LA INSTALACIÓN
# =====================================================

echo "🔍 Verificando instalación de Etapa 3..."

# Verificar estructura de directorios
echo "📁 Verificando estructura:"
ls -la agents/
ls -la agents/tools/
ls -la agents/crews/

# Verificar importaciones Python
echo "🐍 Verificando importaciones:"
python -c "
try:
    from agents.tools import RAGTool
    print('✅ RAGTool importado correctamente')
except Exception as e:
    print(f'❌ Error importando RAGTool: {e}')

try:
    from agents.agent_manager import AgentManager
    print('✅ AgentManager importado correctamente')
except Exception as e:
    print(f'❌ Error importando AgentManager: {e}')

try:
    import nltk
    from textblob import TextBlob
    print('✅ Dependencias de NLP disponibles')
except Exception as e:
    print(f'❌ Error con dependencias NLP: {e}')
"

# Verificar herramientas disponibles
echo "🔧 Verificando herramientas:"
python -c "
from agents.tools import WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from agents.tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from agents.tools import IdeaGenerator, VisualPromptGenerator

tools = [
    WritingAnalyzer(),
    StyleAnalyzer(), 
    CharacterAnalyzer(),
    ConsistencyChecker(),
    PacingAnalyzer(),
    PlotAnalyzer(),
    IdeaGenerator(),
    VisualPromptGenerator()
]

print(f'✅ {len(tools)} herramientas creadas exitosamente')
for tool in tools:
    print(f'   - {tool.name}')
"

echo "✅ Verificación de Etapa 3 completada"

# =====================================================
# COMANDOS DE TROUBLESHOOTING
# =====================================================

echo "🛠️ Comandos de troubleshooting si hay problemas:"

echo "
# Si hay errores con NLTK:
python -c \"
import nltk
nltk.download('all')
\"

# Si hay errores con TextBlob:
pip uninstall textblob
pip install textblob

# Si hay errores con crewai_tools:
pip install crewai[tools]

# Para reinstalar todo:
pip uninstall crewai langchain langgraph
pip install crewai>=0.28.0 langchain>=0.1.0 langgraph>=0.0.40

# Para verificar versiones:
pip list | grep -E '(crewai|langchain|langgraph|nltk|textblob)'
"