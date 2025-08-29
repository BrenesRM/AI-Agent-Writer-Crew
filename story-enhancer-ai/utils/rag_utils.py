#"""Utilidades para el sistema RAG"""
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from rag.vector_store import VectorStore
from rag.document_ingestion import DocumentIngestion

class RAGManager:
    """Gestor principal del sistema RAG"""
    
    def __init__(self, collection_name: str = "story_documents"):
        self.collection_name = collection_name
        self.vector_store = VectorStore(collection_name)
        self.ingestion = DocumentIngestion(collection_name)
        self.history_file = Path("data/processed/search_history.json")
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
    
    def quick_setup(self) -> Dict[str, Any]:
        """Configuración rápida inicial"""
        results = {
            "status": "success",
            "steps": [],
            "warnings": []
        }
        
        # Verificar configuración
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_key_here":
            results["warnings"].append("OpenAI API key no configurada, usando modelo local")
        
        # Crear directorios necesarios
        dirs_to_create = [
            "data/documents",
            "data/manuscripts", 
            "data/processed",
            "outputs/novels",
            "outputs/libraries",
            "outputs/characters",
            "outputs/video_prompts"
        ]
        
        for dir_path in dirs_to_create:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        results["steps"].append("Directorios creados")
        
        # Verificar estado del vector store
        stats = self.vector_store.get_collection_stats()
        results["vector_store_stats"] = stats
        results["steps"].append(f"Vector store verificado: {stats.get('total_chunks', 0)} chunks")
        
        return results
    
    def ingest_documents_interactive(self) -> Dict[str, Any]:
        """Ingesta interactiva de documentos"""
        print("📁 Ingesta de Documentos de Referencia")
        print("-" * 40)
        
        documents_dir = Path("data/documents")
        
        # Verificar si hay documentos
        existing_files = []
        for ext in ["pdf", "docx", "txt", "json", "md", "xlsx"]:
            existing_files.extend(list(documents_dir.glob(f"*.{ext}")))
        
        if existing_files:
            print(f"📄 Encontrados {len(existing_files)} documentos:")
            for file in existing_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  - {file.name} ({size_mb:.1f}MB)")
            
            # Procesar automáticamente
            results = self.ingestion.ingest_directory(str(documents_dir))
            
            print(f"\n✅ Procesamiento completado:")
            print(f"  - Archivos procesados: {results['summary']['successful']}")
            print(f"  - Total de chunks: {results['total_chunks']}")
            
            if results['failed_files']:
                print(f"  - Archivos con errores: {len(results['failed_files'])}")
        
        else:
            print("ℹ️  No se encontraron documentos en data/documents/")
            print("   Puedes agregar archivos PDF, DOCX, TXT, JSON, MD o XLSX")
            results = {"message": "No documents found"}
        
        return results
    
    def search_with_history(self, query: str, k: int = 5) -> Dict[str, Any]:
        """Búsqueda con historial"""
        # Realizar búsqueda
        results = self.vector_store.search(query, k)
        
        # Guardar en historial
        search_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results_count": len(results),
            "top_sources": [r['source'] for r in results[:3]]
        }
        
        self._save_search_history(search_entry)
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    def get_context_for_agents(self, topic: str, max_chunks: int = 8) -> List[Dict[str, Any]]:
        """Obtener contexto relevante para los agentes"""
        results = self.vector_store.search(topic, k=max_chunks)
        
        # Formatear para uso de agentes
        context_chunks = []
        for result in results:
            context_chunks.append({
                "content": result['content'],
                "source": result['source'],
                "relevance": result['similarity'],
                "metadata": result['metadata']
            })
        
        return context_chunks
    
    def _save_search_history(self, entry: Dict[str, Any]):
        """Guardar entrada en historial de búsquedas"""
        try:
            # Cargar historial existente
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Agregar nueva entrada
            history.append(entry)
            
            # Mantener solo las últimas 100 búsquedas
            if len(history) > 100:
                history = history[-100:]
            
            # Guardar
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️  Error guardando historial: {e}")
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """Obtener historial de búsquedas"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def export_knowledge_base(self) -> Dict[str, Any]:
        """Exportar base de conocimientos"""
        stats = self.vector_store.get_collection_stats()
        
        # Obtener muestra de documentos
        sample_queries = [
            "personajes principales",
            "lugares importantes", 
            "sistema de magia",
            "historia del mundo",
            "reglas narrativas"
        ]
        
        knowledge_export = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "collection_stats": stats,
                "total_chunks": stats.get('total_chunks', 0)
            },
            "sample_knowledge": {}
        }
        
        for query in sample_queries:
            results = self.vector_store.search(query, k=3)
            knowledge_export["sample_knowledge"][query] = [
                {
                    "content": r['content'][:300] + "...",
                    "source": r['source'],
                    "relevance": r['similarity']
                }
                for r in results
            ]
        
        # Guardar export
        export_file = Path("outputs/libraries/knowledge_base_export.json")
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_export, f, ensure_ascii=False, indent=2)
        
        return knowledge_export

def create_sample_documents():
    """Crear documentos de muestra para pruebas"""
    documents_dir = Path("data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    
    # Documento de worldbuilding
    worldbuilding = """# Worldbuilding: Reino de Aetheria

