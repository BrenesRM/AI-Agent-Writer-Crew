import streamlit as st
import time
from datetime import datetime
from typing import Dict, List

def render_manuscript_page(agent_manager):
    """Renderiza la página del editor de manuscrito"""
    
    st.header("✍️ Editor de Manuscrito")
    st.markdown("*Escribe tu manuscrito y mejóralo con la ayuda de agentes especializados*")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Editor",
        "🔄 Procesamiento",
        "📋 Historial",
        "⚙️ Configuración"
    ])
    
    with tab1:
        render_editor_tab(agent_manager)
    
    with tab2:
        render_processing_tab(agent_manager)
    
    with tab3:
        render_history_tab()
    
    with tab4:
        render_config_tab()

def render_editor_tab(agent_manager):
    """Tab del editor principal"""
    st.subheader("📝 Editor de Manuscrito")
    
    # Estadísticas del manuscrito
    if st.session_state.manuscript:
        word_count = len(st.session_state.manuscript.split())
        char_count = len(st.session_state.manuscript)
        paragraph_count = len([p for p in st.session_state.manuscript.split('\n\n') if p.strip()])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Palabras", word_count)
        with col2:
            st.metric("Caracteres", char_count)
        with col3:
            st.metric("Párrafos", paragraph_count)
        with col4:
            reading_time = max(1, word_count // 250)  # ~250 palabras por minuto
            st.metric("Tiempo de lectura", f"{reading_time} min")
    
    # Editor principal
    manuscript_text = st.text_area(
        "Escribe tu manuscrito aquí:",
        value=st.session_state.manuscript,
        height=400,
        placeholder="""Ejemplo:

En el reino de Aethermoor, donde la magia fluye como ríos de luz dorada a través de cristales ancestrales, la joven maga Lyra Stormwind descubrió que su destino estaba escrito en runas que solo ella podía leer.

El día que encontró el grimorio perdido de Arcanum Infinitus en las ruinas de la Torre de Marfil, no sabía que estaba por desencadenar una guerra que cambiaría para siempre el equilibrio entre la luz y las sombras...

[Continúa escribiendo tu historia aquí]""",
        key="manuscript_editor"
    )
    
    # Actualizar manuscrito en session state
    if manuscript_text != st.session_state.manuscript:
        st.session_state.manuscript = manuscript_text
    
    # Herramientas rápidas
    st.markdown("---")
    st.subheader("🛠️ Herramientas Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Guardar Borrador", use_container_width=True):
            # Implementar guardado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_name = f"borrador_{timestamp}"
            
            if 'drafts' not in st.session_state:
                st.session_state.drafts = {}
            
            st.session_state.drafts[draft_name] = {
                'content': st.session_state.manuscript,
                'timestamp': datetime.now().isoformat(),
                'word_count': len(st.session_state.manuscript.split())
            }
            
            st.success(f"✅ Borrador guardado como: {draft_name}")
    
    with col2:
        if st.button("📊 Análisis Rápido", use_container_width=True):
            if st.session_state.manuscript:
                with st.spinner("Analizando manuscrito..."):
                    # Simular análisis rápido
                    time.sleep(2)
                    
                    # Análisis básico
                    words = st.session_state.manuscript.split()
                    sentences = st.session_state.manuscript.split('.')
                    
                    # Mostrar resultados básicos
                    st.success("📈 Análisis completado")
                    
                    with st.expander("Ver resultados del análisis"):
                        st.markdown("**Métricas de legibilidad:**")
                        st.markdown(f"- Promedio palabras por oración: {len(words)/len(sentences):.1f}")
                        st.markdown(f"- Palabras únicas: {len(set(word.lower() for word in words))}")
                        
                        # Palabras más frecuentes (análisis básico)
                        word_freq = {}
                        for word in words:
                            clean_word = word.lower().strip('.,!?";')
                            if len(clean_word) > 3:
                                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
                        
                        if word_freq:
                            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                            st.markdown("**Palabras más frecuentes:**")
                            for word, count in top_words:
                                st.markdown(f"- {word}: {count} veces")
            else:
                st.warning("⚠️ Escribe algo en el manuscrito primero")
    
    with col3:
        if st.button("🎨 Sugerencia Creativa", use_container_width=True):
            # Generar sugerencia creativa
            suggestions = [
                "🌟 Considera añadir un detalle sensorial que haga la escena más vívida",
                "🎭 ¿Qué pasaría si tu personaje tomara la decisión opuesta?",
                "🔮 Introduce un elemento inesperado que cambie la dinámica",
                "💎 Desarrolla más la voz interior de tu personaje principal",
                "⚡ Acelera el ritmo con un diálogo dinámico",
                "🌊 Explora las emociones profundas de este momento",
                "🔍 Añade un detalle que revele algo sobre el personaje",
                "🎪 Introduce un contraste que sorprenda al lector"
            ]
            
            import random
            suggestion = random.choice(suggestions)
            st.info(f"💡 {suggestion}")
    
    # Plantillas y ejemplos
    if not st.session_state.manuscript:
        st.markdown("---")
        st.subheader("📋 Plantillas de Inicio")
        
        templates = {
            "🏰 Fantasía Épica": """En el reino de [NOMBRE_REINO], donde [ELEMENTO_MÁGICO] determina el destino de los mortales, [PROTAGONISTA] descubrió que [SECRETO_REVELADOR] cambiaría para siempre [MUNDO/VIDA].

El día que [EVENTO_INICIAL], no sabía que estaba por [CONSECUENCIA_MAYOR] que [IMPACTO_EN_EL_MUNDO].""",
            
            "🕵️ Misterio": """El detective [NOMBRE] había visto muchas cosas en sus [AÑOS] años de servicio, pero nunca algo como esto. El cuerpo de [VÍCTIMA] yacía en [LUGAR], rodeado de [EVIDENCIA_EXTRAÑA] que desafiaba toda lógica.

Lo que más le inquietaba no era [DETALLE_OBVIO], sino [DETALLE_SUTIL] que sugería que el asesino [PISTA_CLAVE].""",
            
            "🚀 Ciencia Ficción": """En el año [AÑO_FUTURO], la humanidad había [AVANCE_TECNOLÓGICO], pero [PROTAGONISTA] sabía que algo estaba terriblemente mal. Las [SEÑALES/DATOS] que había detectado en [LUGAR/SISTEMA] apuntaban a una verdad que [ORGANIZACIÓN/GOBIERNO] haría cualquier cosa por ocultar.

Mientras [ACCIÓN_ACTUAL], no podía ignorar la evidencia: [REVELACIÓN_INQUIETANTE].""",
            
            "💕 Romance": """[PROTAGONISTA] nunca esperó encontrar el amor en [LUGAR_INESPERADO]. Después de [EVENTO_DEL_PASADO], había decidido que [BARRERA_EMOCIONAL]. Pero cuando [ENCUENTRO_CON_AMOR_INTERÉS], algo en su interior [CAMBIO_EMOCIONAL].

Era [DESCRIPCIÓN_FÍSICA/EMOCIONAL] lo que la/lo desarmo completamente, pero fue [MOMENTO_ESPECÍFICO] cuando supo que [REALIZACIÓN_ROMÁNTICA]."""
        }
        
        selected_template = st.selectbox("Elige una plantilla:", list(templates.keys()))
        
        if st.button("📝 Usar Plantilla"):
            st.session_state.manuscript = templates[selected_template]
            st.rerun()

def render_processing_tab(agent_manager):
    """Tab de procesamiento con agentes"""
    st.subheader("🔄 Procesamiento con Agentes IA")
    
    if not st.session_state.manuscript:
        st.warning("⚠️ Primero escribe algo en el editor para poder procesarlo con los agentes.")
        return
    
    # Información del manuscrito actual
    word_count = len(st.session_state.manuscript.split())
    
    st.info(f"📝 Manuscrito actual: {word_count} palabras")
    
    # Selección de fases de análisis
    st.subheader("🎯 Seleccionar Fases de Análisis")
    
    phases = {
        "worldbuilding": {
            "name": "🏰 Worldbuilding",
            "description": "Coherencia del mundo, lore y reglas mágicas",
            "agents": ["Lorekeeper", "Researcher", "Continuity Auditor"],
            "time": "2-3 min"
        },
        "character": {
            "name": "👥 Desarrollo de Personajes", 
            "description": "Profundidad, motivaciones y arcos narrativos",
            "agents": ["Character Developer", "Beta Reader"],
            "time": "3-4 min"
        },
        "plot": {
            "name": "📖 Estructura Narrativa",
            "description": "Trama, ritmo y elementos dramáticos",
            "agents": ["Plot Weaver", "Pacing Specialist", "Innovation Scout"],
            "time": "4-5 min"
        },
        "style": {
            "name": "✨ Refinamiento de Estilo",
            "description": "Voz narrativa, tono y fluidez de la prosa",
            "agents": ["Style Editor", "Beta Reader"],
            "time": "2-3 min"
        },
        "visual": {
            "name": "🎬 Generación Visual",
            "description": "Prompts cinematográficos para IA de video",
            "agents": ["Visualizer"],
            "time": "1-2 min"
        },
        "quality": {
            "name": "🔍 Control de Calidad",
            "description": "Corrección, consistencia y pulido final",
            "agents": ["Proofreader", "Continuity Auditor"],
            "time": "2-3 min"
        }
    }
    
    selected_phases = []
    
    for phase_id, phase_info in phases.items():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected = st.checkbox(
                phase_info["name"],
                key=f"phase_{phase_id}",
                value=(phase_id in ["worldbuilding", "character", "plot"])  # Seleccionar por defecto
            )
            
            if selected:
                selected_phases.append(phase_id)
        
        with col2:
            st.markdown(f"**{phase_info['description']}**")
            st.caption(f"Agentes: {', '.join(phase_info['agents'])} • Tiempo estimado: {phase_info['time']}")
    
    # Configuración de procesamiento
    st.markdown("---")
    st.subheader("⚙️ Configuración de Procesamiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        processing_mode = st.selectbox(
            "Modo de procesamiento:",
            ["Análisis Completo", "Análisis Rápido", "Solo Sugerencias"],
            help="Completo: análisis detallado, Rápido: insights principales, Sugerencias: solo recomendaciones"
        )
    
    with col2:
        creativity_level = st.slider(
            "Nivel de creatividad:",
            min_value=1,
            max_value=10,
            value=7,
            help="1 = Conservador, 10 = Muy creativo y experimental"
        )
    
    # Procesamiento
    if selected_phases:
        total_time = sum(int(phases[phase]["time"].split("-")[1].split(" ")[0]) for phase in selected_phases)
        
        st.markdown("---")
        st.markdown(f"**📊 Resumen:** {len(selected_phases)} fases seleccionadas • Tiempo estimado: ~{total_time} minutos")
        
        if st.button("🚀 Iniciar Procesamiento con Agentes", type="primary", use_container_width=True):
            process_manuscript_with_agents(agent_manager, selected_phases, phases, processing_mode, creativity_level)
    else:
        st.warning("⚠️ Selecciona al menos una fase de análisis.")

def process_manuscript_with_agents(agent_manager, selected_phases, phases_info, mode, creativity):
    """Procesa el manuscrito con los agentes seleccionados"""
    
    # Configurar el manuscrito en el agent manager
    agent_manager.set_manuscript(st.session_state.manuscript)
    
    # Barra de progreso general
    main_progress = st.progress(0)
    status_text = st.empty()
    
    # Contenedor para resultados
    results_container = st.container()
    
    try:
        st.session_state.processing = True
        st.session_state.analysis_results = {}
        
        total_phases = len(selected_phases)
        
        for i, phase_id in enumerate(selected_phases):
            phase_info = phases_info[phase_id]
            
            # Actualizar estado
            st.session_state.current_phase = phase_info["name"]
            status_text.text(f"🔄 Procesando {phase_info['name']}... ({i+1}/{total_phases})")
            
            # Simular procesamiento (en implementación real, usar agent_manager)
            phase_progress = st.progress(0)
            
            # Proceso simulado por agente
            for agent_idx, agent_name in enumerate(phase_info["agents"]):
                phase_progress.progress((agent_idx + 1) / len(phase_info["agents"]))
                time.sleep(1)  # Simular trabajo del agente
            
            # Generar resultados simulados
            result = generate_simulated_results(phase_id, phase_info, mode, creativity)
            st.session_state.analysis_results[phase_id] = result
            
            # Mostrar resultado de la fase
            with results_container:
                with st.expander(f"✅ {phase_info['name']} - Completado", expanded=True):
                    display_phase_results(result, phase_info)
            
            # Actualizar progreso principal
            main_progress.progress((i + 1) / total_phases)
            phase_progress.empty()
        
        # Completado
        st.session_state.processing = False
        st.session_state.current_phase = ""
        status_text.text("✅ ¡Procesamiento completado!")
        
        # Mostrar resumen final
        with results_container:
            st.success("🎉 ¡Análisis completado exitosamente!")
            
            # Estadísticas finales
            total_suggestions = sum(len(result.get('suggestions', [])) for result in st.session_state.analysis_results.values())
            st.metric("Sugerencias generadas", total_suggestions)
    
    except Exception as e:
        st.session_state.processing = False
        st.error(f"❌ Error durante el procesamiento: {str(e)}")

def generate_simulated_results(phase_id, phase_info, mode, creativity):
    """Genera resultados simulados para demostración"""
    
    results_templates = {
        "worldbuilding": {
            "score": 8.2,
            "suggestions": [
                "El sistema de magia basado en cristales es coherente, pero considera especificar las limitaciones",
                "Excelente descripción de Aethermoor. Podrías añadir detalles sobre el clima/geografía",
                "La Torre de Marfil tiene potencial narrativo. Desarrolla más su historia"
            ],
            "strengths": [
                "Mitología sólida y bien establecida",
                "Elementos mágicos únicos e interesantes", 
                "Coherencia en las reglas del mundo"
            ],
            "improvements": [
                "Expandir la geografía política del reino",
                "Definir mejor las consecuencias del uso de magia",
                "Añadir más detalles culturales/sociales"
            ]
        },
        "character": {
            "score": 7.5,
            "suggestions": [
                "Lyra es una protagonista prometedora. Desarrolla más sus miedos/debilidades internas",
                "Su motivación está clara, pero podrías añadir conflictos emocionales más profundos",
                "Considera crear un mentor o aliado que desafíe sus perspectivas"
            ],
            "strengths": [
                "Protagonista con potencial de crecimiento",
                "Motivación clara y comprensible",
                "Personalidad distintiva"
            ],
            "improvements": [
                "Añadir flaws más complejos",
                "Desarrollar relationships interpersonales",
                "Crear arco de transformación más definido"
            ]
        },
        "plot": {
            "score": 8.7,
            "suggestions": [
                "El inciting incident (encontrar el grimorio) es efectivo y intrigante",
                "La escalada hacia la guerra es prometedora. Asegúrate de mantener el ritmo",
                "Considera añadir obstáculos más personales además de los externos"
            ],
            "strengths": [
                "Hook inicial muy efectivo",
                "Stakes claros y elevados",
                "Potential para múltiples plot threads"
            ],
            "improvements": [
                "Desarrollar más los antagonistas",
                "Añadir subplots que enriquezcan la trama principal",
                "Planificar mejor los plot twists"
            ]
        }
    }
    
    # Personalizar según creatividad y modo
    base_result = results_templates.get(phase_id, {
        "score": 7.0 + creativity * 0.2,
        "suggestions": ["Análisis en desarrollo..."],
        "strengths": ["Elementos prometedores identificados"],
        "improvements": ["Áreas de mejora detectadas"]
    })
    
    return base_result

def display_phase_results(result, phase_info):
    """Muestra los resultados de una fase"""
    
    # Score
    score = result.get('score', 7.0)
    score_color = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
    
    st.markdown(f"**Puntuación General:** {score_color} {score}/10")
    
    # Fortalezas
    if result.get('strengths'):
        st.markdown("**✅ Fortalezas detectadas:**")
        for strength in result['strengths']:
            st.markdown(f"- {strength}")
    
    # Sugerencias de mejora
    if result.get('suggestions'):
        st.markdown("**💡 Sugerencias de mejora:**")
        for suggestion in result['suggestions']:
            st.markdown(f"- {suggestion}")
    
    # Áreas de mejora
    if result.get('improvements'):
        st.markdown("**🔧 Áreas de mejora:**")
        for improvement in result['improvements']:
            st.markdown(f"- {improvement}")

def render_history_tab():
    """Tab de historial de versiones"""
    st.subheader("📋 Historial de Versiones")
    
    # Mostrar borradores guardados
    if 'drafts' in st.session_state and st.session_state.drafts:
        st.markdown("**💾 Borradores Guardados:**")
        
        for draft_name, draft_info in st.session_state.drafts.items():
            with st.expander(f"📄 {draft_name} ({draft_info['word_count']} palabras)"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Guardado:** {draft_info['timestamp']}")
                    st.text_area(
                        "Contenido:",
                        value=draft_info['content'][:500] + "..." if len(draft_info['content']) > 500 else draft_info['content'],
                        height=150,
                        disabled=True,
                        key=f"draft_preview_{draft_name}"
                    )
                
                with col2:
                    if st.button(f"📤 Restaurar", key=f"restore_{draft_name}"):
                        st.session_state.manuscript = draft_info['content']
                        st.success("✅ Borrador restaurado")
                        st.rerun()
                    
                    if st.button(f"🗑️ Eliminar", key=f"delete_{draft_name}"):
                        del st.session_state.drafts[draft_name]
                        st.success("✅ Borrador eliminado")
                        st.rerun()
    else:
        st.info("📭 No hay borradores guardados. Usa el botón 'Guardar Borrador' en el editor.")
    
    # Historial de análisis
    st.markdown("---")
    st.markdown("**🤖 Historial de Análisis:**")
    
    if st.session_state.analysis_results:
        for phase_id, result in st.session_state.analysis_results.items():
            score = result.get('score', 0)
            suggestions_count = len(result.get('suggestions', []))
            
            st.markdown(f"- **{phase_id.title()}**: {score}/10 ({suggestions_count} sugerencias)")
    else:
        st.info("📭 No hay análisis previos. Procesa tu manuscrito en la pestaña 'Procesamiento'.")

def render_config_tab():
    """Tab de configuración del editor"""
    st.subheader("⚙️ Configuración del Editor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎨 Preferencias de Escritura:**")
        
        # Configuraciones de escritura
        genre = st.selectbox(
            "Género principal:",
            ["Fantasía", "Ciencia Ficción", "Romance", "Misterio", "Terror", "Aventura", "Drama", "Otro"],
            help="Ayuda a los agentes a dar sugerencias más precisas"
        )
        
        target_audience = st.selectbox(
            "Audiencia objetivo:",
            ["Adultos", "Jóvenes Adultos", "Adolescentes", "Infantil", "Todos los públicos"],
            help="Influye en el tono y complejidad de las sugerencias"
        )
        
        writing_style = st.selectbox(
            "Estilo de escritura:",
            ["Descriptivo", "Directo", "Poético", "Conversacional", "Académico"],
            help="Preferencia de estilo para el refinamiento"
        )
    
    with col2:
        st.markdown("**🤖 Configuración de Agentes:**")
        
        # Configuraciones de agentes
        agent_feedback_level = st.selectbox(
            "Nivel de feedback:",
            ["Básico", "Detallado", "Exhaustivo"],
            help="Cantidad de sugerencias y análisis que recibirás"
        )
        
        focus_areas = st.multiselect(
            "Áreas de enfoque:",
            ["Worldbuilding", "Personajes", "Diálogos", "Descripción", "Ritmo", "Estilo"],
            default=["Personajes", "Ritmo"],
            help="Los agentes se enfocarán más en estas áreas"
        )
        
        auto_save = st.checkbox(
            "Auto-guardado cada 5 minutos",
            value=True,
            help="Guarda automáticamente borradores mientras escribes"
        )
    
    # Guardar configuraciones
    if st.button("💾 Guardar Configuración"):
        # Guardar en session state
        st.session_state.editor_config = {
            'genre': genre,
            'target_audience': target_audience,
            'writing_style': writing_style,
            'agent_feedback_level': agent_feedback_level,
            'focus_areas': focus_areas,
            'auto_save': auto_save
        }
        
        st.success("✅ Configuración guardada exitosamente")
    
    # Restablecer configuración
    st.markdown("---")
    if st.button("🔄 Restablecer a Valores por Defecto"):
        if 'editor_config' in st.session_state:
            del st.session_state.editor_config
        st.success("✅ Configuración restablecida")
        st.rerun()