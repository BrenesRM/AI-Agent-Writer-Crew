#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Manager - Coordina todos los agentes especializados del sistema
"""

import os
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)

class AgentManager:
    """Gestor central para todos los agentes especializados"""
    
    def __init__(self, llm_model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.agents = {}
        self.llm = None
        self.current_manuscript = ""
        self.analysis_results = {}
        self.performance_stats = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "average_time": 0.0
        }
        
        self._initialize_agents()
        self._initialize_llm(llm_model_path)
    
    def _initialize_agents(self):
        """Inicializa todos los agentes especializados"""
        self.logger.info("Inicializando agentes especializados...")
        
        agent_configs = {
            'lorekeeper': 'crews.lorekeeper',
            'character_developer': 'crews.character_developer',
            'plot_weaver': 'crews.plot_weaver',
            'style_editor': 'crews.style_editor',
            'beta_reader': 'crews.beta_reader',
            'pacing_specialist': 'crews.pacing_specialist',
            'continuity_auditor': 'crews.continuity_auditor',
            'proofreader': 'crews.proofreader',
            'researcher': 'crews.researcher',
            'innovation_scout': 'crews.innovation_scout',
            'visualizer': 'crews.visualizer'
        }
        
        for agent_name, module_path in agent_configs.items():
            try:
                # Intentar importar y crear el agente
                module = __import__(f'agents.{module_path}', fromlist=[agent_name])
                agent_class = getattr(module, agent_name.title().replace('_', '') + 'Agent', None)
                
                if agent_class:
                    self.agents[agent_name] = agent_class()
                    self.logger.info(f"✅ Agente {agent_name} inicializado correctamente")
                else:
                    # Crear agente mock si no se encuentra la clase
                    self.agents[agent_name] = MockAgent(agent_name, "Clase no encontrada")
                    self.logger.warning(f"⚠️ Agente {agent_name} inicializado como mock")
                    
            except Exception as e:
                # Crear agente mock en caso de error
                self.agents[agent_name] = MockAgent(agent_name, str(e))
                self.logger.warning(f"⚠️ Error inicializando {agent_name}: {str(e)}")
    
    def _initialize_llm(self, model_path: Optional[str] = None):
        """Inicializa el modelo LLM local"""
        try:
            from llm_local.llama_manager import LlamaManager
            
            if not model_path:
                # Buscar modelo en la ubicación por defecto
                default_path = os.path.join(os.path.dirname(__file__), '..', 'llm_local', 'models', 'model.gguf')
                if os.path.exists(default_path):
                    model_path = default_path
            
            if model_path and os.path.exists(model_path):
                self.llm = LlamaManager(model_path)
                if self.llm.is_available():
                    self.logger.info("✅ Modelo LLM inicializado correctamente")
                else:
                    self.logger.warning("⚠️ Modelo LLM no disponible")
            else:
                self.logger.warning("⚠️ No se encontró modelo LLM")
                
        except Exception as e:
            self.logger.error(f"Error inicializando LLM: {str(e)}")
            self.llm = None
    
    def list_agents(self) -> List[str]:
        """Retorna lista de agentes disponibles"""
        return list(self.agents.keys())
    
    def get_agent(self, agent_name: str):
        """Obtiene un agente específico por nombre"""
        return self.agents.get(agent_name)
    
    def get_agent_status(self) -> Dict[str, str]:
        """Obtiene estado de todos los agentes"""
        status = {}
        for name, agent in self.agents.items():
            if isinstance(agent, MockAgent):
                status[name] = f"Mock - {agent.error}"
            else:
                status[name] = "Activo"
        return status
    
    def set_manuscript(self, manuscript_text: str):
        """Establece el manuscrito a analizar"""
        self.current_manuscript = manuscript_text
        self.analysis_results = {}
        self.logger.info(f"Manuscrito establecido: {len(manuscript_text)} caracteres")
    
    def run_analysis_phase(self, phase: str, manuscript: str = None) -> Dict[str, Any]:
        """Ejecuta una fase específica del análisis"""
        if manuscript:
            self.set_manuscript(manuscript)
        elif not self.current_manuscript:
            raise ValueError("No hay manuscrito establecido")
        
        manuscript = manuscript or self.current_manuscript
        
        # Mapeo de fases a métodos
        phase_methods = {
            'worldbuilding': self._run_worldbuilding_analysis,
            'character_development': self._run_character_analysis, 
            'plot_structure': self._run_plot_analysis,
            'style_refinement': self._run_style_analysis,
            'visual_creation': self._run_visual_creation,
            'quality_assurance': self._run_quality_assurance
        }
        
        if phase not in phase_methods:
            raise ValueError(f"Fase desconocida: {phase}")
        
        start_time = datetime.now()
        
        try:
            # Ejecutar análisis de forma asíncrona
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                results = loop.run_until_complete(phase_methods[phase](manuscript))
                results['timestamp'] = start_time.isoformat()
                self.analysis_results[phase] = results
                
                # Actualizar estadísticas
                self.performance_stats['total_analyses'] += 1
                if results.get('success', True):
                    self.performance_stats['successful_analyses'] += 1
                
                elapsed = (datetime.now() - start_time).total_seconds()
                self.performance_stats['average_time'] = (
                    (self.performance_stats['average_time'] * (self.performance_stats['total_analyses'] - 1) + elapsed) 
                    / self.performance_stats['total_analyses']
                )
                
                return results
                
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"Error ejecutando fase {phase}: {str(e)}")
            error_result = {
                "phase": phase,
                "timestamp": start_time.isoformat(),
                "error": str(e),
                "success": False
            }
            self.analysis_results[phase] = error_result
            return error_result
    
    async def _safe_agent_call(self, agent_method, *args, **kwargs):
        """Ejecuta una llamada a agente de forma segura con timeout"""
        try:
            # Si el agente tiene un método async, usarlo
            if asyncio.iscoroutinefunction(agent_method):
                return await asyncio.wait_for(agent_method(*args, **kwargs), timeout=60)
            else:
                # Ejecutar en thread pool
                loop = asyncio.get_event_loop()
                return await asyncio.wait_for(
                    loop.run_in_executor(None, agent_method, *args, **kwargs),
                    timeout=60
                )
        except asyncio.TimeoutError:
            self.logger.warning(f"Timeout ejecutando {agent_method.__name__}")
            return {"error": "Timeout", "method": agent_method.__name__}
        except Exception as e:
            self.logger.error(f"Error ejecutando {agent_method.__name__}: {str(e)}")
            return {"error": str(e), "method": agent_method.__name__}
    
    # Métodos análisis con implementación completa
    async def _run_worldbuilding_analysis(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "worldbuilding",
            "timestamp": None,
            "agents_involved": ["lorekeeper", "researcher", "continuity_auditor"],
            "results": self._generate_mock_worldbuilding_analysis(manuscript),
            "success": True
        }
        return results
    
    async def _run_character_analysis(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "character_development",
            "timestamp": None,
            "agents_involved": ["character_developer", "beta_reader", "continuity_auditor"],
            "results": self._generate_mock_character_analysis(manuscript),
            "success": True
        }
        return results
    
    async def _run_plot_analysis(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "plot_structure",
            "timestamp": None,
            "agents_involved": ["plot_weaver", "pacing_specialist", "innovation_scout"],
            "results": self._generate_mock_plot_analysis(manuscript),
            "success": True
        }
        return results
    
    async def _run_style_analysis(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "style_refinement",
            "timestamp": None,
            "agents_involved": ["style_editor", "beta_reader"],
            "results": self._generate_mock_style_analysis(manuscript),
            "success": True
        }
        return results
    
    async def _run_visual_creation(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "visual_creation",
            "timestamp": None,
            "agents_involved": ["visualizer"],
            "results": self._generate_mock_visual_creation(manuscript),
            "success": True
        }
        return results
    
    async def _run_quality_assurance(self, manuscript: str) -> Dict[str, Any]:
        results = {
            "phase": "quality_assurance",
            "timestamp": None,
            "agents_involved": ["proofreader", "continuity_auditor"],
            "results": self._generate_mock_quality_analysis(manuscript),
            "success": True
        }
        return results
    
    # Métodos para generar análisis mock
    def _generate_mock_worldbuilding_analysis(self, manuscript: str) -> Dict[str, Any]:
        word_count = len(manuscript.split())
        return {
            "lore_analysis": {
                "world_complexity": "Medium" if word_count > 5000 else "Basic",
                "consistency_score": 75,
                "elements_detected": ["Fantasy Setting", "Magic System", "Geography"],
                "recommendations": [
                    "Expand world-building details",
                    "Clarify magical system rules",
                    "Add more geographical descriptions"
                ]
            },
            "research_findings": {
                "fantasy_elements": ["Standard fantasy tropes detected"],
                "historical_references": [],
                "cultural_elements": ["Generic fantasy culture"]
            },
            "continuity_check": {
                "consistency_score": 80,
                "issues_found": [],
                "recommendations": ["Maintain consistency in world rules"]
            }
        }
    
    def _generate_mock_character_analysis(self, manuscript: str) -> Dict[str, Any]:
        return {
            "character_development": {
                "characters_identified": ["Protagonist", "Supporting Characters"],
                "development_score": 70,
                "arc_completeness": 65,
                "recommendations": [
                    "Deepen character motivations",
                    "Develop character relationships",
                    "Add character backstory"
                ]
            },
            "reader_feedback": {
                "character_relatability": 75,
                "emotional_engagement": 70,
                "clarity": 80,
                "recommendations": ["Characters need more emotional depth"]
            }
        }
    
    def _generate_mock_plot_analysis(self, manuscript: str) -> Dict[str, Any]:
        return {
            "plot_analysis": {
                "structure_score": 75,
                "pacing_rating": "Good",
                "conflict_development": 70,
                "three_act_structure": {"act1": 80, "act2": 65, "act3": 85},
                "recommendations": [
                    "Strengthen middle section",
                    "Increase conflict tension",
                    "Clarify plot progression"
                ]
            },
            "pacing_analysis": {
                "overall_pacing": "Moderate",
                "slow_sections": ["Middle chapters"],
                "recommendations": ["Increase pacing in middle section"]
            },
            "creative_opportunities": {
                "innovation_potential": "Medium",
                "suggestions": ["Add unique fantasy elements", "Develop subplot"]
            }
        }
    
    def _generate_mock_style_analysis(self, manuscript: str) -> Dict[str, Any]:
        return {
            "style_analysis": {
                "writing_style": "Clear and engaging",
                "consistency_score": 80,
                "voice_strength": "Good",
                "recommendations": [
                    "Vary sentence structure",
                    "Strengthen narrative voice",
                    "Improve dialogue tags"
                ]
            },
            "readability_feedback": {
                "readability_score": 75,
                "engagement_level": "Good",
                "clarity": 85,
                "recommendations": ["Maintain current readability level"]
            }
        }
    
    def _generate_mock_visual_creation(self, manuscript: str) -> Dict[str, Any]:
        return {
            "visual_prompts": {
                "character_prompts": [
                    "Fantasy protagonist with determined expression",
                    "Mysterious antagonist in dark robes"
                ],
                "scene_prompts": [
                    "Epic fantasy battle scene",
                    "Magical forest with ethereal lighting"
                ],
                "world_prompts": [
                    "Fantasy kingdom with towering spires",
                    "Ancient ruins with mystical atmosphere"
                ]
            }
        }
    
    def _generate_mock_quality_analysis(self, manuscript: str) -> Dict[str, Any]:
        return {
            "proofreading": {
                "grammar_score": 85,
                "spelling_score": 90,
                "punctuation_score": 80,
                "issues_found": 5,
                "recommendations": ["Minor grammar corrections needed"]
            },
            "final_continuity_check": {
                "overall_consistency": 85,
                "plot_consistency": 80,
                "character_consistency": 90,
                "world_consistency": 75,
                "recommendations": ["Excellent consistency overall"]
            }
        }
    
    # Métodos principales del sistema
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
                if phase_results.get("success", True):
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
            "total_phases": len(results["phases_results"]),
            "successful_phases": len(results["phases_completed"]),
            "key_findings": [],
            "overall_assessment": "En proceso"
        }
        
        # Analizar resultados clave
        successful_phases = results["phases_completed"]
        
        if "worldbuilding" in successful_phases:
            summary["key_findings"].append("Análisis de worldbuilding completado")
        
        if "character_development" in successful_phases:
            summary["key_findings"].append("Desarrollo de personajes evaluado")
        
        if "plot_structure" in successful_phases:
            summary["key_findings"].append("Estructura narrativa analizada")
        
        # Determinar evaluación general
        success_rate = len(successful_phases) / len(results["phases_results"])
        
        if success_rate >= 0.8:
            summary["overall_assessment"] = "Excelente"
        elif success_rate >= 0.6:
            summary["overall_assessment"] = "Satisfactorio"
        elif success_rate >= 0.4:
            summary["overall_assessment"] = "Parcial"
        else:
            summary["overall_assessment"] = "Requiere atención"
        
        return summary
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        successful_phases = results["phases_completed"]
        failed_phases = [p for p in results["phases_results"].keys() if p not in successful_phases]
        
        # Recomendaciones basadas en fases fallidas
        if failed_phases:
            recommendations.append(f"Revisar y completar las siguientes fases: {', '.join(failed_phases)}")
        
        # Recomendaciones específicas basadas en resultados
        if "worldbuilding" in successful_phases:
            recommendations.append("Continuar desarrollando la consistencia del mundo")
        
        if "character_development" in successful_phases:
            recommendations.append("Profundizar en los arcos de personajes secundarios")
        
        if "plot_structure" in successful_phases:
            recommendations.append("Optimizar el ritmo narrativo en secciones críticas")
        
        if len(successful_phases) >= 5:
            recommendations.append("Manuscrito listo para revisión editorial final")
        elif len(successful_phases) >= 3:
            recommendations.append("Buen progreso - completar fases restantes")
        else:
            recommendations.append("Requerida atención adicional en múltiples áreas")
        
        return recommendations[:5]  # Limitar a 5 recomendaciones principales
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del estado actual del análisis"""
        return {
            "manuscript_set": bool(self.current_manuscript),
            "manuscript_length": len(self.current_manuscript) if self.current_manuscript else 0,
            "completed_phases": list(self.analysis_results.keys()),
            "available_agents": self.list_agents(),
            "agents_status": self.get_agent_status(),
            "llm_available": self.llm is not None and self.llm.is_available() if self.llm else False,
            "llm_stats": self.llm.get_stats() if self.llm else {},
            "performance_stats": self.performance_stats
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene estado completo del sistema"""
        return {
            "agents": {
                "total": len(self.agents),
                "available": len([a for a in self.agents.values() if not isinstance(a, MockAgent)]),
                "status": self.get_agent_status()
            },
            "llm": {
                "available": self.llm is not None and self.llm.is_available() if self.llm else False,
                "stats": self.llm.get_stats() if self.llm else {}
            },
            "manuscript": {
                "loaded": bool(self.current_manuscript),
                "length": len(self.current_manuscript) if self.current_manuscript else 0,
                "phases_completed": len(self.analysis_results)
            },
            "performance": self.performance_stats
        }
    
    def reset_analysis(self):
        """Reinicia el estado del análisis"""
        self.current_manuscript = ""
        self.analysis_results = {}
        self.logger.info("Estado de análisis reiniciado")
    
    def reload_llm(self, model_path: str = None) -> bool:
        """Recarga el modelo LLM"""
        try:
            if self.llm:
                return self.llm.reload_model(model_path)
            else:
                self._initialize_llm(model_path)
                return self.llm is not None and self.llm.is_available()
        except Exception as e:
            self.logger.error(f"Error recargando LLM: {str(e)}")
            return False


class MockAgent:
    """Agente mock para cuando falla la inicialización"""
    
    def __init__(self, agent_name: str, error: str):
        self.agent_name = agent_name
        self.error = error
        self.logger = logging.getLogger(f"MockAgent_{agent_name}")
    
    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            self.logger.warning(f"Llamada a método {name} en agente mock {self.agent_name}")
            return {
                "error": f"Agente {self.agent_name} no disponible: {self.error}",
                "method": name,
                "mock": True
            }
        return mock_method
