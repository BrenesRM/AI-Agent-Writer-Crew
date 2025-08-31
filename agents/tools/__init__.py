# agents/tools/__init__.py
from .rag_tool import RAGTool
from .writing_tools import WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer
from .analysis_tools import ConsistencyChecker, PacingAnalyzer, PlotAnalyzer
from .creative_tools import IdeaGenerator, VisualPromptGenerator

__all__ = [
    'RAGTool',
    'WritingAnalyzer', 
    'StyleAnalyzer',
    'CharacterAnalyzer',
    'ConsistencyChecker',
    'PacingAnalyzer', 
    'PlotAnalyzer',
    'IdeaGenerator',
    'VisualPromptGenerator'
]


# agents/tools/rag_tool.py
import logging
from typing import Dict, Any, Optional, List
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from rag.rag_manager import RAGManager

class RAGToolInput(BaseModel):
    query: str = Field(..., description="La consulta a realizar en la base de conocimiento")
    doc_type: Optional[str] = Field(None, description="Tipo de documento específico a buscar")
    k: int = Field(5, description="Número máximo de documentos relevantes a retornar")

class RAGTool(BaseTool):
    name: str = "Consultar Base de Conocimiento"
    description: str = """
    Herramienta para consultar la base de conocimiento RAG con documentos de referencia.
    Útil para obtener información sobre lore, personajes, reglas del mundo, referencias históricas,
    y cualquier otro contexto relevante para la historia.
    """
    args_schema: type[BaseModel] = RAGToolInput
    
    def __init__(self, **data):
        super().__init__(**data)
        self.rag_manager = RAGManager()
        self.logger = logging.getLogger(__name__)
    
    def _run(self, query: str, doc_type: Optional[str] = None, k: int = 5) -> str:
        """Ejecuta una consulta en el sistema RAG"""
        try:
            self.logger.info(f"Consultando RAG: {query}")
            
            result = self.rag_manager.query(query, k=k, doc_type=doc_type)
            
            if not result['context']:
                return f"No se encontró información relevante para: {query}"
            
            # Formatear respuesta
            response = f"INFORMACIÓN ENCONTRADA para '{query}':\n\n"
            response += result['context']
            response += f"\n\nFuentes consultadas: {result['num_sources']} documentos"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error en consulta RAG: {str(e)}")
            return f"Error consultando la base de conocimiento: {str(e)}"


# agents/tools/writing_tools.py
import re
import logging
from typing import Dict, Any, List, Tuple
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import nltk
from collections import Counter
from textblob import TextBlob

# Descargar recursos necesarios de NLTK (solo primera vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

class WritingAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto a analizar")

class WritingAnalyzer(BaseTool):
    name: str = "Analizador de Escritura"
    description: str = """
    Analiza un texto narrativo y proporciona estadísticas detalladas:
    - Conteo de palabras, párrafos, oraciones
    - Longitud promedio de oraciones
    - Diversidad léxica
    - Análisis de legibilidad
    """
    args_schema: type[BaseModel] = WritingAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza las características generales de un texto"""
        try:
            # Estadísticas básicas
            words = len(text.split())
            sentences = len(nltk.sent_tokenize(text))
            paragraphs = len([p for p in text.split('\n\n') if p.strip()])
            characters = len(text)
            
            # Longitud promedio de oraciones
            avg_sentence_length = words / max(sentences, 1)
            
            # Diversidad léxica
            unique_words = len(set(word.lower() for word in text.split()))
            lexical_diversity = unique_words / max(words, 1)
            
            # Palabras más frecuentes
            word_counts = Counter(word.lower().strip('.,!?;:"()[]') for word in text.split())
            most_common = word_counts.most_common(5)
            
            analysis = f"""ANÁLISIS DE ESCRITURA:
            
📊 ESTADÍSTICAS BÁSICAS:
- Palabras: {words:,}
- Oraciones: {sentences:,}
- Párrafos: {paragraphs:,}
- Caracteres: {characters:,}

📏 MÉTRICAS DE ESTILO:
- Longitud promedio de oración: {avg_sentence_length:.1f} palabras
- Diversidad léxica: {lexical_diversity:.2%}

🔤 PALABRAS MÁS FRECUENTES:
{chr(10).join([f"- {word}: {count} veces" for word, count in most_common])}

