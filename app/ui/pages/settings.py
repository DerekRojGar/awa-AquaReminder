import flet as ft
from config import Colors, Design
from services.profile_service import reset_app_data
from services.theme_service import load_theme_preference, save_theme_preference

ft.with_opacity = Colors.with_opacity


def _current_tab_index(route: str) -> int:
    if route in ("/", ""):
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


def create_settings_page(page: ft.Page) -> ft.View:
    def reset_app(e):
        def confirm_reset(e):
            close_dialog()
            success = reset_app_data()
            if success:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Datos eliminados. Reinicia la aplicación."),
                    bgcolor=Colors.SUCCESS
                )
                page.snack_bar.open = True
                page.update()
                # En Android, redirigir al onboarding en lugar de cerrar
                import time
                import threading
                def redirect_to_onboarding():
                    time.sleep(2)
                    page.go("/onboarding")
                threading.Thread(target=redirect_to_onboarding, daemon=True).start()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar datos"), bgcolor=Colors.ERROR)
                page.snack_bar.open = True
                page.update()
        
        # Diálogo de confirmación moderno
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "🗑️ Resetear aplicación",
                size=Design.FONT_SIZE_MEDIUM,
                weight=ft.FontWeight.BOLD,
                color=Colors.TEXT_PRIMARY,
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "¿Estás seguro que deseas continuar?",
                        size=Design.FONT_SIZE_NORMAL,
                        color=Colors.TEXT_PRIMARY,
                        weight=Colors.get_font_weight("MEDIUM"),
                    ),
                    ft.Container(height=Design.SPACE_XS),
                    ft.Text(
                        "Se eliminarán permanentemente:",
                        size=Design.FONT_SIZE_SMALL,
                        color=Colors.TEXT_SECONDARY,
                    ),
                    ft.Text(
                        "• Tu perfil personal\n• Historial de consumo\n• Configuraciones personalizadas",
                        size=Design.FONT_SIZE_SMALL,
                        color=Colors.TEXT_SECONDARY,
                    ),
                ], spacing=Design.SPACE_XS),
                padding=ft.padding.symmetric(vertical=Design.SPACE_XS),
            ),
            bgcolor=Colors.CARD_BACKGROUND,
            actions=[
                ft.Row([
                    ft.Container(expand=True, content=ft.Container(
                        content=ft.Text(
                            "Cancelar",
                            color=Colors.TEXT_SECONDARY,
                            weight=Colors.get_font_weight("MEDIUM"),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=Design.SPACE_SM),
                        border=ft.border.all(1, Colors.BORDER),
                        border_radius=Design.BORDER_RADIUS_SM,
                        on_click=lambda e: close_dialog(),
                        ink=True,
                    )),
                    ft.Container(width=Design.SPACE_SM),
                    ft.Container(expand=True, content=ft.Container(
                        content=ft.Text(
                            "Sí, eliminar",
                            color=Colors.TEXT_LIGHT,
                            weight=Colors.get_font_weight("SEMIBOLD"),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=Design.SPACE_SM),
                        bgcolor=Colors.ERROR,
                        border_radius=Design.BORDER_RADIUS_SM,
                        on_click=confirm_reset,
                        ink=True,
                    )),
                ]),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        def close_dialog():
            dlg.open = False
            page.update()
        
        page.dialog = dlg
        dlg.open = True
        page.update()

    def toggle_dark_mode(e):
        # Alternar tema
        current_dark = load_theme_preference()
        new_dark = not current_dark
        save_theme_preference(new_dark)
        
        # Aplicar tema inmediatamente
        Colors.set_dark_mode(new_dark)
        page.theme_mode = ft.ThemeMode.DARK if new_dark else ft.ThemeMode.LIGHT
        
        # Mostrar feedback moderno
        theme_name = "oscuro" if new_dark else "claro"
        page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE_ROUNDED,
                    color=Colors.TEXT_LIGHT,
                    size=Design.ICON_SIZE_MD,
                ),
                ft.Text(
                    f"Tema {theme_name} activado",
                    color=Colors.TEXT_LIGHT,
                    weight=Colors.get_font_weight("MEDIUM"),
                ),
            ], spacing=Design.SPACE_XXS),
            bgcolor=Colors.SUCCESS,
            shape=ft.RoundedRectangleBorder(radius=Design.BORDER_RADIUS_SM),
        )
        page.snack_bar.open = True
        
        # Recargar página para aplicar colores
        page.go(page.route)
        page.update()

    # Estado actual del tema
    is_dark = load_theme_preference()

    # Header moderno con gradiente
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(
                        "Ajustes", 
                        size=Design.FONT_SIZE_LARGE, 
                        weight=ft.FontWeight.BOLD, 
                        color=Colors.TEXT_LIGHT
                    ),
                    ft.Text(
                        "Personaliza tu experiencia", 
                        size=Design.FONT_SIZE_SMALL, 
                        color=ft.with_opacity(0.9, Colors.TEXT_LIGHT)
                    ),
                ], expand=True, spacing=Design.SPACE_XXXS),
                ft.Icon(
                    ft.Icons.SETTINGS_ROUNDED,
                    color=ft.with_opacity(0.3, Colors.TEXT_LIGHT),
                    size=Design.ICON_SIZE_XXL,
                ),
            ]),
        ]),
        bgcolor=Colors.PRIMARY,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=Colors.GRADIENT_PRIMARY,
        ),
        padding=ft.padding.symmetric(horizontal=Design.SPACE_LG, vertical=Design.SPACE_LG),
    )

    # Función para crear elementos de configuración modernos
    def create_setting_item(icon, title, subtitle, action_widget=None, on_click=None, text_color=None):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(
                        icon, 
                        color=text_color or Colors.PRIMARY,
                        size=Design.ICON_SIZE_LG,
                    ),
                    width=40,
                    height=40,
                    bgcolor=ft.with_opacity(0.1, text_color or Colors.PRIMARY),
                    border_radius=Design.BORDER_RADIUS_SM,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=Design.SPACE_SM),
                ft.Container(expand=True, content=ft.Column([
                    ft.Text(
                        title, 
                        size=Design.FONT_SIZE_NORMAL,
                        color=text_color or Colors.TEXT_PRIMARY,
                        weight=Colors.get_font_weight("MEDIUM"),
                    ),
                    ft.Text(
                        subtitle, 
                        size=Design.FONT_SIZE_SMALL,
                        color=Colors.TEXT_SECONDARY,
                    ),
                ], spacing=Design.SPACE_XXXS)),
                action_widget if action_widget else ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    color=Colors.TEXT_TERTIARY,
                    size=Design.ICON_SIZE_SM,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(Design.SPACE_LG),
            on_click=on_click,
            ink=True,
        )

    # Lista de configuraciones moderna
    settings_list = ft.Column([
        create_setting_item(
            ft.Icons.PERSON_OUTLINE_ROUNDED,
            "Editar perfil",
            "Cambiar datos personales y avatar",
            on_click=lambda e: page.go("/profile"),
        ),
        
        ft.Divider(height=1, color=Colors.BORDER, thickness=0.5),
        
        create_setting_item(
            ft.Icons.DARK_MODE_ROUNDED if not is_dark else ft.Icons.LIGHT_MODE_ROUNDED,
            "Modo oscuro" if not is_dark else "Modo claro",
            "Cambiar a tema oscuro" if not is_dark else "Cambiar a tema claro",
            action_widget=ft.Switch(
                value=is_dark,
                on_change=toggle_dark_mode,
                active_color=Colors.PRIMARY,
                inactive_track_color=Colors.GREY_LIGHT,
            ),
            on_click=toggle_dark_mode,
        ),
        
        ft.Divider(height=1, color=Colors.BORDER, thickness=0.5),
        
        create_setting_item(
            ft.Icons.NOTIFICATIONS_OUTLINED,
            "Recordatorios",
            "Configurar notificaciones de hidratación",
            on_click=lambda e: page.snack_bar.__setattr__('open', True) or page.update() if not hasattr(page, '_temp_snack') and setattr(page, '_temp_snack', True) and setattr(page, 'snack_bar', ft.SnackBar(
                content=ft.Text("Función próximamente disponible", color=Colors.TEXT_LIGHT),
                bgcolor=Colors.INFO,
            )) else None,
        ),
        
        ft.Divider(height=1, color=Colors.BORDER, thickness=0.5),
        
        create_setting_item(
            ft.Icons.DELETE_OUTLINE_ROUNDED,
            "Resetear aplicación",
            "Eliminar todos los datos y volver al inicio",
            text_color=Colors.ERROR,
            on_click=reset_app,
        ),
    ], spacing=0)

    # Tarjeta de configuraciones moderna
    settings_card = ft.Container(
        content=settings_list,
        bgcolor=Colors.CARD_BACKGROUND,
        border_radius=Design.BORDER_RADIUS_XL,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.with_opacity(0.08, Colors.DARK_NAVY),
            offset=ft.Offset(0, 4),
        ),
    )

    # Información adicional
    app_info = ft.Container(
        content=ft.Column([
            ft.Text(
                "🌊 awa - AquaReminder",
                size=Design.FONT_SIZE_NORMAL,
                color=Colors.TEXT_PRIMARY,
                weight=Colors.get_font_weight("SEMIBOLD"),
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Mantente hidratado, mantente saludable",
                size=Design.FONT_SIZE_SMALL,
                color=Colors.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=Design.SPACE_XS),
            ft.Text(
                "v1.0.0",
                size=Design.FONT_SIZE_CAPTION,
                color=Colors.TEXT_TERTIARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.all(Design.SPACE_LG),
    )

    body = ft.Container(
        content=ft.Column([
            settings_card,
            ft.Container(height=Design.SPACE_LG),
            app_info,
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        padding=ft.padding.symmetric(horizontal=Design.SPACE_LG, vertical=Design.SPACE_LG),
        bgcolor=Colors.BACKGROUND,
        expand=True,
    )

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
        "/settings",
        [content],
        padding=ft.padding.all(0),
        bgcolor=Colors.BACKGROUND,
    )
