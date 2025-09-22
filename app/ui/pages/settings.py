import flet as ft
from config import Colors, Design
from services.profile_service import reset_app_data


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
    color = Colors.PRIMARY if active else Colors.GREY_SAGE
    text_color = Colors.TEXT_PRIMARY if active else Colors.GREY_SAGE
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(icon, size=24, color=color),
                ft.Text(label, size=12, color=text_color),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=12, horizontal=8),
        on_click=on_click,
        expand=True,
    )


def _bottom_nav(page: ft.Page):
    idx = _current_tab_index(page.route)
    return ft.Container(
        content=ft.Row(
            [
                _nav_item("Inicio", ft.Icons.HOME, idx == 0, lambda e: page.go("/")),
                _nav_item("Historial", ft.Icons.HISTORY, idx == 1, lambda e: page.go("/history")),
                _nav_item("Perfil", ft.Icons.PERSON, idx == 2, lambda e: page.go("/profile")),
                _nav_item("Ajustes", ft.Icons.SETTINGS, idx == 3, lambda e: page.go("/settings")),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=Colors.ACCENT,
        padding=ft.padding.only(left=16, right=16, top=6, bottom=6),
        border=ft.border.only(top=ft.border.BorderSide(1, Colors.GREY_LIGHT)),
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
        
        # Diálogo de confirmación
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Resetear aplicación"),
            content=ft.Text("¿Estás seguro? Se eliminarán todos tus datos (perfil e historial de consumo)."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
                ft.TextButton("Sí, eliminar", on_click=confirm_reset, style=ft.ButtonStyle(color=Colors.ERROR)),
            ],
        )
        
        def close_dialog():
            dlg.open = False
            page.update()
        
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Text("Ajustes", size=20, weight=ft.FontWeight.BOLD, color=Colors.TEXT_LIGHT),
            ft.Text("Configuración de la aplicación", size=12, color=Colors.TEXT_LIGHT),
        ], spacing=4),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    # Opciones de configuración
    settings_list = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON_OUTLINE, color=Colors.PRIMARY),
                ft.Column([
                    ft.Text("Editar perfil", size=16, color=Colors.TEXT_PRIMARY),
                    ft.Text("Cambiar datos personales y avatar", size=12, color=Colors.TEXT_SECONDARY),
                ], spacing=2),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=Colors.GREY_SAGE),
            ]),
            padding=ft.padding.all(16),
            on_click=lambda e: page.go("/profile"),
        ),
        
        ft.Divider(height=1, color=Colors.GREY_LIGHT),
        
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DELETE_OUTLINE, color=Colors.ERROR),
                ft.Column([
                    ft.Text("Resetear aplicación", size=16, color=Colors.ERROR),
                    ft.Text("Eliminar todos los datos y volver al inicio", size=12, color=Colors.TEXT_SECONDARY),
                ], spacing=2),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=Colors.GREY_SAGE),
            ]),
            padding=ft.padding.all(16),
            on_click=reset_app,
        ),
    ], spacing=0)

    settings_card = ft.Container(
        content=settings_list,
        bgcolor=Colors.ACCENT,
        border_radius=12,
        margin=ft.margin.all(16),
    )

    body = ft.Container(
        content=ft.Column([settings_card], spacing=16),
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