📖 EVALUACIÓN:
- Complejidad: {'Alta' if avg_sentence_length > 20 else 'Media' if avg_sentence_length > 15 else 'Baja'}
- Variedad vocabulario: {'Rica' if lexical_diversity > 0.7 else 'Media' if lexical_diversity > 0.5 else 'Limitada'}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando texto: {str(e)}"

class StyleAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto a analizar estilísticamente")

class StyleAnalyzer(BaseTool):
    name: str = "Analizador de Estilo"
    description: str = """
    Analiza el estilo narrativo de un texto:
    - Tono y sentimiento
    - Uso de diálogos
    - Perspectiva narrativa
    - Tiempo verbal dominante
    """
    args_schema: type[BaseModel] = StyleAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza el estilo narrativo del texto"""
        try:
            blob = TextBlob(text)
            
            # Análisis de sentimientos
            sentiment = blob.sentiment
            
            # Detectar diálogos
            dialogue_count = len(re.findall(r'["\'].*?["\']', text))
            dialogue_percentage = (dialogue_count * 100) / max(len(text.split()), 1)
            
            # Detectar perspectiva narrativa
            first_person = len(re.findall(r'\b(yo|me|mi|nosotros|nos)\b', text.lower()))
            third_person = len(re.findall(r'\b(él|ella|ellos|ellas)\b', text.lower()))
            
            if first_person > third_person:
                perspective = "Primera persona"
            elif third_person > first_person:
                perspective = "Tercera persona"
            else:
                perspective = "Mixta o indefinida"
            
            # Análisis de tiempo verbal (simple)
            past_tense = len(re.findall(r'\w+(ó|ía|aba|ieron|ado|ido)\b', text))
            present_tense = len(re.findall(r'\w+(a|e|o|an|en|on)\b', text))
            
            dominant_tense = "Pasado" if past_tense > present_tense else "Presente"
            
            # Determinar tono
            if sentiment.polarity > 0.1:
                tone = "Positivo"
            elif sentiment.polarity < -0.1:
                tone = "Negativo"
            else:
                tone = "Neutral"
            
            analysis = f"""ANÁLISIS DE ESTILO:
            
🎭 TONO Y SENTIMIENTO:
- Polaridad: {sentiment.polarity:.2f} (-1 negativo, +1 positivo)
- Subjetividad: {sentiment.subjectivity:.2f} (0 objetivo, 1 subjetivo)  
- Tono general: {tone}

👥 PERSPECTIVA NARRATIVA:
- Perspectiva dominante: {perspective}
- Marcadores 1ª persona: {first_person}
- Marcadores 3ª persona: {third_person}

🕐 TIEMPO NARRATIVO:
- Tiempo dominante: {dominant_tense}
- Marcadores de pasado: {past_tense}
- Marcadores de presente: {present_tense}

💬 DIÁLOGOS:
- Fragmentos de diálogo detectados: {dialogue_count}
- Porcentaje estimado de diálogo: {dialogue_percentage:.1f}%

📝 RECOMENDACIONES:
- {'Considera variar la perspectiva para mayor dinamismo' if perspective == 'Mixta o indefinida' else '✓ Perspectiva narrativa consistente'}
- {'Equilibra narración y diálogo' if dialogue_percentage < 10 or dialogue_percentage > 50 else '✓ Buen balance narración/diálogo'}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando estilo: {str(e)}"

class CharacterAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto que contiene personajes a analizar")

class CharacterAnalyzer(BaseTool):
    name: str = "Analizador de Personajes"
    description: str = """
    Identifica y analiza personajes en un texto narrativo:
    - Extrae nombres de personajes
    - Cuenta menciones de cada personaje
    - Identifica roles y relaciones
    """
    args_schema: type[BaseModel] = CharacterAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza los personajes presentes en el texto"""
        try:
            # Extraer nombres propios (patrón simple)
            names = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', text)
            
            # Filtrar nombres comunes que no son personajes
            common_words = {'El', 'La', 'Los', 'Las', 'Un', 'Una', 'Por', 'Para', 'Con', 'Sin', 'Sobre', 'Desde', 'Hasta'}
            character_names = [name for name in names if name not in common_words and len(name) > 2]
            
            # Contar menciones
            character_counts = Counter(character_names)
            
            # Buscar relaciones (patrones simples)
            relationships = []
            for char in character_counts.keys():
                # Buscar patrones de relación
                if re.search(rf'{char}.*?(hermano|hermana|padre|madre|hijo|hija)', text, re.IGNORECASE):
                    relationships.append(f"{char} - relación familiar mencionada")
                if re.search(rf'{char}.*?(amigo|amiga|enemigo|enemiga)', text, re.IGNORECASE):
                    relationships.append(f"{char} - relación de amistad/enemistad mencionada")
                if re.search(rf'{char}.*?(rey|reina|príncipe|princesa|lord|lady)', text, re.IGNORECASE):
                    relationships.append(f"{char} - posible rol de nobleza")
            
            analysis = f"""ANÁLISIS DE PERSONAJES:
            
