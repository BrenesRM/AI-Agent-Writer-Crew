#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Project Fix Script
Fixes all identified issues in the AI-Agent-Writer-Crew project
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a system command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def fix_encoding_issues():
    """Fix encoding issues in Python files"""
    print("🔧 Fixing encoding issues...")
    
    # Files that might have encoding issues
    files_to_check = [
        "agents/crews/character_developer.py",
        "agents/test_agents.py",
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            try:
                # Read with different encodings and write as UTF-8
                content = None
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content:
                    # Ensure UTF-8 BOM at start
                    if not content.startswith('# -*- coding: utf-8 -*-'):
                        content = '# -*- coding: utf-8 -*-\n' + content
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fixed encoding for {file_path}")
                else:
                    print(f"❌ Could not read {file_path}")
                    
            except Exception as e:
                print(f"❌ Error fixing {file_path}: {e}")

def install_missing_dependencies():
    """Install missing Python dependencies"""
    print("🔧 Installing missing dependencies...")
    
    dependencies = [
        "pydantic-settings>=2.0.0",
        "nltk>=3.8", 
        "textblob>=0.17.1",
        "mammoth>=1.6.0"
    ]
    
    for dep in dependencies:
        if run_command(f"pip install {dep}", f"Installing {dep}"):
            continue
        else:
            print(f"⚠️  Failed to install {dep}")

def setup_nltk_data():
    """Download required NLTK data"""
    print("🔧 Setting up NLTK data...")
    
    nltk_commands = [
        "python -c \"import nltk; nltk.download('punkt', quiet=True)\"",
        "python -c \"import nltk; nltk.download('averaged_perceptron_tagger', quiet=True)\"",
        "python -c \"import nltk; nltk.download('stopwords', quiet=True)\"",
        "python -c \"import nltk; nltk.download('wordnet', quiet=True)\""
    ]
    
    for cmd in nltk_commands:
        run_command(cmd, "Downloading NLTK data")

def verify_project_structure():
    """Verify that all required directories exist"""
    print("🔧 Verifying project structure...")
    
    required_dirs = [
        "logs",
        "outputs/final_novel",
        "outputs/character_guide", 
        "outputs/story_library",
        "outputs/video_prompts",
        "rag/documents",
        "rag/processed",
        "rag/vectorstore",
        "data/sessions"
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created/verified directory: {dir_path}")

def test_imports():
    """Test critical imports to ensure they work"""
    print("🔧 Testing critical imports...")
    
    imports_to_test = [
        ("pydantic_settings", "BaseSettings"),
        ("nltk", ""),
        ("textblob", "TextBlob"),
        ("sentence_transformers", "SentenceTransformer"),
        ("chromadb", ""),
        ("crewai", "Agent"),
        ("langchain", ""),
        ("streamlit", "")
    ]
    
    failed_imports = []
    
    for module, submodule in imports_to_test:
        try:
            if submodule:
                exec(f"from {module} import {submodule}")
            else:
                exec(f"import {module}")
            print(f"✅ {module} import successful")
        except ImportError as e:
            print(f"❌ {module} import failed: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"⚠️  Failed imports: {failed_imports}")
        print("   Consider installing missing packages with pip install")
    else:
        print("✅ All critical imports successful!")

def create_env_file():
    """Create a basic .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("🔧 Creating basic .env file...")
        env_content = """# AI Agent Writer Crew Configuration
PYTHONPATH=.
PYTHONIOENCODING=utf-8
LANG=C.UTF-8
LC_ALL=C.UTF-8

# LLM Configuration (optional)
LLM_MODEL_PATH=./llm_local/models/model.gguf

# OpenAI API (if using external LLM)
# OPENAI_API_KEY=your_api_key_here

# Logging
LOG_LEVEL=INFO

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./rag/vectorstore
EMBEDDING_MODEL=all-MiniLM-L6-v2
"""
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Created .env file")

def rebuild_docker():
    """Rebuild Docker images"""
    print("🔧 Rebuilding Docker images...")
    
    commands = [
        "docker-compose down",
        "docker-compose build --no-cache",
    ]
    
    for cmd in commands:
        run_command(cmd, f"Running: {cmd}")

def main():
    """Run all fixes"""
    print("🚀 Starting comprehensive project fix...\n")
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"📁 Working in: {project_root.absolute()}\n")
    
    # Run all fixes
    fixes = [
        ("Fixing encoding issues", fix_encoding_issues),
        ("Installing missing dependencies", install_missing_dependencies),
        ("Setting up NLTK data", setup_nltk_data),
        ("Verifying project structure", verify_project_structure),
        ("Creating .env file", create_env_file),
        ("Testing imports", test_imports),
    ]
    
    successful_fixes = 0
    
    for fix_name, fix_function in fixes:
        try:
            print(f"\n{'='*60}")
            print(f"🔧 {fix_name}")
            print('='*60)
            fix_function()
            successful_fixes += 1
            print(f"✅ {fix_name} completed")
        except Exception as e:
            print(f"❌ {fix_name} failed: {e}")
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎯 FINAL SUMMARY")
    print('='*60)
    print(f"✅ Completed fixes: {successful_fixes}/{len(fixes)}")
    
    if successful_fixes == len(fixes):
        print("🎉 All fixes applied successfully!")
        print("\n🚀 Next steps:")
        print("1. Run: docker-compose build --no-cache")
        print("2. Run: docker-compose up")
        print("3. Test the system")
    else:
        print("⚠️  Some fixes failed. Please review the errors above.")
        
    print("\n🔍 To test the system, run:")
    print("   docker-compose up agent-test")

if __name__ == "__main__":
    main()
