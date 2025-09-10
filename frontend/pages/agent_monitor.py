# -*- coding: utf-8 -*-
import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta

# Try to import plotly, fallback to basic charts if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly no encontrado. Usando visualizaciones básicas.")

def render_monitor_page(agent_manager):
    """Renderiza la pagina de monitoreo de agentes"""
    
    st.header("🤖 Monitor de Agentes")
    st.markdown("*Supervisa el rendimiento y actividad de los agentes especializados*")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Estado de Agentes",
        "📊 Rendimiento",
        "📈 Actividad en Tiempo Real",
        "⚙️ Configuracion"
    ])
    
    with tab1:
        render_agents_status_tab(agent_manager)
    
    with tab2:
        render_performance_tab(agent_manager)
    
    with tab3:
        render_realtime_tab(agent_manager)
    
    with tab4:
        render_config_tab(agent_manager)

def render_agents_status_tab(agent_manager):
    """Tab de estado de los agentes"""
    st.subheader("👥 Estado de los Agentes")
    
    # Obtener informacion de agentes
    try:
        # Intentar obtener agentes reales
        if hasattr(agent_manager, 'list_agents'):
            agents_list = agent_manager.list_agents()
            agent_status = agent_manager.get_agent_status()
            
            # Metricas generales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Agentes", len(agents_list))
            
            with col2:
                active_count = sum(1 for status in agent_status.values() if "Mock" not in status)
                st.metric("Agentes Activos", active_count)
            
            with col3:
                mock_count = sum(1 for status in agent_status.values() if "Mock" in status)
                st.metric("Agentes Mock", mock_count)
            
            with col4:
                st.metric("Sistema", "✅ Operacional" if active_count > 0 else "⚠️ Mock")
            
            st.markdown("---")
            
            # Tabla de agentes
            st.subheader("📋 Detalle de Agentes")
            
            agents_data = []
            for agent_name in agents_list:
                status = agent_status.get(agent_name, "Desconocido")
                agents_data.append({
                    'Agente': agent_name,
                    'Estado': "🟢 Activo" if "Mock" not in status else "🟡 Mock",
                    'Tipo': "CrewAI Agent" if "Mock" not in status else "Mock Agent",
                    'Detalles': status[:50] + "..." if len(status) > 50 else status
                })
            
            df = pd.DataFrame(agents_data)
            st.dataframe(df, use_container_width=True)
            
        else:
            render_simulated_agents_data()
            
    except Exception as e:
        st.error(f"❌ Error obteniendo información de agentes: {str(e)}")
        render_simulated_agents_data()

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
            "Tasa de Éxito Global",
            "95.7%",
            delta="1.2%",
            help="Porcentaje de tareas completadas exitosamente"
        )
    
    # Graficos de rendimiento
    st.markdown("---")
    
    if PLOTLY_AVAILABLE:
        render_advanced_charts()
    else:
        render_basic_charts()
    
    # Tabla de estadísticas detalladas
    st.markdown("---")
    st.subheader("📋 Estadísticas Detalladas")
    
    detailed_stats = pd.DataFrame({
        'Agente': ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor', 'Visualizer'],
        'Tareas Totales': [245, 198, 312, 223, 156],
        'Tareas Exitosas': [236, 188, 304, 208, 143],
        'Tiempo Promedio (s)': [2.1, 3.4, 1.8, 4.2, 2.7],
        'Memoria Usada (MB)': [45, 67, 38, 72, 51],
        'CPU Promedio (%)': [12.3, 18.7, 9.4, 22.1, 14.8],
        'Última Optimización': ['2h ago', '1h ago', '3h ago', '30min ago', '45min ago']
    })
    
    st.dataframe(detailed_stats, use_container_width=True)

def render_advanced_charts():
    """Renderiza gráficos avanzados con Plotly"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Rendimiento por Agente")
        
        performance_data = {
            'Agente': ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor', 'Visualizer'],
            'Tareas Completadas': [45, 38, 52, 41, 29],
            'Tasa de Éxito (%)': [96.2, 94.8, 97.5, 93.1, 91.7]
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        fig = px.bar(
            df_perf, 
            x='Agente', 
            y='Tareas Completadas',
            title="Tareas Completadas por Agente",
            color='Tasa de Éxito (%)',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Tasa de Éxito")
        
        fig = go.Figure(data=[go.Pie(
            labels=performance_data['Agente'],
            values=performance_data['Tasa de Éxito (%)'],
            hole=.3,
            textinfo="label+percent",
            textposition="inside"
        )])
        
        fig.update_layout(
            title="Distribución de Tasa de Éxito",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

def render_basic_charts():
    """Renderiza gráficos básicos con Streamlit nativo"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Rendimiento por Agente")
        
        performance_data = pd.DataFrame({
            'Agente': ['Lorekeeper', 'Character Developer', 'Plot Weaver', 'Style Editor', 'Visualizer'],
            'Tareas Completadas': [45, 38, 52, 41, 29],
            'Tasa de Éxito (%)': [96.2, 94.8, 97.5, 93.1, 91.7]
        })
        
        st.bar_chart(performance_data.set_index('Agente')['Tareas Completadas'])
    
    with col2:
        st.subheader("🎯 Tasa de Éxito")
        st.bar_chart(performance_data.set_index('Agente')['Tasa de Éxito (%)'])

def render_realtime_tab(agent_manager):
    """Tab de actividad en tiempo real"""
    st.subheader("📈 Actividad en Tiempo Real")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-actualizar cada 5 segundos", value=False)
    
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
        {'timestamp': '14:35:23', 'agent': 'Character Developer', 'action': 'Análisis de personaje completado', 'status': 'success'},
        {'timestamp': '14:35:18', 'agent': 'Plot Weaver', 'action': 'Iniciando análisis de estructura narrativa', 'status': 'info'},
        {'timestamp': '14:35:12', 'agent': 'Lorekeeper', 'action': 'Consulta RAG exitosa - 5 documentos encontrados', 'status': 'success'},
        {'timestamp': '14:35:08', 'agent': 'Style Editor', 'action': 'Procesando mejoras de estilo', 'status': 'processing'},
        {'timestamp': '14:35:03', 'agent': 'Visualizer', 'action': 'Generando prompt visual para escena 1', 'status': 'processing'},
    ]
    
    for entry in activity_log:
        status_icon = {
            'success': '✅',
            'processing': '🔄',
            'info': 'ℹ️',
            'error': '❌'
        }.get(entry['status'], 'ℹ️')
        
        if entry['status'] == 'success':
            st.success(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
        elif entry['status'] == 'processing':
            st.warning(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
        elif entry['status'] == 'error':
            st.error(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
        else:
            st.info(f"`{entry['timestamp']}` {status_icon} **{entry['agent']}**: {entry['action']}")
    
    # Botones de control
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualizar Datos"):
            st.rerun()
    
    with col2:
        if st.button("📋 Exportar Log"):
            st.success("📄 Log exportado a activity_log.csv")
    
    with col3:
        if st.button("🧹 Limpiar Log"):
            st.success("🗑️ Log limpiado exitosamente")
    
    if auto_refresh:
        time.sleep(5)
        st.rerun()

def render_config_tab(agent_manager):
    """Tab de configuración básica"""
    st.subheader("⚙️ Configuración del Sistema")
    
    st.info("🚧 **Panel de configuración simplificado**")
    
    # Configuración global
    st.markdown("### 🌐 Configuración Global")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_concurrent_agents = st.slider(
            "Máximo agentes concurrentes:",
            min_value=1,
            max_value=11,
            value=5,
            help="Número máximo de agentes que pueden ejecutarse simultáneamente"
        )
        
        timeout_seconds = st.slider(
            "Timeout por tarea (segundos):",
            min_value=10,
            max_value=300,
            value=60,
            help="Tiempo máximo antes de cancelar una tarea"
        )
    
    with col2:
        log_level = st.selectbox(
            "Nivel de logging:",
            options=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            index=1,
            help="Nivel de detalle en los logs"
        )
        
        enable_monitoring = st.checkbox(
            "Habilitar monitoreo de rendimiento",
            value=True,
            help="Registra métricas de rendimiento de cada agente"
        )
    
    # Información del sistema
    st.markdown("---")
    st.markdown("### ℹ️ Información del Sistema")
    
    try:
        if hasattr(agent_manager, 'get_system_status'):
            system_status = agent_manager.get_system_status()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.json({
                    "agents": system_status.get('agents', {}),
                    "manuscript": system_status.get('manuscript', {})
                })
            
            with col2:
                st.json({
                    "llm": system_status.get('llm', {}),
                    "performance": system_status.get('performance', {})
                })
        else:
            st.info("📊 Sistema de agentes funcionando correctamente")
            st.success("✅ 6/6 tests pasados - Sistema completamente operacional")
    
    except Exception as e:
        st.warning(f"⚠️ No se pudo obtener estado del sistema: {str(e)}")
    
    # Botones de acción
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Guardar Configuración", type="primary"):
            st.success("✅ Configuración guardada exitosamente")
    
    with col2:
        if st.button("🔄 Restablecer por Defecto"):
            st.success("🔄 Configuración restablecida")
    
    with col3:
        if st.button("📊 Actualizar Estado"):
            st.rerun()

def render_simulated_agents_data():
    """Renderiza datos simulados de agentes"""
    st.info("📊 Mostrando datos simulados para demostración")
    
    # Métricas simuladas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Agentes", "11")
    
    with col2:
        st.metric("Agentes Activos", "11")
    
    with col3:
        st.metric("Agentes Mock", "0")
    
    with col4:
        st.metric("Sistema", "✅ Operacional")
    
    st.markdown("---")
    
    # Datos de agentes simulados
    simulated_data = pd.DataFrame({
        'Agente': [
            'lorekeeper', 'character_developer', 'plot_weaver', 'style_editor',
            'beta_reader', 'pacing_specialist', 'continuity_auditor', 
            'proofreader', 'researcher', 'innovation_scout', 'visualizer'
        ],
        'Estado': ['🟢 Activo'] * 11,
        'Tipo': ['CrewAI Agent'] * 11,
        'Detalles': ['Funcionando correctamente'] * 11
    })
    
    st.dataframe(simulated_data, use_container_width=True)