👥 PERSONAJES IDENTIFICADOS:
{chr(10).join([f"- {char}: {count} menciones" for char, count in character_counts.most_common(10)])}

🔗 RELACIONES DETECTADAS:
{chr(10).join([f"- {rel}" for rel in relationships]) if relationships else "- No se detectaron relaciones explícitas"}

📊 ESTADÍSTICAS:
- Total de personajes únicos: {len(character_counts)}
- Personaje más mencionado: {character_counts.most_common(1)[0][0] if character_counts else 'Ninguno'} 
- Distribución de menciones: {'Equilibrada' if len(set(character_counts.values())) > 3 else 'Concentrada'}

💡 OBSERVACIONES:
- {'Historia centrada en pocos personajes' if len(character_counts) < 5 else 'Historia con amplio elenco de personajes'}
- {'Considerar desarrollar más a los personajes secundarios' if len(character_counts) > 1 and character_counts.most_common(1)[0][1] > sum(character_counts.values()) * 0.5 else '✓ Buen equilibrio entre personajes'}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando personajes: {str(e)}"


# agents/tools/analysis_tools.py
import re
import logging
from typing import Dict, Any, List
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class ConsistencyCheckerInput(BaseModel):
    text: str = Field(..., description="Texto a verificar por consistencia")
    reference_text: str = Field("", description="Texto de referencia para comparar consistencia")

