# -*- coding: utf-8 -*-
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str = "Multi-Agent Novel System"
    project_root: Path = Path(__file__).parent.parent
    
    # LLM Configuration
    llm_model_path: str = ""
    llm_context_length: int = 4096
    llm_max_tokens: int = 2048
    
    # RAG Configuration
    chroma_persist_directory: str = "./rag/vectorstore"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
