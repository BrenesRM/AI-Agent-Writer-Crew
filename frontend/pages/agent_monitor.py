# -*- coding: utf-8 -*-
import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

def render_performance_tab(agent_manager):
    """Tab de rendimiento y metricas"""
    st.subheader("📊 Rendimiento de Agentes")
    
    # Metricas de rendimiento general
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Throughput Promedio",
            "12.3 tareas/min",
            delta="2.1",
            help="Tareas completadas por minuto en promedio"
        )
    
    with col2:
        st.metric(
            "Tiempo de Respuesta",
            "1.8s",
            delta="-0.3s",
            help="Tiempo promedio de respuesta de los agentes"
        )
    
    with col3:
        st.metric(
            "Tasa de Exito Global",
            "95.7%",
            delta="1.2%",
            help="Porcentaje de tareas completadas exitosamente"
        )
    
    # Graficos de rendimiento
    st.markdown("---")
    
    # Grafico de rendimiento por agente
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Rendimiento por Agente")
        
        # Datos simulados para el grafico
        performance_data = {
            'Agente': ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor', 'Visualizer'],
            'Tareas Completadas': [45, 38, 52, 41, 29],
            'Tasa de Exito (%)': [96.2, 94.8, 97.5, 93.1, 91.7]
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        # Grafico de barras
        fig = px.bar(
            df_perf, 
            x='Agente', 
            y='Tareas Completadas',
            title="Tareas Completadas por Agente",
            color='Tasa de Exito (%)',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Tasa de Exito")
        
        # Grafico de dona
        fig = go.Figure(data=[go.Pie(
            labels=performance_data['Agente'],
            values=performance_data['Tasa de Exito (%)'],
            hole=.3,
            textinfo="label+percent",
            textposition="inside"
        )])
        
        fig.update_layout(
            title="Distribucion de Tasa de Exito",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Metricas temporales
    st.markdown("---")
    st.subheader("⏱️ Analisis Temporal")
    
    # Grafico de lineas temporal
    import numpy as np
    
    # Generar datos temporales simulados
    time_range = pd.date_range(start='2025-01-01', periods=30, freq='D')
    agents_data = {}
    
    for agent in ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor']:
        # Datos simulados con tendencia y ruido
        base_trend = np.linspace(10, 25, 30)
        noise = np.random.normal(0, 2, 30)
        agents_data[agent] = np.maximum(0, base_trend + noise)
    
    # Crear DataFrame temporal
    df_temporal = pd.DataFrame(agents_data, index=time_range)
    
    # Grafico de lineas
    fig = go.Figure()
    
    for agent in df_temporal.columns:
        fig.add_trace(go.Scatter(
            x=df_temporal.index,
            y=df_temporal[agent],
            mode='lines+markers',
            name=agent,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title="Actividad de Agentes en el Tiempo (Ultimos 30 dias)",
        xaxis_title="Fecha",
        yaxis_title="Tareas por Dia",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de estadisticas detalladas
    st.markdown("---")
    st.subheader("📋 Estadisticas Detalladas")
    
    detailed_stats = pd.DataFrame({
        'Agente': ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor', 'Visualizer'],
        'Tareas Totales': [245, 198, 312, 223, 156],
        'Tareas Exitosas': [236, 188, 304, 208, 143],
        'Tiempo Promedio (s)': [2.1, 3.4, 1.8, 4.2, 2.7],
        'Memoria Usada (MB)': [45, 67, 38, 72, 51],
        'CPU Promedio (%)': [12.3, 18.7, 9.4, 22.1, 14.8],
        'Ultima Optimizacion': ['2h ago', '1h ago', '3h ago', '30min ago', '45min ago']
    })
    
    st.dataframe(detailed_stats, use_container_width=True)
    
    # Alertas y recomendaciones
    st.markdown("---")
    st.subheader("⚠️ Alertas y Recomendaciones")
    
    # Alertas simuladas
    alerts = [
        {'type': 'warning', 'agent': 'Style Editor', 'message': 'Tiempo de respuesta por encima del promedio (4.2s vs 2.5s esperado)'},
        {'type': 'info', 'agent': 'Visualizer', 'message': 'Rendimiento estable, considerar aumentar carga de trabajo'},
        {'type': 'success', 'agent': 'Plot Weaver', 'message': 'Excelente rendimiento - 97.5% de exito'},
    ]
    
    for alert in alerts:
        if alert['type'] == 'warning':
            st.warning(f"⚠️ **{alert['agent']}**: {alert['message']}")
        elif alert['type'] == 'info':
            st.info(f"ℹ️ **{alert['agent']}**: {alert['message']}")
        elif alert['type'] == 'success':
            st.success(f"✅ **{alert['agent']}**: {alert['message']}")

def render_realtime_tab(agent_manager):
    """Tab de actividad en tiempo real"""
    st.subheader("📈 Actividad en Tiempo Real")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-actualizar cada 5 segundos", value=False)
    
    if auto_refresh:
        # Placeholder para auto-refresh
        placeholder = st.empty()
        
        # Simulacion de datos en tiempo real
        with placeholder.container():
            render_realtime_content()
        
        # Auto-refresh (en una implementacion real, usar st.rerun() con timer)
        time.sleep(5)
    else:
        render_realtime_content()

def render_realtime_content():
    """Contenido de la actividad en tiempo real"""
    
    # Dashboard en tiempo real
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Agentes Activos Ahora", "3/11", delta="1")
    
    with col2:
        st.metric("Tareas en Cola", "7", delta="-2")
    
    with col3:
        st.metric("CPU Total", "23.4%", delta="5.1%")
    
    with col4:
        st.metric("Memoria Total", "342 MB", delta="15 MB")
    
    # Log de actividad en tiempo real
    st.markdown("---")
    st.subheader("📜 Log de Actividad")
    
    # Simular log en tiempo real
    activity_log = [
        {'timestamp': '14:35:23', 'agent': 'Character Developer', 'action': 'Analisis de personaje completado', 'status': 'success'},
        {'timestamp': '14:35:18', 'agent': 'Plot Weaver', 'action': 'Iniciando analisis de estructura narrativa', 'status': 'info'},
        {'timestamp': '14:35:12', 'agent': 'Lorekeeper', 'action': 'Consulta RAG exitosa - 5 documentos encontrados', 'status': 'success'},
        {'timestamp': '14:35:08', 'agent': 'Style Editor', 'action': 'Procesando mejoras de estilo', 'status': 'processing'},
        {'timestamp': '14:35:03', 'agent': 'Visualizer', 'action': 'Generando prompt visual para escena 1', 'status': 'processing'},
        {'timestamp': '14:34:58', 'agent': 'Proofreader', 'action': 'Correccion ortografica completada', 'status': 'success'},
        {'timestamp': '14:34:52', 'agent': 'Innovation Scout', 'action': 'Identificadas 3 oportunidades creativas', 'status': 'success'},
        {'timestamp': '14:34:47', 'agent': 'Beta Reader', 'action': 'Simulacion de feedback de lector', 'status': 'processing'},
    ]
    
    # Contenedor con scroll para el log
    log_container = st.container()
    with log_container:
        for entry in activity_log:
            status_color = {
                'success': 'success',
                'processing': 'warning', 
                'info': 'info',
                'error': 'error'
            }.get(entry['status'], 'info')
            
            status_icon = {
                'success': '✅',
                'processing': '🔄',
                'info': 'ℹ️',
                'error': '❌'
            }.get(entry['status'], 'ℹ️')
            
            if status_color == 'success':
                st.success(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
            elif status_color == 'warning':
                st.warning(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
            elif status_color == 'error':
                st.error(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
            else:
                st.info(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
    
    # Grafico de actividad en tiempo real
    st.markdown("---")
    st.subheader("📊 Actividad por Minuto")
    
    # Generar datos simulados para grafico en tiempo real
    import random
    
    minutes = [f"14:{30+i:02d}" for i in range(10)]
    activity_counts = [random.randint(2, 12) for _ in range(10)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=minutes,
        y=activity_counts,
        mode='lines+markers',
        name='Actividad',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Actividad de Agentes (Ultimos 10 minutos)",
        xaxis_title="Tiempo",
        yaxis_title="Acciones por Minuto",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Botones de control
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualizar Datos"):
            st.rerun()
    
    with col2:
        if st.button("📋 Exportar Log"):
            # Simular exportacion
            st.success("📄 Log exportado a activity_log.csv")
    
    with col3:
        if st.button("🧹 Limpiar Log"):
            # Simular limpieza
            st.success("🗑️ Log limpiado exitosamente")

def render_advanced_config_tab(agent_manager):
    """Tab de configuracion avanzada"""
    st.subheader("⚙️ Configuracion Avanzada de Agentes")
    
    st.warning("⚠️ **Advertencia**: Los cambios en esta seccion pueden afectar el rendimiento del sistema.")
    
    # Configuracion global
    st.markdown("### 🌐 Configuracion Global")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_concurrent_agents = st.slider(
            "Maximo agentes concurrentes:",
            min_value=1,
            max_value=11,
            value=5,
            help="Numero maximo de agentes que pueden ejecutarse simultaneamente"
        )
        
        timeout_seconds = st.slider(
            "Timeout por tarea (segundos):",
            min_value=10,
            max_value=300,
            value=60,
            help="Tiempo maximo antes de cancelar una tarea"
        )
    
    with col2:
        memory_limit_mb = st.slider(
            "Limite de memoria por agente (MB):",
            min_value=50,
            max_value=500,
            value=150,
            help="Limite de memoria RAM por agente"
        )
        
        retry_attempts = st.slider(
            "Intentos de reintento:",
            min_value=0,
            max_value=5,
            value=2,
            help="Numero de reintentos en caso de error"
        )
    
    # Configuracion por agente
    st.markdown("---")
    st.markdown("### 🤖 Configuracion por Agente")
    
    # Selector de agente para configurar
    agents_list = ['LorekeeperAgent', 'CharacterDeveloperAgent', 'PlotWeaverAgent', 
                   'StyleEditorAgent', 'VisualizerAgent']
    
    selected_agent_config = st.selectbox(
        "Selecciona agente para configurar:",
        options=agents_list
    )
    
    if selected_agent_config:
        st.markdown(f"**Configurando: {selected_agent_config}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            agent_enabled = st.checkbox(f"Habilitar {selected_agent_config}", value=True)
            agent_priority = st.selectbox(
                "Prioridad:",
                options=['Baja', 'Normal', 'Alta', 'Critica'],
                index=1
            )
        
        with col2:
            agent_temperature = st.slider(
                "Temperatura (creatividad):",
                min_value=0.1,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="Controla la creatividad del agente"
            )
            
            agent_max_tokens = st.slider(
                "Maximo tokens de respuesta:",
                min_value=100,
                max_value=4000,
                value=1000,
                help="Longitud maxima de las respuestas"
            )
        
        with col3:
            agent_frequency_penalty = st.slider(
                "Penalizacion por frecuencia:",
                min_value=0.0,
                max_value=2.0,
                value=0.5,
                step=0.1,
                help="Reduce repeticion de palabras"
            )
            
            agent_presence_penalty = st.slider(
                "Penalizacion por presencia:",
                min_value=0.0,
                max_value=2.0,
                value=0.3,
                step=0.1,
                help="Fomenta temas nuevos"
            )
    
    # Configuracion de herramientas
    st.markdown("---")
    st.markdown("### 🛠️ Configuracion de Herramientas")
    
    tools_config = {
        'RAG Tool': {
            'enabled': st.checkbox('RAG Tool', value=True),
            'similarity_threshold': st.slider('Umbral de similitud RAG:', 0.0, 1.0, 0.7, key='rag_sim')
        },
        'Writing Analyzer': {
            'enabled': st.checkbox('Writing Analyzer', value=True),
            'complexity_level': st.selectbox('Nivel de complejidad analisis:', ['Basico', 'Intermedio', 'Avanzado'], key='write_complex')
        },
        'Character Analyzer': {
            'enabled': st.checkbox('Character Analyzer', value=True),
            'depth_analysis': st.checkbox('Analisis profundo de personajes', value=True, key='char_depth')
        }
    }
    
    # Monitoreo y alertas
    st.markdown("---")
    st.markdown("### 📊 Monitoreo y Alertas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_performance_monitoring = st.checkbox(
            "Habilitar monitoreo de rendimiento",
            value=True,
            help="Registra metricas de rendimiento de cada agente"
        )
        
        performance_alert_threshold = st.slider(
            "Umbral de alerta de rendimiento (%):",
            min_value=50,
            max_value=95,
            value=80,
            help="Porcentaje de exito minimo antes de generar alerta"
        )
    
    with col2:
        enable_error_notifications = st.checkbox(
            "Notificaciones de error",
            value=True,
            help="Envia notificaciones cuando ocurren errores"
        )
        
        log_level = st.selectbox(
            "Nivel de logging:",
            options=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            index=1,
            help="Nivel de detalle en los logs"
        )
    
    # Botones de accion
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Guardar Configuracion", type="primary"):
            # Simular guardado de configuracion
            config_data = {
                'max_concurrent_agents': max_concurrent_agents,
                'timeout_seconds': timeout_seconds,
                'memory_limit_mb': memory_limit_mb,
                'retry_attempts': retry_attempts,
                'selected_agent_config': selected_agent_config,
                'tools_config': tools_config,
                'monitoring': {
                    'enabled': enable_performance_monitoring,
                    'alert_threshold': performance_alert_threshold,
                    'error_notifications': enable_error_notifications,
                    'log_level': log_level
                }
            }
            
            # Guardar en session state
            st.session_state.agent_config = config_data
            st.success("✅ Configuracion guardada exitosamente")
    
    with col2:
        if st.button("🔄 Restablecer por Defecto"):
            if st.confirm("¿Restablecer toda la configuracion a valores por defecto?"):
                # Limpiar configuracion
                if 'agent_config' in st.session_state:
                    del st.session_state.agent_config
                st.success("🔄 Configuracion restablecida")
                st.rerun()
    
    with col3:
        if st.button("📤 Exportar Configuracion"):
            # Simular exportacion
            st.success("📄 Configuracion exportada a config.json")
    
    with col4:
        if st.button("📥 Importar Configuracion"):
            uploaded_config = st.file_uploader(
                "Selecciona archivo de configuracion:",
                type=['json'],
                key="config_upload"
            )
            if uploaded_config:
                st.success("📥 Configuracion importada exitosamente")_monitor_page(agent_manager):
    """Renderiza la pagina de monitoreo de agentes"""
    
    st.header("🤖 Monitor de Agentes")
    st.markdown("*Supervisa el rendimiento y actividad de los agentes especializados*")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Estado de Agentes",
        "📊 Rendimiento",
        "📈 Actividad en Tiempo Real",
        "⚙️ Configuracion Avanzada"
    ])
    
    with tab1:
        render_agents_status_tab(agent_manager)
    
    with tab2:
        render_performance_tab(agent_manager)
    
    with tab3:
        render_realtime_tab(agent_manager)
    
    with tab4:
        render_advanced_config_tab(agent_manager)

def render_agents_status_tab(agent_manager):
    """Tab de estado de los agentes"""
    st.subheader("👥 Estado de los Agentes")
    
    # Obtener informacion de agentes
    try:
        agents = agent_manager.list_agents()
        
        # Metricas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Agentes", len(agents))
        
        with col2:
            active_agents = sum(1 for agent in agents if agent.get('status') == 'active')
            st.metric("Agentes Activos", active_agents)
        
        with col3:
            idle_agents = sum(1 for agent in agents if agent.get('status') == 'idle')
            st.metric("Agentes Inactivos", idle_agents)
        
        with col4:
            total_tasks = sum(agent.get('tasks_completed', 0) for agent in agents)
            st.metric("Tareas Completadas", total_tasks)
        
        st.markdown("---")
        
        # Lista detallada de agentes
        st.subheader("📋 Detalle de Agentes")
        
        # Crear DataFrame para mejor visualizacion
        agents_data = []
        for agent in agents:
            agents_data.append({
                'Nombre': agent['name'],
                'Especialidad': agent['role'],
                'Estado': get_status_emoji(agent.get('status', 'idle')) + ' ' + agent.get('status', 'idle').title(),
                'Ultima Actividad': agent.get('last_activity', 'Nunca'),
                'Tareas': agent.get('tasks_completed', 0),
                'Tiempo Activo': agent.get('active_time', '0m'),
                'Exito Rate': f"{agent.get('success_rate', 95):.1f}%"
            })
        
        df = pd.DataFrame(agents_data)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filtrar por estado:",
                options=['Active', 'Idle', 'Processing', 'Error'],
                default=['Active', 'Processing']
            )
        
        with col2:
            specialty_filter = st.multiselect(
                "Filtrar por especialidad:",
                options=df['Especialidad'].unique(),
                default=df['Especialidad'].unique()
            )
        
        # Aplicar filtros
        if status_filter:
            df = df[df['Estado'].str.contains('|'.join(status_filter))]
        if specialty_filter:
            df = df[df['Especialidad'].isin(specialty_filter)]
        
        # Mostrar tabla
        st.dataframe(df, use_container_width=True)
        
        # Cards de agentes individuales
        st.markdown("---")
        st.subheader("🔍 Vista Detallada de Agentes")
        
        # Selector de agente
        selected_agent = st.selectbox(
            "Selecciona un agente para ver detalles:",
            options=[agent['name'] for agent in agents]
        )
        
        if selected_agent:
            agent_info = next(agent for agent in agents if agent['name'] == selected_agent)
            render_agent_detail_card(agent_info)
    
    except Exception as e:
        st.error(f"❌ Error obteniendo informacion de agentes: {str(e)}")
        
        # Mostrar informacion simulada
        st.info("📊 Mostrando datos simulados para demostracion")
        render_simulated_agents_data()

def get_status_emoji(status):
    """Retorna emoji basado en el estado del agente"""
    status_map = {
        'active': '🟢',
        'idle': '⚪',
        'processing': '🟡',
        'error': '🔴',
        'maintenance': '🟠'
    }
    return status_map.get(status.lower(), '⚪')

def render_agent_detail_card(agent_info):
    """Renderiza card detallado de un agente especifico"""
    
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">{get_status_emoji(agent_info.get('status', 'idle'))} {agent_info['name']}</h3>
            <p style="margin: 0.5rem 0;"><strong>Especialidad:</strong> {agent_info['role']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metricas del agente
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tareas Completadas", agent_info.get('tasks_completed', 0))
        
        with col2:
            st.metric("Tasa de Exito", f"{agent_info.get('success_rate', 95):.1f}%")
        
        with col3:
            st.metric("Tiempo Activo", agent_info.get('active_time', '0m'))
        
        with col4:
            avg_time = agent_info.get('avg_task_time', '2.3s')
            st.metric("Tiempo Promedio/Tarea", avg_time)
        
        # Capacidades y herramientas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🛠️ Herramientas Disponibles:**")
            tools = agent_info.get('tools', ['RAG Tool', 'Analysis Tool', 'Writing Tool'])
            for tool in tools:
                st.markdown(f"- {tool}")
        
        with col2:
            st.markdown("**🎯 Capacidades Principales:**")
            capabilities = agent_info.get('capabilities', [
                'Analisis de texto',
                'Generacion de sugerencias',
                'Evaluacion de calidad'
            ])
            for cap in capabilities:
                st.markdown(f"- {cap}")
        
        # Historial reciente
        st.markdown("**📜 Actividad Reciente:**")
        recent_activity = agent_info.get('recent_activity', [
            {'time': '10:30', 'action': 'Analisis de personajes completado', 'status': 'success'},
            {'time': '10:25', 'action': 'Iniciado analisis de manuscrito', 'status': 'info'},
            {'time': '10:20', 'action': 'Herramientas actualizadas', 'status': 'info'}
        ])
        
        for activity in recent_activity:
            status_icon = {
                'success': '✅',
                'info': 'ℹ️', 
                'warning': '⚠️',
                'error': '❌'
            }.get(activity['status'], 'ℹ️')
            
            st.markdown(f"`{activity['time']}` {status_icon} {activity['action']}")

def render_simulated_agents_data():
    """Renderiza datos simulados de agentes"""
    
    simulated_agents = [
        {
            'name': 'LorekeeperAgent',
            'role': 'Guardian del Conocimiento',
            'status': 'active',
            'last_activity': '2 min ago',
            'tasks_completed': 23,
            'active_time': '45m',
            'success_rate': 96.2,
            'tools': ['RAG Tool', 'Consistency Checker', 'Research Tool'],
            'capabilities': ['Verificacion de lore', 'Consulta de documentos', 'Analisis de consistencia']
        },
        {
            'name': 'CharacterDeveloperAgent',
            'role': 'Arquitecto de Personajes',
            'status': 'processing',
            'last_activity': 'Activo',
            'tasks_completed': 18,
            'active_time': '32m',
            'success_rate': 94.8,
            'tools': ['Character Analyzer', 'Idea Generator', 'Writing Analyzer'],
            'capabilities': ['Analisis de personajes', 'Desarrollo de arcos', 'Generacion de ideas']
        },
        {
            'name': 'PlotWeaverAgent',
            'role': 'Maestro de la Narrativa',
            'status': 'idle',
            'last_activity': '15 min ago',
            'tasks_completed': 31,
            'active_time': '67m',
            'success_rate': 97.5,
            'tools': ['Plot Analyzer', 'Pacing Analyzer', 'Structure Tool'],
            'capabilities': ['Analisis de trama', 'Optimizacion de estructura', 'Control de ritmo']
        }
    ]
    
    # Mostrar como cards
    for agent in simulated_agents:
        render_agent_detail_card(agent)

def render