class ConsistencyChecker(BaseTool):
    name: str = "Verificador de Consistencia"
    description: str = """
    Verifica la consistencia interna de un texto narrativo:
    - Detecta contradicciones en nombres y descripciones
    - Verifica continuidad temporal
    - Identifica inconsistencias en características de personajes
    """
    args_schema: type[BaseModel] = ConsistencyCheckerInput
    
    def _run(self, text: str, reference_text: str = "") -> str:
        """Verifica la consistencia del texto"""
        try:
            issues = []
            
            # Extraer nombres de personajes y lugares
            names = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', text)
            
            # Buscar variaciones en nombres (posibles inconsistencias)
            name_variations = {}
            for name in set(names):
                similar_names = [n for n in set(names) if n != name and (
                    name.startswith(n) or n.startswith(name) or 
                    abs(len(name) - len(n)) <= 2
                )]
                if similar_names:
                    name_variations[name] = similar_names
            
            if name_variations:
                issues.append("POSIBLES VARIACIONES EN NOMBRES:")
                for main_name, variations in name_variations.items():
                    issues.append(f"- {main_name} vs {', '.join(variations)}")
            
            # Verificar marcadores temporales
            time_markers = re.findall(r'\b(ayer|hoy|mañana|hace\s+\w+|después\s+de\s+\w+|antes\s+de\s+\w+)\b', text.lower())
            if len(set(time_markers)) > 5:
                issues.append("ADVERTENCIA: Múltiples marcadores temporales - verificar cronología")
            
            # Buscar contradictions en descripción física
            physical_descriptions = re.findall(r'(ojos\s+\w+|cabello\s+\w+|pelo\s+\w+|altura\s+\w+)', text.lower())
            if len(physical_descriptions) > len(set(physical_descriptions)):
                issues.append("POSIBLE INCONSISTENCIA: Descripciones físicas repetidas o contradictorias")
            
            # Comparar con texto de referencia si se proporciona
            if reference_text:
                ref_names = set(re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', reference_text))
                text_names = set(names)
                
                new_names = text_names - ref_names
                missing_names = ref_names - text_names
                
                if new_names:
                    issues.append(f"PERSONAJES NUEVOS: {', '.join(new_names)}")
                if missing_names:
                    issues.append(f"PERSONAJES AUSENTES: {', '.join(missing_names)}")
            
            if not issues:
                return "✅ No se detectaron inconsistencias evidentes en el texto."
            else:
                return "🔍 VERIFICACIÓN DE CONSISTENCIA:\n\n" + "\n".join(issues)
                
        except Exception as e:
            return f"Error verificando consistencia: {str(e)}"

class PacingAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto para analizar el ritmo narrativo")

class PacingAnalyzer(BaseTool):
    name: str = "Analizador de Ritmo"
    description: str = """
    Analiza el ritmo y flujo narrativo del texto:
    - Identifica variación en longitud de párrafos y oraciones
    - Detecta momentos de acción vs. reflexión
    - Evalúa el balance narrativo
    """
    args_schema: type[BaseModel] = PacingAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza el ritmo narrativo del texto"""
        try:
            # Dividir en párrafos
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            if not paragraphs:
                return "❌ No se pudieron identificar párrafos en el texto."
            
            # Análisis de longitud de párrafos
            paragraph_lengths = [len(p.split()) for p in paragraphs]
            avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths)
            
            # Variación en longitud de párrafos
            length_variation = max(paragraph_lengths) - min(paragraph_lengths)
            
            # Detectar párrafos de acción (oraciones cortas, verbos dinámicos)
            action_keywords = ['corrió', 'saltó', 'gritó', 'atacó', 'luchó', 'escapó', 'golpeó', 'disparó']
            action_paragraphs = []
            
            for i, p in enumerate(paragraphs):
                sentences = p.split('.')
                avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
                action_words = sum(1 for word in action_keywords if word.lower() in p.lower())
                
                if avg_sentence_length < 12 or action_words > 0:
                    action_paragraphs.append(i + 1)
            
            # Detectar párrafos reflexivos (oraciones largas, palabras introspectivas)
            reflection_keywords = ['pensó', 'reflexionó', 'recordó', 'sintió', 'consideró', 'meditó']
            reflective_paragraphs = []
            
            for i, p in enumerate(paragraphs):
                sentences = p.split('.')
                avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
                reflection_words = sum(1 for word in reflection_keywords if word.lower() in p.lower())
                
                if avg_sentence_length > 20 or reflection_words > 0:
                    reflective_paragraphs.append(i + 1)
            
            # Evaluar el ritmo general
            if length_variation < 20:
                rhythm_assessment = "Ritmo uniforme - considera variar la longitud de párrafos"
            elif length_variation > 100:
                rhythm_assessment = "Ritmo muy variable - buen dinamismo narrativo"
            else:
                rhythm_assessment = "Ritmo balanceado"
            
            analysis = f"""ANÁLISIS DE RITMO NARRATIVO:
            
📏 ESTRUCTURA:
- Total de párrafos: {len(paragraphs)}
- Longitud promedio: {avg_paragraph_length:.1f} palabras por párrafo
- Variación de longitud: {length_variation} palabras
- Párrafo más corto: {min(paragraph_lengths)} palabras
- Párrafo más largo: {max(paragraph_lengths)} palabras

⚡ MOMENTOS DE ACCIÓN:
- Párrafos identificados: {action_paragraphs if action_paragraphs else 'Ninguno detectado'}
- Porcentaje: {len(action_paragraphs) / len(paragraphs) * 100:.1f}%

🤔 MOMENTOS REFLEXIVOS:
- Párrafos identificados: {reflective_paragraphs if reflective_paragraphs else 'Ninguno detectado'}
- Porcentaje: {len(reflective_paragraphs) / len(paragraphs) * 100:.1f}%

🎯 EVALUACIÓN DEL RITMO:
- {rhythm_assessment}
- Balance acción/reflexión: {'Equilibrado' if abs(len(action_paragraphs) - len(reflective_paragraphs)) <= 2 else 'Desbalanceado hacia ' + ('acción' if len(action_paragraphs) > len(reflective_paragraphs) else 'reflexión')}

💡 RECOMENDACIONES:
- {'Añadir más momentos de acción para dinamismo' if len(action_paragraphs) < len(paragraphs) * 0.2 else ''}
- {'Incluir más momentos reflexivos para profundidad' if len(reflective_paragraphs) < len(paragraphs) * 0.2 else ''}
- {'✓ Buen equilibrio narrativo' if abs(len(action_paragraphs) - len(reflective_paragraphs)) <= 2 else ''}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando ritmo: {str(e)}"

class PlotAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto narrativo para analizar la trama")

class PlotAnalyzer(BaseTool):
    name: str = "Analizador de Trama"
    description: str = """
    Analiza la estructura narrativa y elementos de la trama:
    - Identifica puntos de la trama (exposición, conflicto, clímax, resolución)
    - Detecta subtramas
    - Evalúa la progresión narrativa
    """
    args_schema: type[BaseModel] = PlotAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza los elementos de la trama"""
        try:
            # Dividir el texto en secciones
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            total_length = len(text.split())
            
            # Detectar elementos de exposición (típicamente al inicio)
            exposition_markers = ['había una vez', 'en un reino', 'hace mucho tiempo', 'era una vez']
            has_exposition = any(marker in text.lower() for marker in exposition_markers)
            
            # Detectar conflicto/tensión
            conflict_markers = ['pero', 'sin embargo', 'repentinamente', 'de pronto', 'amenaza', 'peligro', 'problema']
            conflict_count = sum(1 for marker in conflict_markers if marker in text.lower())
            
            # Detectar clímax (palabras intensas, típicamente en la parte media-final)
            climax_markers = ['batalla', 'lucha', 'enfrentamiento', 'decisión', 'momento crucial', 'todo dependía']
            climax_indicators = sum(1 for marker in climax_markers if marker in text.lower())
            
            # Detectar resolución
            resolution_markers = ['finalmente', 'al final', 'por último', 'así fue como', 'desde entonces']
            has_resolution = any(marker in text.lower() for marker in resolution_markers)
            
            # Analizar progresión temporal
            time_progression = len(re.findall(r'\b(luego|después|más tarde|entonces|posteriormente)\b', text.lower()))
            
            # Detectar posibles subtramas (cambios de enfoque o personajes)
            character_names = list(set(re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', text)))
            subplot_potential = len(character_names) > 3
            
            # Evaluar estructura general
            structure_score = 0
            structure_feedback = []
            
            if has_exposition:
                structure_score += 1
                structure_feedback.append("✓ Exposición presente")
            else:
                structure_feedback.append("⚠ Exposición no clara")
            
            if conflict_count > 0:
                structure_score += 1
                structure_feedback.append("✓ Elementos de conflicto detectados")
            else:
                structure_feedback.append("⚠ Falta desarrollo del conflicto")
            
            if climax_indicators > 0:
                structure_score += 1
                structure_feedback.append("✓ Momentos de intensidad presentes")
            else:
                structure_feedback.append("⚠ Clímax no evidente")
                
            if has_resolution:
                structure_score += 1
                structure_feedback.append("✓ Resolución identificada")
            else:
                structure_feedback.append("⚠ Resolución incompleta")
            
            analysis = f"""ANÁLISIS DE TRAMA:
            
📖 ESTRUCTURA NARRATIVA:
- Puntuación estructural: {structure_score}/4
{chr(10).join([f"- {feedback}" for feedback in structure_feedback])}

🔥 ELEMENTOS DE TENSIÓN:
- Marcadores de conflicto: {conflict_count}
- Indicadores de clímax: {climax_indicators}
- Progresión temporal: {time_progression} transiciones

👥 COMPLEJIDAD NARRATIVA:
- Personajes principales: {len(character_names)}
- Potencial de subtramas: {'Alto' if subplot_potential else 'Bajo'}

⏳ FLUJO TEMPORAL:
- Transiciones temporales: {time_progression}
- Progresión: {'Fluida' if time_progression > 3 else 'Estática'}

🎭 EVALUACIÓN GENERAL:
- Estructura: {'Sólida' if structure_score >= 3 else 'En desarrollo' if structure_score >= 2 else 'Necesita trabajo'}
- Complejidad: {'Alta' if len(character_names) > 5 else 'Media' if len(character_names) > 2 else 'Simple'}
- Tensión narrativa: {'Adecuada' if conflict_count > 2 else 'Insuficiente'}

💡 SUGERENCIAS:
- {'Desarrollar más el conflicto central' if conflict_count < 2 else ''}
- {'Clarificar el momento climático' if climax_indicators == 0 else ''}
- {'Fortalecer la resolución' if not has_resolution else ''}
- {'Considerar subtramas para enriquecer la narrativa' if not subplot_potential else ''}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando trama: {str(e)}"