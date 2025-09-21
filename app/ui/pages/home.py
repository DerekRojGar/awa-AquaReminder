import flet as ft
from config import Colors, Design
from services.intake_service import add_intake, get_today_total
from services.profile_service import load_profile


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


def _quick_button(text: str, amount_ml: int, page: ft.Page, goal_ml: int, total_text: ft.Text, progress_bar: ft.ProgressBar, progress_text: ft.Text):
    def on_click(e):
        add_intake(amount_ml)
        # Feedback visual
        page.snack_bar = ft.SnackBar(ft.Text(f"+{amount_ml} ml registrados"), bgcolor=Colors.PRIMARY)
        page.snack_bar.open = True
        # Actualizar total y progreso
        total = get_today_total()
        total_text.value = f"{total} ml"
        ratio = min(total / max(goal_ml, 1), 1.0)
        progress_bar.value = ratio
        progress_bar.color = Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY
        progress_text.value = f"{total} / {goal_ml} ml"
        page.update()
    return ft.ElevatedButton(
        text,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=Colors.PRIMARY,
            color=Colors.TEXT_LIGHT,
            text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL, weight=ft.FontWeight.BOLD),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        height=44,
    )


def create_home_page(page: ft.Page):
    # Cargar meta desde el perfil
    profile = load_profile() or {}
    goal_ml = int(profile.get("daily_goal_ml", 2000) or 2000)

    # Total diario inicial
    total = get_today_total()
    total_text = ft.Text(f"{total} ml", size=40, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)

    # Barra de progreso
    ratio = min(total / max(goal_ml, 1), 1.0)
    progress_bar = ft.ProgressBar(value=ratio, color=Colors.SUCCESS if ratio >= 1.0 else Colors.PRIMARY, bgcolor=Colors.GREY_LIGHT)
    progress_text = ft.Text(f"{total} / {goal_ml} ml", size=12, color=Colors.TEXT_SECONDARY)

    # Encabezado minimalista
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text("awa", size=22, weight=ft.FontWeight.BOLD, color=Colors.TEXT_LIGHT),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.WATER_DROP, color=Colors.TEXT_LIGHT),
            ]
        ),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    # Tarjeta de progreso diario (simple y moderna)
    daily_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Consumo de hoy", size=14, color=Colors.TEXT_SECONDARY),
                total_text,
                ft.Container(height=8),
                progress_bar,
                ft.Container(height=6),
                progress_text,
                ft.Text(f"Meta {goal_ml} ml", size=12, color=Colors.GREY_SAGE),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.padding.all(20),
        bgcolor=Colors.ACCENT,
        border_radius=16,
    )

    # Acciones rápidas (tres tamaños)
    quick_actions = ft.Row(
        [
            _quick_button("+250 ml", 250, page, goal_ml, total_text, progress_bar, progress_text),
            _quick_button("+350 ml", 350, page, goal_ml, total_text, progress_bar, progress_text),
            _quick_button("+500 ml", 500, page, goal_ml, total_text, progress_bar, progress_text),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Sugerencia / CTA secundaria
    tip_card = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=Colors.PRIMARY),
                ft.Text("Activa recordatorios para no olvidar hidratarte", color=Colors.TEXT_PRIMARY),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(14),
        bgcolor=Colors.ACCENT,
        border_radius=12,
    )

    body = ft.Container(
        content=ft.Column(
            [
                daily_card,
                ft.Container(height=Design.SPACING_LARGE),
                quick_actions,
                ft.Container(height=Design.SPACING_LARGE),
                tip_card,
            ],
            spacing=Design.SPACING_LARGE,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        expand=True,
        bgcolor=Colors.BACKGROUND,
    )

    return ft.View(
        "/",
        [header, body, _bottom_nav(page)],
        padding=ft.padding.all(0),
        bgcolor=Colors.BACKGROUND,
    )
