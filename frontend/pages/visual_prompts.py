# -*- coding: utf-8 -*-
import streamlit as st
import json
import random
from datetime import datetime
from typing import List, Dict

def render_visual_page():
    """Renderiza la pagina de generacion de prompts visuales"""
    
    st.header("🎬 Prompts Visuales para IA de Video")
    st.markdown("*Convierte tu manuscrito en prompts cinematograficos para herramientas de IA como Runway, Pika Labs, etc.*")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Generador",
        "📽️ Galeria de Prompts",
        "⚙️ Configuracion",
        "📚 Biblioteca de Estilos"
    ])
    
    with tab1:
        render_generator_tab()
    
    with tab2:
        render_gallery_tab()
    
    with tab3:
        render_config_tab()
    
    with tab4:
        render_styles_library_tab()

def render_generator_tab():
    """Tab principal de generacion de prompts"""
    st.subheader("🎨 Generador de Prompts Cinematograficos")
    
    # Verificar si hay manuscrito
    if not st.session_state.manuscript:
        st.warning("⚠️ Necesitas tener un manuscrito en el editor para generar prompts visuales.")
        
        if st.button("📝 Ir al Editor de Manuscrito"):
            st.session_state.page_selector = "manuscript"
            st.rerun()
        
        # Opcion de usar manuscrito de ejemplo
        if st.button("🎭 Usar Manuscrito de Ejemplo"):
            st.session_state.manuscript = get_example_manuscript()
            st.success("✅ Manuscrito de ejemplo cargado")
            st.rerun()
        
        return
    
    # Mostrar informacion del manuscrito
    word_count = len(st.session_state.manuscript.split())
    st.info(f"📖 Manuscrito cargado: {word_count} palabras")
    
    # Opciones de generacion
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎬 Configuracion de Video")
        
        video_style = st.selectbox(
            "Estilo cinematografico:",
            [
                "Fantasia Epica",
                "Drama Intimista", 
                "Accion/Aventura",
                "Misterio/Thriller",
                "Romance Cinematografico",
                "Horror Atmosferico",
                "Ciencia Ficcion",
                "Documental Estilizado"
            ]
        )
        
        aspect_ratio = st.selectbox(
            "Relacion de aspecto:",
            ["16:9 (Estandar)", "21:9 (Cinemascope)", "9:16 (Vertical/TikTok)", "1:1 (Cuadrado)"]
        )
        
        duration = st.selectbox(
            "Duracion del clip:",
            ["3 segundos", "5 segundos", "10 segundos", "15 segundos", "30 segundos"]
        )
    
    with col2:
        st.markdown("### 🎨 Configuracion Visual")
        
        camera_style = st.selectbox(
            "Estilo de camara:",
            [
                "Plano fijo profesional",
                "Movimiento de camara fluido",
                "Camara en mano dinamico",
                "Planos aereos/drone",
                "Primeros planos intimos",
                "Planos generales epicos"
            ]
        )
        
        lighting = st.selectbox(
            "Iluminacion:",
            [
                "Luz natural suave",
                "Luz dramatica/contrastada", 
                "Luz dorada/golden hour",
                "Luz azul/hora azul",
                "Luz artificial/neon",
                "Luz mistica/fantastica"
            ]
        )
        
        color_palette = st.selectbox(
            "Paleta de colores:",
            [
                "Colores naturales/realistas",
                "Paleta calida (dorados/rojos)",
                "Paleta fria (azules/verdes)",
                "Alto contraste/dramatico",
                "Desaturado/cinematografico",
                "Colores vibrantes/saturados"
            ]
        )
    
    # Opciones avanzadas
    with st.expander("⚙️ Configuracion Avanzada"):
        col1, col2 = st.columns(2)
        
        with col1:
            include_characters = st.checkbox("Incluir descripciones de personajes", value=True)
            include_dialogue = st.checkbox("Generar prompts para dialogos", value=False)
            include_action = st.checkbox("Enfatizar secuencias de accion", value=True)
        
        with col2:
            quality_level = st.selectbox("Calidad de prompt:", ["Basica", "Detallada", "Profesional"])
            creative_liberty = st.slider("Libertad creativa:", 1, 10, 7, help="1 = Fiel al texto, 10 = Interpretacion libre")
            technical_details = st.checkbox("Incluir detalles tecnicos", value=False, help="ISO, focal length, etc.")
    
    # Boton de generacion
    if st.button("🎬 Generar Prompts Visuales", type="primary", use_container_width=True):
        generate_visual_prompts(
            st.session_state.manuscript,
            video_style,
            aspect_ratio,
            duration,
            camera_style,
            lighting,
            color_palette,
            include_characters,
            include_dialogue,
            include_action,
            quality_level,
            creative_liberty,
            technical_details
        )

