import flet as ft
from config.themes import MoodDayTheme


def SleepView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/sueno", [ft.Text("Redireccionando al login...")])

    view = ft.View(
        route="/sueno",
        bgcolor=MoodDayTheme.DARK_BACKGROUND,
        appbar=ft.AppBar(
            title=ft.Text("Rutina de sueño y relajación", color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.DARK_SURFACE,
            color=MoodDayTheme.TEXT_LIGHT,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="Volver",
                icon_color=MoodDayTheme.TEXT_LIGHT,
                on_click=lambda e: page.go("/dashboard")
            ),
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LIGHTBULB,
                    tooltip="Ver recomendaciones",
                    icon_color=MoodDayTheme.TEXT_LIGHT,
                    on_click=lambda e: page.go("/recomendaciones")
                )
            ]
        ),
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=ft.Padding(24, 24, 24, 24),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=20, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Relájate antes de dormir", size=26, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text(
                                        "Una rutina nocturna más tranquila puede ayudarte a dormir mejor y a despertar con menos estrés.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    )
                                ],
                                spacing=12
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(18, 18, 18, 18),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Rutina para un sueño reparador", size=18, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text(
                                        "Apaga pantallas 30 minutos antes de dormir. Ajusta iluminación suave y respira profundo.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                    ft.Text("1. Ajusta temperatura e iluminación.", size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("2. Evita cafeína y desconecta de las pantallas.", size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("3. Mantén una hora de descanso constante.", size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                ],
                                spacing=10
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(18, 18, 18, 18),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Ejercicio de calma rápida", size=18, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text(
                                        "Cierra los ojos, inhala 4 segundos, mantén 4 y exhala 6. Repite 3 veces mientras relajas hombros y cuello.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                    ft.Text("Haz un escaneo corporal y suelta la tensión donde la notes.", size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                ],
                                spacing=10
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(18, 18, 18, 18),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Relajación mental", size=18, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text(
                                        "Escribe qué sientes y por qué; esto ayuda a soltar la tensión mental antes de dormir.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                    ft.Text("Si quieres, escucha sonidos suaves o una breve meditación guiada.", size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                ],
                                spacing=10
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(18, 18, 18, 18),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Contacto de emergencia", size=18, weight="bold", color=MoodDayTheme.ERROR),
                                    ft.Text(
                                        "Si te sientes en peligro o necesitas apoyo inmediato, contacta a un familiar de confianza o a los servicios de emergencia de tu país.",
                                        size=13,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                    ft.Text(
                                        "En situaciones urgentes, marca 911 o el número de emergencia local. Pedir ayuda es un acto de cuidado.",
                                        size=13,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                ],
                                spacing=10
                            )
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Volver al inicio",
                                    on_click=lambda e: page.go("/dashboard"),
                                    bgcolor=MoodDayTheme.PRIMARY,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=45,
                                    expand=True
                                ),
                                ft.ElevatedButton(
                                    "Ayuda Rápida 🫁",
                                    on_click=lambda e: page.go("/ayuda-rapida"),
                                    bgcolor=MoodDayTheme.SECONDARY,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=45,
                                    expand=True
                                )
                            ],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ],
                    spacing=18
                )
            )
        ]
    )

    return view
