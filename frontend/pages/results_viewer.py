st.markdown(f"- **Caracteres:** {char_count:,}")
            st.markdown(f"- **Párrafos:** {paragraph_count}")
            st.markdown(f"- **Tiempo de lectura:** ~{max(1, word_count // 250)} min")
    
    with col2:
        st.markdown("**🎯 Resumen de Análisis:**")
        st.markdown(f"- **Fases analizadas:** {len(results)}")
        st.markdown(f"- **Fecha del análisis:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.markdown(f"- **Estado:** {'✅ Completado' if results else '⏳ Pendiente'}")
        
        # Nivel de calidad general
        if avg_score >= 8:
            st.success("🌟 **Calidad:** Excelente")
        elif avg_score >= 6:
            st.warning("📈 **Calidad:** Buena - Con potencial de mejora")
        else:
            st.error("🔧 **Calidad:** Necesita trabajo significativo")

def render_detailed_analysis_tab():
    """Tab de análisis detallado por fase"""
    st.subheader("🔍 Análisis Detallado por Fase")
    
    results = st.session_state.analysis_results
    
    if not results:
        st.info("No hay resultados disponibles.")
        return
    
    # Selector de fase
    phase_options = {
        'worldbuilding': '🏰 Worldbuilding',
        'character': '👥 Desarrollo de Personajes',
        'plot': '📖 Estructura Narrativa',
        'style': '✨ Refinamiento de Estilo',
        'visual': '🎬 Generación Visual',
        'quality': '🔍 Control de Calidad'
    }
    
    available_phases = [phase for phase in phase_options.keys() if phase in results]
    
    if not available_phases:
        st.warning("No hay fases de análisis completadas.")
        return
    
    selected_phase = st.selectbox(
        "Selecciona la fase para análisis detallado:",
        options=available_phases,
        format_func=lambda x: phase_options[x]
    )
    
    phase_data = results[selected_phase]
    
    # Mostrar análisis detallado de la fase seleccionada
    render_phase_detailed_analysis(selected_phase, phase_data, phase_options[selected_phase])

def render_phase_detailed_analysis(phase_id, phase_data, phase_name):
    """Renderiza análisis detallado de una fase específica"""
    
    st.markdown(f"## {phase_name}")
    
    # Puntuación principal
    score = phase_data.get('score', 0)
    score_color = "success" if score >= 8 else "warning" if score >= 6 else "error"
    
    if score_color == "success":
        st.success(f"🌟 **Puntuación General: {score:.1f}/10** - Excelente")
    elif score_color == "warning":
        st.warning(f"📈 **Puntuación General: {score:.1f}/10** - Buena, con margen de mejora")
    else:
        st.error(f"🔧 **Puntuación General: {score:.1f}/10** - Necesita atención")
    
    # Métricas detalladas si están disponibles
    if 'details' in phase_data:
        st.markdown("---")
        st.subheader("📊 Métricas Detalladas")
        
        details = phase_data['details']
        cols = st.columns(len(details))
        
        for i, (metric, value) in enumerate(details.items()):
            with cols[i]:
                metric_name = metric.replace('_', ' ').title()
                st.metric(metric_name, f"{value:.1f}")
    
    # Crear tabs para organizar la información
    detail_tabs = st.tabs(["✅ Fortalezas", "💡 Sugerencias", "🔧 Mejoras", "📈 Análisis Profundo"])
    
    with detail_tabs[0]:
        strengths = phase_data.get('strengths', [])
        if strengths:
            st.markdown("**🌟 Aspectos Destacados:**")
            for i, strength in enumerate(strengths, 1):
                st.markdown(f"{i}. ✅ {strength}")
        else:
            st.info("No se identificaron fortalezas específicas en esta fase.")
    
    with detail_tabs[1]:
        suggestions = phase_data.get('suggestions', [])
        if suggestions:
            st.markdown("**💡 Sugerencias de los Agentes:**")
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"{i}. 💡 {suggestion}")
                
                # Botón para aplicar sugerencia (simulado)
                if st.button(f"🔄 Aplicar sugerencia {i}", key=f"apply_sugg_{phase_id}_{i}"):
                    st.success(f"✅ Sugerencia {i} marcada para aplicar")
        else:
            st.info("No hay sugerencias específicas para esta fase.")
    
    with detail_tabs[2]:
        improvements = phase_data.get('improvements', [])
        if improvements:
            st.markdown("**🔧 Áreas de Mejora Identificadas:**")
            for i, improvement in enumerate(improvements, 1):
                priority = ["🔴 Alta", "🟡 Media", "🟢 Baja"][i % 3]  # Simular prioridades
                st.markdown(f"{i}. {priority} {improvement}")
        else:
            st.info("No se identificaron áreas específicas de mejora.")
    
    with detail_tabs[3]:
        # Análisis más profundo específico por fase
        render_deep_analysis(phase_id, phase_data)

