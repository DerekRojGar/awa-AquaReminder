import flet as ft
from datetime import datetime
from config import Colors, Design
from services.profile_service import save_profile, load_profile


# Navegación inferior (se usa en la vista de perfil, no en setup)
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


def _build_profile_page(page: ft.Page, *, view_route: str, header_title: str, header_subtitle: str, button_text: str, after_save_route: str) -> ft.View:
    existing = load_profile() or {}

    # Controles base
    name = ft.TextField(label="Nombre", width=220, value=existing.get("name", ""))
    age = ft.TextField(label="Edad", keyboard_type=ft.KeyboardType.NUMBER, width=120, value=str(existing.get("age", "")))

    weight = ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER, width=140, value=str(existing.get("weight_kg", "")))
    height = ft.TextField(label="Altura (cm)", keyboard_type=ft.KeyboardType.NUMBER, width=140, value=str(existing.get("height_cm", "")))

    sex = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
        width=200,
        value=existing.get("sex", "Otro"),
    )
    activity = ft.Dropdown(
        label="Actividad",
        options=[ft.dropdown.Option("Baja"), ft.dropdown.Option("Moderada"), ft.dropdown.Option("Alta")],
        width=200,
        value=existing.get("activity", "Baja"),
    )
    daily_goal = ft.TextField(
        label="Meta diaria (ml)",
        helper_text="Opcional. Si se deja vacío, se calcula automáticamente.",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=220,
        value=str(existing.get("daily_goal_ml", "")),
    )

    # Avatares por imagen con rutas absolutas
    import os
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    avatares_dir = os.path.join(project_root, "src", "assets", "avatares")
    
    avatar_files = [
        os.path.join(avatares_dir, "Avatar1.jpg"),
        os.path.join(avatares_dir, "Avatar2.jpg"),
        os.path.join(avatares_dir, "Avatar3.jpg"),
        os.path.join(avatares_dir, "Avatar4.jpg"),
    ]
    sel = {"index": int(existing.get("avatar_id", 0)) if str(existing.get("avatar_id", "")).isdigit() else 0}

    # Preview circular más grande
    def avatar_preview_control():
        src = avatar_files[sel["index"] % len(avatar_files)]
        return ft.Container(
            width=80,
            height=80,
            content=ft.Image(src, fit=ft.ImageFit.COVER, width=80, height=80),
            bgcolor=Colors.ACCENT,
            alignment=ft.alignment.center,
            border=ft.border.all(2, Colors.GREY_LIGHT),
            border_radius=40,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    avatar_preview = avatar_preview_control()

    # Miniaturas circulares más grandes
    def make_avatar_chip(i: int):
        src = avatar_files[i]
        selected = sel["index"] == i
        return ft.Container(
            width=64,
            height=64,
            content=ft.Image(src, fit=ft.ImageFit.COVER, width=64, height=64),
            bgcolor=Colors.ACCENT,
            border=ft.border.all(4, Colors.PRIMARY) if selected else ft.border.all(2, Colors.GREY_LIGHT),
            border_radius=32,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            on_click=lambda e, idx=i: select_avatar(idx),
            tooltip="Seleccionar",
        )

    avatar_row = ft.Row([], spacing=10, wrap=True)

    def refresh_avatar_row():
        avatar_row.controls = [make_avatar_chip(i) for i in range(len(avatar_files))]

    def select_avatar(i: int):
        sel["index"] = i
        new_src = avatar_files[i]
        avatar_preview.content = ft.Image(new_src, fit=ft.ImageFit.COVER, width=80, height=80)
        refresh_avatar_row()
        page.update()

    refresh_avatar_row()

    # Resumen en vivo
    bmi_value = ft.Text("—", size=24, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)
    goal_value = ft.Text("—", size=24, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)

    def compute_defaults():
        try:
            w = float(weight.value or 0)
            base = w * 35.0
            adj = {"Baja": 0, "Moderada": 250, "Alta": 500}.get(activity.value or "Baja", 0)
            return int(max(1500, base + adj))
        except Exception:
            return 2000

    def update_preview(e=None):
        try:
            w = float(weight.value or 0)
            h = float(height.value or 0)
            bmi = 0
            if w > 0 and h > 0:
                bmi = round(w / ((h / 100) ** 2), 1)
            suggested = compute_defaults()
            if not (daily_goal.value or "").strip().isdigit():
                goal_value.value = f"{suggested} ml"
            else:
                goal_value.value = f"{int(daily_goal.value)} ml"
            bmi_value.value = f"{bmi}" if bmi else "—"
            page.update()
        except Exception:
            pass

    for c in (name, age, weight, height, sex, activity, daily_goal):
        c.on_change = update_preview

    def save_and_continue(e):
        # Validaciones básicas
        try:
            w = float(weight.value or 0)
            h = float(height.value or 0)
            age_val = int(age.value) if (age.value or "").strip().isdigit() else None
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Revisa los datos numéricos"), bgcolor=Colors.ERROR)
            page.snack_bar.open = True
            page.update()
            return

        if w <= 0 or h <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("Peso y altura deben ser mayores a 0"), bgcolor=Colors.ERROR)
            page.snack_bar.open = True
            page.update()
            return

        goal = int(daily_goal.value) if (daily_goal.value or "").strip().isdigit() else compute_defaults()

        data = {
            "name": (name.value or "").strip(),
            "age": age_val,
            "weight_kg": round(w, 1),
            "height_cm": round(h, 1),
            "sex": sex.value or "Otro",
            "activity": activity.value or "Baja",
            "daily_goal_ml": goal,
            "avatar_id": sel["index"],
            "created_at": datetime.now().isoformat(),
        }
        try:
            save_profile(data)
            page.snack_bar = ft.SnackBar(ft.Text("Perfil guardado"), bgcolor=Colors.SUCCESS)
            page.snack_bar.open = True
            page.update()
            page.go(after_save_route)
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo guardar el perfil"), bgcolor=Colors.ERROR)
            page.snack_bar.open = True
            page.update()

    # Header minimalista
    header = ft.Container(
        content=ft.Column([
            ft.Text(header_title, size=20, weight=ft.FontWeight.BOLD, color=Colors.TEXT_LIGHT),
            ft.Text(header_subtitle, size=12, color=Colors.TEXT_LIGHT),
        ], spacing=4),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    # Tarjeta de avatar + nombre (preview circular)
    avatar_card = ft.Container(
        content=ft.Row([
            avatar_preview,
            ft.Container(width=12),
            ft.Column([
                name,
                ft.Row([age], spacing=8),
            ], spacing=8),
        ]),
        padding=ft.padding.all(12),
        bgcolor=Colors.ACCENT,
        border_radius=12,
    )

    # Tarjeta de resumen
    summary_card = ft.Container(
        content=ft.Column([
            ft.Text("Resumen", size=14, color=Colors.TEXT_SECONDARY),
            ft.Row([
                ft.Column([ft.Text("IMC", size=12, color=Colors.TEXT_SECONDARY), bmi_value], spacing=2),
                ft.Container(width=16),
                ft.Column([ft.Text("Meta diaria", size=12, color=Colors.TEXT_SECONDARY), goal_value], spacing=2),
            ], alignment=ft.MainAxisAlignment.START),
        ], spacing=6),
        padding=ft.padding.all(16),
        bgcolor=Colors.ACCENT,
        border_radius=12,
    )

    # Form modernizado (scrollable)
    form_column = ft.Column(
        [
            avatar_card,
            ft.Text("Elige tu avatar", size=12, color=Colors.TEXT_SECONDARY),
            avatar_row,
            summary_card,
            ft.Row([weight, height], spacing=12),
            ft.Row([sex, activity], spacing=12),
            ft.Row([
                daily_goal,
                ft.TextButton("Usar sugerida", on_click=lambda e: (daily_goal.__setattr__("value", str(compute_defaults())), update_preview()), style=ft.ButtonStyle(color=Colors.PRIMARY)),
            ], spacing=8),
            ft.Text("Podrás cambiar estos datos después en Ajustes", size=12, color=Colors.TEXT_SECONDARY),
            ft.Container(
                content=ft.ElevatedButton(
                    button_text,
                    on_click=save_and_continue,
                    style=ft.ButtonStyle(
                        bgcolor=Colors.PRIMARY,
                        color=Colors.TEXT_LIGHT,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    ),
                    height=48,
                    width=260,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=8),
            ),
        ],
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
    )

    body = ft.Container(
        content=form_column,
        padding=ft.padding.all(16),
        bgcolor=Colors.BACKGROUND,
        expand=True,
    )

    controls = [header, body]
    # Agregar bottom nav sólo en la vista de perfil (no en setup inicial)
    if view_route == "/profile":
        controls.append(_bottom_nav(page))

    update_preview()
    return ft.View(view_route, controls, padding=ft.padding.all(0), bgcolor=Colors.BACKGROUND)


def create_profile_setup_page(page: ft.Page) -> ft.View:
    return _build_profile_page(
        page,
        view_route="/setup",
        header_title="Configura tu perfil",
        header_subtitle="Personaliza tu experiencia",
        button_text="Guardar y continuar",
        after_save_route="/",
    )


def create_profile_page(page: ft.Page) -> ft.View:
    return _build_profile_page(
        page,
        view_route="/profile",
        header_title="Tu perfil",
        header_subtitle="Actualiza tus datos cuando quieras",
        button_text="Guardar cambios",
        after_save_route="/",
    )