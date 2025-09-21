import os
import json
import flet as ft
from ui.pages.onboarding import create_onboarding_page, is_onboarding_completed
from ui.pages.home import create_home_page
from ui.pages.profile_setup import create_profile_setup_page
from ui.pages.history import create_history_page
from services.profile_service import has_profile_data


def _profile_file_path() -> str:
    # app/main.py -> root -> storage/data/profile.json
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # root_dir ahora apunta a .../app; subir uno más al root del proyecto
    project_root = os.path.abspath(os.path.join(root_dir, ".."))
    data_dir = os.path.join(project_root, "storage", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "profile.json")


def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "awa - AquaReminder"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 400
    page.window_height = 700

    # Router/navegación entre páginas
    def route_change(route):
        page.views.clear()

        has_profile = has_profile_data()

        if not has_profile:
            # Sin datos -> flujo onboarding -> setup
            if page.route.startswith("/onboarding"):
                page.views.append(create_onboarding_page(page))
            elif page.route == "/setup":
                page.views.append(create_profile_setup_page(page))
            else:
                page.go("/onboarding/1")
                return
        else:
            # Con datos -> home directo
            if page.route == "/" or page.route == "":
                page.views.append(create_home_page(page))
            elif page.route.startswith("/history"):
                page.views.append(create_history_page(page))
            elif page.route.startswith("/onboarding") or page.route == "/setup":
                page.go("/")
                return
            else:
                page.views.append(create_home_page(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Página inicial


if __name__ == "__main__":
    ft.app(target=main)
