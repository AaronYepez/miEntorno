import flet as ft


def ForgotPasswordView(page: ft.Page, auth_controller):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16
    )

    def on_send_click(e):
        if not email_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, ingresa tu correo electrónico."))
            page.snack_bar.open = True
            page.update()
            return

        success, msg = auth_controller.enviar_email_recuperacion(email_input.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()
        if success:
            page.go("/reset")

    return ft.View(
        route="/recuperar",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Recuperar contraseña"),
            bgcolor=ft.colors.SEA_GREEN_700,
            color="white"
        ),
        controls=[
            ft.Container(
                width=420,
                padding=ft.Padding(30, 30, 30, 30),
                bgcolor="#F2F8FF",
                border_radius=20,
                content=ft.Column(
                    [
                        ft.Text("Recupera tu cuenta", size=24, weight="bold"),
                        ft.Text("Ingresa tu correo y te enviaremos un código de recuperación.", size=14),
                        email_input,
                        ft.ElevatedButton("Enviar correo de recuperación", on_click=on_send_click, width=350, bgcolor=ft.colors.SEA_GREEN_700, color="white"),
                        ft.TextButton("Volver al inicio de sesión", on_click=lambda _: page.go("/"))
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )


def ResetPasswordView(page: ft.Page, auth_controller):
    token_input = ft.TextField(
        label="Código de recuperación",
        width=350,
        border_radius=10,
        text_size=16
    )
    password_input = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10,
        text_size=16
    )
    password_confirm_input = ft.TextField(
        label="Confirmar nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10,
        text_size=16
    )

    def on_reset_click(e):
        if not token_input.value or not password_input.value or not password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."))
            page.snack_bar.open = True
            page.update()
            return

        if password_input.value != password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden."))
            page.snack_bar.open = True
            page.update()
            return

        success, msg = auth_controller.restablecer_contrasena(token_input.value, password_input.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()
        if success:
            page.go("/")

    return ft.View(
        route="/reset",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Cambiar contraseña"),
            bgcolor=ft.colors.SEA_GREEN_700,
            color="white"
        ),
        controls=[
            ft.Container(
                width=420,
                padding=ft.Padding(30, 30, 30, 30),
                bgcolor="#F2F8FF",
                border_radius=20,
                content=ft.Column(
                    [
                        ft.Text("Cambia tu contraseña", size=24, weight="bold"),
                        ft.Text("Usa el código que te enviamos por correo para restablecer tu acceso.", size=14),
                        token_input,
                        password_input,
                        password_confirm_input,
                        ft.ElevatedButton("Restablecer contraseña", on_click=on_reset_click, width=350, bgcolor=ft.colors.SEA_GREEN_700, color="white"),
                        ft.TextButton("Volver al inicio de sesión", on_click=lambda _: page.go("/"))
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )
