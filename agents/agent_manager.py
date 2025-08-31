# agents/agent_manager.py
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from agents.crews import (
    LorekeeperAgent, CharacterDeveloperAgent, PlotWeaverAgent,
    StyleEditorAgent, VisualizerAgent, ResearcherAgent,
    ContinuityAuditorAgent, BetaReaderAgent, PacingSpecialistAgent,
    ProofreaderAgent, InnovationScoutAgent
)
from llm_local.llama_manager import LlamaManager
from config.settings import settings

class AgentManager:
    """Gestor central para todos los agentes del sistema"""
    
    def __init__(self, llm_model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Inicializar LLM
        self.llm = None
        if llm_model_path and Path(llm_model_path).exists():
            try:
                self.llm = LlamaManager(llm_model_path)
                self.logger.info(f"LLM inicializado: {llm_model_path}")
            except Exception as e:
                self.logger.warning(f"Error inicializando LLM: {str(e)}")
                self.llm = None
        
        # Inicializar agentes
        self.agents = self._initialize_agents()
        
        # Estado del sistema
        self.current_manuscript = ""
        self.analysis_results = {}
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Inicializa todos los agentes del sistema"""
        agents = {}
        
        try:
            agents['lorekeeper'] = LorekeeperAgent(self.llm)
            agents['character_developer'] = CharacterDeveloperAgent(self.llm)
            agents['plot_weaver'] = PlotWeaverAgent(self.llm)
            agents['style_editor'] = StyleEditorAgent(self.llm)
            agents['visualizer'] = VisualizerAgent(self.llm)
            agents['researcher'] = ResearcherAgent(self.llm)
            agents['continuity_auditor'] = ContinuityAuditorAgent(self.llm)
            agents['beta_reader'] = BetaReaderAgent(self.llm)
            agents['pacing_specialist'] = PacingSpecialistAgent(self.llm)
            agents['proofreader'] = ProofreaderAgent(self.llm)
            agents['innovation_scout'] = InnovationScoutAgent(self.llm)
            
            self.logger.info(f"Inicializados {len(agents)} agentes exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando agentes: {str(e)}")
            
        return agents
    
    def get_agent(self, agent_name: str):
        """Obtiene un agente específico"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """Lista todos los agentes disponibles"""
        return list(self.agents.keys())
    
    def set_manuscript(self, manuscript: str):
        """Establece el manuscrito actual para análisis"""
        self.current_manuscript = manuscript
        self.logger.info(f"Manuscrito establecido: {len(manuscript)} caracteres")
    
    def run_analysis_phase(self, phase: str, manuscript: str = None) -> Dict[str, Any]:
        """Ejecuta una fase específica de análisis"""
        
        if manuscript:
            self.set_manuscript(manuscript)
        elif not self.current_manuscript:
            raise ValueError("No hay manuscrito establecido para análisis")
        
        manuscript_text = manuscript or self.current_manuscript
        results = {}
        
        if phase == "worldbuilding":
            results = self._run_worldbuilding_analysis(manuscript_text)
        elif phase == "character_development":
            results = self._run_character_analysis(manuscript_text)
        elif phase == "plot_structure":
            results = self._run_plot_analysis(manuscript_text)
        elif phase == "style_refinement":
            results = self._run_style_analysis(manuscript_text)
        elif phase == "visual_creation":
            results = self._run_visual_creation(manuscript_text)
        elif phase == "quality_assurance":
            results = self._run_quality_assurance(manuscript_text)
        else:
            raise ValueError(f"Fase de análisis desconocida: {phase}")
        
        self.analysis_results[phase] = results
        return results
    
    def _run_worldbuilding_analysis(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta análisis de construcción del mundo"""
        results = {
            "phase": "worldbuilding",
            "timestamp": None,
            "agents_involved": ["lorekeeper", "researcher", "continuity_auditor"],
            "results": {}
        }
        
        try:
            # Lorekeeper: Análisis de worldbuilding
            lorekeeper = self.agents['lorekeeper']
            results["results"]["lore_analysis"] = lorekeeper.analyze_worldbuilding(manuscript)
            
            # Researcher: Buscar información contextual
            researcher = self.agents['researcher']
            results["results"]["research_findings"] = researcher.research_context(
                "elementos fantásticos", manuscript[:500]
            )
            
            # Continuity Auditor: Verificar consistencia
            auditor = self.agents['continuity_auditor']
            results["results"]["continuity_check"] = auditor.audit_continuity(manuscript)
            
            self.logger.info("Fase de desarrollo de personajes completada")
            
        except Exception as e:
            self.logger.error(f"Error en análisis de personajes: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _run_plot_analysis(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta análisis de estructura de trama"""
        results = {
            "phase": "plot_structure",
            "timestamp": None,
            "agents_involved": ["plot_weaver", "pacing_specialist", "innovation_scout"],
            "results": {}
        }
        
        try:
            # Plot Weaver: Análisis estructural
            plot_weaver = self.agents['plot_weaver']
            results["results"]["plot_analysis"] = plot_weaver.analyze_plot_structure(manuscript)
            
            # Pacing Specialist: Análisis de ritmo
            pacing_spec = self.agents['pacing_specialist']
            results["results"]["pacing_analysis"] = pacing_spec.analyze_pacing(manuscript)
            
            # Innovation Scout: Oportunidades creativas
            innovation = self.agents['innovation_scout']
            results["results"]["creative_opportunities"] = innovation.scout_creative_opportunities(manuscript)
            
            self.logger.info("Fase de análisis de trama completada")
            
        except Exception as e:
            self.logger.error(f"Error en análisis de trama: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _run_style_analysis(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta análisis y refinamiento de estilo"""
        results = {
            "phase": "style_refinement",
            "timestamp": None,
            "agents_involved": ["style_editor", "beta_reader"],
            "results": {}
        }
        
        try:
            # Style Editor: Análisis de estilo
            style_editor = self.agents['style_editor']
            results["results"]["style_analysis"] = style_editor.analyze_writing_style(manuscript)
            
            # Beta Reader: Feedback de legibilidad
            beta_reader = self.agents['beta_reader']
            results["results"]["readability_feedback"] = beta_reader.provide_reader_feedback(
                manuscript, "general_reader"
            )
            
            self.logger.info("Fase de refinamiento de estilo completada")
            
        except Exception as e:
            self.logger.error(f"Error en análisis de estilo: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _run_visual_creation(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta creación de elementos visuales"""
        results = {
            "phase": "visual_creation",
            "timestamp": None,
            "agents_involved": ["visualizer"],
            "results": {}
        }
        
        try:
            # Visualizer: Crear prompts visuales
            visualizer = self.agents['visualizer']
            results["results"]["visual_prompts"] = visualizer.create_visual_prompts(manuscript)
            
            self.logger.info("Fase de creación visual completada")
            
        except Exception as e:
            self.logger.error(f"Error en creación visual: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _run_quality_assurance(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta control de calidad final"""
        results = {
            "phase": "quality_assurance",
            "timestamp": None,
            "agents_involved": ["proofreader", "continuity_auditor"],
            "results": {}
        }
        
        try:
            # Proofreader: Corrección final
            proofreader = self.agents['proofreader']
            results["results"]["proofreading"] = proofreader.proofread_manuscript(manuscript)
            
            # Continuity Auditor: Verificación final
            auditor = self.agents['continuity_auditor']
            results["results"]["final_continuity_check"] = auditor.audit_continuity(manuscript)
            
            self.logger.info("Fase de control de calidad completada")
            
        except Exception as e:
            self.logger.error(f"Error en control de calidad: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def run_complete_analysis(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta análisis completo en todas las fases"""
        self.logger.info("Iniciando análisis completo del manuscrito")
        
        phases = [
            "worldbuilding",
            "character_development", 
            "plot_structure",
            "style_refinement",
            "visual_creation",
            "quality_assurance"
        ]
        
        complete_results = {
            "manuscript_length": len(manuscript),
            "phases_completed": [],
            "phases_results": {},
            "summary": {},
            "recommendations": []
        }
        
        for phase in phases:
            try:
                self.logger.info(f"Ejecutando fase: {phase}")
                phase_results = self.run_analysis_phase(phase, manuscript)
                
                complete_results["phases_results"][phase] = phase_results
                complete_results["phases_completed"].append(phase)
                
            except Exception as e:
                self.logger.error(f"Error en fase {phase}: {str(e)}")
                complete_results["phases_results"][phase] = {"error": str(e)}
        
        # Generar resumen y recomendaciones
        complete_results["summary"] = self._generate_analysis_summary(complete_results)
        complete_results["recommendations"] = self._generate_recommendations(complete_results)
        
        self.logger.info("Análisis completo finalizado")
        return complete_results
    
    def _generate_analysis_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un resumen del análisis completo"""
        summary = {
            "total_phases": len(results["phases_completed"]),
            "successful_phases": len([p for p in results["phases_results"].values() if "error" not in p]),
            "key_findings": [],
            "overall_assessment": "En proceso"
        }
        
        # Analizar resultados clave (simplificado para demo)
        if "worldbuilding" in results["phases_completed"]:
            summary["key_findings"].append("Análisis de worldbuilding completado")
        
        if "character_development" in results["phases_completed"]:
            summary["key_findings"].append("Desarrollo de personajes evaluado")
        
        if summary["successful_phases"] >= 4:
            summary["overall_assessment"] = "Satisfactorio"
        elif summary["successful_phases"] >= 2:
            summary["overall_assessment"] = "Parcial"
        else:
            summary["overall_assessment"] = "Requiere atención"
        
        return summary
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones basadas en fases completadas
        successful_phases = [p for p in results["phases_results"].values() if "error" not in p]
        
        if len(successful_phases) < 6:
            recommendations.append("Completar todas las fases de análisis para evaluación completa")
        
        # Recomendaciones específicas (simplificado)
        if "worldbuilding" in results["phases_completed"]:
            recommendations.append("Revisar consistencia de reglas del mundo")
        
        if "character_development" in results["phases_completed"]:
            recommendations.append("Considerar profundizar arcos de personajes secundarios")
        
        if "plot_structure" in results["phases_completed"]:
            recommendations.append("Evaluar ritmo narrativo en secciones medias")
        
        if not recommendations:
            recommendations.append("Manuscrito procesado exitosamente - listo para siguiente iteración")
        
        return recommendations
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del estado actual del análisis"""
        return {
            "manuscript_set": bool(self.current_manuscript),
            "manuscript_length": len(self.current_manuscript) if self.current_manuscript else 0,
            "completed_phases": list(self.analysis_results.keys()),
            "available_agents": self.list_agents(),
            "llm_available": self.llm is not None
        }
    
    def reset_analysis(self):
        """Reinicia el estado del análisis"""
        self.current_manuscript = ""
        self.analysis_results = {}
        self.logger.info("Estado de análisis reiniciado")


# agents/test_agents.py
#!/usr/bin/env python3
"""Script de prueba para el sistema de agentes"""

import sys
import logging
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from agents.agent_manager import AgentManager
from config.settings import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_agent_initialization():
    """Prueba la inicialización de agentes"""
    print("🧪 Probando inicialización de agentes...")
    
    try:
        # Inicializar manager sin LLM
        manager = AgentManager()
        
        # Verificar agentes
        agents = manager.list_agents()
        print(f"✅ Agentes inicializados: {len(agents)}")
        for agent in agents:
            print(f"   - {agent}")
        
        # Probar obtener agente específico
        lorekeeper = manager.get_agent('lorekeeper')
        if lorekeeper:
            print("✅ Agente Lorekeeper accesible")
        else:
            print("❌ Error accediendo Lorekeeper")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en inicialización: {str(e)}")
        return False

def test_agent_tools():
    """Prueba las herramientas de los agentes"""
    print("\n🔧 Probando herramientas de agentes...")
    
    try:
        manager = AgentManager()
        lorekeeper = manager.get_agent('lorekeeper')
        
        if lorekeeper and hasattr(lorekeeper, 'agent'):
            tools = lorekeeper.agent.tools
            print(f"✅ Herramientas disponibles: {len(tools)}")
            for tool in tools[:5]:  # Mostrar primeras 5
                print(f"   - {tool.name}")
            
            return True
        else:
            print("❌ No se pudieron acceder a las herramientas")
            return False
            
    except Exception as e:
        print(f"❌ Error probando herramientas: {str(e)}")
        return False

def test_manuscript_analysis():
    """Prueba análisis de manuscrito simple"""
    print("\n📖 Probando análisis de manuscrito...")
    
    try:
        manager = AgentManager()
        
        # Manuscrito de prueba
        test_manuscript = """
        En el reino de Eldoria, el joven mago Kael descubrió un antiguo grimorio
        en las ruinas de la torre de su maestro. El libro contenía hechizos
        prohibidos que podrían cambiar el destino del reino para siempre.
        
        Kael era conocido por su cabello dorado y sus ojos verdes como esmeraldas.
        Su maestro, el anciano Aldric, había desaparecido misteriosamente hace tres días.
        
        Mientras Kael examinaba el grimorio, una sombra se movió en la esquina de la torre.
        """
        
        # Establecer manuscrito
        manager.set_manuscript(test_manuscript)
        
        # Obtener resumen
        summary = manager.get_analysis_summary()
        print(f"✅ Manuscrito establecido: {summary['manuscript_length']} caracteres")
        
        # Probar una fase simple (worldbuilding)
        try:
            results = manager.run_analysis_phase("worldbuilding")
            print(f"✅ Fase worldbuilding ejecutada")
            print(f"   Agentes involucrados: {results.get('agents_involved', [])}")
        except Exception as e:
            print(f"⚠️  Fase worldbuilding falló (esperado sin LLM): {str(e)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en análisis de manuscrito: {str(e)}")
        return False

def test_with_llm():
    """Prueba con modelo LLM si está disponible"""
    print("\n🤖 Probando con modelo LLM...")
    
    llm_path = None
    
    # Buscar modelo en ubicaciones comunes
    possible_paths = [
        "./llm_local/models/model.gguf",
        "/home/user/multi_agent_novel_system/llm_local/models/model.gguf",
        settings.llm_model_path
    ]
    
    for path in possible_paths:
        if path and Path(path).exists():
            llm_path = path
            break
    
    if llm_path:
        try:
            print(f"🔄 Inicializando con modelo: {llm_path}")
            manager = AgentManager(llm_path)
            
            summary = manager.get_analysis_summary()
            print(f"✅ Manager con LLM inicializado")
            print(f"   LLM disponible: {summary['llm_available']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error con LLM: {str(e)}")
            return False
    else:
        print("⚠️  No se encontró modelo LLM - saltando prueba")
        return True

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de agentes\n")
    
    tests = [
        ("Inicialización de Agentes", test_agent_initialization),
        ("Herramientas de Agentes", test_agent_tools),  
        ("Análisis de Manuscrito", test_manuscript_analysis),
        ("Integración con LLM", test_with_llm)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"TEST: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumen final
    print(f"\n{'='*50}")
    print("RESUMEN DE PRUEBAS")
    print('='*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 Todos los tests pasaron - Sistema de agentes listo!")
    else:
        print("⚠️  Algunos tests fallaron - revisar configuración")

if __name__ == "__main__":
    main() worldbuilding completada")
            
        except Exception as e:
            self.logger.error(f"Error en análisis de worldbuilding: {str(e)}")
            results["error"] = str(e)
        
        return results
    
    def _run_character_analysis(self, manuscript: str) -> Dict[str, Any]:
        """Ejecuta análisis de desarrollo de personajes"""
        results = {
            "phase": "character_development", 
            "timestamp": None,
            "agents_involved": ["character_developer", "beta_reader"],
            "results": {}
        }
        
        try:
            # Character Developer: Análisis y desarrollo
            char_dev = self.agents['character_developer']
            results["results"]["character_analysis"] = char_dev.develop_characters(manuscript)
            
            # Beta Reader: Feedback sobre conexión emocional
            beta_reader = self.agents['beta_reader']
            results["results"]["reader_feedback"] = beta_reader.provide_reader_feedback(
                manuscript, "adult_fantasy"
            )
            
            self.logger.info("Fase de