## Geografía
El Reino de Aetheria se extiende por tres continentes principales:
- **Lumina**: Continente de la luz, hogar de la Academia de Magia
- **Umbra**: Continente de las sombras, territorio peligroso
- **Equilibrium**: Continente neutral, centro de comercio

## Sistema de Magia
La magia en Aetheria se basa en seis elementos fundamentales:
1. **Fuego**: Destructivo pero purificador
2. **Agua**: Sanador y adaptable  
3. **Tierra**: Estable y defensivo
4. **Aire**: Rápido y evasivo
5. **Luz**: Revelador y protector
6. **Sombra**: Oculto y manipulador

Los magos deben especializarse en máximo dos elementos complementarios.

## Jerarquía Mágica
- Novato (0-2 años de estudio)
- Aprendiz (3-7 años de estudio)
- Adepto (8-15 años de estudio)  
- Maestro (16-25 años de estudio)
- Archimago (26+ años de estudio)
"""
    
    with open(documents_dir / "worldbuilding.md", "w", encoding="utf-8") as f:
        f.write(worldbuilding)
    
    # Guía de personajes
    characters = {
        "main_characters": {
            "Alex": {
                "full_name": "Alexander Brightward",
                "age": 18,
                "origin": "Valle Verde",
                "magic_affinity": ["Luz", "Fuego"],
                "personality": ["valiente", "curioso", "impulsivo"],
                "background": "Huérfano criado por granjeros, descubre su potencial mágico a los 17",
                "arc": "De novato inseguro a héroe confiado"
            },
            "Eldrin": {
                "full_name": "Maestro Eldrin Starweaver", 
                "age": 165,
                "origin": "Academia de Lumina",
                "magic_affinity": ["Luz", "Aire"],
                "personality": ["sabio", "paciente", "misterioso"],
                "role": "Mentor principal de Alex",
                "secret": "Fue alumno del anterior Archimago Oscuro"
            },
            "Lyra": {
                "full_name": "Lyra Moonwhisper",
                "age": 19,
                "origin": "Bosques de Plata",
                "magic_affinity": ["Agua", "Tierra"], 
                "personality": ["intuitiva", "protectora", "independiente"],
                "role": "Compañera de Alex, sanadora del grupo"
            }
        },
        "antagonists": {
            "Void_Shadow": {
                "name": "Sombra del Vacío",
                "origin": "Dimensión paralela",
                "magic_affinity": ["Sombra", "Vacío"],
                "motivation": "Consumir toda la luz y magia del mundo",
                "weakness": "La magia de luz pura combinada"
            }
        }
    }
    
    with open(documents_dir / "characters.json", "w", encoding="utf-8") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)
    
    # Reglas narrativas
    narrative_rules = """# Reglas Narrativas para la Historia

## Tono y Estilo
- **Género**: Fantasía épica juvenil
- **Tono**: Aventurero pero con momentos de reflexión
- **Estilo**: Narrativa en tercera persona, lenguaje accesible
- **Ritmo**: Alternancia entre acción y desarrollo de personajes

## Reglas del Sistema Mágico
1. La magia tiene un costo: fatiga mental y física
2. Los hechizos poderosos requieren tiempo de preparación
3. La magia emocional (ira, miedo) es impredecible
4. Los elementos opuestos se cancelan (Luz vs Sombra, Fuego vs Agua)
5. La sobre-utilización causa "agotamiento mágico"

## Estructura Narrativa
- **Acto I**: Descubrimiento y llamada a la aventura
- **Acto II**: Entrenamiento y primeros conflictos  
- **Acto III**: Crisis y crecimiento del personaje
- **Acto IV**: Confrontación final y resolución

## Arcos de Personajes Obligatorios
- Alex debe fallar antes de triunfar (crecimiento por adversidad)
- Lyra debe superar su desconfianza inicial hacia los humanos
- Eldrin debe revelar su pasado conectado con la oscuridad
- El grupo debe separarse y reunirse al menos una vez

## Elementos Recurrentes
- Los sueños proféticos de Alex
- Las runas antiguas como pistas
- La importancia de la amistad sobre el poder individual
- La conexión entre emociones y control mágico
"""
    
    with open(documents_dir / "narrative_rules.txt", "w", encoding="utf-8") as f:
        f.write(narrative_rules)
    
    return {
        "created_files": [
            "worldbuilding.md",
            "characters.json", 
            "narrative_rules.txt"
        ],
        "location": str(documents_dir)
    }