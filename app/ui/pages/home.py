import flet as ft
from config import Colors, Design

def create_home_page(page):
    return ft.View(
        "/",
        [
            ft.AppBar(
                title=ft.Text(
                    "awa - Hidratación",
                    color=Colors.TEXT_LIGHT,
                    size=Design.FONT_SIZE_MEDIUM,
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=Colors.PRIMARY,
                elevation=0
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.WATER_DROP,
                            size=80,
                            color=Colors.PRIMARY
                        ),
                        padding=ft.padding.only(top=Design.PADDING_LARGE)
                    ),
                    ft.Text(
                        "¡Bienvenido a awa!",
                        size=Design.FONT_SIZE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.TEXT_PRIMARY
                    ),
                    ft.Text(
                        "Tu panel principal estará aquí",
                        size=Design.FONT_SIZE_NORMAL,
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.TEXT_SECONDARY
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Configurar perfil",
                            style=ft.ButtonStyle(
                                bgcolor=Colors.PRIMARY,
                                color=Colors.TEXT_LIGHT,
                                text_style=ft.TextStyle(
                                    size=Design.FONT_SIZE_NORMAL,
                                    weight=ft.FontWeight.BOLD
                                ),
                                shape=ft.RoundedRectangleBorder(radius=Design.BORDER_RADIUS_SMALL)
                            ),
                            width=200,
                            height=50
                        ),
                        padding=ft.padding.only(top=Design.PADDING_LARGE)
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Design.SPACING_MEDIUM),
                padding=ft.padding.all(Design.PADDING_LARGE),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=Colors.ACCENT
            )
        ]
    )
            