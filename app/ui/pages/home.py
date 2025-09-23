import flet as ft
from config import Colors, Design
from services.intake_service import add_intake, get_today_total
from services.profile_service import load_profile


# Compat: algunas versiones de Flet no exponen with_opacity; usamos nuestro helper
ft.with_opacity = Colors.with_opacity


def _current_tab_index(route: str) -> int:
    if route in ("/", ""):  # inicio
        return 0
    if route.startswith("/history"):
        return 1
    if route.startswith("/profile"):
        return 2
    if route.startswith("/settings"):
        return 3
    return 0


def _nav_item(label: str, icon, active: bool, on_click):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(
                        icon, 
                        size=Design.ICON_SIZE_LG, 
                        color=Colors.TEXT_LIGHT if active else Colors.TEXT_SECONDARY
                    ),
                    width=40,
                    height=40,
                    bgcolor=Colors.PRIMARY if active else Colors.SURFACE,
                    border_radius=Design.BORDER_RADIUS_SM,
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    label, 
                    size=Design.FONT_SIZE_CAPTION, 
                    color=Colors.TEXT_PRIMARY if active else Colors.TEXT_SECONDARY,
                    weight=Colors.get_font_weight("MEDIUM") if active else ft.FontWeight.NORMAL,
                ),
            ],
            spacing=Design.SPACE_XXXS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=Design.SPACE_XS, horizontal=Design.SPACE_XXS),
        on_click=on_click,
        expand=True,
    )


def _bottom_nav(page: ft.Page):
    idx = _current_tab_index(page.route)

    return ft.Container(
        content=ft.Row(
            [
                _nav_item("Inicio", ft.Icons.HOME_ROUNDED, idx == 0, lambda e: page.go("/")),
                _nav_item("Historial", ft.Icons.ANALYTICS_ROUNDED, idx == 1, lambda e: page.go("/history")),
                _nav_item("Perfil", ft.Icons.PERSON_ROUNDED, idx == 2, lambda e: page.go("/profile")),
                _nav_item("Ajustes", ft.Icons.SETTINGS_ROUNDED, idx == 3, lambda e: page.go("/settings")),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=Colors.CARD_BACKGROUND,
        padding=ft.padding.only(left=Design.SPACE_SM, right=Design.SPACE_SM, top=Design.SPACE_XS, bottom=Design.SPACE_XS),
        border=ft.border.only(top=ft.border.BorderSide(1, Colors.BORDER)),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.with_opacity(0.1, Colors.DARK_NAVY),
            offset=ft.Offset(0, -4),
        ),
    )


# Lista global para almacenar ingestas personalizadas
custom_intakes = []

def _add_intake_and_update(amount_ml: int, page: ft.Page, goal_ml: int, total_text: ft.Text, progress_bar: ft.ProgressBar, progress_text: ft.Text):
    """Función auxiliar para agregar ingesta y actualizar UI"""
    add_intake(amount_ml)
    # Feedback visual mejorado
    page.snack_bar = ft.SnackBar(
        content=ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=Colors.TEXT_LIGHT, size=Design.ICON_SIZE_MD),
            ft.Text(f"+{amount_ml} ml registrados", color=Colors.TEXT_LIGHT, weight=Colors.get_font_weight("MEDIUM")),
        ], spacing=Design.SPACE_XS),
        bgcolor=Colors.SUCCESS,
        shape=ft.RoundedRectangleBorder(radius=Design.BORDER_RADIUS_SM),
    )
    page.snack_bar.open = True
    
    # Actualizar total y progreso
    total = get_today_total()
    total_text.value = f"{total:,} ml"
    ratio = min(total / max(goal_ml, 1), 1.0)
    progress_bar.value = ratio
    progress_bar.color = Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY
    progress_text.value = f"{total:,} / {goal_ml:,} ml"
    page.update()

