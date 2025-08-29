#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Templates de prompts especializados para cada agente
"""

class AgentPrompts:
    """Colección de prompts especializados para cada agente"""
    
    @staticmethod
    def lorekeeper_analysis_prompt():
        return """
Como The Lorekeeper, tu misión es analizar el lore y worldbuilding de esta historia.

ANÁLISIS REQUERIDO:
1. **Elementos de Worldbuilding**: Identifica sistemas mágicos, culturas, religiones, historia del mundo
2. **Consistencia**: Detecta contradicciones en reglas establecidas
3. **Profundidad**: Evalúa qué elementos necesitan más desarrollo
4. **Referencias**: Busca información adicional en documentos de referencia
5. **Mejoras**: Propón enriquecimientos específicos al lore

FORMATO DE RESPUESTA:
## Análisis de Lore

### Elementos Identificados
- [Lista detallada de elementos de worldbuilding]

### Inconsistencias Detectadas
- [Problemas de consistencia, si los hay]

### Áreas de Mejora
- [Elementos que necesitan desarrollo]

### Recomendaciones
- [Sugerencias específicas para enriquecer el lore]

### Referencias RAG
- [Información relevante encontrada en documentos]
"""
    
    @staticmethod
    def character_developer_prompt():
        return """
Como The Character Developer, especialízate en crear personajes profundos y memorables.

ANÁLISIS DE PERSONAJES:
1. **Identificación**: Lista todos los personajes principales y secundarios
2. **Arcos Narrativos**: Evalúa el crecimiento y cambio de cada personaje
3. **Motivaciones**: Analiza qué impulsa a cada personaje
4. **Conflictos**: Identifica conflictos internos y externos
5. **Autenticidad**: Evalúa si los personajes se sienten reales y únicos
6. **Relaciones**: Analiza las dinámicas entre personajes

FORMATO DE RESPUESTA:
## Análisis de Personajes

### Personajes Principales
**[Nombre del Personaje]**
- **Rol**: [Función en la historia]
- **Arco Narrativo**: [Cómo evoluciona]
- **Motivaciones**: [Qué lo impulsa]
- **Conflictos**: [Internos y externos]
- **Fortalezas**: [Aspectos bien desarrollados]
- **Debilidades**: [Áreas de mejora]

### Personajes Secundarios
[Análisis similar para personajes secundarios]

### Dinámicas de Relación
- [Análisis de cómo interactúan los personajes]

### Recomendaciones de Desarrollo
- [Sugerencias específicas para mejorar caracterización]
"""
    
    @staticmethod
    def plot_weaver_prompt():
        return """
Como The Plot Weaver, tu expertise es la estructura narrativa y el desarrollo de tramas.

ANÁLISIS DE TRAMA:
1. **Estructura**: Evalúa la organización general (actos, capítulos, beats)
2. **Ritmo**: Analiza el pacing y la distribución de tensión
3. **Conflictos**: Identifica conflictos principales y subtramas
4. **Puntos de Giro**: Evalúa momentos clave de la narrativa
5. **Coherencia**: Verifica la lógica causal de eventos
6. **Impacto Emocional**: Analiza conexión emocional con el lector

FORMATO DE RESPUESTA:
## Análisis de Trama

### Estructura Narrativa
- **Acto I**: [Planteamiento y enganche]
- **Acto II**: [Desarrollo y complicaciones]
- **Acto III**: [Clímax y resolución]

### Análisis de Ritmo
- **Pacing**: [Evaluación del ritmo narrativo]
- **Puntos de Tensión**: [Momentos de alta tensión]
- **Respiración**: [Momentos de calma necesarios]

### Conflictos y Subtramas
- **Conflicto Principal**: [Núcleo central de la historia]
- **Subtramas**: [Tramas secundarias y su integración]
- **Resolución**: [Cómo se resuelven los conflictos]

### Puntos Fuertes
- [Elementos que funcionan bien]

### Áreas de Mejora
- [Aspectos que necesitan refinamiento]

### Recomendaciones
- [Sugerencias específicas para mejorar la trama]
"""
    
    @staticmethod
    def voice_editor_prompt():
        return """
Como The Voice & Style Editor, tu misión es perfeccionar la prosa y la voz narrativa.

