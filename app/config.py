# Configuración de la aplicación awa (AquaReminder)

# Paleta de colores moderna - Gradients App Style
class ColorsTheme:
    def __init__(self):
        self._dark_mode = False
    
    def set_dark_mode(self, enabled: bool):
        self._dark_mode = enabled
    
    def is_dark_mode(self) -> bool:
        return self._dark_mode
    
    # Utilidad: aplicar opacidad a un color HEX (retorna rgba)
    @staticmethod
    def with_opacity(opacity: float, hex_color: str) -> str:
        """Convierte un color HEX (#RRGGBB) y una opacidad [0-1] a cadena rgba(r,g,b,a).
        Evita dependencia de ft.colors.with_opacity para compatibilidad entre versiones de Flet.
        """
        try:
            h = hex_color.lstrip('#')
            if len(h) == 3:  # e.g. #abc
                h = ''.join([c*2 for c in h])
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            a = max(0.0, min(1.0, float(opacity)))
            return f"rgba({r}, {g}, {b}, {a})"
        except Exception:
            # Fallback sin opacidad
            return hex_color
    
    # Utilidad: compatibilidad para FontWeight
    @staticmethod
    def get_font_weight(weight_name: str):
        """Obtiene el FontWeight compatible con versiones antiguas de Flet."""
        import flet as ft
        # Mapeo de nombres a valores numéricos o atributos disponibles
        weight_map = {
            'LIGHT': getattr(ft.FontWeight, 'W_300', ft.FontWeight.W_300) if hasattr(ft.FontWeight, 'W_300') else ft.FontWeight.NORMAL,
            'NORMAL': ft.FontWeight.NORMAL,
            'MEDIUM': getattr(ft.FontWeight, 'W_500', ft.FontWeight.BOLD) if hasattr(ft.FontWeight, 'W_500') else ft.FontWeight.NORMAL,
            'SEMIBOLD': getattr(ft.FontWeight, 'W_600', ft.FontWeight.BOLD) if hasattr(ft.FontWeight, 'W_600') else ft.FontWeight.BOLD,
            'BOLD': ft.FontWeight.BOLD,
        }
        return weight_map.get(weight_name, ft.FontWeight.NORMAL)
    
    # Nueva paleta de colores moderna (basada en Gradients.app)
    DARK_NAVY = "#040513"         # Azul marino muy oscuro
    CORAL_RED = "#FB5B4B"         # Rojo coral vibrante
    WARM_ORANGE = "#FBAD8C"       # Naranja cálido
    BRIGHT_RED = "#E6433C"        # Rojo brillante
    CHARCOAL = "#341F23"          # Carbón oscuro
    
    # Colores principales - Light Mode
    PRIMARY = "#FB5B4B"           # Coral como color principal
    PRIMARY_DARK = "#E6433C"      # Rojo brillante para contraste
    PRIMARY_LIGHT = "#FBAD8C"     # Naranja cálido para acentos
    SECONDARY = "#341F23"         # Carbón para elementos secundarios
    
    # Colores principales - Dark Mode
    PRIMARY_DARK_MODE = "#FBAD8C"      # Naranja cálido (más suave en oscuro)
    PRIMARY_DARK_DARK_MODE = "#FB5B4B" # Coral principal
    SECONDARY_DARK_MODE = "#E6433C"    # Rojo brillante para acentos
    
    # Colores de estado (actualizados para la nueva paleta)
    SUCCESS = "#27ae60"           # Verde éxito
    WARNING = "#FBAD8C"           # Naranja cálido para advertencias
    ERROR = "#E6433C"             # Rojo brillante para errores
    INFO = "#FB5B4B"              # Coral para información
    
    # Propiedades dinámicas basadas en el modo
    @property
    def ACCENT(self) -> str:
        return "#341F23" if self._dark_mode else "#FFF8F6"
    
    @property
    def BACKGROUND(self) -> str:
        return "#040513" if self._dark_mode else "#FFFFFF"
    
    @property
    def SURFACE(self) -> str:
        return "#1A1625" if self._dark_mode else "#F8F9FA"
    
    @property
    def CARD_BACKGROUND(self) -> str:
        return "#252033" if self._dark_mode else "#FFFFFF"
    
    @property
    def BORDER(self) -> str:
        return "#3A3145" if self._dark_mode else "#F0F0F0"
    
    @property
    def GREY_LIGHT(self) -> str:
        return "#4A4458" if self._dark_mode else "#F5F5F5"
    
    @property
    def GREY_MEDIUM(self) -> str:
        return "#5E5A6B" if self._dark_mode else "#E0E0E0"
    
    @property
    def GREY_DARK(self) -> str:
        return "#73707E" if self._dark_mode else "#BDBDBD"
    
    @property
    def TEXT_PRIMARY(self) -> str:
        return "#FFFFFF" if self._dark_mode else "#040513"
    
    @property
    def TEXT_SECONDARY(self) -> str:
        return "#B8B5C1" if self._dark_mode else "#6B6B6B"
    
    @property
    def TEXT_TERTIARY(self) -> str:
        return "#8E8A96" if self._dark_mode else "#9E9E9E"
    
    @property
    def TEXT_LIGHT(self) -> str:
        return "#FFFFFF"
    
    # Gradientes para elementos modernos
    @property
    def GRADIENT_PRIMARY(self) -> tuple:
        if self._dark_mode:
            return ("#FBAD8C", "#FB5B4B")
        return ("#FB5B4B", "#E6433C")
    
    @property
    def GRADIENT_SECONDARY(self) -> tuple:
        if self._dark_mode:
            return ("#341F23", "#040513")
        return ("#FBAD8C", "#FB5B4B")