def _drink_icon_button(icon, label: str, amount_ml: int, page: ft.Page, goal_ml: int, total_text: ft.Text, progress_bar: ft.ProgressBar, progress_text: ft.Text, color=None):
    def on_click(e):
        _add_intake_and_update(amount_ml, page, goal_ml, total_text, progress_bar, progress_text)
    
    btn_color = color or Colors.PRIMARY
    
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(
                    icon,
                    size=32,  # Tamaño más pequeño para móvil
                    color=Colors.TEXT_LIGHT,
                ),
                width=60,  # Tamaño más compacto
                height=60,
                bgcolor=btn_color,
                border_radius=Design.BORDER_RADIUS_LG,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.with_opacity(0.15, btn_color),
                    offset=ft.Offset(0, 2),
                ),
            ),
            ft.Container(height=4),  # Espaciado reducido
            ft.Text(
                label,
                size=Design.FONT_SIZE_CAPTION,  # Texto más pequeño
                weight=Colors.get_font_weight("MEDIUM"),
                color=Colors.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text(
                f"{amount_ml} ml",
                size=10,  # Texto muy pequeño para cantidad
                color=Colors.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        on_click=on_click,
        ink=True,
        border_radius=Design.BORDER_RADIUS_SM,
        padding=ft.padding.all(8),  # Padding reducido
        width=80,  # Ancho fijo para consistencia
    )


def _show_custom_intake_form(page: ft.Page, goal_ml: int, total_text: ft.Text, progress_bar: ft.ProgressBar, progress_text: ft.Text, custom_drinks_row: ft.Row):
    """Muestra formulario simple para crear ingesta personalizada"""
    
    # Variables para el formulario
    amount_input = ft.TextField(
        label="Cantidad (ml)",
        hint_text="Ej: 300",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        value="300"
    )
    
    # Iconos predefinidos simples
    icon_options = [
        ft.Icons.LOCAL_CAFE,
        ft.Icons.WINE_BAR, 
        ft.Icons.SPORTS_BAR,
        ft.Icons.LOCAL_DRINK,
        ft.Icons.COFFEE,
        ft.Icons.EMOJI_FOOD_BEVERAGE,
    ]
    
    # Variable para el índice del icono seleccionado
    selected_icon_index = [0]  # Usar lista para permitir modificación
    
    def create_icon_button(icon, index):
        def on_select(e):
            selected_icon_index[0] = index  # Modificar el valor en la lista
            # Actualizar visual de selección
            for i, btn in enumerate(icon_row.controls):
                btn.bgcolor = Colors.PRIMARY if i == index else Colors.SURFACE
                btn.border = ft.border.all(2, Colors.PRIMARY) if i == index else ft.border.all(1, Colors.BORDER)
            page.update()
        
        return ft.Container(
            content=ft.Icon(icon, size=24, color=Colors.TEXT_PRIMARY),
            width=50,
            height=50,
            bgcolor=Colors.PRIMARY if index == 0 else Colors.SURFACE,
            border=ft.border.all(2, Colors.PRIMARY) if index == 0 else ft.border.all(1, Colors.BORDER),
            border_radius=Design.BORDER_RADIUS_SM,
            alignment=ft.alignment.center,
            on_click=on_select,
            ink=True,
        )
    
    icon_row = ft.Row([
        create_icon_button(icon, i) for i, icon in enumerate(icon_options)
    ], spacing=8, wrap=True)
    
    def add_custom_drink(e):
        try:
            amount = int(amount_input.value or 0)
            if amount <= 0:
                return
                
            # Agregar la ingesta
            _add_intake_and_update(amount, page, goal_ml, total_text, progress_bar, progress_text)
            
            # Crear botón personalizado
            selected_icon = icon_options[selected_icon_index[0]]  # Usar el valor de la lista
            
            custom_button = _drink_icon_button(
                selected_icon,
                f"{amount}ml",
                amount,
                page,
                goal_ml,
                total_text,
                progress_bar,
                progress_text,
                color=Colors.PRIMARY_LIGHT
            )
            
            # Agregar a la fila de bebidas personalizadas
            custom_drinks_row.controls.append(custom_button)
            
            # Limpiar formulario
            amount_input.value = "300"
            selected_icon_index[0] = 0  # Reiniciar selección usando la lista
            
            # Ocultar formulario
            form_container.visible = False
            add_button_container.visible = True
            
            page.update()
            
        except ValueError:
            # Error de conversión - mostrar mensaje
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor ingresa un número válido", color=Colors.TEXT_LIGHT),
                bgcolor=Colors.ERROR,
            )
            page.snack_bar.open = True
            page.update()
    
    def cancel_form(e):
        form_container.visible = False
        add_button_container.visible = True
        page.update()
    
    def show_form(e):
        form_container.visible = True
        add_button_container.visible = False
        page.update()
    
    # Contenedor del formulario (inicialmente oculto)
    form_container = ft.Container(
        content=ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Nueva ingesta personalizada", size=Design.FONT_SIZE_NORMAL, weight=Colors.get_font_weight("SEMIBOLD")),
                    ft.Container(height=Design.SPACE_SM),
                    amount_input,
                    ft.Container(height=Design.SPACE_SM),
                    ft.Text("Selecciona un icono:", size=Design.FONT_SIZE_SMALL),
                    icon_row,
                    ft.Container(height=Design.SPACE_SM),
                    ft.Row([
                        ft.ElevatedButton("Cancelar", on_click=cancel_form, bgcolor=Colors.SURFACE, color=Colors.TEXT_PRIMARY),
                        ft.ElevatedButton("Agregar", on_click=add_custom_drink, bgcolor=Colors.PRIMARY, color=Colors.TEXT_LIGHT),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ], spacing=Design.SPACE_XS),
                padding=ft.padding.all(Design.SPACE_MD),
            ),
            elevation=8,
        ),
        visible=False,
        margin=ft.margin.symmetric(horizontal=Design.SPACE_SM),
    )
    
    # Botón de agregar (inicialmente visible)
    add_button_container = ft.Container(
        content=_add_custom_button_direct(show_form),
        visible=True,
    )
    
    return form_container, add_button_container

