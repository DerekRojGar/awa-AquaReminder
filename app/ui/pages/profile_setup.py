import os
import json
import flet as ft
from datetime import datetime
from config import Colors, Design
from services.profile_service import save_profile


def _profile_file_path() -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # -> app
    project_root = os.path.abspath(os.path.join(root_dir, ".."))  # -> repo root
    data_dir = os.path.join(project_root, "storage", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "profile.json")


def _save_profile(data: dict):
    with open(_profile_file_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_profile_setup_page(page: ft.Page) -> ft.View:
    # Controles
    weight = ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER, width=140)
    height = ft.TextField(label="Altura (cm)", keyboard_type=ft.KeyboardType.NUMBER, width=140)
    sex = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
        width=200,
        value="Otro",
    )
    activity = ft.Dropdown(
        label="Actividad",
        options=[
            ft.dropdown.Option("Baja"),
            ft.dropdown.Option("Moderada"),
            ft.dropdown.Option("Alta"),
        ],
        width=200,
        value="Baja",
    )
    daily_goal = ft.TextField(
        label="Meta diaria (ml)",
        helper_text="Opcional. Si se deja vacío, se calcula automáticamente.",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=220,
    )

    # Resumen en vivo (UI modernizada)
    bmi_value = ft.Text("—", size=24, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)
    goal_value = ft.Text("—", size=24, weight=ft.FontWeight.BOLD, color=Colors.TEXT_PRIMARY)

    def compute_defaults():
        # Estimación simple de ingesta: 35 ml por kg + ajuste por actividad
        try:
            w = float(weight.value or 0)
            base = w * 35.0  # ml
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

    for c in (weight, height, sex, activity, daily_goal):
        c.on_change = update_preview

    def use_suggested(e):
        daily_goal.value = str(compute_defaults())
        update_preview()

    def save_and_continue(e):
        # Validaciones básicas
        try:
            w = float(weight.value or 0)
            h = float(height.value or 0)
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Ingresa números válidos en peso y altura"), bgcolor=Colors.ERROR)
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
            "weight_kg": round(w, 1),
            "height_cm": round(h, 1),
            "sex": sex.value or "Otro",
            "activity": activity.value or "Baja",
            "daily_goal_ml": goal,
            "created_at": datetime.now().isoformat(),
        }
        try:
            save_profile(data)
            page.go("/")
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo guardar el perfil"), bgcolor=Colors.ERROR)
            page.snack_bar.open = True
            page.update()

    # Header minimalista
    header = ft.Container(
        content=ft.Column([
            ft.Text("Configura tu perfil", size=20, weight=ft.FontWeight.BOLD, color=Colors.TEXT_LIGHT),
            ft.Text("Personaliza tus objetivos para mejores resultados", size=12, color=Colors.TEXT_LIGHT),
        ], spacing=4),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    # Tarjeta de resumen
    summary_card = ft.Container(
        content=ft.Column([
            ft.Text("Resumen", size=14, color=Colors.TEXT_SECONDARY),
            ft.Row([
                ft.Column([
                    ft.Text("IMC", size=12, color=Colors.TEXT_SECONDARY),
                    bmi_value,
                ], spacing=2),
                ft.Container(width=16),
                ft.Column([
                    ft.Text("Meta diaria", size=12, color=Colors.TEXT_SECONDARY),
                    goal_value,
                ], spacing=2),
            ], alignment=ft.MainAxisAlignment.START),
        ], spacing=6),
        padding=ft.padding.all(16),
        bgcolor=Colors.ACCENT,
        border_radius=12,
    )

    # Form modernizado
    form = ft.Container(
        content=ft.Column(
            [
                summary_card,
                ft.Row([weight, height], spacing=12),
                ft.Row([sex, activity], spacing=12),
                ft.Row([
                    daily_goal,
                    ft.TextButton("Usar sugerida", on_click=use_suggested, style=ft.ButtonStyle(color=Colors.PRIMARY)),
                ], spacing=8),
                ft.Text("Podrás cambiar estos datos después en Ajustes", size=12, color=Colors.TEXT_SECONDARY),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Guardar y continuar",
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
        ),
        padding=ft.padding.all(16),
        bgcolor=Colors.BACKGROUND,
        expand=True,
    )

    # Inicializar vista previa
    update_preview()

    return ft.View("/setup", [header, form], padding=ft.padding.all(0), bgcolor=Colors.BACKGROUND)