def render_deep_analysis(phase_id, phase_data):
    """Renderiza análisis profundo específico por fase"""
    
    if phase_id == "worldbuilding":
        st.markdown("**🏰 Análisis de Worldbuilding:**")
        
        # Elementos del mundo
        world_elements = {
            "Sistema de Magia": {"score": 8.5, "description": "Cristales como conductores mágicos - concepto sólido"},
            "Geografía": {"score": 7.2, "description": "Reino de Aethermoor mencionado, necesita más detalles"},
            "Historia": {"score": 8.8, "description": "Torre de Marfil y grimorio crean historia intrigante"},
            "Culturas": {"score": 6.5, "description": "Aspectos culturales poco desarrollados"},
            "Política": {"score": 6.0, "description": "Estructura política del reino no definida"}
        }
        
        for element, data in world_elements.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(element, f"{data['score']:.1f}/10")
            with col2:
                st.markdown(f"📝 {data['description']}")
    
    elif phase_id == "character":
        st.markdown("**👥 Análisis de Personajes:**")
        
        # Análisis de personaje principal
        character_analysis = {
            "Lyra Stormwind": {
                "Desarrollo": 7.5,
                "Motivación": 8.2,
                "Conflicto Interno": 6.8,
                "Arco Narrativo": 7.0,
                "Originalidad": 7.8
            }
        }
        
        for char_name, metrics in character_analysis.items():
            st.markdown(f"**🎭 {char_name}**")
            cols = st.columns(len(metrics))
            for i, (metric, score) in enumerate(metrics.items()):
                with cols[i]:
                    st.metric(metric, f"{score:.1f}")
        
        # Recomendaciones específicas
        st.markdown("**🎯 Recomendaciones Específicas:**")
        st.markdown("- Desarrollar el trasfondo personal de Lyra")
        st.markdown("- Añadir un conflicto interno relacionado con el poder")
        st.markdown("- Crear personajes secundarios que desafíen sus creencias")
    
    elif phase_id == "plot":
        st.markdown("**📖 Análisis de Estructura Narrativa:**")
        
        # Elementos de la trama
        plot_elements = [
            {"element": "Hook Inicial", "strength": "Muy fuerte", "score": 9.2, "comment": "El descubrimiento del grimorio es intrigante"},
            {"element": "Inciting Incident", "strength": "Fuerte", "score": 8.7, "comment": "Clara transición hacia el conflicto principal"},
            {"element": "Escalada", "strength": "Prometedora", "score": 8.0, "comment": "Guerra entre luz y sombras es épica"},
            {"element": "Stakes", "strength": "Altas", "score": 8.5, "comment": "El equilibrio del mundo está en juego"}
        ]
        
        for element in plot_elements:
            col1, col2, col3 = st.columns([2, 1, 3])
            with col1:
                st.markdown(f"**{element['element']}**")
            with col2:
                st.metric("Score", f"{element['score']:.1f}")
            with col3:
                st.markdown(f"💬 {element['comment']}")

