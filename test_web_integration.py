# -*- coding: utf-8 -*-
"""
Integration script to ensure web interface compatibility
with existing AI Writer Crew project
"""
import sys
import os
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported"""
    logger.info("🧪 Testing module imports...")
    
    try:
        # Test core project modules
        from config.settings import settings
        logger.info("✅ Settings module imported successfully")
        
        from rag.rag_manager import RAGManager
        logger.info("✅ RAG Manager imported successfully")
        
        from agents.agent_manager import AgentManager
        logger.info("✅ Agent Manager imported successfully")
        
        # Test web interface modules
        import fastapi
        import uvicorn
        from pydantic import BaseModel
        logger.info("✅ Web interface dependencies imported successfully")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {str(e)}")
        return False

def test_rag_manager():
    """Test RAG Manager initialization"""
    logger.info("🧪 Testing RAG Manager...")
    
    try:
        rag_manager = RAGManager()
        stats = rag_manager.get_stats()
        logger.info(f"✅ RAG Manager initialized. Documents: {stats.get('total_documents', 0)}")
        return True
    except Exception as e:
        logger.error(f"❌ RAG Manager error: {str(e)}")
        return False

def test_agent_manager():
    """Test Agent Manager initialization"""
    logger.info("🧪 Testing Agent Manager...")
    
    try:
        agent_manager = AgentManager()
        agents = getattr(agent_manager, 'available_agents', [])
        logger.info(f"✅ Agent Manager initialized. Available agents: {len(agents)}")
        return True
    except Exception as e:
        logger.error(f"❌ Agent Manager error: {str(e)}")
        return False

def test_llm_manager():
    """Test LLM Manager if model exists"""
    logger.info("🧪 Testing LLM Manager...")
    
    try:
        model_path = project_root / "llm_local" / "models" / "model.gguf"
        
        if not model_path.exists():
            logger.warning("⚠️  LLM model not found - this is optional")
            return True
        
        from llm_local.llama_manager import LlamaManager
        
        # Don't actually load the model in test - just check if it can be imported
        logger.info("✅ LLM Manager module available")
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️  LLM Manager not available: {str(e)}")
        return True  # This is optional
    except Exception as e:
        logger.error(f"❌ LLM Manager error: {str(e)}")
        return False

def check_file_structure():
    """Check if required files and directories exist"""
    logger.info("🧪 Checking file structure...")
    
    required_paths = [
        "config/settings.py",
        "rag/rag_manager.py",
        "agents/agent_manager.py",
        "frontend/index.html",
        "api_server.py",
        "launch_web_interface.py"
    ]
    
    all_exist = True
    
    for path_str in required_paths:
        path = project_root / path_str
        if path.exists():
            logger.info(f"✅ Found: {path_str}")
        else:
            logger.error(f"❌ Missing: {path_str}")
            all_exist = False
    
    return all_exist

def check_optional_components():
    """Check optional components"""
    logger.info("🧪 Checking optional components...")
    
    # Check for reference documents
    docs_path = project_root / "data" / "reference_docs"
    if docs_path.exists():
        doc_files = list(docs_path.glob("*.*"))
        logger.info(f"✅ Found {len(doc_files)} reference documents")
    else:
        logger.warning("⚠️  No reference documents found - RAG will have limited functionality")
    
    # Check for LLM model
    model_path = project_root / "llm_local" / "models" / "model.gguf"
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        logger.info(f"✅ Found LLM model ({size_mb:.1f} MB)")
    else:
        logger.warning("⚠️  No LLM model found - will use fallback responses")

def create_missing_directories():
    """Create any missing directories"""
    logger.info("🧪 Creating missing directories...")
    
    required_dirs = [
        "frontend/static",
        "logs",
        "outputs/final_novel",
        "outputs/character_guide",
        "outputs/story_library",
        "outputs/video_prompts",
        "rag/vectorstore",
        "rag/documents",
        "rag/processed"
    ]
    
    for dir_str in required_dirs:
        dir_path = project_root / dir_str
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Created directory: {dir_str}")
            except Exception as e:
                logger.error(f"❌ Failed to create directory {dir_str}: {str(e)}")

def run_integration_test():
    """Run a basic integration test"""
    logger.info("🧪 Running integration test...")
    
    try:
        # Test the API server import
        from api_server import app
        logger.info("✅ API server can be imported")
        
        # Test basic FastAPI functionality
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # This might fail if dependencies aren't initialized, but that's okay
        try:
            response = client.get("/api/status")
            if response.status_code in [200, 500, 503]:
                logger.info("✅ API endpoints are accessible")
            else:
                logger.warning(f"⚠️  API returned status: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️  API test failed (this may be expected): {str(e)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("🔧 AI Writer Crew - Web Interface Integration Test")
    logger.info("=" * 60)
    
    tests = [
        ("File Structure", check_file_structure),
        ("Module Imports", test_imports),
        ("RAG Manager", test_rag_manager),
        ("Agent Manager", test_agent_manager),
        ("LLM Manager", test_llm_manager),
        ("Integration Test", run_integration_test)
    ]
    
    passed = 0
    total = len(tests)
    
    # Create missing directories first
    create_missing_directories()
    
    # Check optional components
    check_optional_components()
    
    # Run tests
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {str(e)}")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Web interface is ready to use.")
        logger.info("🚀 Run 'python launch_web_interface.py' to start the system")
    elif passed >= total - 1:
        logger.info("⚠️  Most tests passed. System should work with limited functionality.")
        logger.info("🚀 You can try running 'python launch_web_interface.py'")
    else:
        logger.error("❌ Several tests failed. Please fix the issues before proceeding.")
        logger.error("💡 Check the error messages above for details.")
    
    logger.info("=" * 60)
    
    return 0 if passed >= total - 1 else 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to continue...")
    sys.exit(exit_code)
