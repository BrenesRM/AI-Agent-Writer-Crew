# agents/crews/visualizer.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class VisualizerAgent(BaseNovelAgent):
    """Agente Visualizer - Especialista en prompts cinematográficos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_visualizer()
    
    def _create_visualizer(self) -> Agent:
        return self.create_agent(
            role="Visualizer - Director Cinematográfico Virtual",
            goal="""Convertir escenas narrativas en prompts visuales detallados 
            para generación de video AI. Crear descripciones cinematográficas que 
            capturen la esencia visual y emocional de cada escena.""",
            backstory="""Eres un director de fotografía y visualizador conceptual con 
            experiencia en cine épico y fantasía. Tu visión combina técnica cinematográfica 
            avanzada con sensibilidad artística para traducir palabras en imágenes 
            poderosas.
            
            Entiendes cómo los ángulos de cámara, la iluminación, el color y la 
            composición pueden amplificar el impacto emocional de una escena. Tu 
            especialidad es crear prompts que resulten en videos que no solo muestren 
            la acción, sino que transmitan la atmósfera y el sentimiento de la historia.
            
            Tienes un ojo excepcional para los detalles visuales que hacen que una 
            escena cobre vida: la manera en que la luz filtra a través de las hojas, 
            el polvo que flota en un rayo de sol, la expresión exacta en el rostro 
            de un personaje."""
        )
    
    def create_visual_prompts(self, manuscript: str) -> Dict[str, Any]:
        """Crea prompts visuales para las escenas clave del manuscrito"""
        task_description = f"""
        Crea prompts visuales cinematográficos para las escenas clave:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica las 5-7 escenas más visualmente impactantes
        2. Para cada escena, usa el generador de prompts visuales
        3. Crea variaciones con diferentes estilos cinematográficos
        4. Incluye detalles técnicos específicos (ángulos, iluminación, movimiento)
        5. Optimiza para generación de video AI
        
        FORMATO DE SALIDA:
        - Lista de escenas clave identificadas
        - Prompt principal para cada escena
        - Variaciones estilísticas
        - Detalles técnicos cinematográficos
        - Recomendaciones de post-producción
        """
        
        return {"task": task_description, "agent": "visualizer"}
    
    def optimize_scene_for_video(self, scene_description: str, duration: str = "30s") -> str:
        """Optimiza una escena específica para video AI"""
        task_description = f"""
        Optimiza esta escena para generación de video de {duration}:
        
        ESCENA:
        {scene_description}
        
        Crea un prompt optimizado que funcione bien con herramientas de video AI, 
        considerando limitaciones técnicas y mejores prácticas.
        """
        
        return task_description
