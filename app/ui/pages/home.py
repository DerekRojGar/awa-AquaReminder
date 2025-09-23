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


def _quick_button(text: str, amount_ml: int, page: ft.Page, goal_ml: int, total_text: ft.Text, progress_bar: ft.ProgressBar, progress_text: ft.Text):
    def on_click(e):
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
    
    return ft.Container(
        content=ft.Text(
            text,
            size=Design.FONT_SIZE_NORMAL,
            weight=Colors.get_font_weight("SEMIBOLD"),
            color=Colors.TEXT_LIGHT,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(vertical=Design.SPACE_SM, horizontal=Design.SPACE_MD),
        border_radius=Design.BORDER_RADIUS_LG,
        on_click=on_click,
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=ft.with_opacity(0.3, Colors.PRIMARY),
            offset=ft.Offset(0, 4),
        ),
        expand=True,
        alignment=ft.alignment.center,
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

    # Acciones rápidas modernizadas
    quick_actions = ft.Column([
        ft.Text(
            "Registrar consumo", 
            size=Design.FONT_SIZE_MEDIUM, 
            color=Colors.TEXT_PRIMARY,
            weight=Colors.get_font_weight("SEMIBOLD"),
        ),
        ft.Container(height=Design.SPACE_SM),
        ft.Row([
            _quick_button("+250 ml", 250, page, goal_ml, total_text, progress_bar_functional, progress_text),
            ft.Container(width=Design.SPACE_SM),
            _quick_button("+350 ml", 350, page, goal_ml, total_text, progress_bar_functional, progress_text),
            ft.Container(width=Design.SPACE_SM),
            _quick_button("+500 ml", 500, page, goal_ml, total_text, progress_bar_functional, progress_text),
        ]),
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
