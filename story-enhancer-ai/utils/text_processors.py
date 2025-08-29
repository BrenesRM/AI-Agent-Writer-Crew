#"""Procesadores de texto y documentos"""
import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path

import PyPDF2
from docx import Document
import markdown
from config.rag_config import rag_config

class DocumentProcessor:
    """Procesador de documentos para diferentes formatos"""
    
    def __init__(self):
        self.supported_formats = rag_config.allowed_extensions
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Procesar un archivo y extraer texto y metadatos"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Verificar tamaño del archivo
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > rag_config.max_file_size_mb:
            raise ValueError(f"Archivo muy grande: {file_size_mb:.1f}MB > {rag_config.max_file_size_mb}MB")
        
        extension = file_path.suffix.lower().lstrip('.')
        
        if extension not in self.supported_formats:
            raise ValueError(f"Formato no soportado: {extension}")
        
        # Procesar según el tipo de archivo
        processor_map = {
            'pdf': self._process_pdf,
            'docx': self._process_docx,
            'txt': self._process_txt,
            'md': self._process_markdown,
            'json': self._process_json,
            'xlsx': self._process_excel
        }
        
        processor = processor_map.get(extension)
        if not processor:
            raise ValueError(f"No hay procesador para: {extension}")
        
        content = processor(file_path)
        
        return {
            'filename': file_path.name,
            'filepath': str(file_path),
            'extension': extension,
            'content': content,
            'size_mb': file_size_mb,
            'metadata': self._extract_metadata(file_path, content)
        }
    
    def _process_pdf(self, file_path: Path) -> str:
        """Procesar archivo PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            raise ValueError(f"Error procesando PDF: {str(e)}")
        return text.strip()
    
    def _process_docx(self, file_path: Path) -> str:
        """Procesar archivo DOCX"""
        try:
            doc = Document(file_path)
            text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error procesando DOCX: {str(e)}")
        return text.strip()
    
    def _process_txt(self, file_path: Path) -> str:
        """Procesar archivo TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
            except Exception as e:
                raise ValueError(f"Error procesando TXT: {str(e)}")
        return content.strip()
    
    def _process_markdown(self, file_path: Path) -> str:
        """Procesar archivo Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                md_content = file.read()
            # Convertir a HTML y luego extraer texto plano
            html = markdown.markdown(md_content)
            # Para simplicidad, retornamos el markdown original
            return md_content.strip()
        except Exception as e:
            raise ValueError(f"Error procesando Markdown: {str(e)}")
    
    def _process_json(self, file_path: Path) -> str:
        """Procesar archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            # Convertir JSON a texto legible
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error procesando JSON: {str(e)}")
    
    def _process_excel(self, file_path: Path) -> str:
        """Procesar archivo Excel"""
        try:
            # Leer todas las hojas
            excel_file = pd.ExcelFile(file_path)
            text_parts = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text_parts.append(f"=== Hoja: {sheet_name} ===")
                text_parts.append(df.to_string(index=False))
                text_parts.append("")
            
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Error procesando Excel: {str(e)}")
    
    def _extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extraer metadatos del archivo y contenido"""
        return {
            'word_count': len(content.split()),
            'char_count': len(content),
            'created_at': file_path.stat().st_ctime,
            'modified_at': file_path.stat().st_mtime,
            'file_size': file_path.stat().st_size
        }

class TextChunker:
    """Divisor de texto en chunks para RAG"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or rag_config.chunk_size
        self.chunk_overlap = chunk_overlap or rag_config.chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Dividir texto en chunks con overlap"""
        if not text.strip():
            return []
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Si no es el último chunk, buscar un punto de corte natural
            if end < len(text):
                # Buscar el último espacio, punto o salto de línea en los últimos 100 chars
                search_start = max(start, end - 100)
                natural_breaks = [
                    text.rfind('\n\n', search_start, end),
                    text.rfind('. ', search_start, end),
                    text.rfind('\n', search_start, end),
                    text.rfind(' ', search_start, end)
                ]
                
                natural_end = max([b for b in natural_breaks if b > search_start], default=end)
                if natural_end > search_start:
                    end = natural_end + (2 if text[natural_end:natural_end+2] == '\n\n' else 1)
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk_metadata = (metadata or {}).copy()
                chunk_metadata.update({
                    'chunk_id': chunk_id,
                    'start_pos': start,
                    'end_pos': end,
                    'chunk_length': len(chunk_text)
                })
                
                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk_metadata
                })
                
                chunk_id += 1
            
            # Calcular siguiente posición con overlap
            start = max(start + 1, end - self.chunk_overlap)
            
            if start >= len(text):
                break
        
        return chunks