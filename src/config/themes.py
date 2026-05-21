"""
Configuración de colores y temas para MoodDay
Paleta basada en colores calmantes para emociones
"""

# Paleta de colores calmante para MoodDay
class MoodDayTheme:
    # Colores principales (azules y verdes suaves - colores calmantes)
    PRIMARY = "#5B9FBF"  # Azul suave - calma
    SECONDARY = "#6DB5A9"  # Verde azulado - serenidad
    ACCENT = "#A8D5BA"  # Verde menta suave - paz
    
    # Fondos
    BACKGROUND_LIGHT = "#F0F7FB"  # Fondo muy claro
    BACKGROUND_CARD = "#FFFFFF"  # Blanco para tarjetas
    BACKGROUND_SECONDARY = "#E8F1F8"  # Gris azulado muy claro
    
    # Colores de emociones
    EMOTION_HAPPY = "#FFD93D"  # Amarillo cálido - alegría
    EMOTION_SAD = "#6DB5A9"  # Verde azulado - tristeza
    EMOTION_ANGRY = "#E97451"  # Coral suave - enojo
    EMOTION_ANXIOUS = "#9B8EC1"  # Púrpura suave - ansiedad
    EMOTION_CALM = "#A8D5BA"  # Verde menta - calma
    EMOTION_NEUTRAL = "#B0A8C1"  # Gris púrpura - neutro
    
    # Estados
    SUCCESS = "#6DB5A9"  # Verde azulado para éxito
    ERROR = "#E97451"  # Coral para error
    WARNING = "#F4D35E"  # Amarillo suave para advertencia
    INFO = "#5B9FBF"  # Azul para información
    
    # Texto
    TEXT_PRIMARY = "#2C3E50"  # Gris oscuro suave
    TEXT_SECONDARY = "#556E7D"  # Gris medio
    TEXT_LIGHT = "#FFFFFF"  # Blanco
    
    # Bordes
    BORDER_COLOR = "#D4E5F0"  # Gris azulado claro
    
    # Valores específicos
    BORDER_RADIUS = 15  # Radio de borde estándar
    PADDING_STANDARD = 20  # Padding estándar
    SPACING_STANDARD = 15  # Espaciado estándar


# Estilos predefinidos
class MoodDayStyles:
    @staticmethod
    def get_appbar_style():
        """Retorna el estilo del AppBar"""
        return {
            "bgcolor": MoodDayTheme.PRIMARY,
            "color": MoodDayTheme.TEXT_LIGHT,
        }
    
    @staticmethod
    def get_button_style(color=None):
        """Retorna el estilo para botones"""
        return {
            "bgcolor": color or MoodDayTheme.PRIMARY,
            "color": MoodDayTheme.TEXT_LIGHT,
            "height": 45,
        }
    
    @staticmethod
    def get_textfield_style():
        """Retorna el estilo para campos de texto"""
        return {
            "border_radius": MoodDayTheme.BORDER_RADIUS,
            "text_size": 16,
            "border_color": MoodDayTheme.BORDER_COLOR,
        }
    
    @staticmethod
    def get_card_style():
        """Retorna el estilo para tarjetas"""
        return {
            "bgcolor": MoodDayTheme.BACKGROUND_CARD,
            "border_radius": MoodDayTheme.BORDER_RADIUS,
            "elevation": 2,
        }
    
    @staticmethod
    def get_container_style():
        """Retorna el estilo para contenedores principales"""
        return {
            "bgcolor": MoodDayTheme.BACKGROUND_LIGHT,
            "border_radius": MoodDayTheme.BORDER_RADIUS,
            "padding": MoodDayTheme.PADDING_STANDARD,
        }