def generate_visual_prompts(manuscript, video_style, aspect_ratio, duration, camera_style, 
                          lighting, color_palette, include_characters, include_dialogue, 
                          include_action, quality_level, creative_liberty, technical_details):
    """Genera prompts visuales basados en el manuscrito y configuracion"""
    
    with st.spinner("🎨 Generando prompts visuales..."):
        # Simular procesamiento
        import time
        time.sleep(3)
        
        # Extraer escenas del manuscrito
        scenes = extract_scenes(manuscript)
        
        # Generar prompts para cada escena
        visual_prompts = []
        
        for i, scene in enumerate(scenes, 1):
            prompt = create_visual_prompt(
                scene, i, video_style, aspect_ratio, duration,
                camera_style, lighting, color_palette,
                include_characters, include_dialogue, include_action,
                quality_level, creative_liberty, technical_details
            )
            visual_prompts.append(prompt)
        
        # Guardar en session state
        st.session_state.visual_prompts = visual_prompts
        
        st.success(f"✅ ¡{len(visual_prompts)} prompts visuales generados exitosamente!")
        
        # Mostrar prompts generados
        render_generated_prompts(visual_prompts)

def extract_scenes(manuscript):
    """Extrae escenas principales del manuscrito"""
    
    # Dividir por parrafos y filtrar escenas significativas
    paragraphs = [p.strip() for p in manuscript.split('\n\n') if p.strip()]
    
    scenes = []
    for i, paragraph in enumerate(paragraphs):
        if len(paragraph) > 100:  # Solo parrafos sustanciales
            scenes.append({
                'id': i + 1,
                'text': paragraph,
                'type': detect_scene_type(paragraph),
                'characters': extract_characters(paragraph),
                'location': extract_location(paragraph),
                'mood': detect_mood(paragraph)
            })
    
    return scenes[:8]  # Maximo 8 escenas para no sobrecargar

def detect_scene_type(text):
    """Detecta el tipo de escena basado en el contenido"""
    
    action_keywords = ['corrio', 'salto', 'lucho', 'ataco', 'huyo', 'persiguio']
    dialogue_keywords = ['dijo', 'pregunto', 'grito', 'susurro', 'respondio']
    description_keywords = ['se veia', 'parecia', 'observo', 'contemplo', 'describio']
    
    if any(keyword in text.lower() for keyword in action_keywords):
        return 'accion'
    elif any(keyword in text.lower() for keyword in dialogue_keywords):
        return 'dialogo'
    elif any(keyword in text.lower() for keyword in description_keywords):
        return 'descripcion'
    else:
        return 'narrativa'

def extract_characters(text):
    """Extrae personajes mencionados en el texto"""
    # Buscar nombres propios (palabras capitalizadas)
    import re
    characters = re.findall(r'\b[A-Z][a-z]+\b', text)
    # Filtrar palabras comunes que no son nombres
    common_words = ['En', 'El', 'La', 'Los', 'Las', 'Un', 'Una', 'Torre', 'Reino', 'Guerra']
    characters = [char for char in characters if char not in common_words]
    return list(set(characters))[:3]  # Maximo 3 personajes por escena

def extract_location(text):
    """Extrae la ubicacion de la escena"""
    location_keywords = {
        'reino': 'reino fantastico',
        'torre': 'torre antigua',
        'bosque': 'bosque misterioso',
        'castillo': 'castillo medieval',
        'ciudad': 'ciudad medieval',
        'montaña': 'paisaje montañoso',
        'rio': 'paisaje fluvial',
        'cueva': 'caverna oscura'
    }
    
    for keyword, location in location_keywords.items():
        if keyword in text.lower():
            return location
    
    return 'paisaje fantastico'

def detect_mood(text):
    """Detecta el mood/atmosfera de la escena"""
    mood_keywords = {
        'misterioso': ['misterio', 'secreto', 'oculto', 'desconocido'],
        'dramatico': ['guerra', 'conflicto', 'lucha', 'batalla'],
        'magico': ['magia', 'magico', 'hechizo', 'cristal'],
        'epico': ['reino', 'destino', 'poder', 'epico'],
        'intimo': ['susurro', 'penso', 'sintio', 'recordo'],
        'amenazante': ['sombras', 'peligro', 'amenaza', 'miedo']
    }
    
    for mood, keywords in mood_keywords.items():
        if any(keyword in text.lower() for keyword in keywords):
            return mood
    
    return 'narrativo'

