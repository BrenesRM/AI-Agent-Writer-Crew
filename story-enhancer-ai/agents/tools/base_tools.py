#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramientas base para todos los agentes del sistema
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import sys

# Agregar el directorio raíz al path para importaciones
sys.path.append(str(Path(__file__).parent.parent.parent))
from rag.vector_store import VectorStore

class RAGSearchTool(BaseTool):
    """Herramienta para buscar información en el sistema RAG"""
    name: str = "RAG Search"
    description: str = (
        "Busca información relevante en los documentos de referencia. "
        "Útil para encontrar lore, reglas del mundo, detalles de personajes, "
        "información histórica y contexto narrativo."
    )
    
    def __init__(self, collection_name: str = "documentos_procesados"):
        super().__init__()
        self.vector_store = VectorStore(collection_name)
    
    def _run(self, query: str, k: int = 5) -> str:
        """Ejecutar búsqueda en RAG"""
        try:
            results = self.vector_store.search(query, k=k)
            
            if not results:
                return f"No se encontró información relevante para: '{query}'"
            
            # Formatear resultados
            formatted_results = []
            for i, result in enumerate(results, 1):
                similarity = result.get('similarity', 0)
                source = result.get('source', 'Fuente desconocida')
                content = result.get('content', '')
                
                formatted_results.append(
                    f"**Resultado {i}** (Similitud: {similarity:.3f})\n"
                    f"**Fuente:** {source}\n"
                    f"**Contenido:** {content[:300]}...\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error en búsqueda RAG: {str(e)}"

class ManuscriptReaderTool(BaseTool):
    """Herramienta para leer el manuscrito base"""
    name: str = "Manuscript Reader"
    description: str = (
        "Lee y analiza el manuscrito base de la historia. "
        "Puede extraer capítulos específicos, personajes, tramas, o secciones completas."
    )
    
    def __init__(self, manuscript_path: str = "data/manuscripts/"):
        super().__init__()
        self.manuscript_path = Path(manuscript_path)
    
    def _run(self, section: str = "all", chapter: Optional[str] = None) -> str:
        """Leer manuscrito"""
        try:
            if not self.manuscript_path.exists():
                return "Error: Directorio de manuscritos no encontrado"
            
            # Buscar archivos de manuscrito
            manuscript_files = []
            for ext in ['*.docx', '*.txt', '*.md']:
                manuscript_files.extend(list(self.manuscript_path.glob(ext)))
            
            if not manuscript_files:
                return "Error: No se encontraron archivos de manuscrito"
            
            # Para simplificar, leer el primer archivo encontrado
            main_manuscript = manuscript_files[0]
            
            if main_manuscript.suffix == '.txt':
                with open(main_manuscript, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif main_manuscript.suffix == '.md':
                with open(main_manuscript, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # Para .docx necesitaríamos python-docx, pero por ahora devolvemos info básica
                return f"Manuscrito encontrado: {main_manuscript.name} ({main_manuscript.stat().st_size / 1024:.1f} KB)"
            
            if section == "summary":
                return f"**Manuscrito:** {main_manuscript.name}\n**Tamaño:** {len(content)} caracteres\n**Primeros 500 caracteres:**\n{content[:500]}..."
            elif section == "all":
                return content
            else:
                # Buscar sección específica
                lines = content.split('\n')
                relevant_lines = [line for line in lines if section.lower() in line.lower()]
                return "\n".join(relevant_lines[:10]) if relevant_lines else f"No se encontró la sección: {section}"
                
        except Exception as e:
            return f"Error leyendo manuscrito: {str(e)}"

class StoryElementExtractorTool(BaseTool):
    """Herramienta para extraer elementos específicos de la historia"""
    name: str = "Story Element Extractor"
    description: str = (
        "Extrae y analiza elementos específicos como personajes, lugares, "
        "eventos, diálogos, o temas de textos narrativos."
    )
    
    def _run(self, text: str, element_type: str = "characters") -> str:
        """Extraer elementos de la historia"""
        try:
            # Análisis básico por tipo de elemento
            if element_type.lower() == "characters":
                return self._extract_characters(text)
            elif element_type.lower() == "locations":
                return self._extract_locations(text)
            elif element_type.lower() == "events":
                return self._extract_events(text)
            elif element_type.lower() == "themes":
                return self._extract_themes(text)
            else:
                return f"Tipo de elemento no soportado: {element_type}"
                
        except Exception as e:
            return f"Error extrayendo elementos: {str(e)}"
    
    def _extract_characters(self, text: str) -> str:
        """Extraer menciones de personajes"""
        # Análisis simple - buscar nombres propios
        import re
        
        # Patrones básicos para nombres
        name_patterns = [
            r'\b[A-Z][a-z]+\b',  # Nombres simples
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Nombres compuestos
        ]
        
        potential_names = set()
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            potential_names.update(matches)
        
        # Filtrar palabras comunes que no son nombres
        common_words = {'The', 'And', 'But', 'For', 'With', 'Chapter', 'Book', 'Part'}
        names = [name for name in potential_names if name not in common_words]
        
        return f"Posibles personajes encontrados: {', '.join(sorted(names)[:20])}"
    
    def _extract_locations(self, text: str) -> str:
        """Extraer menciones de lugares"""
        # Buscar patrones de lugares
        import re
        
        location_indicators = [
            r'in [A-Z][a-z]+',
            r'at [A-Z][a-z]+',
            r'from [A-Z][a-z]+',
            r'to [A-Z][a-z]+'
        ]
        
        locations = set()
        for pattern in location_indicators:
            matches = re.findall(pattern, text)
            for match in matches:
                location = match.split()[-1]
                locations.add(location)
        
        return f"Posibles ubicaciones: {', '.join(sorted(locations)[:15])}"
    
    def _extract_events(self, text: str) -> str:
        """Extraer eventos principales"""
        # Buscar frases que indiquen eventos
        sentences = text.split('.')
        event_sentences = [s.strip() for s in sentences if len(s.strip()) > 20 and len(s.strip()) < 200]
        
        return f"Eventos principales (primeras 5 oraciones relevantes):\n" + "\n".join([f"- {s}." for s in event_sentences[:5]])
    
    def _extract_themes(self, text: str) -> str:
        """Extraer temas potenciales"""
        # Análisis básico de temas basado en palabras clave
        theme_keywords = {
            'Guerra': ['war', 'battle', 'fight', 'conflict', 'enemy', 'soldier', 'weapon', 'guerra', 'batalla', 'lucha', 'enemigo'],
            'Amor': ['love', 'heart', 'romance', 'kiss', 'beloved', 'amor', 'corazon', 'romance'],
            'Poder': ['power', 'king', 'queen', 'rule', 'throne', 'crown', 'poder', 'rey', 'reina', 'trono'],
            'Misterio': ['secret', 'mystery', 'unknown', 'hidden', 'mysterious', 'secreto', 'misterio', 'oculto'],
            'Magia': ['magic', 'spell', 'wizard', 'enchant', 'mystical', 'magia', 'hechizo', 'mago']
        }
        
        found_themes = {}
        text_lower = text.lower()
        
        for theme, keywords in theme_keywords.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            if count > 0:
                found_themes[theme] = count
        
        if found_themes:
            sorted_themes = sorted(found_themes.items(), key=lambda x: x[1], reverse=True)
            return f"Temas detectados: {', '.join([f'{theme} ({count})' for theme, count in sorted_themes])}"
        else:
            return "No se detectaron temas específicos con los patrones actuales"

class OutputWriterTool(BaseTool):
    """Herramienta para escribir outputs finales"""
    name: str = "Output Writer"
    description: str = (
        "Guarda contenido en archivos de output específicos. "
        "Puede escribir novelas, bibliotecas de lore, guías de personajes, etc."
    )
    
    def _run(self, content: str, output_type: str, filename: str = None) -> str:
        """Escribir output"""
        try:
            # Determinar directorio y archivo
            base_dir = Path("outputs")
            
            if output_type == "novel":
                output_dir = base_dir / "novel"
                default_filename = "enhanced_story.md"
            elif output_type == "library":
                output_dir = base_dir / "library"
                default_filename = "story_library.json"
            elif output_type == "characters":
                output_dir = base_dir / "characters"
                default_filename = "character_guide.md"
            elif output_type == "prompts":
                output_dir = base_dir / "prompts"
                default_filename = "video_prompts.json"
            else:
                return f"Tipo de output no soportado: {output_type}"
            
            # Crear directorio si no existe
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Usar filename proporcionado o default
            final_filename = filename if filename else default_filename
            output_path = output_dir / final_filename
            
            # Escribir archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Contenido guardado exitosamente en: {output_path}"
            
        except Exception as e:
            return f"Error escribiendo output: {str(e)}"