# -*- coding: utf-8 -*-
# agents/tools/analysis_tools.py
import re
import logging
from typing import Dict, Any, List
from crewai.tools import BaseTool
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
    - Identifica inconsistencias en caracteristicas de personajes
    """
    args_schema: type[BaseModel] = ConsistencyCheckerInput
    
    def _run(self, text: str, reference_text: str = "") -> str:
        """Verifica la consistencia del texto"""
        try:
            issues = []
            
            # Extraer nombres de personajes y lugares
            names = re.findall(r'\b[A-ZAEIOUÑ][a-zaeiouñ]+(?:\s+[A-ZAEIOUÑ][a-zaeiouñ]+)*\b', text)
            
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
            time_markers = re.findall(r'\b(ayer|hoy|mañana|hace\s+\w+|despues\s+de\s+\w+|antes\s+de\s+\w+)\b', text.lower())
            if len(set(time_markers)) > 5:
                issues.append("ADVERTENCIA: Multiples marcadores temporales - verificar cronologia")
            
            # Buscar contradictions en descripcion fisica
            physical_descriptions = re.findall(r'(ojos\s+\w+|cabello\s+\w+|pelo\s+\w+|altura\s+\w+)', text.lower())
            if len(physical_descriptions) > len(set(physical_descriptions)):
                issues.append("POSIBLE INCONSISTENCIA: Descripciones fisicas repetidas o contradictorias")
            
            # Comparar con texto de referencia si se proporciona
            if reference_text:
                ref_names = set(re.findall(r'\b[A-ZAEIOUÑ][a-zaeiouñ]+(?:\s+[A-ZAEIOUÑ][a-zaeiouñ]+)*\b', reference_text))
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
                return "🔍 VERIFICACION DE CONSISTENCIA:\n\n" + "\n".join(issues)
                
        except Exception as e:
            return f"Error verificando consistencia: {str(e)}"

class PacingAnalyzerInput(BaseModel):
    text: str = Field(..., description="Texto para analizar el ritmo narrativo")

class PacingAnalyzer(BaseTool):
    name: str = "Analizador de Ritmo"
    description: str = """
    Analiza el ritmo y flujo narrativo del texto:
    - Identifica variacion en longitud de parrafos y oraciones
    - Detecta momentos de accion vs. reflexion
    - Evalua el balance narrativo
    """
    args_schema: type[BaseModel] = PacingAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza el ritmo narrativo del texto"""
        try:
            # Dividir en parrafos
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            if not paragraphs:
                return "❌ No se pudieron identificar parrafos en el texto."
            
            # Analisis de longitud de parrafos
            paragraph_lengths = [len(p.split()) for p in paragraphs]
            avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths)
            
            # Variacion en longitud de parrafos
            length_variation = max(paragraph_lengths) - min(paragraph_lengths)
            
            # Detectar parrafos de accion (oraciones cortas, verbos dinamicos)
            action_keywords = ['corrio', 'salto', 'grito', 'ataco', 'lucho', 'escapo', 'golpeo', 'disparo']
            action_paragraphs = []
            
            for i, p in enumerate(paragraphs):
                sentences = p.split('.')
                avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
                action_words = sum(1 for word in action_keywords if word.lower() in p.lower())
                
                if avg_sentence_length < 12 or action_words > 0:
                    action_paragraphs.append(i + 1)
            
            # Detectar parrafos reflexivos (oraciones largas, palabras introspectivas)
            reflection_keywords = ['penso', 'reflexiono', 'recordo', 'sintio', 'considero', 'medito']
            reflective_paragraphs = []
            
            for i, p in enumerate(paragraphs):
                sentences = p.split('.')
                avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
                reflection_words = sum(1 for word in reflection_keywords if word.lower() in p.lower())
                
                if avg_sentence_length > 20 or reflection_words > 0:
                    reflective_paragraphs.append(i + 1)
            
            # Evaluar el ritmo general
            if length_variation < 20:
                rhythm_assessment = "Ritmo uniforme - considera variar la longitud de parrafos"
            elif length_variation > 100:
                rhythm_assessment = "Ritmo muy variable - buen dinamismo narrativo"
            else:
                rhythm_assessment = "Ritmo balanceado"
            
            analysis = f"""ANALISIS DE RITMO NARRATIVO:
            
📏 ESTRUCTURA:
- Total de parrafos: {len(paragraphs)}
- Longitud promedio: {avg_paragraph_length:.1f} palabras por parrafo
- Variacion de longitud: {length_variation} palabras
- Parrafo mas corto: {min(paragraph_lengths)} palabras
- Parrafo mas largo: {max(paragraph_lengths)} palabras

⚡ MOMENTOS DE ACCION:
- Parrafos identificados: {action_paragraphs if action_paragraphs else 'Ninguno detectado'}
- Porcentaje: {len(action_paragraphs) / len(paragraphs) * 100:.1f}%

🤔 MOMENTOS REFLEXIVOS:
- Parrafos identificados: {reflective_paragraphs if reflective_paragraphs else 'Ninguno detectado'}
- Porcentaje: {len(reflective_paragraphs) / len(paragraphs) * 100:.1f}%

🎯 EVALUACION DEL RITMO:
- {rhythm_assessment}
- Balance accion/reflexion: {'Equilibrado' if abs(len(action_paragraphs) - len(reflective_paragraphs)) <= 2 else 'Desbalanceado hacia ' + ('accion' if len(action_paragraphs) > len(reflective_paragraphs) else 'reflexion')}

💡 RECOMENDACIONES:
- {'Añadir mas momentos de accion para dinamismo' if len(action_paragraphs) < len(paragraphs) * 0.2 else ''}
- {'Incluir mas momentos reflexivos para profundidad' if len(reflective_paragraphs) < len(paragraphs) * 0.2 else ''}
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
    - Identifica puntos de la trama (exposicion, conflicto, climax, resolucion)
    - Detecta subtramas
    - Evalua la progresion narrativa
    """
    args_schema: type[BaseModel] = PlotAnalyzerInput
    
    def _run(self, text: str) -> str:
        """Analiza los elementos de la trama"""
        try:
            # Dividir el texto en secciones
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            total_length = len(text.split())
            
            # Detectar elementos de exposicion (tipicamente al inicio)
            exposition_markers = ['habia una vez', 'en un reino', 'hace mucho tiempo', 'era una vez']
            has_exposition = any(marker in text.lower() for marker in exposition_markers)
            
            # Detectar conflicto/tension
            conflict_markers = ['pero', 'sin embargo', 'repentinamente', 'de pronto', 'amenaza', 'peligro', 'problema']
            conflict_count = sum(1 for marker in conflict_markers if marker in text.lower())
            
            # Detectar climax (palabras intensas, tipicamente en la parte media-final)
            climax_markers = ['batalla', 'lucha', 'enfrentamiento', 'decision', 'momento crucial', 'todo dependia']
            climax_indicators = sum(1 for marker in climax_markers if marker in text.lower())
            
            # Detectar resolucion
            resolution_markers = ['finalmente', 'al final', 'por ultimo', 'asi fue como', 'desde entonces']
            has_resolution = any(marker in text.lower() for marker in resolution_markers)
            
            # Analizar progresion temporal
            time_progression = len(re.findall(r'\b(luego|despues|mas tarde|entonces|posteriormente)\b', text.lower()))
            
            # Detectar posibles subtramas (cambios de enfoque o personajes)
            character_names = list(set(re.findall(r'\b[A-ZAEIOUÑ][a-zaeiouñ]+\b', text)))
            subplot_potential = len(character_names) > 3
            
            # Evaluar estructura general
            structure_score = 0
            structure_feedback = []
            
            if has_exposition:
                structure_score += 1
                structure_feedback.append("✓ Exposicion presente")
            else:
                structure_feedback.append("⚠ Exposicion no clara")
            
            if conflict_count > 0:
                structure_score += 1
                structure_feedback.append("✓ Elementos de conflicto detectados")
            else:
                structure_feedback.append("⚠ Falta desarrollo del conflicto")
            
            if climax_indicators > 0:
                structure_score += 1
                structure_feedback.append("✓ Momentos de intensidad presentes")
            else:
                structure_feedback.append("⚠ Climax no evidente")
                
            if has_resolution:
                structure_score += 1
                structure_feedback.append("✓ Resolucion identificada")
            else:
                structure_feedback.append("⚠ Resolucion incompleta")
            
            analysis = f"""ANALISIS DE TRAMA:
            
📖 ESTRUCTURA NARRATIVA:
- Puntuacion estructural: {structure_score}/4
{chr(10).join([f"- {feedback}" for feedback in structure_feedback])}

🔥 ELEMENTOS DE TENSION:
- Marcadores de conflicto: {conflict_count}
- Indicadores de climax: {climax_indicators}
- Progresion temporal: {time_progression} transiciones

👥 COMPLEJIDAD NARRATIVA:
- Personajes principales: {len(character_names)}
- Potencial de subtramas: {'Alto' if subplot_potential else 'Bajo'}

⏳ FLUJO TEMPORAL:
- Transiciones temporales: {time_progression}
- Progresion: {'Fluida' if time_progression > 3 else 'Estatica'}

🎭 EVALUACION GENERAL:
- Estructura: {'Solida' if structure_score >= 3 else 'En desarrollo' if structure_score >= 2 else 'Necesita trabajo'}
- Complejidad: {'Alta' if len(character_names) > 5 else 'Media' if len(character_names) > 2 else 'Simple'}
- Tension narrativa: {'Adecuada' if conflict_count > 2 else 'Insuficiente'}

💡 SUGERENCIAS:
- {'Desarrollar mas el conflicto central' if conflict_count < 2 else ''}
- {'Clarificar el momento climatico' if climax_indicators == 0 else ''}
- {'Fortalecer la resolucion' if not has_resolution else ''}
- {'Considerar subtramas para enriquecer la narrativa' if not subplot_potential else ''}
"""
            return analysis
            
        except Exception as e:
            return f"Error analizando trama: {str(e)}"