def create_visual_prompt(scene, scene_num, video_style, aspect_ratio, duration,
                        camera_style, lighting, color_palette, include_characters,
                        include_dialogue, include_action, quality_level,
                        creative_liberty, technical_details):
    """Crea un prompt visual para una escena especifica"""
    
    # Prompt base
    prompt_parts = []
    
    # Descripcion de la escena
    scene_description = create_scene_description(scene, video_style, creative_liberty)
    prompt_parts.append(scene_description)
    
    # Personajes si estan habilitados
    if include_characters and scene['characters']:
        char_description = create_character_description(scene['characters'], video_style)
        prompt_parts.append(char_description)
    
    # Configuracion de camara
    camera_description = get_camera_description(camera_style, scene['type'])
    prompt_parts.append(camera_description)
    
    # Iluminacion
    lighting_description = get_lighting_description(lighting, scene['mood'])
    prompt_parts.append(lighting_description)
    
    # Paleta de colores
    color_description = get_color_description(color_palette, scene['mood'])
    prompt_parts.append(color_description)
    
    # Detalles tecnicos si estan habilitados
    if technical_details:
        tech_details = get_technical_details(quality_level)
        prompt_parts.append(tech_details)
    
    # Estilo y calidad
    style_suffix = get_style_suffix(video_style, quality_level)
    prompt_parts.append(style_suffix)
    
    # Construir prompt final
    main_prompt = ", ".join(prompt_parts)
    
    # Crear objeto de prompt completo
    visual_prompt = {
        'id': scene_num,
        'title': f"Escena {scene_num}: {scene['location'].title()}",
        'prompt': main_prompt,
        'scene_type': scene['type'],
        'characters': scene['characters'],
        'location': scene['location'],
        'mood': scene['mood'],
        'technical_settings': {
            'aspect_ratio': aspect_ratio,
            'duration': duration,
            'style': video_style
        },
        'original_text': scene['text'][:200] + "..." if len(scene['text']) > 200 else scene['text'],
        'timestamp': datetime.now().isoformat()
    }
    
    return visual_prompt

def create_scene_description(scene, video_style, creative_liberty):
    """Crea descripcion visual de la escena"""
    
    base_description = scene['text'][:100] + "..."
    
    # Adaptar segun estilo
    style_adaptations = {
        'Fantasia Epica': f"Epic fantasy scene: {scene['location']} with magical atmosphere",
        'Drama Intimista': f"Intimate dramatic moment in {scene['location']}",
        'Accion/Aventura': f"Dynamic action sequence in {scene['location']}",
        'Misterio/Thriller': f"Mysterious scene unfolding in {scene['location']}",
        'Romance Cinematografico': f"Romantic cinematic moment in {scene['location']}",
        'Horror Atmosferico': f"Dark atmospheric horror scene in {scene['location']}",
        'Ciencia Ficcion': f"Futuristic sci-fi scene in {scene['location']}",
        'Documental Estilizado': f"Stylized documentary approach to {scene['location']}"
    }
    
    return style_adaptations.get(video_style, f"Cinematic scene in {scene['location']}")

def create_character_description(characters, video_style):
    """Crea descripcion de personajes"""
    
    if not characters:
        return ""
    
    char_descriptions = {
        'Lyra': 'young female mage with flowing robes and mystical aura',
        'Stormwind': 'powerful figure with commanding presence',
        'Default': 'fantasy character with period-appropriate clothing'
    }
    
    descriptions = []
    for char in characters:
        desc = char_descriptions.get(char, char_descriptions['Default'])
        descriptions.append(f"{char}: {desc}")
    
    return f"Characters: {', '.join(descriptions)}"

def get_camera_description(camera_style, scene_type):
    """Genera descripcion de camara"""
    
    camera_map = {
        'Plano fijo profesional': 'static professional shot, tripod mounted',
        'Movimiento de camara fluido': 'smooth camera movement, cinematic flow',
        'Camara en mano dinamico': 'handheld dynamic camera work',
        'Planos aereos/drone': 'aerial drone shot, sweeping overhead view',
        'Primeros planos intimos': 'intimate close-up shots',
        'Planos generales epicos': 'epic wide establishing shots'
    }
    
    return camera_map.get(camera_style, 'cinematic camera work')

