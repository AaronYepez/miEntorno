import flet as ft

def LoginView(page: ft.Page, auth_controller):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=380,
        border_radius=15,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16
    )

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=15,
        text_size=16
    )

    def login_click(e):
        if not email_input.value or not pass_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos."))
            page.snack_bar.open = True
            page.update()
            return

        user, msg = auth_controller.login(email_input.value, pass_input.value)
        if user:
            page.session.store.set("user", user)
            page.go("/dashboard")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()

    login_button = ft.ElevatedButton(
        "Entrar",
        on_click=login_click,
        width=380,
        bgcolor="#5E97D1",
        color="white"
    )

    pass_input.on_submit = login_click

    # Retorno de la vista
    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Diario Emocional"),
            bgcolor="#5E97D1",
            color="white"
        ),
        controls=[
            ft.Container(
                width=460,
                padding=ft.Padding(28, 28, 28, 28),
                bgcolor="#F2F9FF",
                border_radius=25,
                content=ft.Column(
                    [
                        ft.Text("Bienvenido a MoodDay", size=26, weight="bold"),
                        ft.Text("Registra tus emociones y crea hábitos para regular tu estado de ánimo.", size=14),
                        email_input,
                        pass_input,
                        login_button,
                        ft.Row(
                            [
                                ft.TextButton("Crear una cuenta nueva", on_click=lambda _: page.go("/registro")),
                                ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda _: page.go("/recuperar"))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )