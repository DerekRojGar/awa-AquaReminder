import flet as ft
from datetime import datetime, date, timedelta
from config import Colors, Design
from services.intake_service import get_recent, get_daily_totals, delete_last_intake

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
                        ft.Text(dt.strftime("%H:%M"), size=14, color=Colors.GREY_DARK),
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

    content_column = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)

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
        "/history",
        [content],
        padding=ft.padding.all(0),
        bgcolor=Colors.BACKGROUND,
    )