def get_lighting_description(lighting, mood):
    """Genera descripcion de iluminacion"""
    
    lighting_map = {
        'Luz natural suave': 'soft natural lighting, gentle shadows',
        'Luz dramatica/contrastada': 'dramatic high contrast lighting',
        'Luz dorada/golden hour': 'golden hour lighting, warm sunlight',
        'Luz azul/hora azul': 'blue hour lighting, cool tones',
        'Luz artificial/neon': 'artificial neon lighting effects',
        'Luz mistica/fantastica': 'mystical magical lighting, ethereal glow'
    }
    
    return lighting_map.get(lighting, 'cinematic lighting')

def get_color_description(color_palette, mood):
    """Genera descripcion de paleta de colores"""
    
    color_map = {
        'Colores naturales/realistas': 'natural realistic color palette',
        'Paleta calida (dorados/rojos)': 'warm color palette, golds and reds',
        'Paleta fria (azules/verdes)': 'cool color palette, blues and greens',
        'Alto contraste/dramatico': 'high contrast dramatic colors',
        'Desaturado/cinematografico': 'desaturated cinematic color grading',
        'Colores vibrantes/saturados': 'vibrant saturated colors'
    }
    
    return color_map.get(color_palette, 'cinematic color grading')

def get_technical_details(quality_level):
    """Genera detalles tecnicos"""
    
    if quality_level == "Profesional":
        return "shot on RED camera, 4K resolution, 24fps, shallow depth of field"
    elif quality_level == "Detallada":
        return "high quality cinematography, professional camera work"
    else:
        return "good video quality"

def get_style_suffix(video_style, quality_level):
    """Genera sufijo de estilo"""
    
    quality_suffixes = {
        'Basica': 'good quality',
        'Detallada': 'high quality, professional cinematography',
        'Profesional': 'masterpiece cinematography, award-winning visual effects, 8K resolution'
    }
    
    return quality_suffixes.get(quality_level, 'cinematic quality')

