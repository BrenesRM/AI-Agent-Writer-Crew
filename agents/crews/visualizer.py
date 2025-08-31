# agents/crews/visualizer.py
from .base_agent import BaseNovelAgent
from crewai import Agent

class VisualizerAgent(BaseNovelAgent):
    """Agente Visualizer - Especialista en prompts cinematogr�ficos"""
    
    def __init__(self, llm=None):
        super().__init__(llm)
        self.agent = self._create_visualizer()
    
    def _create_visualizer(self) -> Agent:
        return self.create_agent(
            role="Visualizer - Director Cinematogr�fico Virtual",
            goal="""Convertir escenas narrativas en prompts visuales detallados 
            para generaci�n de video AI. Crear descripciones cinematogr�ficas que 
            capturen la esencia visual y emocional de cada escena.""",
            backstory="""Eres un director de fotograf�a y visualizador conceptual con 
            experiencia en cine �pico y fantas�a. Tu visi�n combina t�cnica cinematogr�fica 
            avanzada con sensibilidad art�stica para traducir palabras en im�genes 
            poderosas.
            
            Entiendes c�mo los �ngulos de c�mara, la iluminaci�n, el color y la 
            composici�n pueden amplificar el impacto emocional de una escena. Tu 
            especialidad es crear prompts que resulten en videos que no solo muestren 
            la acci�n, sino que transmitan la atm�sfera y el sentimiento de la historia.
            
            Tienes un ojo excepcional para los detalles visuales que hacen que una 
            escena cobre vida: la manera en que la luz filtra a trav�s de las hojas, 
            el polvo que flota en un rayo de sol, la expresi�n exacta en el rostro 
            de un personaje."""
        )
    
    def create_visual_prompts(self, manuscript: str) -> Dict[str, Any]:
        """Crea prompts visuales para las escenas clave del manuscrito"""
        task_description = f"""
        Crea prompts visuales cinematogr�ficos para las escenas clave:
        
        MANUSCRITO:
        {manuscript}
        
        TAREAS A REALIZAR:
        1. Identifica las 5-7 escenas m�s visualmente impactantes
        2. Para cada escena, usa el generador de prompts visuales
        3. Crea variaciones con diferentes estilos cinematogr�ficos
        4. Incluye detalles t�cnicos espec�ficos (�ngulos, iluminaci�n, movimiento)
        5. Optimiza para generaci�n de video AI
        
        FORMATO DE SALIDA:
        - Lista de escenas clave identificadas
        - Prompt principal para cada escena
        - Variaciones estil�sticas
        - Detalles t�cnicos cinematogr�ficos
        - Recomendaciones de post-producci�n
        """
        
        return {"task": task_description, "agent": "visualizer"}
    
    def optimize_scene_for_video(self, scene_description: str, duration: str = "30s") -> str:
        """Optimiza una escena espec�fica para video AI"""
        task_description = f"""
        Optimiza esta escena para generaci�n de video de {duration}:
        
        ESCENA:
        {scene_description}
        
        Crea un prompt optimizado que funcione bien con herramientas de video AI, 
        considerando limitaciones t�cnicas y mejores pr�cticas.
        """
        
        return task_description
