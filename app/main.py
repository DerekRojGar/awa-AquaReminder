import flet as ft
from ui.pages.onboarding import create_onboarding_page, is_onboarding_completed
from ui.pages.home import create_home_page

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

        print(f"Navegando a ruta: {page.route}")
        
        # Verificar si es la primera vez (onboarding)
        if not is_onboarding_completed() and page.route != "/onboarding":
            print("Redirigiendo a onboarding (primera vez)")
            page.views.append(create_onboarding_page(page))
        elif page.route == "/" or page.route == "/onboarding":
            if is_onboarding_completed():
                print("Onboarding completado, mostrando home")
                page.views.append(create_home_page(page))
            else:
                print("Mostrando onboarding")
                page.views.append(create_onboarding_page(page))
        else:
            # Página por defecto
            print("Mostrando página por defecto (home)")
            page.views.append(create_home_page(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Página inicial

if __name__ == "__main__":
    ft.app(target=main)
