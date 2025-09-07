#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Verification Script
Tests all components after fixes have been applied
"""

import sys
import logging
from pathlib import Path
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_imports = {
        'pydantic_settings': ['BaseSettings'],
        'nltk': [],
        'textblob': ['TextBlob'], 
        'crewai': ['Agent'],
        'sentence_transformers': ['SentenceTransformer'],
        'chromadb': [],
        'streamlit': [],
        'langchain': []
    }
    
    failed_imports = []
    
    for module, classes in required_imports.items():
        try:
            if classes:
                for cls in classes:
                    exec(f"from {module} import {cls}")
            else:
                exec(f"import {module}")
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_project_structure():
    """Verify project directory structure"""
    print("🧪 Testing project structure...")
    
    required_files = [
        'requirements.txt',
        'docker-compose.yml', 
        'Dockerfile',
        'config/settings.py',
        'agents/__init__.py',
        'agents/tools/__init__.py',
        'agents/crews/__init__.py',
        'rag/__init__.py'
    ]
    
    required_dirs = [
        'agents/crews',
        'agents/tools',
        'config',
        'rag',
        'frontend',
        'data',
        'outputs'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}/")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
    if missing_dirs:
        print(f"  ❌ Missing directories: {missing_dirs}")
        
    return len(missing_files) == 0 and len(missing_dirs) == 0

def test_settings_import():
    """Test that settings can be imported with pydantic-settings"""
    print("🧪 Testing settings import...")
    
    try:
        from config.settings import settings
        print(f"  ✅ Settings imported successfully")
        print(f"  📊 Project name: {settings.project_name}")
        return True
    except Exception as e:
        print(f"  ❌ Settings import failed: {e}")
        traceback.print_exc()
        return False

def test_agent_tools():
    """Test that agent tools can be imported and initialized"""
    print("🧪 Testing agent tools...")
    
    tools_to_test = [
        ('creative_tools', 'IdeaGenerator'),
        ('creative_tools', 'VisualPromptGenerator'),
        ('rag_tool', 'RAGTool'),
        ('analysis_tools', 'WritingAnalyzer'),
        ('writing_tools', 'PacingAnalyzer')
    ]
    
    successful_tools = 0
    
    for module, tool_class in tools_to_test:
        try:
            exec(f"from agents.tools.{module} import {tool_class}")
            # Try to instantiate the tool
            tool_instance = eval(f"{tool_class}()")
            print(f"  ✅ {tool_class} from {module}")
            successful_tools += 1
        except Exception as e:
            print(f"  ❌ {tool_class} from {module}: {e}")
    
    return successful_tools >= len(tools_to_test) * 0.8  # 80% success rate

def test_rag_system():
    """Test RAG system initialization"""
    print("🧪 Testing RAG system...")
    
    try:
        from rag.rag_manager import RAGManager
        
        # Try to initialize RAG manager
        rag_manager = RAGManager()
        stats = rag_manager.get_stats()
        
        print(f"  ✅ RAG Manager initialized")
        print(f"  📊 Documents in vector store: {stats.get('total_documents', 0)}")
        return True
    except Exception as e:
        print(f"  ❌ RAG system test failed: {e}")
        return False

def test_agents_initialization():
    """Test that agents can be initialized"""
    print("🧪 Testing agent initialization...")
    
    try:
        from agents.agent_manager import AgentManager
        
        # Initialize agent manager without LLM (for testing)
        manager = AgentManager()
        agents = manager.list_agents()
        
        print(f"  ✅ Agent Manager initialized")
        print(f"  📊 Available agents: {len(agents)}")
        
        # Test specific agent
        if agents:
            test_agent_name = agents[0]
            agent = manager.get_agent(test_agent_name)
            if agent:
                print(f"  ✅ Agent '{test_agent_name}' accessible")
                return True
            else:
                print(f"  ❌ Agent '{test_agent_name}' not accessible")
                return False
        else:
            print(f"  ⚠️  No agents found")
            return False
            
    except Exception as e:
        print(f"  ❌ Agent initialization failed: {e}")
        traceback.print_exc()
        return False

def test_docker_compose_syntax():
    """Test docker-compose file syntax"""
    print("🧪 Testing Docker Compose syntax...")
    
    try:
        import yaml
        
        with open('docker-compose.yml', 'r') as f:
            compose_config = yaml.safe_load(f)
        
        # Check that services exist
        if 'services' not in compose_config:
            print(f"  ❌ No 'services' section in docker-compose.yml")
            return False
        
        services = compose_config['services']
        expected_services = ['ai-writer', 'frontend-streamlit', 'rag-service', 'agent-test']
        
        for service in expected_services:
            if service in services:
                print(f"  ✅ Service '{service}' defined")
            else:
                print(f"  ❌ Service '{service}' missing")
                return False
        
        print(f"  ✅ Docker Compose syntax valid")
        return True
        
    except Exception as e:
        print(f"  ❌ Docker Compose test failed: {e}")
        return False

def test_encoding_fixes():
    """Test that encoding issues are fixed"""
    print("🧪 Testing encoding fixes...")
    
    files_to_check = [
        'agents/crews/character_developer.py',
        'config/settings.py'
    ]
    
    encoding_issues = []
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for UTF-8 BOM or encoding declaration
                if content.startswith('# -*- coding: utf-8 -*-') or 'coding:' in content[:100]:
                    print(f"  ✅ {file_path} - encoding declaration found")
                else:
                    print(f"  ⚠️  {file_path} - no explicit encoding declaration")
                    
            except UnicodeDecodeError as e:
                print(f"  ❌ {file_path} - encoding issue: {e}")
                encoding_issues.append(file_path)
        else:
            print(f"  ⚠️  {file_path} - file not found")
    
    return len(encoding_issues) == 0

def run_comprehensive_test():
    """Run a comprehensive test of the fixed system"""
    print("🧪 Running comprehensive system test...")
    
    try:
        # Test a simple workflow
        from agents.tools.creative_tools import IdeaGenerator
        
        idea_gen = IdeaGenerator()
        result = idea_gen._run("reino magico con dragones", "character", 3)
        
        if result and len(result) > 50:
            print(f"  ✅ Creative tools working")
            print(f"  📝 Sample output: {result[:100]}...")
            return True
        else:
            print(f"  ❌ Creative tools returned empty/short result")
            return False
            
    except Exception as e:
        print(f"  ❌ Comprehensive test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Starting project verification...\n")
    
    # Change to project directory
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print(f"📁 Testing project at: {project_root.absolute()}\n")
    
    # Define all tests
    tests = [
        ("Import Tests", test_imports),
        ("Project Structure", test_project_structure),
        ("Settings Import", test_settings_import),
        ("Encoding Fixes", test_encoding_fixes),
        ("Docker Compose Syntax", test_docker_compose_syntax),
        ("Agent Tools", test_agent_tools),
        ("RAG System", test_rag_system),
        ("Agent Initialization", test_agents_initialization),
        ("Comprehensive Test", run_comprehensive_test)
    ]
    
    results = []
    
    for test_name, test_function in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {test_name}")
        print('='*60)
        
        try:
            result = test_function()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
                
        except Exception as e:
            print(f"💥 {test_name} - ERROR: {e}")
            results.append((test_name, False))
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎯 VERIFICATION SUMMARY")
    print('='*60)
    
    passed_tests = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Ready to run:")
        print("   docker-compose up")
        
    elif passed_tests >= total_tests * 0.8:
        print("⚠️  Most tests passed. System should work with minor issues.")
        print("\n🔧 Consider fixing the failed tests before production use.")
        
    else:
        print("❌ Many tests failed. System needs additional fixes.")
        print("\n🛠️  Please address the failed tests before proceeding.")
    
    print(f"\n📋 Next steps:")
    print("1. If tests passed: docker-compose build --no-cache")
    print("2. Then run: docker-compose up")
    print("3. Access Streamlit at: http://localhost:8501")

if __name__ == "__main__":
    main()