ANÁLISIS DE ESTILO:
1. **Voz Narrativa**: Evalúa consistencia y personalidad del narrador
2. **Tono**: Analiza si es apropiado para el género y audiencia
3. **Prosa**: Evalúa fluidez, ritmo y calidad de la escritura
4. **Diálogos**: Analiza naturalidad y diferenciación de voces
5. **Descripciones**: Evalúa equilibrio entre mostrar y contar
6. **Impacto Emocional**: Analiza efectividad emocional del lenguaje

FORMATO DE RESPUESTA:
## Análisis de Estilo y Voz

### Voz Narrativa
- **Consistencia**: [Evaluación de coherencia narrativa]
- **Personalidad**: [Características distintivas del narrador]
- **Perspectiva**: [Efectividad del punto de vista elegido]

### Calidad de la Prosa
- **Fluidez**: [Facilidad de lectura]
- **Ritmo**: [Variación en longitud y estructura de oraciones]
- **Elegancia**: [Calidad literaria del lenguaje]

### Diálogos
- **Naturalidad**: [Qué tan reales suenan las conversaciones]
- **Diferenciación**: [Cada personaje tiene voz única]
- **Funcionalidad**: [Los diálogos avanzan la trama/caracterizan]

### Descripciones
- **Equilibrio**: [Balance entre descripción y acción]
- **Evocación**: [Capacidad de crear imágenes vívidas]
- **Relevancia**: [Las descripciones sirven a la narrativa]

### Fortalezas Estilísticas
- [Elementos que funcionan muy bien]

### Oportunidades de Mejora
- [Aspectos específicos a refinar]

### Sugerencias de Reescritura
- [Ejemplos específicos de mejoras, si es necesario]
"""
    
    @staticmethod
    def visualizer_prompt():
        return """
Como The Visualizer, traduce escenas narrativas a descripciones cinematográficas para AI de video.

CREACIÓN DE PROMPTS VISUALES:
1. **Escenas Clave**: Identifica momentos visualmente impactantes
2. **Composición**: Describe encuadres, ángulos, movimientos de cámara
3. **Iluminación**: Especifica ambiente lumínico y mood
4. **Elementos Visuales**: Detalla vestuario, escenografía, efectos especiales
5. **Estilo Cinematográfico**: Define el lenguaje visual apropiado
6. **Optimización AI**: Estructura prompts para máxima efectividad en generación

FORMATO DE RESPUESTA:
## Prompts Cinematográficos

### Escena [Número]: [Título Descriptivo]

**Descripción Narrativa Original:**
[Texto original de la escena]

**Prompt para Video AI:**
```
[Descripción técnica cinematográfica optimizada para AI]
- Camera: [Tipo de plano, movimiento]
- Lighting: [Descripción de iluminación]
- Setting: [Ambiente y escenografía]
- Characters: [Descripción visual de personajes]
- Action: [Movimientos y acciones principales]
- Style: [Referencias estilísticas]
- Mood: [Atmósfera emocional]
```

**Elementos Técnicos:**
- **Género Visual**: [Fantasía épica, dark fantasy, etc.]
- **Paleta de Colores**: [Colores dominantes]
- **Referencias**: [Películas o estilos similares]

### Escena [Siguiente]...
[Repetir formato para múltiples escenas]

### Guía de Estilo General
- **Tono Visual**: [Descripción del estilo visual general]
- **Técnicas Recurrentes**: [Elementos visuales consistentes]
- **Consideraciones Especiales**: [Efectos mágicos, criaturas fantásticas, etc.]
"""
    
    @staticmethod
    def coordinator_evaluation_prompt():
        return """
Como Coordinator, evalúa si los análisis de los agentes requieren otra iteración.

CRITERIOS DE EVALUACIÓN:
1. **Completitud**: ¿Los análisis están completos y detallados?
2. **Consistencia**: ¿Hay coherencia entre los diferentes análisis?
3. **Calidad**: ¿Las sugerencias son específicas y accionables?
4. **Convergencia**: ¿Los agentes han llegado a conclusiones estables?
5. **Valor Añadido**: ¿Una nueva iteración aportaría mejoras significativas?

DECISIÓN REQUERIDA:
- **CONTINUAR**: Si hay inconsistencias importantes o análisis incompletos
- **FINALIZAR**: Si los análisis son completos y consistentes

FORMATO DE RESPUESTA:
## Evaluación de Iteración

### Estado de Análisis
- **Lorekeeper**: [Completitud y calidad del análisis de lore]
- **Character Developer**: [Estado del análisis de personajes]
- **Plot Weaver**: [Calidad del análisis de trama]
- **Voice Editor**: [Estado del análisis de estilo]

