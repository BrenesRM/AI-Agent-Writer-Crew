# -*- coding: utf-8 -*-
# agents/tools/creative_tools.py
import random
import logging
from typing import Dict, Any, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class IdeaGeneratorInput(BaseModel):
    context: str = Field(..., description="Contexto o tema para generar ideas")
    idea_type: str = Field("general", description="Tipo de idea: 'character', 'plot', 'setting', 'conflict', 'general'")
    quantity: int = Field(5, description="Número de ideas a generar")

class IdeaGenerator(BaseTool):
    name: str = "Generador de Ideas Creativas"
    description: str = """
    Genera ideas creativas para elementos narrativos basado en el contexto proporcionado.
    Puede generar ideas para personajes, tramas, escenarios, conflictos y elementos generales.
    """
    args_schema: type[BaseModel] = IdeaGeneratorInput
    
    # Define as class attributes for Pydantic v2 compatibility
    character_elements: Dict[str, List[str]] = {}
    plot_elements: Dict[str, List[str]] = {}
    setting_elements: Dict[str, List[str]] = {}
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize after parent initialization
        if not self.character_elements:
            self._initialize_elements()
    
    def _initialize_elements(self):
        """Initialize the creative elements after object creation"""
        # Bancos de datos para generación de ideas
        self.character_elements = {
            'professions': ['mago', 'guerrero', 'mercader', 'ladron', 'noble', 'artesano', 'cazador', 'sanador', 'escriba', 'soldado'],
            'traits': ['valiente', 'astuto', 'leal', 'ambicioso', 'misterioso', 'carismatico', 'testarudo', 'compasivo', 'calculador', 'impulsivo'],
            'backgrounds': ['huerfano', 'exiliado', 'heredero perdido', 'ex-soldado', 'forastero', 'refugiado', 'desertor', 'autodidacta'],
            'motivations': ['venganza', 'redencion', 'poder', 'conocimiento', 'amor', 'supervivencia', 'justicia', 'libertad', 'familia', 'honor']
        }
        
        self.plot_elements = {
            'conflicts': ['traicion', 'guerra', 'conspiracion', 'maldicion', 'invasion', 'rebelion', 'busqueda', 'rescate', 'supervivencia', 'secreto familiar'],
            'twists': ['aliado es enemigo', 'enemigo es aliado', 'profecia malinterpretada', 'identidad oculta', 'poder heredado', 'sacrificio necesario'],
            'obstacles': ['ejercito enemigo', 'traidor interno', 'barrera magica', 'tiempo limitado', 'recursos escasos', 'dilema moral']
        }
        
        self.setting_elements = {
            'locations': ['reino montanoso', 'ciudad flotante', 'bosque encantado', 'desierto magico', 'isla misteriosa', 'fortaleza antigua', 'ciudad subterranea'],
            'environments': ['perpetuo invierno', 'lluvias eternas', 'niebla constante', 'auroras magicas', 'cristales flotantes', 'ruinas antiguas'],
            'societies': ['reino feudal', 'republica mercantil', 'tribu nomada', 'imperio magico', 'ciudad-estado', 'confederacion']
        }
    
    def _run(self, context: str, idea_type: str = "general", quantity: int = 5) -> str:
        """Genera ideas creativas basadas en el contexto y tipo especificado"""
        try:
            # Ensure elements are initialized
            if not self.character_elements:
                self._initialize_elements()
                
            ideas = []
            context_words = context.lower().split()
            
            if idea_type == "character":
                ideas = self._generate_character_ideas(context_words, quantity)
            elif idea_type == "plot":
                ideas = self._generate_plot_ideas(context_words, quantity)
            elif idea_type == "setting":
                ideas = self._generate_setting_ideas(context_words, quantity)
            elif idea_type == "conflict":
                ideas = self._generate_conflict_ideas(context_words, quantity)
            else:
                # Generar ideas generales mixtas
                ideas = self._generate_general_ideas(context_words, quantity)
            
            result = f"💡 IDEAS CREATIVAS ({idea_type.upper()}) para '{context}':\n\n"
            for i, idea in enumerate(ideas, 1):
                result += f"{i}. {idea}\n"
            
            result += f"\n🎯 Contexto analizado: {context}\n"
            result += f"📊 {len(ideas)} ideas generadas"
            
            return result
            
        except Exception as e:
            return f"Error generando ideas: {str(e)}"
    
    def _generate_character_ideas(self, context_words: List[str], quantity: int) -> List[str]:
        """Genera ideas para personajes"""
        ideas = []
        
        for _ in range(quantity):
            profession = random.choice(self.character_elements['professions'])
            trait = random.choice(self.character_elements['traits'])
            background = random.choice(self.character_elements['backgrounds'])
            motivation = random.choice(self.character_elements['motivations'])
            
            # Adaptar al contexto
            if any(word in context_words for word in ['magico', 'magia', 'hechizo']):
                if random.random() > 0.5:
                    profession = random.choice(['mago', 'hechicero', 'alquimista'])
            
            if any(word in context_words for word in ['guerra', 'batalla', 'conflicto']):
                if random.random() > 0.5:
                    profession = random.choice(['guerrero', 'soldado', 'estratega'])
            
            idea = f"Un {profession} {trait} con pasado de {background}, motivado por {motivation}"
            
            # Añadir detalle contextual
            if 'reino' in context_words:
                idea += f", originario del reino mencionado"
            if 'misterio' in context_words:
                idea += f", que guarda un secreto relacionado con la historia"
                
            ideas.append(idea)
        
        return ideas
    
    def _generate_plot_ideas(self, context_words: List[str], quantity: int) -> List[str]:
        """Genera ideas para tramas"""
        ideas = []
        
        for _ in range(quantity):
            conflict = random.choice(self.plot_elements['conflicts'])
            twist = random.choice(self.plot_elements['twists'])
            obstacle = random.choice(self.plot_elements['obstacles'])
            
            idea = f"Trama centrada en {conflict}, con giro de {twist}, obstaculizada por {obstacle}"
            
            # Adaptar al contexto
            if 'personajes' in context_words:
                idea += f", enfocada en el desarrollo de multiples personajes"
            if 'magia' in context_words:
                idea += f", con elementos magicos como catalizador"
                
            ideas.append(idea)
        
        return ideas
    
    def _generate_setting_ideas(self, context_words: List[str], quantity: int) -> List[str]:
        """Genera ideas para escenarios"""
        ideas = []
        
        for _ in range(quantity):
            location = random.choice(self.setting_elements['locations'])
            environment = random.choice(self.setting_elements['environments'])
            society = random.choice(self.setting_elements['societies'])
            
            idea = f"{location} con {environment}, habitado por {society}"
            
            # Adaptar al contexto
            if 'antiguo' in context_words:
                idea += f", con ruinas y vestigios de civilizaciones pasadas"
            if 'conflicto' in context_words:
                idea += f", en estado de tension o guerra"
                
            ideas.append(idea)
        
        return ideas
    
    def _generate_conflict_ideas(self, context_words: List[str], quantity: int) -> List[str]:
        """Genera ideas para conflictos"""
        ideas = []
        
        conflict_types = [
            "Conflicto interno: personaje debe elegir entre lealtad y justicia",
            "Conflicto externo: fuerzas opuestas luchan por el control del territorio",
            "Conflicto temporal: eventos del pasado amenazan el presente",
            "Conflicto moral: el bien mayor requiere sacrificar algo valioso",
            "Conflicto de poder: diferentes facciones buscan dominio",
            "Conflicto existencial: cuestionamiento de proposito y destino",
            "Conflicto cultural: choques entre diferentes formas de vida",
            "Conflicto generacional: viejas tradiciones vs. nuevas ideas"
        ]
        
        selected_conflicts = random.sample(conflict_types, min(quantity, len(conflict_types)))
        
        for conflict in selected_conflicts:
            # Adaptar al contexto
            if 'reino' in context_words:
                conflict += " en el contexto del reino"
            if 'personaje' in context_words:
                conflict += ", afectando directamente al protagonista"
                
            ideas.append(conflict)
        
        return ideas
    
    def _generate_general_ideas(self, context_words: List[str], quantity: int) -> List[str]:
        """Genera ideas generales mixtas"""
        ideas = []
        idea_types = ['character', 'plot', 'setting', 'conflict']
        
        for _ in range(quantity):
            idea_type = random.choice(idea_types)
            
            if idea_type == 'character':
                ideas.extend(self._generate_character_ideas(context_words, 1))
            elif idea_type == 'plot':
                ideas.extend(self._generate_plot_ideas(context_words, 1))
            elif idea_type == 'setting':
                ideas.extend(self._generate_setting_ideas(context_words, 1))
            else:
                ideas.extend(self._generate_conflict_ideas(context_words, 1))
        
        return ideas[:quantity]


