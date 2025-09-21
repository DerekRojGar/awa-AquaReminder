import flet as ft
from datetime import datetime, date, timedelta
from config import Colors, Design
from services.intake_service import get_recent, get_daily_totals, delete_last_intake


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


def _friendly_date(d: date) -> str:
    today = date.today()
    if d == today:
        return "Hoy"
    if d == today - timedelta(days=1):
        return "Ayer"
    return d.strftime("%d/%m/%Y")


def _filter_chips(current: str, on_change):
    def chip(label: str, value: str):
        selected = current == value
        return ft.Container(
            content=ft.Text(label, color=Colors.TEXT_LIGHT if selected else Colors.PRIMARY, size=12),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            bgcolor=Colors.PRIMARY if selected else Colors.ACCENT,
            border_radius=16,
            on_click=lambda e, v=value: on_change(v),
        )

    return ft.Row(
        [chip("Hoy", "today"), chip("7 días", "7d"), chip("30 días", "30d")],
        spacing=8,
    )


def _build_header(on_filter_change, current_filter: str):
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Historial", size=20, weight=ft.FontWeight.BOLD, color=Colors.TEXT_LIGHT),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.UNDO, tooltip="Deshacer última", on_click=lambda e: on_filter_change(current_filter, undo=True), icon_color=Colors.TEXT_LIGHT),
            ]),
            _filter_chips(current_filter, lambda f: on_filter_change(f, undo=False)),
        ], spacing=10),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )


def _build_list_view(filter_key: str) -> ft.Control:
    # Cargar datos según filtro
    if filter_key == "today":
        rows = get_recent(100)  # mostramos recientes; el grouping visual aclarará días
    elif filter_key == "7d":
        rows = get_recent(300)
    else:
        rows = get_recent(1000)

    items: list[ft.Control] = []
    last_group: str | None = None

    for ts_iso, amount in rows:
        try:
            dt = datetime.fromisoformat(ts_iso)
        except Exception:
            continue
        d_key = dt.date().isoformat()
        if d_key != last_group:
            # Sección por día
            items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(_friendly_date(dt.date()), size=14, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY),
                        ft.Container(expand=True),
                        # Total del día (opcional futuro)
                    ]),
                    padding=ft.padding.only(top=8, bottom=4),
                )
            )
            last_group = d_key
        items.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(dt.strftime("%H:%M"), size=14, color=Colors.GREY_SAGE),
                        ft.Container(expand=True),
                        ft.Text(f"{amount} ml", size=16, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.symmetric(vertical=10, horizontal=12),
                bgcolor=Colors.ACCENT,
                border_radius=12,
            )
        )

    if not items:
        items.append(ft.Text("Sin registros aún", size=14, color=Colors.TEXT_SECONDARY))

    return ft.ListView(controls=items, expand=True, spacing=10, padding=ft.padding.all(0))


def create_history_page(page: ft.Page) -> ft.View:
    current_filter = {"value": "today"}

    content_column = ft.Column(spacing=12, expand=True)

    def refresh(filter_key: str, undo: bool = False):
        if undo:
            deleted = delete_last_intake()
            if deleted:
                page.snack_bar = ft.SnackBar(ft.Text("Última ingesta eliminada"), bgcolor=Colors.WARNING)
                page.snack_bar.open = True
        current_filter["value"] = filter_key
        content_column.controls = [_build_list_view(filter_key)]
        page.update()

    header = _build_header(refresh, current_filter["value"])
    refresh(current_filter["value"])  # primera carga

    body = ft.Container(
        content=content_column,
        padding=ft.padding.all(16),
        bgcolor=Colors.BACKGROUND,
        expand=True,
    )

    return ft.View(
        "/history",
        [header, body, _bottom_nav(page)],
        padding=ft.padding.all(0),
        bgcolor=Colors.BACKGROUND,
    )
