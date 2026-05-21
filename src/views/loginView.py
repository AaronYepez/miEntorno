import flet as ft
from config.themes import MoodDayTheme

def LoginView(page: ft.Page, auth_controller):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=380,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    error_text = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)
    def login_click(e):
        error_text.visible = False
        if not email_input.value:
            error_text.value = "El correo es obligatorio."
            error_text.visible = True
            page.update()
            return
        if "@" not in email_input.value or "." not in email_input.value:
            error_text.value = "Ingresa un correo electrónico válido."
            error_text.visible = True
            page.update()
            return
        if not pass_input.value:
            error_text.value = "La contraseña es obligatoria."
            error_text.visible = True
            page.update()
            return
        user, msg = auth_controller.login(email_input.value, pass_input.value)
        if user:
            page.session.store.set("user", user)
            page.go("/dashboard")
        else:
            error_text.value = msg
            error_text.visible = True
            page.update()

    login_button = ft.ElevatedButton(
        "Entrar",
        on_click=login_click,
        width=380,
        bgcolor=MoodDayTheme.PRIMARY,
        color=MoodDayTheme.TEXT_LIGHT,
        height=45
    )

    pass_input.on_submit = login_click

    # Retorno de la vista
    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Diario Emocional"),
            bgcolor=MoodDayTheme.PRIMARY,
            color=MoodDayTheme.TEXT_LIGHT
        ),
        controls=[
            ft.Container(
                width=460,
                padding=ft.Padding(28, 28, 28, 28),
                bgcolor=MoodDayTheme.BACKGROUND_CARD,
                border_radius=MoodDayTheme.BORDER_RADIUS,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                content=ft.Column(
                    [
                        ft.Text("Bienvenido a MoodDay", size=26, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        ft.Text("Registra tus emociones y crea hábitos para regular tu estado de ánimo.", size=14, color=MoodDayTheme.TEXT_SECONDARY),
                        error_text,
                        email_input,
                        pass_input,
                        login_button,
                        ft.Row(
                            [
                                ft.TextButton("Crear una cuenta nueva", on_click=lambda _: page.go("/registro"), style=ft.ButtonStyle(color=MoodDayTheme.PRIMARY)),
                                ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda _: page.go("/recuperar"), style=ft.ButtonStyle(color=MoodDayTheme.SECONDARY))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True
                        )
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )
