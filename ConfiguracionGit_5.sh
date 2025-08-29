# Inicializar repositorio Git
git init

# Configurar .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Data files
data/documents/*
data/manuscripts/*
!data/documents/.gitkeep
!data/manuscripts/.gitkeep

# Outputs
outputs/novels/*
outputs/libraries/*
outputs/characters/*
outputs/video_prompts/*
!outputs/*/.gitkeep

# ChromaDB
chromadb/
.chromadb/

# Temporary files
*.tmp
*.temp
temp/
tmp/
EOF