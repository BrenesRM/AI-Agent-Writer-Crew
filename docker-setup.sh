#!/bin/bash
# Docker Setup and Usage Commands for AI Agent Writer Crew

# =============================================================================
# INITIAL SETUP
# =============================================================================

echo "=== AI Agent Writer Crew - Docker Setup ==="

# 1. Build the Docker image
echo "Building Docker image..."
docker build -t ai-writer-crew .

# 2. Create and start all services
echo "Starting all services with docker-compose..."
docker-compose up -d

# =============================================================================
# INDIVIDUAL SERVICE COMMANDS
# =============================================================================

# Start only the main application
docker-compose up -d ai-writer

# Start Streamlit frontend
docker-compose up -d frontend-streamlit
echo "Streamlit will be available at: http://localhost:8501"

# Start RAG service
docker-compose up -d rag-service

# Run agent tests
docker-compose up agent-test

# =============================================================================
# INTERACTIVE USAGE
# =============================================================================

# Open interactive shell in the container
docker-compose exec ai-writer bash

# Run specific Python commands
docker-compose exec ai-writer python -c "from agents.agent_manager import AgentManager; print('Available agents:', len(AgentManager().list_agents()))"

# Test RAG system
docker-compose exec ai-writer python scripts/test_rag.py

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

# View logs of a specific service
docker-compose logs -f frontend-streamlit

# Restart a service
docker-compose restart ai-writer

# Stop all services
docker-compose down

# Stop and remove all containers, networks, and volumes
docker-compose down -v

# =============================================================================
# DATA MANAGEMENT
# =============================================================================

# Copy documents to the container for processing
echo "To add reference documents:"
echo "1. Place your documents in ./data/reference_docs/ on the host"
echo "2. They will be automatically available in the container"

# Process documents with RAG
docker-compose exec ai-writer python -c "
from rag.rag_manager import RAGManager
rag = RAGManager()
rag.ingest_directory('data/reference_docs')
print('Documents processed!')
print('Stats:', rag.get_stats())
"

# =============================================================================
# MANUSCRIPT PROCESSING
# =============================================================================

# Process a manuscript with the agent system
docker-compose exec ai-writer python -c "
from agents.agent_manager import AgentManager

# Load your manuscript
with open('data/manuscripts/your_manuscript.txt', 'r') as f:
    manuscript = f.read()

# Initialize agent manager and process
manager = AgentManager()
manager.set_manuscript(manuscript)
summary = manager.get_analysis_summary()
print('Analysis complete!')
print(summary)
"

# =============================================================================
# MONITORING AND MAINTENANCE
# =============================================================================

# Check container status
docker-compose ps

# View resource usage
docker stats

# Access container shell for debugging
docker-compose exec ai-writer bash

# =============================================================================
# EXAMPLE WORKFLOW
# =============================================================================

echo "=== Example Complete Workflow ==="
echo "1. Start services:"
echo "   docker-compose up -d"
echo ""
echo "2. Access Streamlit UI:"
echo "   http://localhost:8501"
echo ""
echo "3. Or use command line:"
echo "   docker-compose exec ai-writer python scripts/test_rag.py"
echo ""
echo "4. Process your manuscript:"
echo "   # Place your manuscript in ./data/manuscripts/"
echo "   docker-compose exec ai-writer python -c 'from agents.agent_manager import AgentManager; manager = AgentManager(); print(\"Ready to process!\")'"
echo ""
echo "5. View results:"
echo "   # Check ./outputs/ directory for generated content"