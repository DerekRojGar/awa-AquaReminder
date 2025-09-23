import flet as ft
from datetime import datetime
from config import Colors, Design
from services.profile_service import save_profile, load_profile

ft.with_opacity = Colors.with_opacity


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


def _build_profile_page(page: ft.Page, *, view_route: str, header_title: str, header_subtitle: str, button_text: str, after_save_route: str) -> ft.View:
    existing = load_profile() or {}

    # Controles de formulario modernos
    name = ft.TextField(
        label="Nombre completo",
        value=existing.get("name", ""),
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        prefix_icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
    )
    
    age = ft.TextField(
        label="Edad",
        keyboard_type=ft.KeyboardType.NUMBER,
        value=str(existing.get("age", "")),
        width=150,
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        prefix_icon=ft.Icons.CAKE_OUTLINED,
    )

    weight = ft.TextField(
        label="Peso (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        value=str(existing.get("weight_kg", "")),
        width=150,
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        prefix_icon=ft.Icons.MONITOR_WEIGHT_OUTLINED,
    )
    
    height = ft.TextField(
        label="Altura (cm)",
        keyboard_type=ft.KeyboardType.NUMBER,
        value=str(existing.get("height_cm", "")),
        width=150,
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        prefix_icon=ft.Icons.HEIGHT_ROUNDED,
    )

    sex = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option("Masculino", text="Masculino"),
            ft.dropdown.Option("Femenino", text="Femenino"),
            ft.dropdown.Option("Otro", text="Otro")
        ],
        value=existing.get("sex", "Otro"),
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
    )
    
    activity = ft.Dropdown(
        label="Nivel de actividad",
        options=[
            ft.dropdown.Option("Baja", text="Baja - Trabajo sedentario"),
            ft.dropdown.Option("Moderada", text="Moderada - Ejercicio ligero"),
            ft.dropdown.Option("Alta", text="Alta - Ejercicio intenso")
        ],
        value=existing.get("activity", "Baja"),
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
    )
    
    daily_goal = ft.TextField(
        label="Meta diaria (ml)",
        helper_text="Opcional. Si se deja vacío, se calcula automáticamente según tu perfil.",
        keyboard_type=ft.KeyboardType.NUMBER,
        value=str(existing.get("daily_goal_ml", "")),
        border_radius=Design.BORDER_RADIUS_SM,
        bgcolor=Colors.CARD_BACKGROUND,
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        text_style=ft.TextStyle(size=Design.FONT_SIZE_NORMAL),
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY),
        prefix_icon=ft.Icons.LOCAL_DRINK_OUTLINED,
    )

    # Rutas relativas dentro de assets/ para el APK
    avatar_files = [
        "avatares/Avatar1.jpg",
        "avatares/Avatar2.jpg",
        "avatares/Avatar3.jpg",
        "avatares/Avatar4.jpg",
    ]
    avatar_icons = [ft.Icons.PERSON, ft.Icons.FACE, ft.Icons.ACCOUNT_CIRCLE, ft.Icons.SUPERVISED_USER_CIRCLE]
    
    sel = {"index": int(existing.get("avatar_id", 0)) if str(existing.get("avatar_id", "")).isdigit() else 0}

    # Preview de avatar moderno
    def avatar_preview_control():
        src = avatar_files[sel["index"] % len(avatar_files)]
        fallback_icon = avatar_icons[sel["index"] % len(avatar_icons)]
        return ft.Container(
            width=96,
            height=96,
            content=ft.Container(
                content=ft.Image(
                    src=src, 
                    fit=ft.ImageFit.COVER, 
                    width=88, 
                    height=88,
                    error_content=ft.Icon(fallback_icon, size=44, color=Colors.PRIMARY)
                ),
                width=88,
                height=88,
                border_radius=Design.BORDER_RADIUS_FULL,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ),
            bgcolor=Colors.PRIMARY,
            alignment=ft.alignment.center,
            border_radius=Design.BORDER_RADIUS_FULL,
            padding=ft.padding.all(4),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.with_opacity(0.3, Colors.PRIMARY),
                offset=ft.Offset(0, 4),
            ),
        )

    avatar_preview = avatar_preview_control()

    # Miniaturas de avatares modernizadas
    def make_avatar_chip(i: int):
        src = avatar_files[i]
        fallback_icon = avatar_icons[i % len(avatar_icons)]
        selected = sel["index"] == i
        return ft.Container(
            width=72,
            height=72,
            content=ft.Container(
                content=ft.Image(
                    src=src, 
                    fit=ft.ImageFit.COVER, 
                    width=64 if selected else 60, 
                    height=64 if selected else 60,
                    error_content=ft.Icon(fallback_icon, size=32 if selected else 28, color=Colors.PRIMARY)
                ),
                width=64 if selected else 60,
                height=64 if selected else 60,
                border_radius=Design.BORDER_RADIUS_FULL,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ),
            bgcolor=Colors.PRIMARY if selected else Colors.CARD_BACKGROUND,
            border_radius=Design.BORDER_RADIUS_FULL,
            padding=ft.padding.all(4 if selected else 6),
            on_click=lambda e, idx=i: select_avatar(idx),
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8 if selected else 4,
                color=ft.with_opacity(0.2 if selected else 0.1, Colors.PRIMARY),
                offset=ft.Offset(0, 2),
            ) if selected else None,
            tooltip="Seleccionar",
        )

    avatar_row = ft.Row([], spacing=10, wrap=True)

    def refresh_avatar_row():
        avatar_row.controls = [make_avatar_chip(i) for i in range(len(avatar_files))]

    def select_avatar(i: int):
        sel["index"] = i
        # Actualizar el preview completo
        avatar_preview.content = avatar_preview_control().content
        refresh_avatar_row()
        page.update()

    refresh_avatar_row()

    # Tarjetas de resumen modernas
    bmi_value = ft.Text("—", size=Design.FONT_SIZE_TITLE, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)
    goal_value = ft.Text("—", size=Design.FONT_SIZE_TITLE, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY)

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

    # Header moderno con gradiente
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(
                        header_title, 
                        size=Design.FONT_SIZE_LARGE, 
                        weight=ft.FontWeight.BOLD, 
                        color=Colors.TEXT_LIGHT
                    ),
                    ft.Text(
                        header_subtitle, 
                        size=Design.FONT_SIZE_SMALL, 
                        color=ft.with_opacity(0.9, Colors.TEXT_LIGHT)
                    ),
                ], expand=True, spacing=Design.SPACE_XXXS),
                ft.Icon(
                    ft.Icons.PERSON_ROUNDED,
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

    # Tarjeta de avatar y información personal
    avatar_card = ft.Container(
        content=ft.Column([
            ft.Row([
                avatar_preview,
                ft.Container(width=Design.SPACE_LG),
                ft.Container(expand=True, content=ft.Column([
                    ft.Text(
                        "Información personal", 
                        size=Design.FONT_SIZE_MEDIUM,
                        color=Colors.TEXT_PRIMARY,
                        weight=Colors.get_font_weight("SEMIBOLD"),
                    ),
                    ft.Container(height=Design.SPACE_SM),
                    name,
                    ft.Container(height=Design.SPACE_XS),
                    age,
                ], spacing=0)),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=Design.SPACE_SM),
            ft.Text(
                "Elige tu avatar", 
                size=Design.FONT_SIZE_NORMAL,
                color=Colors.TEXT_PRIMARY,
                weight=Colors.get_font_weight("MEDIUM"),
            ),
            ft.Container(height=Design.SPACE_XS),
            avatar_row,
        ]),
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

    # Tarjetas de salud y actividad
    health_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Información de salud", 
                size=Design.FONT_SIZE_MEDIUM,
                color=Colors.TEXT_PRIMARY,
                weight=Colors.get_font_weight("SEMIBOLD"),
            ),
            ft.Container(height=Design.SPACE_SM),
            ft.Row([weight, height], spacing=Design.SPACE_SM),
            ft.Container(height=Design.SPACE_XS),
            sex,
        ]),
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

    # Tarjeta de actividad y meta
    activity_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Actividad y meta diaria", 
                size=Design.FONT_SIZE_MEDIUM,
                color=Colors.TEXT_PRIMARY,
                weight=Colors.get_font_weight("SEMIBOLD"),
            ),
            ft.Container(height=Design.SPACE_SM),
            activity,
            ft.Container(height=Design.SPACE_XS),
            ft.Row([
                ft.Container(expand=True, content=daily_goal),
                ft.Container(width=Design.SPACE_XS),
                ft.Container(
                    content=ft.TextButton(
                        "Usar sugerida",
                        on_click=lambda e: (daily_goal.__setattr__("value", str(compute_defaults())), update_preview()),
                        style=ft.ButtonStyle(
                            color=Colors.PRIMARY,
                            bgcolor=ft.with_opacity(0.1, Colors.PRIMARY),
                            padding=ft.padding.symmetric(horizontal=Design.SPACE_SM, vertical=Design.SPACE_XS),
                            shape=ft.RoundedRectangleBorder(radius=Design.BORDER_RADIUS_SM),
                        ),
                    ),
                    alignment=ft.alignment.center,
                ),
            ]),
        ]),
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

    # Tarjeta de resumen moderna
    summary_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Tu resumen", 
                size=Design.FONT_SIZE_MEDIUM,
                color=Colors.TEXT_PRIMARY,
                weight=Colors.get_font_weight("SEMIBOLD"),
            ),
            ft.Container(height=Design.SPACE_SM),
            ft.Row([
                ft.Container(expand=True, content=ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.MONITOR_WEIGHT_OUTLINED,
                            color=Colors.PRIMARY,
                            size=Design.ICON_SIZE_LG,
                        ),
                        ft.Container(height=Design.SPACE_XS),
                        ft.Text(
                            "IMC", 
                            size=Design.FONT_SIZE_SMALL, 
                            color=Colors.TEXT_SECONDARY,
                            weight=Colors.get_font_weight("MEDIUM"),
                        ),
                        bmi_value,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    padding=ft.padding.all(Design.SPACE_SM),
                    bgcolor=ft.with_opacity(0.05, Colors.PRIMARY),
                    border_radius=Design.BORDER_RADIUS_SM,
                )),
                ft.Container(width=Design.SPACE_SM),
                ft.Container(expand=True, content=ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.LOCAL_DRINK_OUTLINED,
                            color=Colors.PRIMARY,
                            size=Design.ICON_SIZE_LG,
                        ),
                        ft.Container(height=Design.SPACE_XS),
                        ft.Text(
                            "Meta diaria", 
                            size=Design.FONT_SIZE_SMALL, 
                            color=Colors.TEXT_SECONDARY,
                            weight=Colors.get_font_weight("MEDIUM"),
                        ),
                        goal_value,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    padding=ft.padding.all(Design.SPACE_SM),
                    bgcolor=ft.with_opacity(0.05, Colors.PRIMARY),
                    border_radius=Design.BORDER_RADIUS_SM,
                )),
            ]),
        ]),
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

    # Formulario modernizado y organizado
    form_column = ft.Column([
        avatar_card,
        ft.Container(height=Design.SPACE_MD),
        health_card,
        ft.Container(height=Design.SPACE_MD),
        activity_card,
        ft.Container(height=Design.SPACE_MD),
        summary_card,
        ft.Container(height=Design.SPACE_SM),
        ft.Text(
            "💡 Podrás cambiar estos datos después en Ajustes", 
            size=Design.FONT_SIZE_SMALL, 
            color=Colors.TEXT_SECONDARY,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(height=Design.SPACE_LG),
        ft.Container(
            content=ft.Container(
                content=ft.Text(
                    button_text,
                    size=Design.FONT_SIZE_NORMAL,
                    weight=Colors.get_font_weight("SEMIBOLD"),
                    color=Colors.TEXT_LIGHT,
                ),
                bgcolor=Colors.PRIMARY,
                padding=ft.padding.symmetric(vertical=Design.SPACE_SM, horizontal=Design.SPACE_XL),
                border_radius=Design.BORDER_RADIUS_LG,
                on_click=save_and_continue,
                ink=True,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color=ft.with_opacity(0.3, Colors.PRIMARY),
                    offset=ft.Offset(0, 4),
                ),
            ),
            alignment=ft.alignment.center,
        ),
        ft.Container(height=Design.SPACE_LG),  # Espacio extra al final
    ], spacing=0, scroll=ft.ScrollMode.AUTO)

    body = ft.Container(
        content=form_column,
        padding=ft.padding.symmetric(horizontal=Design.SPACE_LG, vertical=Design.SPACE_LG),
        bgcolor=Colors.BACKGROUND,
        expand=True,
    )

    controls = [header, body]
    has_bottom_nav = view_route == "/profile"

    # Respect safe areas: top for content, bottom for nav if present
    if has_bottom_nav:
        content = ft.Column([
            ft.SafeArea(
                content=ft.Column([header, body], spacing=0),
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
    else:
        content = ft.SafeArea(
            content=ft.Column([header, body], spacing=0),
            top=True,
            bottom=True,
            expand=True,
        )

    update_preview()
    return ft.View(view_route, [content], padding=ft.padding.all(0), bgcolor=Colors.BACKGROUND)


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
