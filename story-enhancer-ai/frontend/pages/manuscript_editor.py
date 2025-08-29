"""
Página del editor de manuscrito
"""

import streamlit as st
import tempfile
from pathlib import Path
from datetime import datetime
from frontend.utils.session_state import add_log_entry

def render_manuscript_editor():
    """Renderiza la página del editor de manuscrito"""
    
    st.title("✍️ Editor de Manuscrito")
    st.markdown("Carga y edita tu historia base que será mejorada por los agentes.")
    
    # Tabs para organizar la funcionalidad
    tab1, tab2, tab3 = st.tabs(["📤 Cargar Manuscrito", "✏️ Editor", "📊 Análisis"])
    
    with tab1:
        render_manuscript_upload()
        
    with tab2:
        render_manuscript_editor_tab()
        
    with tab3:
        render_manuscript_analysis()

def render_manuscript_upload():
    """Sección para cargar manuscrito desde archivo"""
    
    st.subheader("📤 Cargar Manuscrito desde Archivo")
    
    # File uploader para manuscrito
    uploaded_file = st.file_uploader(
        "Selecciona tu manuscrito",
        type=['txt', 'md', 'docx', 'pdf'],
        help="Formatos soportados: TXT, Markdown, DOCX, PDF"
    )
    
    if uploaded_file:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(f"📄 {uploaded_file.name}")
        with col2:
            st.text(f"📏 {uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.text(uploaded_file.type or "Texto")
        
        # Botón para procesar archivo
        if st.button("📖 Cargar Contenido", type="primary"):
            load_manuscript_file(uploaded_file)
    
    st.markdown("---")
    
    # Opción de manuscrito de ejemplo
    st.subheader("📝 Usar Manuscrito de Ejemplo")
    st.markdown("Si no tienes un manuscrito listo, puedes usar uno de ejemplo para probar el sistema.")
    
    if st.button("📖 Cargar Ejemplo: 'La Espada Perdida'"):
        load_example_manuscript()

def load_manuscript_file(uploaded_file):
    """Carga el contenido del archivo de manuscrito"""
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Procesar según el tipo de archivo
        content = ""
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension in ['.txt', '.md']:
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
        elif file_extension == '.docx':
            from docx import Document
            doc = Document(tmp_path)
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
        elif file_extension == '.pdf':
            import PyPDF2
            with open(tmp_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = '\n'.join([page.extract_text() for page in pdf_reader.pages])
        
        if content.strip():
            st.session_state.manuscript_content = content
            st.session_state.manuscript_file = uploaded_file.name
            st.success(f"✅ Manuscrito '{uploaded_file.name}' cargado exitosamente!")
            st.info(f"📊 {len(content)} caracteres, ~{len(content.split())} palabras")
            
            add_log_entry(f"Manuscrito cargado: {uploaded_file.name}", "success", "manuscript_loader")
            
            # Limpiar archivo temporal
            Path(tmp_path).unlink()
            
        else:
            st.error("❌ El archivo está vacío o no se pudo leer el contenido")
            
    except Exception as e:
        st.error(f"❌ Error cargando el manuscrito: {e}")
        add_log_entry(f"Error cargando manuscrito: {str(e)}", "error", "manuscript_loader")

def load_example_manuscript():
    """Carga un manuscrito de ejemplo"""
    
    example_story = """# La Espada Perdida

## Capítulo 1: El Llamado

En las brumosas tierras de Valderon, donde las montañas tocan las nubes y los antiguos secretos duermen bajo piedras milenarias, Aria despertó con el corazón acelerado. El sueño había vuelto.

Siempre el mismo. Una espada de plata brillando bajo la luz de la luna, enterrada en el corazón de un bosque que no existía en ningún mapa. Una voz que la llamaba, susurrando su nombre entre los árboles ancestrales.

—Aria... la espada te espera...

Se levantó de su humilde cama en la posada "El Dragón Dormido", donde había trabajado los últimos tres años como sirvienta. A los dieciocho años, su vida transcurría entre limpiar mesas y servir cerveza a viajeros que llegaban con historias de tierras lejanas.

Pero los sueños la perseguían. Y cada noche, la voz se hacía más clara.

## Capítulo 2: La Profecía

El anciano Theron llegó esa mañana envuelto en una capa gris, con ojos que parecían haber visto siglos. Se sentó en su mesa habitual y pidió solo agua.

—Tú eres la chica de los sueños —no fue una pregunta.

Aria se sobresaltó, casi derramando la jarra que llevaba.

—¿Cómo...?

—Los vientos me trajeron tu llamado. La Espada de Luminar ha despertado después de mil años. Y te ha elegido.

El mundo de Aria se tambaleó. Las leyendas que su abuela le contaba cuando era niña... ¿eran ciertas?

—Pero yo no soy nadie especial. Solo una sirvienta...

—Los héroes nacen en los lugares más humildes, niña. La espada no se equivoca. Valderon necesita un campeón. Las fuerzas oscuras se agitan en el norte. El Señor de las Sombras ha vuelto.

Theron extendió un mapa amarillento.

—El Bosque de Susurros. Allí encontrarás tu destino.

## Capítulo 3: El Viaje Comienza

Aria miró por última vez la posada que había sido su hogar. Con una pequeña mochila y el mapa de Theron, se dirigió hacia lo desconocido.

El camino al Bosque de Susurros era traicionero. Criaturas extrañas se movían entre las sombras, y el aire mismo parecía espeso con magia antigua.

Al tercer día de viaje, encontró a Kael, un joven guerrero herido al borde del camino. Sus ropas estaban desgarradas y una garra había marcado su brazo.

—Lobos sombra —murmuró cuando Aria lo ayudó—. Vienen del norte. Algo los ha despertado.

—Voy al Bosque de Susurros —le dijo Aria—. ¿Conoces el lugar?

Los ojos de Kael se abrieron con sorpresa.

—¿Tú? ¿Una chica sola va a ese lugar maldito? Nadie que entra allí sale vivo.

—Tengo que hacerlo.

Algo en la determinación de Aria convenció al guerrero.

—Entonces iré contigo. Mi hermana desapareció cerca de esas tierras. Tal vez...

Y así, dos destinos se unieron en el camino hacia una espada que cambiaría el mundo.

---

*[Este es solo el comienzo de la historia. Los agentes la expandirán y mejorarán, desarrollando personajes, añadiendo profundidad al worldbuilding y refinando la narrativa...]*
"""
    
    st.session_state.manuscript_content = example_story
    st.session_state.manuscript_file = "ejemplo_la_espada_perdida.md"
    st.success("✅ Manuscrito de ejemplo cargado!")
    st.info("📊 Historia de ejemplo lista para mejorar con los agentes")
    
    add_log_entry("Manuscrito de ejemplo cargado", "success", "manuscript_loader")

def render_manuscript_editor_tab():
    """Editor de texto para el manuscrito"""
    
    st.subheader("✏️ Editor de Texto")
    
    if not st.session_state.manuscript_content:
        st.info("📝 Carga un manuscrito primero para poder editarlo.")
        return
    
    # Información del manuscrito actual
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Archivo", st.session_state.manuscript_file or "Sin nombre")
    with col2:
        word_count = len(st.session_state.manuscript_content.split())
        st.metric("📝 Palabras", word_count)
    with col3:
        char_count = len(st.session_state.manuscript_content)
        st.metric("🔤 Caracteres", char_count)
    
    st.markdown("---")
    
    # Editor de texto principal
    new_content = st.text_area(
        "Contenido del manuscrito:",
        value=st.session_state.manuscript_content,
        height=400,
        help="Edita tu historia aquí. Los cambios se guardan automáticamente."
    )
    
    # Detectar cambios y guardar
    if new_content != st.session_state.manuscript_content:
        st.session_state.manuscript_content = new_content
        add_log_entry("Manuscrito editado", "info", "manuscript_editor")
    
    # Controles del editor
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Guardar"):
            save_manuscript_to_file()
    
    with col2:
        if st.button("🔄 Revertir"):
            # Aquí podrías implementar un sistema de versiones
            st.info("Función de revertir en desarrollo")
    
    with col3:
        if st.button("📋 Copiar"):
            st.code(st.session_state.manuscript_content)
            st.info("Contenido mostrado arriba para copiar")
    
    with col4:
        if st.button("🗑️ Limpiar"):
            if st.confirm("¿Estás seguro de que quieres borrar todo el contenido?"):
                st.session_state.manuscript_content = ""
                st.success("Manuscrito limpiado")

def save_manuscript_to_file():
    """Guarda el manuscrito en un archivo local"""
    try:
        filename = f"manuscript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = Path("static/outputs") / filename
        
        # Crear directorio si no existe
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(st.session_state.manuscript_content)
        
        st.success(f"✅ Manuscrito guardado como {filename}")
        add_log_entry(f"Manuscrito guardado: {filename}", "success", "manuscript_editor")
        
    except Exception as e:
        st.error(f"❌ Error guardando manuscrito: {e}")

def render_manuscript_analysis():
    """Análisis del manuscrito actual"""
    
    st.subheader("📊 Análisis del Manuscrito")
    
    if not st.session_state.manuscript_content:
        st.info("📝 Carga un manuscrito primero para ver su análisis.")
        return
    
    content = st.session_state.manuscript_content
    
    # Métricas básicas
    words = content.split()
    sentences = content.split('.')
    paragraphs = [p for p in content.split('\n\n') if p.strip()]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Palabras", len(words))
    with col2:
        st.metric("📖 Oraciones", len(sentences))
    with col3:
        st.metric("📄 Párrafos", len(paragraphs))
    with col4:
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        st.metric("📊 Palabras/Oración", f"{avg_words_per_sentence:.1f}")
    
    st.markdown("---")
    
    # Análisis de estructura
    st.subheader("🏗️ Estructura")
    
    # Detectar capítulos/secciones
    lines = content.split('\n')
    headers = [line for line in lines if line.startswith('#') or line.startswith('##')]
    
    if headers:
        st.write(f"**📚 Secciones encontradas: {len(headers)}**")
        for header in headers[:10]:  # Mostrar solo los primeros 10
            st.text(f"• {header}")
        if len(headers) > 10:
            st.text(f"... y {len(headers) - 10} más")
    else:
        st.info("No se detectaron capítulos o secciones marcadas con #")
    
    # Análisis de personajes (simple)
    st.subheader("👥 Personajes Detectados")
    
    # Lista simple de palabras capitalizadas que podrían ser nombres
    import re
    potential_names = re.findall(r'\b[A-Z][a-z]+\b', content)
    name_counts = {}
    for name in potential_names:
        if len(name) > 2:  # Filtrar palabras muy cortas
            name_counts[name] = name_counts.get(name, 0) + 1
    
    # Mostrar los nombres más frecuentes (excluyendo palabras comunes)
    common_words = {'The', 'And', 'But', 'For', 'With', 'When', 'Where', 'What', 'How', 'Who'}
    character_candidates = {name: count for name, count in name_counts.items() 
                          if count > 1 and name not in common_words}
    
    if character_candidates:
        sorted_characters = sorted(character_candidates.items(), key=lambda x: x[1], reverse=True)
        st.write("**Posibles personajes (por frecuencia de mención):**")
        for name, count in sorted_characters[:10]:
            st.text(f"• {name}: {count} menciones")
    else:
        st.info("No se detectaron personajes claramente identificables")
    
    # Análisis de legibilidad simple
    st.subheader("📖 Legibilidad")
    
    if words:
        avg_word_length = sum(len(word) for word in words) / len(words)
        st.metric("📏 Longitud promedio de palabra", f"{avg_word_length:.1f} caracteres")
        
        # Nivel de lectura simple basado en longitud de palabras y oraciones
        complexity_score = (avg_word_length * 0.5) + (avg_words_per_sentence * 0.1)
        
        if complexity_score < 5:
            level = "Fácil"
            color = "green"
        elif complexity_score < 7:
            level = "Intermedio"
            color = "orange"
        else:
            level = "Avanzado"
            color = "red"
        
        st.markdown(f"**Nivel de lectura estimado:** :{color}[{level}]")
    
def perform_ai_analysis(content: str):
    """Realiza un análisis más profundo usando IA"""
    
    with st.spinner("🤖 Analizando manuscrito con IA..."):
        try:
            # Aquí se conectaría con el LLM para análisis profundo
            # Por ahora, simulamos el análisis
            
            analysis_results = {
                "tone": "Aventura épica con elementos de fantasía clásica",
                "pacing": "Ritmo acelerado en el inicio, establece tensión efectivamente",
                "character_development": "Protagonista con potencial, necesita más profundidad emocional",
                "world_building": "Mundo fantástico tradicional, podría beneficiarse de elementos únicos",
                "dialogue": "Diálogo funcional, podría ser más distintivo por personaje",
                "strengths": [
                    "Inicio enganchador con el sueño recurrente",
                    "Establecimiento claro del llamado a la aventura",
                    "Buena progresión del protagonista pasivo a activo"
                ],
                "areas_for_improvement": [
                    "Desarrollar más la voz interna de Aria",
                    "Añadir detalles únicos al worldbuilding",
                    "Profundizar en las motivaciones de los personajes secundarios",
                    "Expandir la descripción de los peligros y obstáculos"
                ],
                "suggestions": [
                    "Considerar añadir un conflicto interno más profundo para Aria",
                    "Desarrollar una mecánica de magia más específica",
                    "Crear subtramas que conecten con el arco principal"
                ]
            }
            
            # Mostrar resultados
            st.success("✅ Análisis completado!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎭 Elementos Narrativos")
                st.write(f"**Tono:** {analysis_results['tone']}")
                st.write(f"**Ritmo:** {analysis_results['pacing']}")
                st.write(f"**Desarrollo de personajes:** {analysis_results['character_development']}")
                st.write(f"**Construcción del mundo:** {analysis_results['world_building']}")
                st.write(f"**Diálogo:** {analysis_results['dialogue']}")
            
            with col2:
                st.subheader("💪 Fortalezas")
                for strength in analysis_results['strengths']:
                    st.write(f"✅ {strength}")
                
                st.subheader("🎯 Áreas de Mejora")
                for area in analysis_results['areas_for_improvement']:
                    st.write(f"📈 {area}")
            
            st.subheader("💡 Sugerencias")
            for suggestion in analysis_results['suggestions']:
                st.write(f"💭 {suggestion}")
            
            add_log_entry("Análisis IA completado", "success", "ai_analyzer")
            
        except Exception as e:
            st.error(f"❌ Error en análisis IA: {e}")
            add_log_entry(f"Error en análisis IA: {str(e)}", "error", "ai_analyzer")