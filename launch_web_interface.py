#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Writer Crew - Modern Web Interface Launcher
Starts the FastAPI server and serves the modern chat interface
"""
import os
import sys
import asyncio
import subprocess
import webbrowser
from pathlib import Path
import time
import signal
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'pydantic-settings'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Please install missing packages:")
        logger.info(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_model_exists():
    """Check if local LLM model exists"""
    model_path = project_root / "llm_local" / "models" / "model.gguf"
    
    if not model_path.exists():
        logger.warning("⚠️  Local LLM model not found!")
        logger.warning(f"Expected path: {model_path}")
        logger.warning("The system will work in limited mode without local LLM.")
        logger.warning("To add a model:")
        logger.warning("1. Download a GGUF model (e.g., from Hugging Face)")
        logger.warning("2. Place it at: llm_local/models/model.gguf")
        return False
    
    logger.info(f"✅ Local LLM model found: {model_path}")
    return True

def check_rag_documents():
    """Check if RAG documents exist"""
    docs_path = project_root / "data" / "reference_docs"
    
    if not docs_path.exists() or not list(docs_path.iterdir()):
        logger.warning("⚠️  No RAG documents found!")
        logger.warning(f"Expected path: {docs_path}")
        logger.warning("Add your reference documents to enhance AI responses.")
        return False
    
    doc_count = len(list(docs_path.glob("*.*")))
    logger.info(f"✅ Found {doc_count} RAG documents")
    return True

def start_server():
    """Start the FastAPI server"""
    try:
        logger.info("🚀 Starting AI Writer Crew API server...")
        
        # Import and run the server
        from api_server import app
        import uvicorn
        
        # Start the server in a separate process
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "api_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=project_root)
        
        return server_process
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {str(e)}")
        return None

def open_browser():
    """Open the browser to the chat interface"""
    url = "http://localhost:8000"
    
    # Wait a bit for the server to start
    time.sleep(3)
    
    try:
        logger.info(f"🌐 Opening browser to: {url}")
        webbrowser.open(url)
    except Exception as e:
        logger.warning(f"⚠️  Could not open browser automatically: {str(e)}")
        logger.info(f"Please manually open: {url}")

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("🎯 AI Writer Crew - Modern Web Interface")
    logger.info("=" * 60)
    
    # Check requirements
    logger.info("📋 Checking system requirements...")
    if not check_requirements():
        return 1
    
    # Check optional components
    check_model_exists()
    check_rag_documents()
    
    # Start server
    server_process = start_server()
    if not server_process:
        logger.error("❌ Failed to start server")
        return 1
    
    # Open browser
    open_browser()
    
    # Keep running and handle shutdown
    try:
        logger.info("✅ System is running!")
        logger.info("📖 Access the chat interface at: http://localhost:8000")
        logger.info("🔧 API documentation at: http://localhost:8000/docs")
        logger.info("Press Ctrl+C to stop the server")
        
        # Wait for the server process
        server_process.wait()
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        server_process.terminate()
        
        # Wait a bit for graceful shutdown
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning("⚠️  Force killing server process...")
            server_process.kill()
        
        logger.info("✅ Shutdown complete")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