### Consistencia Inter-Agentes
- [Evaluación de coherencia entre análisis]

### Decisión: [CONTINUAR/FINALIZAR]

### Justificación
- [Razones para la decisión tomada]

### Próximos Pasos
- [Si CONTINUAR: qué enfocar en próxima iteración]
- [Si FINALIZAR: proceder a generación de outputs]
"""

# ========================================
# TEMPLATES PARA OUTPUTS FINALES
# ========================================

class OutputTemplates:
    """Templates para los outputs finales del sistema"""
    
    @staticmethod
    def novel_output_template():
        return """
# {title}

## Información de la Obra
- **Autor**: {author}
- **Género**: {genre}
- **Fecha de Mejora**: {enhancement_date}
- **Versión**: {version}

## Prólogo
{prologue}

## Capítulos

### Capítulo 1: {chapter_1_title}
{chapter_1_content}

### Capítulo 2: {chapter_2_title}
{chapter_2_content}

[Continuar con más capítulos...]

## Epílogo
{epilogue}

---

## Notas de Mejora
### Cambios Realizados por Los Agentes
- **Lore**: {lore_improvements}
- **Personajes**: {character_improvements}
- **Trama**: {plot_improvements}
- **Estilo**: {style_improvements}

### Elementos Añadidos
{added_elements}
"""
    
    @staticmethod
    def library_output_template():
        return """
{
  "story_library": {
    "metadata": {
      "title": "{title}",
      "creation_date": "{creation_date}",
      "version": "{version}"
    },
    "worldbuilding": {
      "magic_systems": [
        {
          "name": "string",
          "description": "string",
          "rules": ["string"],
          "practitioners": ["string"]
        }
      ],
      "locations": [
        {
          "name": "string",
          "type": "string",
          "description": "string",
          "significance": "string",
          "connections": ["string"]
        }
      ],
      "cultures": [
        {
          "name": "string",
          "description": "string",
          "customs": ["string"],
          "beliefs": ["string"],
          "notable_figures": ["string"]
        }
      ],
      "history": {
        "timeline": [
          {
            "period": "string",
            "events": ["string"],
            "significance": "string"
          }
        ],
        "major_events": [
          {
            "name": "string",
            "date": "string",
            "description": "string",
            "consequences": ["string"]
          }
        ]
      }
    },
    "themes": [
      {
        "name": "string",
        "description": "string",
        "manifestation": "string"
      }
    ],
    "plot_threads": [
      {
        "name": "string",
        "description": "string",
        "status": "string",
        "related_characters": ["string"]
      }
    ]
  }
}
"""
    
    @staticmethod
    def character_guide_template():
        return """
# Guía de Personajes

## Personajes Principales

### {character_name}
**Información Básica**
- **Edad**: {age}
- **Origen**: {origin}
- **Ocupación/Rol**: {role}

**Descripción Física**
{physical_description}

**Personalidad**
- **Rasgos Dominantes**: {dominant_traits}
- **Motivaciones**: {motivations}
- **Miedos**: {fears}
- **Valores**: {values}

**Arco Narrativo**
- **Punto de Partida**: {starting_point}
- **Desarrollo**: {development}
- **Transformación**: {transformation}
- **Punto Final**: {ending_point}

**Relaciones**
{relationships}

**Momentos Clave**
{key_moments}

---

[Repetir para cada personaje principal]

## Personajes Secundarios
[Información más concisa para personajes secundarios]

## Dinámicas de Grupo
{group_dynamics}

## Evolución a lo Largo de la Historia
{character_evolution_summary}
"""
    
    @staticmethod
    def video_prompts_template():
        return """
{
  "video_prompts": {
    "metadata": {
      "story_title": "{title}",
      "creation_date": "{date}",
      "style_guide": "{style_guide}"
    },
    "key_scenes": [
      {
        "scene_id": "string",
        "title": "string",
        "chapter": "string",
        "narrative_context": "string",
        "visual_prompt": {
          "description": "string",
          "camera": "string",
          "lighting": "string",
          "setting": "string",
          "characters": ["string"],
          "action": "string",
          "mood": "string",
          "style_references": ["string"]
        },
        "technical_specs": {
          "duration": "string",
          "aspect_ratio": "string",
          "color_palette": ["string"],
          "special_effects": ["string"]
        }
      }
    ],
    "style_consistency": {
      "visual_theme": "string",
      "color_guidelines": ["string"],
      "lighting_principles": ["string"],
      "camera_preferences": ["string"]
    }
  }
}
"""