# Configuración de la aplicación awa (AquaReminder)

# Paleta de colores moderna
class ColorsTheme:
    def __init__(self):
        self._dark_mode = False
    
    def set_dark_mode(self, enabled: bool):
        self._dark_mode = enabled
    
    def is_dark_mode(self) -> bool:
        return self._dark_mode
    
    # Colores principales (azules/turquesa) - Light Mode
    PRIMARY = "#04a4b4"           # Azul principal
    PRIMARY_DARK = "#045273"      # Azul oscuro
    PRIMARY_LIGHT = "#19bcc3"     # Turquesa claro
    SECONDARY = "#96bcc1"         # Azul secundario
    
    # Colores principales - Dark Mode
    PRIMARY_DARK_MODE = "#19bcc3"      # Turquesa claro (más visible en oscuro)
    PRIMARY_DARK_DARK_MODE = "#04a4b4" # Azul principal
    SECONDARY_DARK_MODE = "#7ca4a4"    # Gris salvia
    
    # Colores de estado (iguales en ambos modos)
    SUCCESS = "#27ae60"           # Verde éxito
    WARNING = "#f39c12"           # Naranja advertencia
    ERROR = "#e74c3c"             # Rojo error
    
    # Propiedades dinámicas basadas en el modo
    @property
    def ACCENT(self) -> str:
        return "#2c2c2e" if self._dark_mode else "#fbfaec"
    
    @property
    def BACKGROUND(self) -> str:
        return "#1c1c1e" if self._dark_mode else "#f8f9fa"
    
    @property
    def GREY_LIGHT(self) -> str:
        return "#3a3a3c" if self._dark_mode else "#cbe0dc"
    
    @property
    def GREY_MEDIUM(self) -> str:
        return "#48484a" if self._dark_mode else "#96bcc1"
    
    @property
    def GREY_DARK(self) -> str:
        return "#636366" if self._dark_mode else "#c4d0cc"
    
    @property
    def GREY_BLUE(self) -> str:
        return "#636366" if self._dark_mode else "#c4c4cc"
    
    @property
    def GREY_SAGE(self) -> str:
        return "#8e8e93" if self._dark_mode else "#7ca4a4"
    
    @property
    def TEXT_PRIMARY(self) -> str:
        return "#ffffff" if self._dark_mode else "#2c3e50"
    
    @property
    def TEXT_SECONDARY(self) -> str:
        return "#8e8e93" if self._dark_mode else "#7f8c8d"
    
    @property
    def TEXT_LIGHT(self) -> str:
        return "#ffffff" if self._dark_mode else "#ffffff"

# Instancia singleton global
Colors = ColorsTheme()

# Configuración de diseño
class Design:
    # Tamaños de fuente
    FONT_SIZE_LARGE = 32
    FONT_SIZE_MEDIUM = 20
    FONT_SIZE_NORMAL = 16
    FONT_SIZE_SMALL = 14
    
    # Espaciado
    PADDING_LARGE = 32
    PADDING_MEDIUM = 20
    PADDING_SMALL = 12
    SPACING_LARGE = 24
    SPACING_MEDIUM = 16
    SPACING_SMALL = 8
    
    # Bordes y sombras
    BORDER_RADIUS = 16
    BORDER_RADIUS_SMALL = 8
    ELEVATION = 4

# Configuración de la aplicación
class App:
    # Meta diaria por defecto (ml)
    DAILY_GOAL_DEFAULT = 2000
    
    # Intervalos de recordatorio (minutos)
    REMINDER_INTERVALS = [30, 60, 90, 120]
    
    # Cantidades rápidas (ml)
    QUICK_AMOUNTS = [250, 350, 500, 750]