class VisualPromptGeneratorInput(BaseModel):
    scene_description: str = Field(..., description="Descripción de la escena a convertir en prompt visual")
    style: str = Field("cinematografico", description="Estilo visual: 'cinematografico', 'artistico', 'realista', 'fantasia'")
    detail_level: str = Field("medio", description="Nivel de detalle: 'basico', 'medio', 'detallado'")

class VisualPromptGenerator(BaseTool):
    name: str = "Generador de Prompts Visuales"
    description: str = """
    Convierte descripciones narrativas en prompts detallados para generación de video AI.
    Especializado en crear prompts cinematográficos con detalles técnicos de cámara, iluminación y composición.
    """
    args_schema: type[BaseModel] = VisualPromptGeneratorInput
    
    # Define as class attributes for Pydantic v2 compatibility
    camera_angles: List[str] = []
    lighting_styles: List[str] = []
    color_palettes: List[str] = []
    movement_types: List[str] = []
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.camera_angles:
            self._initialize_elements()
    
    def _initialize_elements(self):
        """Initialize visual elements after object creation"""
        self.camera_angles = [
            "plano general", "plano medio", "primer plano", "plano detalle",
            "plano cenital", "contrapicado", "picado", "plano holandes"
        ]
        
        self.lighting_styles = [
            "iluminacion dramatica", "luz natural", "contraluz", "luz dorada",
            "iluminacion de tres puntos", "luz de luna", "luz de antorcha", "luz magica"
        ]
        
        self.color_palettes = [
            "paleta calida", "tonos frios", "colores desaturados", "alto contraste",
            "monocromatico", "colores vibrantes", "tonos tierra", "paleta magica"
        ]
        
        self.movement_types = [
            "camara estatica", "movimiento suave de camara", "zoom lento",
            "paneo horizontal", "paneo vertical", "travelling", "plano secuencia"
        ]
    
    def _run(self, scene_description: str, style: str = "cinematografico", detail_level: str = "medio") -> str:
        """Genera prompts visuales para video AI"""
        try:
            # Ensure elements are initialized
            if not self.camera_angles:
                self._initialize_elements()
                
            # Analizar la escena para extraer elementos clave
            elements = self._extract_visual_elements(scene_description)
            
            # Generar prompt base
            base_prompt = self._create_base_prompt(scene_description, elements)
            
            # Añadir detalles técnicos según el estilo
            technical_details = self._add_technical_details(style, detail_level, elements)
            
            # Construir prompt final
            final_prompt = f"{base_prompt}, {technical_details}"
            
            # Generar variaciones
            variations = self._create_variations(base_prompt, technical_details)
            
            result = f"""🎬 PROMPT VISUAL GENERADO:

📝 ESCENA ORIGINAL:
{scene_description}

🎯 PROMPT PRINCIPAL:
{final_prompt}

🎨 VARIACIONES:
{chr(10).join([f"{i}. {var}" for i, var in enumerate(variations, 1)])}

📋 ELEMENTOS IDENTIFICADOS:
- Personajes: {elements.get('characters', 'No identificados')}
- Ubicación: {elements.get('location', 'No especificada')}
- Ambiente: {elements.get('mood', 'Neutro')}
- Acción: {elements.get('action', 'Estática')}

🎥 DETALLES TÉCNICOS:
- Estilo: {style}
- Nivel de detalle: {detail_level}
- Enfoque: {elements.get('focus', 'General')}
"""
            return result
            
        except Exception as e:
            return f"Error generando prompt visual: {str(e)}"
    
    def _extract_visual_elements(self, description: str) -> Dict[str, Any]:
        """Extrae elementos visuales de la descripción"""
        elements = {}
        desc_lower = description.lower()
        
        # Identificar personajes (nombres propios)
        import re
        characters = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', description)
        elements['characters'] = ', '.join(characters[:3]) if characters else 'personaje principal'
        
        # Identificar ubicaciones
        location_keywords = {
            'bosque': 'bosque encantado',
            'castillo': 'castillo medieval',
            'ciudad': 'ciudad fantastica',
            'montana': 'paisaje montanoso',
            'mar': 'vista oceanica',
            'cueva': 'cueva misteriosa',
            'torre': 'torre antigua',
            'sala': 'gran salon'
        }
        
        location = 'escenario generico'
        for keyword, full_location in location_keywords.items():
            if keyword in desc_lower:
                location = full_location
                break
        elements['location'] = location
        
        # Identificar ambiente/mood
        mood_keywords = {
            'oscur': 'atmosfera oscura y misteriosa',
            'brillant': 'ambiente luminoso y esperanzador',
            'trist': 'ambiente melancolico',
            'alegr': 'ambiente festivo',
            'tenebroso': 'ambiente siniestro',
            'magico': 'ambiente magico y fantasioso',
            'epico': 'ambiente epico y grandioso'
        }
        
        mood = 'ambiente neutro'
        for keyword, mood_desc in mood_keywords.items():
            if keyword in desc_lower:
                mood = mood_desc
                break
        elements['mood'] = mood
        
        # Identificar acción
        action_keywords = {
            'corrio': 'movimiento dinamico',
            'lucho': 'escena de combate',
            'volo': 'secuencia de vuelo',
            'cayo': 'caida dramatica',
            'salto': 'accion acrobatica',
            'grito': 'momento emocional intenso',
            'miro': 'momento contemplativo'
        }
        
        action = 'escena estatica'
        for keyword, action_desc in action_keywords.items():
            if keyword in desc_lower:
                action = action_desc
                break
        elements['action'] = action
        
        return elements
    
    def _create_base_prompt(self, description: str, elements: Dict[str, Any]) -> str:
        """Crea el prompt base"""
        character_part = elements['characters']
        location_part = elements['location']
        mood_part = elements['mood']
        
        base = f"{character_part} en {location_part}, {mood_part}"
        
        # Añadir calidad y estilo base
        base += ", alta calidad, renderizado detallado, estilo cinematografico"
        
        return base
    
    def _add_technical_details(self, style: str, detail_level: str, elements: Dict[str, Any]) -> str:
        """Añade detalles técnicos según estilo y nivel"""
        details = []
        
        # Seleccionar elementos técnicos apropiados
        camera_angle = random.choice(self.camera_angles)
        lighting = random.choice(self.lighting_styles)
        color_palette = random.choice(self.color_palettes)
        movement = random.choice(self.movement_types)
        
        if style == "cinematografico":
            details.extend([camera_angle, lighting, movement])
            if detail_level in ["medio", "detallado"]:
                details.append(color_palette)
                details.append("profundidad de campo")
        elif style == "artistico":
            details.extend([lighting, color_palette])
            if detail_level in ["medio", "detallado"]:
                details.append("estilo pictorico")
                details.append("textura artistica")
        elif style == "realista":
            details.extend(["iluminacion natural", "colores realistas"])
            if detail_level in ["medio", "detallado"]:
                details.append("texturas fotorrealistas")
        elif style == "fantasia":
            details.extend(["iluminacion magica", "colores fantasticos"])
            if detail_level in ["medio", "detallado"]:
                details.append("efectos magicos")
                details.append("atmosfera sobrenatural")
        
        if detail_level == "detallado":
            details.extend([
                "ultra alta definicion",
                "efectos de particulas",
                "renderizado volumetrico"
            ])
        
        return ", ".join(details)
    
    def _create_variations(self, base_prompt: str, technical_details: str) -> List[str]:
        """Crea variaciones del prompt principal"""
        variations = []
        
        # Variación 1: Diferente ángulo de cámara
        alt_camera = random.choice(self.camera_angles)
        var1 = base_prompt + f", {alt_camera}, {technical_details}"
        variations.append(var1)
        
        # Variación 2: Diferente iluminación
        alt_lighting = random.choice(self.lighting_styles)
        var2 = base_prompt + f", {alt_lighting}, {technical_details}"
        variations.append(var2)
        
        # Variación 3: Enfoque en detalles
        var3 = base_prompt + f", primer plano detallado, {technical_details}"
        variations.append(var3)
        
        return variations