def render_metrics_tab():
    """Tab de métricas y gráficos"""
    st.subheader("📊 Métricas y Visualizaciones")
    
    results = st.session_state.analysis_results
    
    if not results:
        st.info("No hay métricas disponibles.")
        return
    
    # Gráfico radar de puntuaciones
    st.markdown("### 🎯 Perfil de Puntuaciones")
    
    # Preparar datos para gráfico radar
    categories = []
    scores = []
    
    phase_names_map = {
        'worldbuilding': 'Worldbuilding',
        'character': 'Personajes', 
        'plot': 'Narrativa',
        'style': 'Estilo',
        'visual': 'Visual',
        'quality': 'Calidad'
    }
    
    for phase_id, phase_data in results.items():
        categories.append(phase_names_map.get(phase_id, phase_id.title()))
        scores.append(phase_data.get('score', 0))
    
    # Crear gráfico radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Puntuaciones Actuales',
        line_color='rgb(99, 110, 250)',
        fillcolor='rgba(99, 110, 250, 0.25)'
    ))
    
    # Añadir línea objetivo (score 8.0)
    fig.add_trace(go.Scatterpolar(
        r=[8.0] * len(categories),
        theta=categories,
        name='Objetivo (8.0)',
        line=dict(color='rgb(255, 99, 132)', dash='dash'),
        showlegend=True
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        title="Perfil de Rendimiento por Área",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas comparativas
    st.markdown("---")
    st.markdown("### 📈 Análisis Comparativo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución de puntuaciones
        fig = px.histogram(
            x=scores,
            nbins=5,
            title="Distribución de Puntuaciones",
            labels={'x': 'Puntuación', 'y': 'Frecuencia'},
            color_discrete_sequence=['#636EFA']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de progreso hacia objetivos
        progress_data = []
        for category, score in zip(categories, scores):
            progress = min(score / 8.0 * 100, 100)
            progress_data.append({'Área': category, 'Progreso (%)': progress})
        
        df_progress = pd.DataFrame(progress_data)
        
        fig = px.bar(
            df_progress,
            x='Progreso (%)',
            y='Área',
            orientation='h',
            title="Progreso hacia Objetivos (8.0)",
            color='Progreso (%)',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de métricas detalladas
    st.markdown("---")
    st.markdown("### 📋 Tabla de Métricas Detalladas")
    
    # Crear tabla con métricas detalladas
    detailed_metrics = []
    
    for phase_id, phase_data in results.items():
        phase_name = phase_names_map.get(phase_id, phase_id.title())
        score = phase_data.get('score', 0)
        suggestions_count = len(phase_data.get('suggestions', []))
        strengths_count = len(phase_data.get('strengths', []))
        improvements_count = len(phase_data.get('improvements', []))
        
        # Calcular métricas derivadas
        completeness = min((suggestions_count + strengths_count + improvements_count) / 10 * 100, 100)
        priority = "Alta" if score < 6 else "Media" if score < 8 else "Baja"
        
        detailed_metrics.append({
            'Fase': phase_name,
            'Puntuación': f"{score:.1f}/10",
            'Sugerencias': suggestions_count,
            'Fortalezas': strengths_count,
            'Mejoras': improvements_count,
            'Completitud (%)': f"{completeness:.1f}%",
            'Prioridad': priority,
            'Estado': '✅ Completado' if score > 0 else '⏳ Pendiente'
        })
    
    df_metrics = pd.DataFrame(detailed_metrics)
    st.dataframe(df_metrics, use_container_width=True)
    
    # Insights automáticos
    st.markdown("---")
    st.markdown("### 🤖 Insights Automáticos")
    
    # Calcular insights
    avg_score = sum(scores) / len(scores) if scores else 0
    best_area = categories[scores.index(max(scores))] if scores else "N/A"
    worst_area = categories[scores.index(min(scores))] if scores else "N/A"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"📊 **Promedio General:** {avg_score:.1f}/10")
    
    with col2:
        st.success(f"🌟 **Área Más Fuerte:** {best_area}")
    
    with col3:
        st.warning(f"🎯 **Área de Enfoque:** {worst_area}")

def render_recommendations_tab():
    """Tab de recomendaciones consolidadas"""
    st.subheader("💡 Recomendaciones Consolidadas")
    
    results = st.session_state.analysis_results
    
    if not results:
        st.info("No hay recomendaciones disponibles.")
        return
    
    # Consolidar todas las sugerencias por prioridad
    all_suggestions = []
    all_improvements = []
    
    for phase_id, phase_data in results.items():
        phase_name = phase_id.replace('_', ' ').title()
        
        # Añadir sugerencias con contexto
        for sugg in phase_data.get('suggestions', []):
            priority = determine_priority(phase_data.get('score', 0))
            all_suggestions.append({
                'text': sugg,
                'phase': phase_name,
                'priority': priority,
                'score': phase_data.get('score', 0)
            })
        
        # Añadir mejoras con contexto  
        for imp in phase_data.get('improvements', []):
            priority = determine_priority(phase_data.get('score', 0))
            all_improvements.append({
                'text': imp,
                'phase': phase_name,
                'priority': priority,
                'score': phase_data.get('score', 0)
            })
    
    # Tabs para organizar recomendaciones
    rec_tabs = st.tabs(["🔥 Prioridad Alta", "📈 Prioridad Media", "🟢 Prioridad Baja", "📋 Todas"])
    
    with rec_tabs[0]:
        render_priority_recommendations(all_suggestions + all_improvements, "Alta")
    
    with rec_tabs[1]:
        render_priority_recommendations(all_suggestions + all_improvements, "Media")
    
    with rec_tabs[2]:
        render_priority_recommendations(all_suggestions + all_improvements, "Baja")
    
    with rec_tabs[3]:
        render_all_recommendations(all_suggestions, all_improvements)

def determine_priority(score):
    """Determina la prioridad basada en la puntuación"""
    if score < 6:
        return "Alta"
    elif score < 8:
        return "Media"
    else:
        return "Baja"

def render_priority_recommendations(recommendations, priority):
    """Renderiza recomendaciones de una prioridad específica"""
    
    filtered_recs = [rec for rec in recommendations if rec['priority'] == priority]
    
    if not filtered_recs:
        st.info(f"No hay recomendaciones de prioridad {priority.lower()}.")
        return
    
    priority_icons = {"Alta": "🔥", "Media": "📈", "Baja": "🟢"}
    icon = priority_icons.get(priority, "📝")
    
    st.markdown(f"**{icon} Recomendaciones de Prioridad {priority}:**")
    
    for i, rec in enumerate(filtered_recs, 1):
        with st.expander(f"{icon} {rec['phase']} - {rec['text'][:50]}..."):
            st.markdown(f"**Área:** {rec['phase']}")
            st.markdown(f"**Puntuación Actual:** {rec['score']:.1f}/10")
            st.markdown(f"**Recomendación:** {rec['text']}")
            
            # Botones de acción
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ Marcar como Aplicada", key=f"apply_{priority}_{i}"):
                    st.success("✅ Marcada como aplicada")
            
            with col2:
                if st.button("💾 Guardar para Después", key=f"save_{priority}_{i}"):
                    st.info("💾 Guardada en lista pendiente")
            
            with col3:
                if st.button("❌ Descartar", key=f"dismiss_{priority}_{i}"):
                    st.warning("❌ Recomendación descartada")

def render_all_recommendations(suggestions, improvements):
    """Renderiza todas las recomendaciones organizadas"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💡 Sugerencias de Mejora")
        
        if suggestions:
            # Ordenar por puntuación (menor primero = mayor prioridad)
            sorted_suggestions = sorted(suggestions, key=lambda x: x['score'])
            
            for i, sugg in enumerate(sorted_suggestions, 1):
                priority_color = get_priority_color(sugg['priority'])
                st.markdown(f"{i}. {priority_color} **{sugg['phase']}**: {sugg['text']}")
        else:
            st.info("No hay sugerencias disponibles.")
    
    with col2:
        st.markdown("### 🔧 Áreas de Mejora")
        
        if improvements:
            sorted_improvements = sorted(improvements, key=lambda x: x['score'])
            
            for i, imp in enumerate(sorted_improvements, 1):
                priority_color = get_priority_color(imp['priority'])
                st.markdown(f"{i}. {priority_color} **{imp['phase']}**: {imp['text']}")
        else:
            st.info("No hay mejoras específicas identificadas.")
    
    # Plan de acción recomendado
    st.markdown("---")
    st.markdown("### 📅 Plan de Acción Sugerido")
    
    # Generar plan basado en prioridades
    high_priority_items = [item for item in suggestions + improvements if item['priority'] == 'Alta']
    medium_priority_items = [item for item in suggestions + improvements if item['priority'] == 'Media']
    
    if high_priority_items:
        st.markdown("**🔥 Fase 1 - Correcciones Críticas (1-2 días):**")
        for item in high_priority_items[:3]:  # Máximo 3 elementos
            st.markdown(f"- {item['text']}")
    
    if medium_priority_items:
        st.markdown("**📈 Fase 2 - Mejoras Incrementales (3-5 días):**")
        for item in medium_priority_items[:4]:  # Máximo 4 elementos
            st.markdown(f"- {item['text']}")
    
    st.markdown("**🟢 Fase 3 - Pulido Final (tiempo disponible):**")
    st.markdown("- Revisión general de estilo y consistencia")
    st.markdown("- Optimización de descripciones y diálogos")
    st.markdown("- Verificación final de continuidad")

def get_priority_color(priority):
    """Retorna el emoji/color correspondiente a la prioridad"""
    colors = {"Alta": "🔴", "Media": "🟡", "Baja": "🟢"}
    return colors.get(priority, "⚪")

def render_reports_tab():
    """Tab de reportes exportables"""
    st.subheader("📄 Reportes y Exportación")
    
    results = st.session_state.analysis_results
    
    if not results:
        st.info("No hay resultados para generar reportes.")
        return
    
    # Opciones de reporte
    st.markdown("### 📋 Tipos de Reporte Disponibles")
    
    report_types = {
        "Reporte Completo": {
            "description": "Análisis completo con todas las métricas, sugerencias y recomendaciones",
            "format": ["PDF", "DOCX", "HTML"],
            "estimated_pages": "15-20 páginas"
        },
        "Resumen Ejecutivo": {
            "description": "Resumen condensado con puntuaciones principales y top 10 recomendaciones",
            "format": ["PDF", "DOCX"],
            "estimated_pages": "3-5 páginas"
        },
        "Plan de Mejoras": {
            "description": "Lista priorizada de acciones con timeline sugerido",
            "format": ["PDF", "Excel", "CSV"],
            "estimated_pages": "2-3 páginas"
        },
        "Métricas Detalladas": {
            "description": "Gráficos y tablas con todas las métricas numéricas",
            "format": ["Excel", "CSV", "JSON"],
            "estimated_pages": "Datos estructurados"
        }
    }
    
    for report_name, report_info in report_types.items():
        with st.expander(f"📊 {report_name}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Descripción:** {report_info['description']}")
                st.markdown(f"**Extensión:** {report_info['estimated_pages']}")
                st.markdown(f"**Formatos:** {', '.join(report_info['format'])}")
            
            with col2:
                selected_format = st.selectbox(
                    "Formato:",
                    options=report_info['format'],
                    key=f"format_{report_name}"
                )
                
                if st.button(f"📥 Generar {report_name}", key=f"gen_{report_name}"):
                    generate_report(report_name, selected_format, results)
    
    # Opciones avanzadas de exportación
    st.markdown("---")
    st.markdown("### ⚙️ Opciones Avanzadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_manuscript = st.checkbox(
            "Incluir texto del manuscrito",
            value=True,
            help="Incluye el manuscrito original en el reporte"
        )
        
        include_graphs = st.checkbox(
            "Incluir gráficos y visualizaciones",
            value=True,
            help="Incluye gráficos de métricas en el reporte"
        )
    
    with col2:
        anonymize_content = st.checkbox(
            "Anonimizar contenido",
            value=False,
            help="Reemplaza nombres y detalles específicos por marcadores genéricos"
        )
        
        compress_output = st.checkbox(
            "Comprimir archivos de salida",
            value=False,
            help="Crea un archivo ZIP con todos los reportes"
        )
    
    # Programar reportes automáticos
    st.markdown("---")
    st.markdown("### 📅 Reportes Automáticos")
    
    st.info("💡 **Próximamente**: Configura reportes automáticos que se generen después de cada análisis.")
    
    auto_report_settings = {
        "frequency": st.selectbox("Frecuencia:", ["Después de cada análisis", "Diario", "Semanal", "Mensual"], disabled=True),
        "format": st.selectbox("Formato preferido:", ["PDF", "DOCX", "HTML"], disabled=True),
        "email": st.text_input("Email para envío:", placeholder="tu@email.com", disabled=True)
    }
    
    if st.button("💾 Configurar Reportes Automáticos", disabled=True):
        st.info("🚧 Función en desarrollo")

def generate_report(report_name, format_type, results):
    """Simula la generación de un reporte"""
    
    # Simular tiempo de generación
    with st.spinner(f"Generando {report_name} en formato {format_type}..."):
        import time
        time.sleep(2)  # Simular procesamiento
        
        # Información del reporte generado
        file_size = {
            "Reporte Completo": "2.3 MB",
            "Resumen Ejecutivo": "856 KB", 
            "Plan de Mejoras": "234 KB",
            "Métricas Detalladas": "145 KB"
        }.get(report_name, "1 MB")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_name.replace(' ', '_')}_{timestamp}.{format_type.lower()}"
        
        # Simular contenido del reporte
        report_content = generate_report_content(report_name, results)
        
        st.success(f"✅ {report_name} generado exitosamente!")
        
        # Mostrar información del archivo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Archivo", filename)
        
        with col2:
            st.metric("Tamaño", file_size)
        
        with col3:
            st.metric("Páginas", "15" if "Completo" in report_name else "5")
        
        # Botón de descarga simulado
        st.download_button(
            label=f"📥 Descargar {report_name}",
            data=report_content,
            file_name=filename,
            mime=get_mime_type(format_type)
        )

def generate_report_content(report_name, results):
    """Genera el contenido del reporte"""
    
    content = f"""
# {report_name}
Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Resumen Ejecutivo
Este reporte contiene el análisis detallado del manuscrito procesado por el Sistema Multi-Agente.

### Puntuaciones Principales:
"""
    
    for phase_id, phase_data in results.items():
        phase_name = phase_id.replace('_', ' ').title()
        score = phase_data.get('score', 0)
        content += f"- {phase_name}: {score:.1f}/10\n"
    
    content += "\n### Sugerencias Principales:\n"
    
    for phase_id, phase_data in results.items():
        suggestions = phase_data.get('suggestions', [])
        if suggestions:
            content += f"\n#### {phase_id.replace('_', ' ').title()}:\n"
            for sugg in suggestions[:3]:  # Top 3 por fase
                content += f"- {sugg}\n"
    
    content += f"""

---
Generado por Sistema Multi-Agente para Novelas v1.0
Fecha: {datetime.now().strftime('%d/%m/%Y')}
"""
    
    return content

def get_mime_type(format_type):
    """Retorna el tipo MIME según el formato"""
    mime_types = {
        "PDF": "application/pdf",
        "DOCX": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "HTML": "text/html",
        "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "CSV": "text/csv",
        "JSON": "application/json"
    }
    return mime_types.get(format_type, "text/plain")import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

def render_results_page():
    """Renderiza la página de visualización de resultados"""
    
    st.header("📊 Resultados del Análisis")
    st.markdown("*Visualiza y explora los resultados del procesamiento de tu manuscrito*")
    
    # Verificar si hay resultados disponibles
    if not st.session_state.analysis_results:
        st.info("📭 No hay resultados de análisis disponibles. Ve al **Editor de Manuscrito** y procesa tu manuscrito primero.")
        
        # Botón para generar resultados de demostración
        if st.button("🎭 Generar Resultados de Demostración"):
            generate_demo_results()
            st.rerun()
        
        return
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Resumen General",
        "🔍 Análisis Detallado", 
        "📊 Métricas y Gráficos",
        "💡 Recomendaciones",
        "📄 Reportes"
    ])
    
    with tab1:
        render_summary_tab()
    
    with tab2:
        render_detailed_analysis_tab()
    
    with tab3:
        render_metrics_tab()
    
    with tab4:
        render_recommendations_tab()
    
    with tab5:
        render_reports_tab()

def generate_demo_results():
    """Genera resultados de demostración"""
    demo_manuscript = """
    En el reino de Aethermoor, donde la magia fluye como ríos de luz dorada a través de cristales ancestrales, 
    la joven maga Lyra Stormwind descubrió que su destino estaba escrito en runas que solo ella podía leer.
    
    El día que encontró el grimorio perdido de Arcanum Infinitus en las ruinas de la Torre de Marfil, 
    no sabía que estaba por desencadenar una guerra que cambiaría para siempre el equilibrio entre 
    la luz y las sombras del mundo conocido.
    """
    
    st.session_state.manuscript = demo_manuscript
    
    # Generar resultados simulados
    st.session_state.analysis_results = {
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
            ],
            "details": {
                "consistency_score": 9.1,
                "creativity_score": 7.8,
                "originality_score": 8.5,
                "depth_score": 7.6
            }
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
            ],
            "details": {
                "development_score": 7.2,
                "complexity_score": 6.8,
                "relatability_score": 8.1,
                "growth_potential": 8.7
            }
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
            ],
            "details": {
                "structure_score": 8.9,
                "pacing_score": 7.8,
                "conflict_score": 8.5,
                "resolution_potential": 9.2
            }
        }
    }

def render_summary_tab():
    """Tab de resumen general"""
    st.subheader("📈 Resumen General del Análisis")
    
    # Métricas principales
    results = st.session_state.analysis_results
    
    # Calcular score promedio
    scores = [phase.get('score', 0) for phase in results.values()]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Contar sugerencias totales
    total_suggestions = sum(len(phase.get('suggestions', [])) for phase in results.values())
    
    # Contar fortalezas y mejoras
    total_strengths = sum(len(phase.get('strengths', [])) for phase in results.values())
    total_improvements = sum(len(phase.get('improvements', [])) for phase in results.values())
    
    # Mostrar métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = "🟢" if avg_score >= 8 else "🟡" if avg_score >= 6 else "🔴"
        st.metric("Puntuación General", f"{avg_score:.1f}/10", help="Promedio de todas las fases analizadas")
        st.markdown(f"<center>{score_color}</center>", unsafe_allow_html=True)
    
    with col2:
        st.metric("Total Sugerencias", total_suggestions, help="Sugerencias de mejora generadas")
    
    with col3:
        st.metric("Fortalezas Identificadas", total_strengths, help="Aspectos positivos encontrados")
    
    with col4:
        st.metric("Áreas de Mejora", total_improvements, help="Aspectos a mejorar identificados")
    
    # Gráfico de puntuaciones por fase
    st.markdown("---")
    st.subheader("📊 Puntuaciones por Fase")
    
    if results:
        phase_names = []
        phase_scores = []
        phase_colors = []
        
        for phase_id, phase_data in results.items():
            score = phase_data.get('score', 0)
            phase_names.append(phase_id.replace('_', ' ').title())
            phase_scores.append(score)
            
            # Color según puntuación
            if score >= 8:
                phase_colors.append('#2E8B57')  # Verde
            elif score >= 6:
                phase_colors.append('#FFD700')  # Amarillo
            else:
                phase_colors.append('#DC143C')  # Rojo
        
        # Crear gráfico de barras
        fig = go.Figure([go.Bar(
            x=phase_names,
            y=phase_scores,
            marker_color=phase_colors,
            text=[f"{score:.1f}" for score in phase_scores],
            textposition='auto',
        )])
        
        fig.update_layout(
            title="Puntuación por Fase de Análisis",
            yaxis_title="Puntuación (0-10)",
            yaxis=dict(range=[0, 10]),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Estado del manuscrito
    st.markdown("---")
    st.subheader("📝 Estado del Manuscrito")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.manuscript:
            word_count = len(st.session_state.manuscript.split())
            char_count = len(st.session_state.manuscript)
            paragraph_count = len([p for p in st.session_state.manuscript.split('\n\n') if p.strip()])
            
            st.markdown("**📊 Estadísticas del Texto:**")
            st.markdown(f"- **Palabras:** {word_count:,}")