def _add_custom_button_direct(on_click_handler):
    """Botón simple para mostrar formulario"""
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.ADD_CIRCLE_OUTLINE,
                    size=32,
                    color=Colors.TEXT_SECONDARY,
                ),
                width=60,
                height=60,
                bgcolor=Colors.SURFACE,
                border=ft.border.all(1, Colors.BORDER),
                border_radius=Design.BORDER_RADIUS_LG,
                alignment=ft.alignment.center,
            ),
            ft.Container(height=4),
            ft.Text(
                "Agregar",
                size=Design.FONT_SIZE_CAPTION,
                color=Colors.TEXT_SECONDARY,
                weight=Colors.get_font_weight("MEDIUM"),
                text_align=ft.TextAlign.CENTER,
                max_lines=1,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        on_click=on_click_handler,
        border_radius=Design.BORDER_RADIUS_SM,
        padding=ft.padding.all(8),
        ink=True,
        width=80,
    )


def create_home_page(page: ft.Page):
    # Cargar meta y datos del perfil
    profile = load_profile() or {}
    goal_ml = int(profile.get("daily_goal_ml", 2000) or 2000)
    user_name = (profile.get("name") or "").strip()
    avatar_id = int(profile.get("avatar_id", 0) or 0)

    # Avatar usando imágenes reales (dentro de assets/ del APK)
    avatar_files = [
        "avatares/Avatar1.jpg",
        "avatares/Avatar2.jpg",
        "avatares/Avatar3.jpg",
        "avatares/Avatar4.jpg",
    ]
    avatar_icons = [ft.Icons.PERSON, ft.Icons.FACE, ft.Icons.ACCOUNT_CIRCLE, ft.Icons.SUPERVISED_USER_CIRCLE]
    
    src = avatar_files[avatar_id % len(avatar_files)]
    fallback_icon = avatar_icons[avatar_id % len(avatar_icons)]
    
    avatar = ft.Container(
        content=ft.Container(
            content=ft.Image(
                src, 
                fit=ft.ImageFit.COVER, 
                width=48, 
                height=48,
                error_content=ft.Icon(fallback_icon, size=Design.ICON_SIZE_LG, color=Colors.PRIMARY)
            ),
            width=48,
            height=48,
            border_radius=Design.BORDER_RADIUS_FULL,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        ),
        padding=ft.padding.all(2),
        bgcolor=Colors.PRIMARY,
        border_radius=Design.BORDER_RADIUS_FULL,
        on_click=lambda e: page.go("/profile"),
        tooltip="Editar perfil",
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.with_opacity(0.2, Colors.PRIMARY),
            offset=ft.Offset(0, 2),
        ),
    )

    # Total diario inicial
    total = get_today_total()
    total_text = ft.Text(
        f"{total:,} ml", 
        size=Design.FONT_SIZE_HERO, 
        weight=ft.FontWeight.BOLD, 
        color=Colors.TEXT_PRIMARY
    )

    # Barra de progreso moderna
    ratio = min(total / max(goal_ml, 1), 1.0)
    progress_bar = ft.Container(
        content=ft.Container(
            bgcolor=Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY,
            border_radius=Design.BORDER_RADIUS_FULL,
            height=8,
        ),
        bgcolor=Colors.GREY_LIGHT,
        border_radius=Design.BORDER_RADIUS_FULL,
        height=8,
        width=None,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )
    
    # Usar ProgressBar tradicional para la funcionalidad
    progress_bar_functional = ft.ProgressBar(
        value=ratio, 
        color=Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY, 
        bgcolor=Colors.GREY_LIGHT,
        height=8,
        border_radius=Design.BORDER_RADIUS_FULL,
    )
    
    progress_text = ft.Text(
        f"{total:,} / {goal_ml:,} ml", 
        size=Design.FONT_SIZE_SMALL, 
        color=Colors.TEXT_SECONDARY,
        weight=Colors.get_font_weight("MEDIUM"),
    )

    # Encabezado moderno con gradiente
    title_text = f"Hola, {user_name}" if user_name else "awa"
    header = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(
                            title_text, 
                            size=Design.FONT_SIZE_LARGE, 
                            weight=ft.FontWeight.BOLD, 
                            color=Colors.TEXT_LIGHT
                        ),
                        ft.Text(
                            "Mantente hidratado hoy", 
                            size=Design.FONT_SIZE_SMALL, 
                            color=ft.with_opacity(0.8, Colors.TEXT_LIGHT)
                        ),
                    ], expand=True, spacing=Design.SPACE_XXXS),
                    avatar,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(horizontal=Design.SPACE_LG, vertical=Design.SPACE_MD),
            ),
        ]),
        bgcolor=Colors.PRIMARY,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=Colors.GRADIENT_PRIMARY,
        ),
    )

    # Tarjeta de progreso diario moderna
    daily_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(
                    "Consumo de hoy", 
                    size=Design.FONT_SIZE_MEDIUM, 
                    color=Colors.TEXT_PRIMARY,
                    weight=Colors.get_font_weight("SEMIBOLD"),
                ),
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.WATER_DROP_ROUNDED, 
                        color=Colors.PRIMARY, 
                        size=Design.ICON_SIZE_LG
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(height=Design.SPACE_SM),
            
            total_text,
            
            ft.Container(height=Design.SPACE_MD),
            
            ft.Column([
                progress_bar_functional,
                ft.Container(height=Design.SPACE_XS),
                ft.Row([
                    progress_text,
                    ft.Text(
                        f"Meta {goal_ml:,} ml", 
                        size=Design.FONT_SIZE_SMALL, 
                        color=Colors.TEXT_TERTIARY,
                        weight=Colors.get_font_weight("MEDIUM"),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], spacing=0),
            
            ft.Container(height=Design.SPACE_XS),
            
            # Porcentaje de completitud
            ft.Text(
                f"{int(ratio * 100)}% completado",
                size=Design.FONT_SIZE_CAPTION,
                color=Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY,
                weight=Colors.get_font_weight("SEMIBOLD"),
            ),
        ], spacing=0),
        padding=ft.padding.all(Design.SPACE_LG),
        bgcolor=Colors.CARD_BACKGROUND,
        border_radius=Design.BORDER_RADIUS_XL,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.with_opacity(0.08, Colors.DARK_NAVY),
            offset=ft.Offset(0, 4),
        ),
    )

    # Fila para bebidas personalizadas (se llenará dinámicamente) - Responsive
    custom_drinks_row = ft.Row([], alignment=ft.MainAxisAlignment.START, spacing=8, wrap=True)
    
    # Crear formulario de ingesta personalizada
    form_container, add_button_container = _show_custom_intake_form(page, goal_ml, total_text, progress_bar_functional, progress_text, custom_drinks_row)
    
    # Acciones rápidas con iconos modernos y mejorados
    quick_actions = ft.Column([
        ft.Text(
            "Registrar consumo", 
            size=Design.FONT_SIZE_MEDIUM, 
            color=Colors.TEXT_PRIMARY,
            weight=Colors.get_font_weight("SEMIBOLD"),
        ),
        ft.Container(height=Design.SPACE_SM),
        # Bebidas predefinidas con mejores iconos - Layout responsive
        ft.Row([
            _drink_icon_button(ft.Icons.WINE_BAR, "Vaso", 250, page, goal_ml, total_text, progress_bar_functional, progress_text),
            _drink_icon_button(ft.Icons.LOCAL_DRINK, "Botella", 500, page, goal_ml, total_text, progress_bar_functional, progress_text),
            _drink_icon_button(ft.Icons.COFFEE, "Termo", 750, page, goal_ml, total_text, progress_bar_functional, progress_text),
            add_button_container,  # Usar el contenedor del botón de agregar
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=8),
        ft.Container(height=Design.SPACE_SM),
        # Formulario para agregar ingestas personalizadas
        form_container,
        # Fila de bebidas personalizadas (inicialmente vacía)
        ft.Container(
            content=custom_drinks_row,
            visible=True,  # Siempre visible, se llena dinámicamente
        ),
    ])

    # Tarjeta de sugerencias moderna
    tip_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED, 
                    color=Colors.PRIMARY,
                    size=Design.ICON_SIZE_LG,
                ),
                width=48,
                height=48,
                bgcolor=ft.with_opacity(0.1, Colors.PRIMARY),
                border_radius=Design.BORDER_RADIUS_SM,
                alignment=ft.alignment.center,
            ),
            ft.Container(width=Design.SPACE_SM),
            ft.Container(expand=True, 
                content=ft.Column([
                    ft.Text(
                        "Recordatorios inteligentes", 
                        size=Design.FONT_SIZE_NORMAL,
                        color=Colors.TEXT_PRIMARY,
                        weight=Colors.get_font_weight("SEMIBOLD"),
                    ),
                    ft.Text(
                        "Activa recordatorios para no olvidar hidratarte durante el día", 
                        size=Design.FONT_SIZE_SMALL,
                        color=Colors.TEXT_SECONDARY,
                    ),
                ], spacing=Design.SPACE_XXXS),
            ),
            ft.Icon(
                ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                color=Colors.TEXT_TERTIARY,
                size=Design.ICON_SIZE_SM,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.all(Design.SPACE_LG),
        bgcolor=Colors.CARD_BACKGROUND,
        border_radius=Design.BORDER_RADIUS_LG,
        on_click=lambda e: page.go("/settings"),
        ink=True,
        border=ft.border.all(1, Colors.BORDER),
    )

    body = ft.Container(
        content=ft.Column([
            daily_card,
            ft.Container(height=Design.SPACE_LG),
            quick_actions,
            ft.Container(height=Design.SPACE_LG),
            tip_card,
            ft.Container(height=Design.SPACE_MD),  # Espacio extra al final
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        padding=ft.padding.symmetric(horizontal=Design.SPACE_LG, vertical=Design.SPACE_LG),
        expand=True,
        bgcolor=Colors.BACKGROUND,
    )

    # Compose with SafeArea: top for header/body, bottom for bottom nav
    content = ft.Column([
        ft.SafeArea(
            content=ft.Column([
                header,
                body,
            ], spacing=0, expand=True),
            top=True,
            bottom=False,
            expand=True,
        ),
        ft.SafeArea(
            content=_bottom_nav(page),
            top=False,
            bottom=True,
        ),
    ], spacing=0, expand=True)

    return ft.View(
        "/",
        [content],
        padding=ft.padding.all(0),
        bgcolor=Colors.BACKGROUND,
    )
