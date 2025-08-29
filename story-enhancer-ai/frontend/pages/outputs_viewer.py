"""
Página de visualización y descarga de outputs finales
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from frontend.utils.session_state import add_log_entry

def render_outputs_viewer():
    """Renderiza la página de visualización de outputs"""
    
    st.title("📊 Resultados y Outputs")
    st.markdown("Visualiza y descarga los outputs finales generados por el proceso de agentes.")
    
    # Verificar si hay outputs disponibles
    if not any(st.session_state.final_outputs.values()):
        render_no_outputs_state()
        return
    
    # Tabs para cada tipo de output
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Historia Final", 
        "📚 Biblia de la Historia", 
        "👥 Guía de Personajes", 
        "🎬 Prompts Visuales",
        "📦 Descargar Todo"
    ])
    
    with tab1:
        render_enhanced_story()
        
    with tab2:
        render_story_bible()
        
    with tab3:
        render_character_guide()
        
    with tab4:
        render_visual_prompts()
        
    with tab5:
        render_download_all()

def render_no_outputs_state():
    """Estado cuando no hay outputs disponibles"""
    
    st.info("📝 No hay outputs generados aún.")
    st.markdown("Los outputs aparecerán aquí una vez que el proceso de agentes se complete.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Para generar outputs necesitas:")
        st.write("• Documentos de referencia procesados")
        st.write("• Manuscrito base cargado")
        st.write("• Proceso de agentes completado")
    
    with col2:
        st.markdown("### 🎯 Los outputs incluirán:")
        st.write("• Historia mejorada")
        st.write("• Biblia del mundo narrativo")
        st.write("• Guía detallada de personajes")
        st.write("• Prompts para video AI")
    
    # Botón para generar outputs de ejemplo (para testing)
    if st.button("🧪 Generar Outputs de Ejemplo (Solo para pruebas)"):
        generate_mock_outputs()
        st.success("✅ Outputs de ejemplo generados!")
        st.experimental_rerun()

def generate_mock_outputs():
    """Genera outputs de ejemplo para testing"""
    
    # Historia mejorada de ejemplo
    enhanced_story = """# La Espada Perdida - Versión Mejorada

## Prólogo: El Eco del Pasado

En las brumas del tiempo, cuando el mundo era joven y la magia fluía como ríos de luz entre las montañas, una espada fue forjada con el corazón de una estrella caída. Su nombre era Luminar, y su destino estaba entrelazado con el equilibrio entre la luz y las sombras.

Mil años han pasado desde que la espada desapareció, oculta en los pliegues de la realidad por aquellos que comprendían el precio del poder absoluto.

Pero las profecías nunca mienten. Y cuando la oscuridad amenaza con devorar el mundo, Luminar despierta... y llama a su elegida.

## Capítulo 1: El Peso de los Sueños

Aria Valorheart despertó con lágrimas en los ojos, el eco de una voz ancestral aún resonando en su mente. La posada "El Dragón Dormido" permanecía en silencio, salvo por el crepitar de las brasas moribundas en la chimenea principal.

Dieciocho años había vivido en este lugar, huérfana desde los cinco, cuando una plaga devastó su aldea natal. Dieciocho años limpiando, sirviendo, sonriendo a extraños que nunca recordarían su nombre. Pero los sueños... los sueños la conocían íntimamente.

*"Aria... hija de dos mundos... la espada aguarda..."*

Se incorporó en su estrecho catre, observando por la ventana las montañas que se alzaban como titanes pétreos contra el cielo estrellado. En algún lugar, entre esos picos cubiertos de misterio, Luminar la esperaba. Lo sabía con la certeza que solo otorgan las verdades que trascienden la razón.

Sus manos, callosas por el trabajo pero extrañamente elegantes, se cerraron en puños. ¿Cómo podía una simple sirvienta ser la elegida de una espada legendaria? ¿Qué había en ella que no podía ver?