# Instancia singleton global
Colors = ColorsTheme()

# Configuración de diseño moderno
class Design:
    # Tamaños de fuente (mejorados para mejor jerarquía)
    FONT_SIZE_HERO = 48           # Para títulos principales
    FONT_SIZE_LARGE = 32          # Para títulos de sección
    FONT_SIZE_TITLE = 24          # Para títulos de cards
    FONT_SIZE_MEDIUM = 20         # Para subtítulos
    FONT_SIZE_NORMAL = 16         # Para texto normal
    FONT_SIZE_SMALL = 14          # Para texto secundario
    FONT_SIZE_CAPTION = 12        # Para captions y labels
    
    # Pesos de fuente
    FONT_WEIGHT_LIGHT = 300
    FONT_WEIGHT_NORMAL = 400
    FONT_WEIGHT_MEDIUM = 500
    FONT_WEIGHT_SEMIBOLD = 600
    FONT_WEIGHT_BOLD = 700
    
    # Espaciado moderno (sistema de 8px)
    SPACE_XXXS = 4                # Micro spacing
    SPACE_XXS = 8                 # Extra extra small
    SPACE_XS = 12                 # Extra small
    SPACE_SM = 16                 # Small
    SPACE_MD = 24                 # Medium
    SPACE_LG = 32                 # Large
    SPACE_XL = 48                 # Extra large
    SPACE_XXL = 64                # Extra extra large
    SPACE_XXXL = 96               # Ultra large
    
    # Legacy spacing (mantener compatibilidad)
    PADDING_LARGE = SPACE_LG
    PADDING_MEDIUM = SPACE_MD
    PADDING_SMALL = SPACE_XS
    SPACING_LARGE = SPACE_MD
    SPACING_MEDIUM = SPACE_SM
    SPACING_SMALL = SPACE_XXS
    
    # Bordes y radios modernos
    BORDER_RADIUS_NONE = 0
    BORDER_RADIUS_SM = 8          # Pequeño
    BORDER_RADIUS_MD = 12         # Medio
    BORDER_RADIUS_LG = 16         # Grande
    BORDER_RADIUS_XL = 24         # Extra grande
    BORDER_RADIUS_FULL = 9999     # Completamente redondeado
    
    # Legacy radius
    BORDER_RADIUS = BORDER_RADIUS_LG
    BORDER_RADIUS_SMALL = BORDER_RADIUS_SM
    
    # Sombras modernas
    SHADOW_NONE = "none"
    SHADOW_SM = "0 1px 2px rgba(0, 0, 0, 0.05)"
    SHADOW_MD = "0 4px 6px rgba(0, 0, 0, 0.07)"
    SHADOW_LG = "0 10px 15px rgba(0, 0, 0, 0.1)"
    SHADOW_XL = "0 20px 25px rgba(0, 0, 0, 0.15)"
    
    # Legacy elevation
    ELEVATION = 4
    
    # Dimensiones de componentes
    BUTTON_HEIGHT_SM = 32
    BUTTON_HEIGHT_MD = 40
    BUTTON_HEIGHT_LG = 48
    BUTTON_HEIGHT_XL = 56
    
    INPUT_HEIGHT_SM = 36
    INPUT_HEIGHT_MD = 44
    INPUT_HEIGHT_LG = 52
    
    ICON_SIZE_XS = 12
    ICON_SIZE_SM = 16
    ICON_SIZE_MD = 20
    ICON_SIZE_LG = 24
    ICON_SIZE_XL = 32
    ICON_SIZE_XXL = 48
    
    # Ancho máximo para contenido
    MAX_WIDTH_SM = 640
    MAX_WIDTH_MD = 768
    MAX_WIDTH_LG = 1024
    MAX_WIDTH_XL = 1280

# Configuración de la aplicación
class App:
    # Meta diaria por defecto (ml)
    DAILY_GOAL_DEFAULT = 2000
    
    # Intervalos de recordatorio (minutos)
    REMINDER_INTERVALS = [30, 60, 90, 120]
    
    # Cantidades rápidas (ml)
    QUICK_AMOUNTS = [250, 350, 500, 750]