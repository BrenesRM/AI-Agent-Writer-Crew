# -*- coding: utf-8 -*-
# agents/tools/writing_tools.py
import re
import logging
from typing import Dict, Any, List, Tuple
from crewai.tools import BaseTool
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
    Analiza un texto narrativo y proporciona estadisticas detalladas:
    - Conteo de palabras, parrafos, oraciones
    - Longitud promedio de oraciones
    - Diversidad lexica
    - Analisis de legibilidad
    """
    args_schema: type[BaseModel] = WritingAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza las caracteristicas generales de un texto"""
        try:
            # Estadisticas basicas
            words = len(text.split())
            sentences = len(nltk.sent_tokenize(text))
            paragraphs = len([p for p in text.split('\n\n') if p.strip()])
            characters = len(text)
            
            # Longitud promedio de oraciones
            avg_sentence_length = words / max(sentences, 1)
            
            # Diversidad lexica
            unique_words = len(set(word.lower() for word in text.split()))
            lexical_diversity = unique_words / max(words, 1)
            
            # Palabras mas frecuentes
            word_counts = Counter(word.lower().strip('.,!?;:"()[]') for word in text.split())
            most_common = word_counts.most_common(5)
            
            analysis = f"""ANALISIS DE ESCRITURA:
            
📊 ESTADISTICAS BASICAS:
- Palabras: {words:,}
- Oraciones: {sentences:,}
- Parrafos: {paragraphs:,}
- Caracteres: {characters:,}

📏 METRICAS DE ESTILO:
- Longitud promedio de oracion: {avg_sentence_length:.1f} palabras
- Diversidad lexica: {lexical_diversity:.2%}

🔤 PALABRAS MAS FRECUENTES:
{chr(10).join([f"- {word}: {count} veces" for word, count in most_common])}

📖 EVALUACION:
- Complejidad: {'Alta' if avg_sentence_length > 20 else 'Media' if avg_sentence_length > 15 else 'Baja'}
- Variedad vocabulario: {'Rica' if lexical_diversity > 0.7 else 'Media' if lexical_diversity > 0.5 else 'Limitada'}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando texto: {str(e)}"

class StyleAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto a analizar estilisticamente")

class StyleAnalyzer(BaseTool):
    name: str = "Analizador de Estilo"
    description: str = """
    Analiza el estilo narrativo de un texto:
    - Tono y sentimiento
    - Uso de dialogos
    - Perspectiva narrativa
    - Tiempo verbal dominante
    """
    args_schema: type[BaseModel] = StyleAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza el estilo narrativo del texto"""
        try:
            blob = TextBlob(text)
            
            # Analisis de sentimientos
            sentiment = blob.sentiment
            
            # Detectar dialogos
            dialogue_count = len(re.findall(r'["\'].*?["\']', text))
            dialogue_percentage = (dialogue_count * 100) / max(len(text.split()), 1)
            
            # Detectar perspectiva narrativa
            first_person = len(re.findall(r'\b(yo|me|mi|nosotros|nos)\b', text.lower()))
            third_person = len(re.findall(r'\b(el|ella|ellos|ellas)\b', text.lower()))
            
            if first_person > third_person:
                perspective = "Primera persona"
            elif third_person > first_person:
                perspective = "Tercera persona"
            else:
                perspective = "Mixta o indefinida"
            
            # Analisis de tiempo verbal (simple)
            past_tense = len(re.findall(r'\w+(o|ia|aba|ieron|ado|ido)\b', text))
            present_tense = len(re.findall(r'\w+(a|e|o|an|en|on)\b', text))
            
            dominant_tense = "Pasado" if past_tense > present_tense else "Presente"
            
            # Determinar tono
            if sentiment.polarity > 0.1:
                tone = "Positivo"
            elif sentiment.polarity < -0.1:
                tone = "Negativo"
            else:
                tone = "Neutral"
            
            analysis = f"""ANALISIS DE ESTILO:
            
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

💬 DIALOGOS:
- Fragmentos de dialogo detectados: {dialogue_count}
- Porcentaje estimado de dialogo: {dialogue_percentage:.1f}%

📝 RECOMENDACIONES:
- {'Considera variar la perspectiva para mayor dinamismo' if perspective == 'Mixta o indefinida' else '✓ Perspectiva narrativa consistente'}
- {'Equilibra narracion y dialogo' if dialogue_percentage < 10 or dialogue_percentage > 50 else '✓ Buen balance narracion/dialogo'}
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
            # Extraer nombres propios (patron simple)
            names = re.findall(r'\b[A-ZAEIOUÑ][a-zaeiouñ]+(?:\s+[A-ZAEIOUÑ][a-zaeiouñ]+)*\b', text)
            
            # Filtrar nombres comunes que no son personajes
            common_words = {'El', 'La', 'Los', 'Las', 'Un', 'Una', 'Por', 'Para', 'Con', 'Sin', 'Sobre', 'Desde', 'Hasta'}
            character_names = [name for name in names if name not in common_words and len(name) > 2]
            
            # Contar menciones
            character_counts = Counter(character_names)
            
            # Buscar relaciones (patrones simples)
            relationships = []
            for char in character_counts.keys():
                # Buscar patrones de relacion
                if re.search(rf'{char}.*?(hermano|hermana|padre|madre|hijo|hija)', text, re.IGNORECASE):
                    relationships.append(f"{char} - relacion familiar mencionada")
                if re.search(rf'{char}.*?(amigo|amiga|enemigo|enemiga)', text, re.IGNORECASE):
                    relationships.append(f"{char} - relacion de amistad/enemistad mencionada")
                if re.search(rf'{char}.*?(rey|reina|principe|princesa|lord|lady)', text, re.IGNORECASE):
                    relationships.append(f"{char} - posible rol de nobleza")
            
            analysis = f"""ANALISIS DE PERSONAJES:
            
👥 PERSONAJES IDENTIFICADOS:
{chr(10).join([f"- {char}: {count} menciones" for char, count in character_counts.most_common(10)])}

🔗 RELACIONES DETECTADAS:
{chr(10).join([f"- {rel}" for rel in relationships]) if relationships else "- No se detectaron relaciones explicitas"}

📊 ESTADISTICAS:
- Total de personajes unicos: {len(character_counts)}
- Personaje mas mencionado: {character_counts.most_common(1)[0][0] if character_counts else 'Ninguno'} 
- Distribucion de menciones: {'Equilibrada' if len(set(character_counts.values())) > 3 else 'Concentrada'}

💡 OBSERVACIONES:
- {'Historia centrada en pocos personajes' if len(character_counts) < 5 else 'Historia con amplio elenco de personajes'}
- {'Considerar desarrollar mas a los personajes secundarios' if len(character_counts) > 1 and character_counts.most_common(1)[0][1] > sum(character_counts.values()) * 0.5 else '✓ Buen equilibrio entre personajes'}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando personajes: {str(e)}"