La respuesta vendría con el amanecer, cuando el destino tomó la forma de un anciano de ojos como estrellas apagadas.

## Capítulo 2: El Heraldo del Destino

[Continuación mejorada con mayor profundidad emocional, worldbuilding expandido y desarrollo de personajes más rico...]

---

*Esta versión ha sido mejorada por los agentes especializados, incorporando:*
- *Mayor profundidad emocional en los personajes*
- *Worldbuilding más detallado y consistente*
- *Estructura narrativa optimizada*
- *Voz narrativa más distintiva y poética*
"""
    
    # Biblia de la historia
    story_bible = {
        "world_name": "Valderon",
        "magic_system": {
            "type": "Crystal-based Channeling",
            "description": "La magia fluye a través de cristales naturales que amplifican la energía espiritual",
            "limitations": "Los cristales se agotan con el uso excesivo y deben recargarse bajo la luz lunar",
            "schools": ["Elementalismo", "Sanación", "Ilusión", "Transmutación"]
        },
        "geography": {
            "regions": [
                {
                    "name": "Las Tierras Centrales",
                    "description": "Llanuras fértiles donde prosperan las ciudades comerciales",
                    "climate": "Templado, con estaciones marcadas"
                },
                {
                    "name": "Los Picos Etéreos", 
                    "description": "Montañas sagradas donde la magia es más fuerte",
                    "climate": "Frío perpetuo, nevadas constantes"
                },
                {
                    "name": "El Bosque de Susurros",
                    "description": "Bosque ancestral donde habitan espíritus antiguos",
                    "climate": "Húmedo, brumoso, temperaturas variables"
                }
            ]
        },
        "timeline": [
            {
                "year": "Año 0 - Era Dorada",
                "event": "Forjado de la Espada Luminar"
            },
            {
                "year": "Año 500 - La Primera Oscuridad", 
                "event": "Primer alzamiento del Señor de las Sombras, derrotado por el héroe Valderon"
            },
            {
                "year": "Año 1000 - El Gran Ocultamiento",
                "event": "Luminar es ocultada para prevenir su mal uso"
            },
            {
                "year": "Año 1500 - Presente",
                "event": "Despertar de Aria y retorno del Señor de las Sombras"
            }
        ]
    }
    
    # Guía de personajes
    character_guide = {
        "main_characters": [
            {
                "name": "Aria Valorheart",
                "age": 18,
                "role": "Protagonista - La Elegida",
                "background": "Huérfana criada en una posada, desconoce su linaje real",
                "personality": "Determinada pero insegura, compasiva, intuitiva",
                "arc": "De sirvienta insegura a heroína confiada que abraza su destino",
                "abilities": "Afinidad natural con cristales mágicos, liderazgo innato",
                "relationships": {
                    "Kael": "Compañero de aventuras, eventual interés romántico",
                    "Theron": "Mentor y guía espiritual",
                    "Señor de las Sombras": "Némesis, representa sus miedos internos"
                }
            },
            {
                "name": "Kael Montañés",
                "age": 22,
                "role": "Deuteragonista - El Guardián",
                "background": "Guerrero de las montañas, hermana desaparecida",
                "personality": "Protector, leal, haunted por el pasado",
                "arc": "De vengador solitario a verdadero compañero",
                "abilities": "Maestría en combate, resistencia sobrenatural",
                "relationships": {
                    "Aria": "Protege y eventualmente ama",
                    "Lysa": "Hermana perdida que debe rescatar"
                }
            }
        ]
    }
    
    # Prompts visuales
    visual_prompts = [
        {
            "scene": "Aria's Awakening",
            "prompt": "A young woman with auburn hair sits up in a narrow bed within a rustic inn, ethereal silver light filtering through a small window, her eyes wide with otherworldly vision, cinematic lighting, fantasy realism, misty atmosphere",
            "style": "Epic fantasy, reminiscent of Lord of the Rings cinematography",
            "mood": "Mystical, contemplative, destiny calling"
        },
        {
            "scene": "The Sword Revelation", 
            "prompt": "Ancient silver sword embedded in crystalline stone within an enchanted forest clearing, beams of moonlight creating lens flares, magical particles floating in the air, photorealistic, dramatic composition",
            "style": "High fantasy, cinematic quality",
            "mood": "Awe-inspiring, magical, pivotal moment"
        },
        {
            "scene": "Character Introduction - Theron",
            "prompt": "Elderly wizard in gray robes with star-filled eyes, sitting in a dim tavern corner, weathered hands wrapped around a simple cup, mysterious aura, character study, dramatic lighting",
            "style": "Character portrait, atmospheric",
            "mood": "Wise, mysterious, harbinger of change"
        }
    ]
    
    # Guardar en session state
    st.session_state.final_outputs = {
        'enhanced_story': enhanced_story,
        'story_bible': story_bible,
        'character_guide': character_guide,
        'visual_prompts': visual_prompts
    }

def render_enhanced_story():
    """Renderiza la historia mejorada"""
    
    st.subheader("📖 Historia Mejorada")
    
    if not st.session_state.final_outputs['enhanced_story']:
        st.info("La historia mejorada aparecerá aquí una vez completado el proceso.")
        return
    
    # Estadísticas de la historia
    content = st.session_state.final_outputs['enhanced_story']
    word_count = len(content.split())
    char_count = len(content)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Palabras", word_count)
    with col2:
        st.metric("🔤 Caracteres", char_count)
    with col3:
        if st.session_state.manuscript_content:
            original_words = len(st.session_state.manuscript_content.split())
            improvement = ((word_count - original_words) / original_words) * 100
            st.metric("📈 Mejora", f"+{improvement:.0f}%")
    
    st.markdown("---")
    
    # Opciones de visualización
    col1, col2, col3 = st.columns(3)
    with col1:
        view_mode = st.selectbox("Vista", ["Completa", "Por Capítulos", "Comparación"])
    with col2:
        if st.button("📋 Copiar Texto"):
            st.code(content)
    with col3:
        if st.button("💾 Descargar"):
            download_text_file(content, "historia_mejorada.md")
    
    # Mostrar contenido
    if view_mode == "Completa":
        st.markdown(content)
    elif view_mode == "Por Capítulos":
        render_story_by_chapters(content)
    else:
        render_story_comparison()

def render_story_by_chapters(content: str):
    """Renderiza la historia dividida por capítulos"""
    
    # Dividir por capítulos (simplificado)
    chapters = content.split("## ")
    
    for i, chapter in enumerate(chapters):
        if chapter.strip():
            chapter_title = chapter.split('\n')[0]
            chapter_content = '\n'.join(chapter.split('\n')[1:])
            
            with st.expander(f"Capítulo {i}: {chapter_title}", expanded=(i == 0)):
                st.markdown(chapter_content)

def render_story_comparison():
    """Renderiza comparación entre historia original y mejorada"""
    
    if not st.session_state.manuscript_content:
        st.warning("No hay historia original para comparar")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Historia Original")
        st.text_area("Original", st.session_state.manuscript_content, height=400, disabled=True)
    
    with col2:
        st.subheader("✨ Historia Mejorada")
        st.text_area("Mejorada", st.session_state.final_outputs['enhanced_story'], height=400, disabled=True)

def render_story_bible():
    """Renderiza la biblia de la historia"""
    
    st.subheader("📚 Biblia de la Historia")
    
    if not st.session_state.final_outputs['story_bible']:
        st.info("La biblia de la historia aparecerá aquí una vez completado el proceso.")
        return
    
    bible = st.session_state.final_outputs['story_bible']
    
    # Tabs para organizar la biblia
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Mundo", "✨ Magia", "📅 Timeline", "🗺️ Geografía"])
    
    with tab