def render_generated_prompts(visual_prompts):
    """Renderiza los prompts visuales generados"""
    
    st.markdown("---")
    st.subheader("🎬 Prompts Generados")
    
    for prompt in visual_prompts:
        with st.expander(f"🎭 {prompt['title']} - {prompt['mood'].title()}"):
            
            # Informacion de la escena
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**📝 Texto Original:**")
                st.markdown(f"_{prompt['original_text']}_")
            
            with col2:
                st.markdown("**ℹ️ Informacion:**")
                st.markdown(f"- **Tipo:** {prompt['scene_type']}")
                st.markdown(f"- **Ubicacion:** {prompt['location']}")
                st.markdown(f"- **Mood:** {prompt['mood']}")
                if prompt['characters']:
                    st.markdown(f"- **Personajes:** {', '.join(prompt['characters'])}")
            
            # Prompt principal
            st.markdown("**🎬 Prompt Visual:**")
            st.code(prompt['prompt'], language="text")
            
            # Configuracion tecnica
            with st.expander("⚙️ Configuracion Tecnica"):
                st.markdown(f"- **Relacion de aspecto:** {prompt['technical_settings']['aspect_ratio']}")
                st.markdown(f"- **Duracion:** {prompt['technical_settings']['duration']}")
                st.markdown(f"- **Estilo:** {prompt['technical_settings']['style']}")
            
            # Botones de accion
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button(f"📋 Copiar", key=f"copy_{prompt['id']}"):
                    # Simular copia al clipboard
                    st.success("📋 Prompt copiado!")
            
            with col2:
                if st.button(f"✏️ Editar", key=f"edit_{prompt['id']}"):
                    st.session_state[f"editing_{prompt['id']}"] = True
                    st.rerun()
            
            with col3:
                if st.button(f"💾 Guardar", key=f"save_{prompt['id']}"):
                    save_prompt_to_gallery(prompt)
                    st.success("💾 Guardado en galeria!")
            
            with col4:
                if st.button(f"🚀 Usar en IA", key=f"ai_{prompt['id']}"):
                    st.info("🚀 Abriendo en herramienta de IA...")
            
            # Editor inline si esta activado
            if st.session_state.get(f"editing_{prompt['id']}", False):
                st.markdown("**✏️ Editar Prompt:**")
                edited_prompt = st.text_area(
                    "Prompt:",
                    value=prompt['prompt'],
                    key=f"edit_text_{prompt['id']}",
                    height=100
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Guardar Cambios", key=f"save_edit_{prompt['id']}"):
                        prompt['prompt'] = edited_prompt
                        st.session_state[f"editing_{prompt['id']}"] = False
                        st.success("✅ Cambios guardados")
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Cancelar", key=f"cancel_edit_{prompt['id']}"):
                        st.session_state[f"editing_{prompt['id']}"] = False
                        st.rerun()

def save_prompt_to_gallery(prompt):
    """Guarda un prompt en la galeria"""
    if 'saved_prompts' not in st.session_state:
        st.session_state.saved_prompts = []
    
    st.session_state.saved_prompts.append(prompt)

def render_gallery_tab():
    """Tab de galeria de prompts guardados"""
    st.subheader("📽️ Galeria de Prompts")
    
    if 'saved_prompts' not in st.session_state or not st.session_state.saved_prompts:
        st.info("📭 No tienes prompts guardados. Genera algunos prompts y guardalos para verlos aqui.")
        return
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mood_filter = st.multiselect(
            "Filtrar por mood:",
            options=list(set(p['mood'] for p in st.session_state.saved_prompts)),
            default=[]
        )
    
    with col2:
        scene_type_filter = st.multiselect(
            "Filtrar por tipo:",
            options=list(set(p['scene_type'] for p in st.session_state.saved_prompts)),
            default=[]
        )
    
    with col3:
        style_filter = st.multiselect(
            "Filtrar por estilo:",
            options=list(set(p['technical_settings']['style'] for p in st.session_state.saved_prompts)),
            default=[]
        )
    
    # Aplicar filtros
    filtered_prompts = st.session_state.saved_prompts
    
    if mood_filter:
        filtered_prompts = [p for p in filtered_prompts if p['mood'] in mood_filter]
    if scene_type_filter:
        filtered_prompts = [p for p in filtered_prompts if p['scene_type'] in scene_type_filter]
    if style_filter:
        filtered_prompts = [p for p in filtered_prompts if p['technical_settings']['style'] in style_filter]
    
    st.markdown(f"**Mostrando {len(filtered_prompts)} de {len(st.session_state.saved_prompts)} prompts**")
    
    # Mostrar prompts en grid
    cols = st.columns(2)
    
    for i, prompt in enumerate(filtered_prompts):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"**🎬 {prompt['title']}**")
                st.markdown(f"*{prompt['mood']} • {prompt['scene_type']}*")
                
                # Mostrar preview del prompt
                st.code(prompt['prompt'][:100] + "...", language="text")
                
                # Botones de accion
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copiar", key=f"gallery_copy_{i}"):
                        st.success("📋 Copiado!")
                with col2:
                    if st.button("🗑️ Eliminar", key=f"gallery_delete_{i}"):
                        st.session_state.saved_prompts.remove(prompt)
                        st.rerun()
            
            st.markdown("---")
    
    # Botones de acciones masivas
    if st.session_state.saved_prompts:
        st.markdown("### 🔧 Acciones Masivas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Exportar Todos"):
                export_prompts_to_file(filtered_prompts)
        
        with col2:
            if st.button("🗑️ Limpiar Galeria"):
                if st.confirm("¿Eliminar todos los prompts guardados?"):
                    st.session_state.saved_prompts = []
                    st.success("🗑️ Galeria limpiada")
                    st.rerun()
        
        with col3:
            if st.button("📊 Generar Reporte"):
                generate_prompts_report(filtered_prompts)

def export_prompts_to_file(prompts):
    """Exporta prompts a archivo JSON"""
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_prompts': len(prompts),
        'prompts': prompts
    }
    
    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Descargar Prompts (JSON)",
        data=json_data,
        file_name=f"visual_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def generate_prompts_report(prompts):
    """Genera reporte de prompts"""
    
    st.markdown("### 📊 Reporte de Prompts")
    
    # Estadisticas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Prompts", len(prompts))
    
    with col2:
        moods = [p['mood'] for p in prompts]
        most_common_mood = max(set(moods), key=moods.count) if moods else "N/A"
        st.metric("Mood Mas Comun", most_common_mood)
    
    with col3:
        avg_length = sum(len(p['prompt']) for p in prompts) / len(prompts) if prompts else 0
        st.metric("Longitud Promedio", f"{avg_length:.0f} chars")
    
    # Distribucion por mood
    if prompts:
        mood_counts = {}
        for prompt in prompts:
            mood = prompt['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        st.markdown("**Distribucion por Mood:**")
        for mood, count in mood_counts.items():
            st.markdown(f"- {mood}: {count} prompts")

def render_config_tab():
    """Tab de configuracion de generacion visual"""
    st.subheader("⚙️ Configuracion de Generacion Visual")
    
    st.markdown("### 🎨 Presets de Estilo")
    
    # Presets predefinidos
    style_presets = {
        "Netflix Original": {
            "video_style": "Drama Intimista",
            "lighting": "Luz dramatica/contrastada",
            "color_palette": "Desaturado/cinematografico",
            "camera_style": "Movimiento de camara fluido",
            "quality": "Profesional"
        },
        "Marvel/Disney+": {
            "video_style": "Accion/Aventura", 
            "lighting": "Luz dramatica/contrastada",
            "color_palette": "Colores vibrantes/saturados",
            "camera_style": "Movimiento de camara fluido",
            "quality": "Profesional"
        },
        "A24 Arthouse": {
            "video_style": "Drama Intimista",
            "lighting": "Luz natural suave", 
            "color_palette": "Colores naturales/realistas",
            "camera_style": "Plano fijo profesional",
            "quality": "Profesional"
        },
        "YouTube/TikTok": {
            "video_style": "Accion/Aventura",
            "lighting": "Luz natural suave",
            "color_palette": "Colores vibrantes/saturados", 
            "camera_style": "Camara en mano dinamico",
            "quality": "Detallada"
        }
    }
    
    selected_preset = st.selectbox("Selecciona un preset:", list(style_presets.keys()))
    
    if st.button("📥 Aplicar Preset"):
        preset = style_presets[selected_preset]
        st.session_state.preset_config = preset
        st.success(f"✅ Preset '{selected_preset}' aplicado")
    
    # Mostrar configuracion del preset seleccionado
    if selected_preset:
        preset = style_presets[selected_preset]
        st.markdown(f"**Configuracion de '{selected_preset}':**")
        for key, value in preset.items():
            st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
    
    st.markdown("---")
    
    # Configuracion de herramientas de IA
    st.markdown("### 🤖 Integracion con Herramientas de IA")
    
    ai_tools = {
        "Runway ML": {
            "url": "https://runwayml.com",
            "specialty": "Video generativo de alta calidad",
            "formats": ["MP4", "MOV"],
            "max_duration": "30 segundos"
        },
        "Pika Labs": {
            "url": "https://pika.art",
            "specialty": "Video a partir de texto e imagen",
            "formats": ["MP4"],
            "max_duration": "15 segundos"
        },
        "Stable Video Diffusion": {
            "url": "https://stability.ai",
            "specialty": "Video open-source",
            "formats": ["MP4", "GIF"],
            "max_duration": "10 segundos"
        },
        "Leonardo AI": {
            "url": "https://leonardo.ai",
            "specialty": "Imagenes y video conceptual",
            "formats": ["MP4", "PNG"],
            "max_duration": "5 segundos"
        }
    }
    
    preferred_ai_tool = st.selectbox(
        "Herramienta de IA preferida:",
        list(ai_tools.keys())
    )
    
    if preferred_ai_tool:
        tool_info = ai_tools[preferred_ai_tool]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🎯 Especialidad:** {tool_info['specialty']}")
            st.markdown(f"**📁 Formatos:** {', '.join(tool_info['formats'])}")
        
        with col2:
            st.markdown(f"**⏱️ Duracion maxima:** {tool_info['max_duration']}")
            st.markdown(f"**🔗 URL:** [Visitar]({tool_info['url']})")
        
        # Optimizacion especifica para la herramienta
        st.markdown("**⚙️ Optimizaciones especificas:**")
        
        if preferred_ai_tool == "Runway ML":
            st.markdown("- Prompts detallados funcionan mejor")
            st.markdown("- Incluir detalles de camara y movimiento")
            st.markdown("- Especificar duracion exacta")
        
        elif preferred_ai_tool == "Pika Labs":
            st.markdown("- Prompts concisos son mas efectivos")
            st.markdown("- Enfocarse en elementos visuales clave")
            st.markdown("- Evitar demasiados detalles tecnicos")
        
        elif preferred_ai_tool == "Stable Video Diffusion":
            st.markdown("- Prompts tecnicos detallados")
            st.markdown("- Incluir parametros de renderizado")
            st.markdown("- Especificar modelo de diffusion")
        
        elif preferred_ai_tool == "Leonardo AI":
            st.markdown("- Enfoque en composicion visual")
            st.markdown("- Describir estilo artistico claramente")
            st.markdown("- Incluir referencias de mood/atmosfera")
    
    st.markdown("---")
    
    # Plantillas personalizadas
    st.markdown("### 📝 Plantillas de Prompt Personalizadas")
    
    if 'custom_templates' not in st.session_state:
        st.session_state.custom_templates = []
    
    # Crear nueva plantilla
    with st.expander("➕ Crear Nueva Plantilla"):
        template_name = st.text_input("Nombre de la plantilla:")
        template_structure = st.text_area(
            "Estructura de la plantilla (usa {variables}):",
            value="{scene_description}, {camera_work}, {lighting}, {mood}, {style_suffix}",
            help="Usa variables como {scene_description}, {characters}, {lighting}, etc."
        )
        
        if st.button("💾 Guardar Plantilla") and template_name:
            new_template = {
                'name': template_name,
                'structure': template_structure,
                'created_date': datetime.now().isoformat()
            }
            st.session_state.custom_templates.append(new_template)
            st.success(f"✅ Plantilla '{template_name}' guardada")
    
    # Mostrar plantillas existentes
    if st.session_state.custom_templates:
        st.markdown("**📋 Plantillas Guardadas:**")
        
        for i, template in enumerate(st.session_state.custom_templates):
            with st.expander(f"📝 {template['name']}"):
                st.code(template['structure'], language="text")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📋 Usar Plantilla", key=f"use_template_{i}"):
                        st.session_state.active_template = template
                        st.success(f"✅ Plantilla '{template['name']}' activada")
                
                with col2:
                    if st.button(f"🗑️ Eliminar", key=f"delete_template_{i}"):
                        st.session_state.custom_templates.pop(i)
                        st.rerun()

def render_styles_library_tab():
    """Tab de biblioteca de estilos cinematograficos"""
    st.subheader("📚 Biblioteca de Estilos Cinematograficos")
    
    # Categorias de estilos
    style_categories = {
        "🎬 Directores Iconicos": {
            "Christopher Nolan": "Dark, complex narratives, practical effects, non-linear storytelling",
            "Wes Anderson": "Symmetrical compositions, pastel colors, whimsical characters", 
            "Denis Villeneuve": "Epic scale, atmospheric lighting, sci-fi aesthetics",
            "Ridley Scott": "Dark, gritty atmosphere, strong visual contrasts",
            "Hayao Miyazaki": "Magical realism, nature themes, hand-drawn animation style",
            "Quentin Tarantino": "Bold colors, dynamic camera work, pop culture references"
        },
        
        "🎨 Movimientos Artisticos": {
            "Film Noir": "High contrast lighting, shadows, urban nighttime scenes",
            "French New Wave": "Handheld camera, natural lighting, documentary style",
            "German Expressionism": "Distorted perspectives, dramatic shadows, psychological themes",
            "Italian Neorealism": "Natural locations, non-professional actors, social themes",
            "Soviet Montage": "Rapid editing, symbolic imagery, political themes"
        },
        
        "🌟 Generos Populares": {
            "Marvel Cinematic": "High contrast, saturated colors, dynamic action",
            "A24 Arthouse": "Natural lighting, muted colors, intimate framing", 
            "Studio Ghibli": "Warm colors, magical elements, nature integration",
            "Netflix Original": "Desaturated palette, cinematic aspect ratio, premium look",
            "YouTube/Creator": "Bright lighting, saturated colors, engaging compositions"
        },
        
        "🎭 Estilos Tematicos": {
            "Cyberpunk": "Neon colors, urban decay, futuristic technology",
            "Steampunk": "Brass tones, Victorian aesthetics, mechanical elements",
            "Post-Apocalyptic": "Desaturated colors, dust and decay, harsh lighting",
            "Fantasy Epic": "Rich colors, magical lighting, grand landscapes",
            "Horror Atmospheric": "Dark shadows, cool tones, unsettling angles",
            "Romantic Comedy": "Warm lighting, soft colors, intimate close-ups"
        }
    }
    
    # Selector de categoria
    selected_category = st.selectbox(
        "Selecciona una categoria:",
        list(style_categories.keys())
    )
    
    if selected_category:
        styles = style_categories[selected_category]
        
        # Grid de estilos
        cols = st.columns(2)
        
        for i, (style_name, description) in enumerate(styles.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {style_name}")
                    st.markdown(f"*{description}*")
                    
                    # Ejemplos de prompts para este estilo
                    example_prompts = get_style_example_prompts(style_name)
                    
                    with st.expander("Ver ejemplos de prompts"):
                        for example in example_prompts:
                            st.code(example, language="text")
                    
                    # Boton para aplicar estilo
                    if st.button(f"🎨 Aplicar Estilo", key=f"apply_style_{i}"):
                        apply_style_to_generation(style_name, description)
                        st.success(f"✅ Estilo '{style_name}' aplicado")
                
                st.markdown("---")
    
    # Comparador de estilos
    st.markdown("## 🔍 Comparador de Estilos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        all_styles = []
        for category_styles in style_categories.values():
            all_styles.extend(category_styles.keys())
        
        style_1 = st.selectbox("Estilo 1:", all_styles, key="style_compare_1")
        
    with col2:
        style_2 = st.selectbox("Estilo 2:", all_styles, key="style_compare_2")
    
    if style_1 != style_2:
        st.markdown("### 📊 Comparacion")
        
        # Encontrar descripciones de los estilos
        desc_1 = None
        desc_2 = None
        
        for category_styles in style_categories.values():
            if style_1 in category_styles:
                desc_1 = category_styles[style_1]
            if style_2 in category_styles:
                desc_2 = category_styles[style_2]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{style_1}**")
            st.markdown(desc_1)
            
            # Ejemplo de prompt
            examples_1 = get_style_example_prompts(style_1)
            if examples_1:
                st.code(examples_1[0], language="text")
        
        with col2:
            st.markdown(f"**{style_2}**")
            st.markdown(desc_2)
            
            # Ejemplo de prompt
            examples_2 = get_style_example_prompts(style_2)
            if examples_2:
                st.code(examples_2[0], language="text")
        
        # Recomendaciones
        st.markdown("### 💡 Recomendaciones de Uso")
        
        recommendations = get_style_recommendations(style_1, style_2)
        for rec in recommendations:
            st.markdown(f"- {rec}")

def get_style_example_prompts(style_name):
    """Retorna prompts de ejemplo para un estilo especifico"""
    
    examples = {
        "Christopher Nolan": [
            "Complex layered scene with multiple time periods, dark atmospheric lighting, practical effects, IMAX quality cinematography",
            "Mind-bending reality scene, rotating camera work, deep shadows and bright highlights, cinematic scope"
        ],
        "Wes Anderson": [
            "Perfectly symmetrical composition, pastel color palette, whimsical characters in vintage clothing, dollhouse aesthetic",
            "Centered frame, flat lighting, quirky dialogue scene, retro production design"
        ],
        "Denis Villeneuve": [
            "Epic sci-fi landscape, atmospheric fog, golden hour lighting, wide cinematic scope, otherworldly atmosphere",
            "Intimate character moment in vast environment, moody lighting, contemplative pacing"
        ],
        "Marvel Cinematic": [
            "Dynamic superhero action sequence, high contrast lighting, saturated colors, epic scale destruction",
            "Hero moment with dramatic lighting, bold colors, cinematic composition"
        ],
        "A24 Arthouse": [
            "Intimate character study, natural window lighting, muted color palette, handheld camera intimacy",
            "Quiet contemplative scene, soft natural light, desaturated colors, emotional depth"
        ]
    }
    
    return examples.get(style_name, [
        "Cinematic scene with professional lighting and composition",
        "High-quality cinematography with attention to visual storytelling"
    ])

def apply_style_to_generation(style_name, description):
    """Aplica un estilo especifico a la configuracion de generacion"""
    
    # Guardar configuracion de estilo en session state
    style_config = {
        'name': style_name,
        'description': description,
        'applied_at': datetime.now().isoformat()
    }
    
    st.session_state.applied_style = style_config

def get_style_recommendations(style_1, style_2):
    """Genera recomendaciones comparativas entre estilos"""
    
    recommendations = [
        f"Para contenido dramatico, considera {style_1}",
        f"Para audiencia general, {style_2} podria ser mas accesible",
        "Ambos estilos se pueden combinar para crear algo unico",
        "Considera el genero de tu historia al elegir entre estos estilos"
    ]
    
    return recommendations

def get_example_manuscript():
    """Retorna manuscrito de ejemplo para demostracion"""
    
    return """En el reino de Aethermoor, donde la magia fluye como rios de luz dorada a traves de cristales ancestrales, la joven maga Lyra Stormwind descubrio que su destino estaba escrito en runas que solo ella podia leer.

El dia que encontro el grimorio perdido de Arcanum Infinitus en las ruinas de la Torre de Marfil, no sabia que estaba por desencadenar una guerra que cambiaria para siempre el equilibrio entre la luz y las sombras del mundo conocido.

Los cristales resonaban con una frecuencia que hacia temblar la tierra bajo sus pies. Lyra extendio su mano hacia el libro antiguo, sintiendo como la energia magica corriera por sus venas como fuego liquido.

"No todos los secretos estan destinados a ser revelados," susurro una voz detras de ella. Al voltearse, vio la silueta encapuchada del Guardian de las Sombras, sus ojos brillando con una luz sobrenatural.

La batalla final habia comenzado."""