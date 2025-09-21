# Configuración de la aplicación awa (AquaReminder)

# Paleta de colores moderna
class Colors:
    # Colores principales (azules/turquesa)
    PRIMARY = "#04a4b4"           # Azul principal
    PRIMARY_DARK = "#045273"      # Azul oscuro
    PRIMARY_LIGHT = "#19bcc3"     # Turquesa claro
    SECONDARY = "#96bcc1"         # Azul secundario
    ACCENT = "#fbfaec"            # Crema/beige claro
    BACKGROUND = "#f8f9fa"        # Fondo principal
    
    # Colores secundarios (grises/neutros)
    GREY_LIGHT = "#cbe0dc"        # Gris verdoso claro
    GREY_MEDIUM = "#96bcc1"       # Gris azulado medio
    GREY_DARK = "#c4d0cc"         # Gris verdoso
    GREY_BLUE = "#c4c4cc"         # Gris azulado
    GREY_SAGE = "#7ca4a4"         # Gris salvia

    # Colores de texto
    TEXT_PRIMARY = "#2c3e50"      # Texto principal oscuro
    TEXT_SECONDARY = "#7f8c8d"    # Texto secundario
    TEXT_LIGHT = "#ffffff"        # Texto claro
    
    # Colores de estado
    SUCCESS = "#27ae60"           # Verde éxito
    WARNING = "#f39c12"           # Naranja advertencia
    ERROR = "#e74c3c"             # Rojo error

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