import flet as ft
from config import Colors, Design

# Estado de finalización del onboarding
onboarding_completed = False


def _get_step_from_route(route: str) -> int:
    # Devuelve índice 0..2 según /onboarding/{1|2|3}
    try:
        parts = route.split("/")
        if len(parts) >= 3 and parts[1] == "onboarding":
            n = int(parts[2])
            if 1 <= n <= 3:
                return n - 1
    except Exception:
        pass
    return 0


def create_onboarding_page(page: ft.Page) -> ft.View:
    global onboarding_completed

    # Slides (3 pasos)
    slides = [
        {
            "title": "¡Bienvenido a awa!",
            "description": "Tu compañero inteligente para mantener una hidratación perfecta todos los días.",
            "icon": ft.Icons.WATER_DROP,
            "color": Colors.PRIMARY,
        },
        {
            "title": "Registro intuitivo",
            "description": "Registra tu consumo de agua de forma rápida con botones inteligentes.",
            "icon": ft.Icons.ADD_CIRCLE_OUTLINE,
            "color": Colors.SECONDARY,
        },
        {
            "title": "Nunca olvides hidratarte",
            "description": "Recibe recordatorios que funcionan incluso con la app cerrada.",
            "icon": ft.Icons.NOTIFICATIONS_ACTIVE,
            "color": Colors.ACCENT,
        },
    ]

    # Paso actual segun la ruta
    idx = _get_step_from_route(page.route)
    if idx < 0 or idx > 2:
        idx = 0
    slide = slides[idx]

    # Handlers basados en la ruta (no usan estado global para el índice)
    def go_to(step_index: int):
        # step_index es 0..2 -> ruta /onboarding/{1..3}
        page.go(f"/onboarding/{step_index + 1}")

    def on_next(e):
        i = _get_step_from_route(e.page.route)
        if i < 2:
            go_to(i + 1)

    def on_prev(e):
        i = _get_step_from_route(e.page.route)
        if i > 0:
            go_to(i - 1)

    def on_finish(e):
        global onboarding_completed
        onboarding_completed = True
        # Ir a setup para capturar datos de perfil si aún no existen
        e.page.go("/setup")

    # Indicadores
    indicators = [
        ft.Container(
            width=12,
            height=12,
            bgcolor=Colors.PRIMARY if i == idx else Colors.GREY_LIGHT,
            border_radius=6,
            border=ft.border.all(2, Colors.PRIMARY if i <= idx else Colors.GREY_LIGHT),
        )
        for i in range(3)
    ]

    # Contenido
    slide_content = ft.Column(
        [
            ft.Container(
                content=ft.Icon(slide["icon"], size=100, color=Colors.TEXT_LIGHT),
                width=180,
                height=180,
                bgcolor=slide["color"],
                border_radius=90,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=30),
            ),
            ft.Text(
                slide["title"],
                size=Design.FONT_SIZE_LARGE,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=Colors.TEXT_PRIMARY,
            ),
            ft.Container(
                content=ft.Text(
                    slide["description"],
                    size=Design.FONT_SIZE_NORMAL,
                    text_align=ft.TextAlign.CENTER,
                    color=Colors.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_400,
                ),
                width=320,
                padding=ft.padding.symmetric(horizontal=Design.PADDING_MEDIUM),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=Design.SPACING_LARGE,
    )

    # Botones
    left_btn = (
        ft.TextButton(
            "Atrás",
            on_click=on_prev,
            style=ft.ButtonStyle(color=Colors.TEXT_SECONDARY, text_style=ft.TextStyle(size=16)),
        )
        if idx > 0
        else ft.Container(width=60)
    )

    right_btn = (
        ft.ElevatedButton(
            "Siguiente",
            on_click=on_next,
            style=ft.ButtonStyle(
                bgcolor=Colors.PRIMARY, color=Colors.TEXT_LIGHT, text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            width=120,
            height=45,
        )
        if idx < 2
        else ft.ElevatedButton(
            "¡Comenzar!",
            on_click=on_finish,
            style=ft.ButtonStyle(
                bgcolor=Colors.SUCCESS, color=Colors.TEXT_LIGHT, text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            width=120,
            height=45,
        )
    )

    main_content = ft.Column(
        [
            ft.Container(
                content=ft.Row(indicators, spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(top=40, bottom=20),
            ),
            ft.Container(content=slide_content, expand=True, alignment=ft.alignment.center),
            ft.Container(
                content=ft.Row([left_btn, right_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(30),
            ),
        ],
        expand=True,
    )

    # Asegurar que la View use ruta con el índice humano (1..3)
    return ft.View(f"/onboarding/{idx + 1}", [main_content], bgcolor=Colors.BACKGROUND, padding=ft.padding.all(0))


def is_onboarding_completed() -> bool:
    return onboarding_completed