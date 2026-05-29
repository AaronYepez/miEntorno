import flet as ft
from config.themes import MoodDayTheme


def ForgotPasswordView(page: ft.Page, auth_controller):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    error_text = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)

    def on_send_click(e):
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
        success, msg = auth_controller.enviar_email_recuperacion(email_input.value)
        if not success:
            error_text.value = msg
            error_text.visible = True
            page.update()
            return
        page.snack_bar = ft.SnackBar(ft.Text(msg, color=MoodDayTheme.TEXT_LIGHT), bgcolor=MoodDayTheme.SUCCESS)
        page.snack_bar.open = True
        page.session.store.set("recovery_email", email_input.value)
        page.go("/reset")

    return ft.View(
        route="/recuperar",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Recuperar contraseña"),
            bgcolor=MoodDayTheme.SECONDARY,
            color=MoodDayTheme.TEXT_LIGHT
        ),
        controls=[
            ft.Container(
                width=420,
                padding=ft.Padding(30, 30, 30, 30),
                bgcolor=MoodDayTheme.BACKGROUND_CARD,
                border_radius=MoodDayTheme.BORDER_RADIUS,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                content=ft.Column(
                    [
                        ft.Text("Recupera tu cuenta", size=24, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        ft.Text("Ingresa tu correo y te enviaremos un código de recuperación.", size=14, color=MoodDayTheme.TEXT_SECONDARY),
                        error_text,
                        email_input,
                        ft.ElevatedButton(
                            "Enviar código de recuperación",
                            on_click=on_send_click,
                            width=350,
                            bgcolor=MoodDayTheme.SECONDARY,
                            color=MoodDayTheme.TEXT_LIGHT,
                            height=45
                        ),
                        ft.TextButton(
                            "Volver al inicio de sesión",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color=MoodDayTheme.PRIMARY)
                        )
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )


def ResetPasswordView(page: ft.Page, auth_controller):
    code_input = ft.TextField(
        label="Código de recuperación",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR,
        text_align=ft.TextAlign.CENTER,
        input_filter=ft.NumbersOnlyInputFilter()
    )
    code_error = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)
    password_input = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR,
        visible=False
    )
    password_confirm_input = ft.TextField(
        label="Confirmar nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR,
        visible=False
    )
    pass_error = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)

    def validate_code(e):
        if not code_input.value:
            code_error.value = "El código es obligatorio."
            code_error.visible = True
            page.update()
            return
        if not code_input.value.isdigit():
            code_error.value = "El código solo debe contener números."
            code_error.visible = True
            page.update()
            return
        if len(code_input.value) != 6:
            code_error.value = "El código debe tener 6 dígitos."
            code_error.visible = True
            page.update()
            return
        user = auth_controller.model.obtener_usuario_por_token(code_input.value)
        if not user:
            code_error.value = "El código es inválido o ha expirado."
            code_error.visible = True
            page.update()
            return
        code_error.visible = False
        code_input.read_only = True
        password_input.visible = True
        password_confirm_input.visible = True
        validar_btn.visible = False
        restablecer_btn.visible = True
        page.update()

    def change_password(e):
        if not password_input.value:
            pass_error.value = "La nueva contraseña es obligatoria."
            pass_error.visible = True
            page.update()
            return
        if not password_confirm_input.value:
            pass_error.value = "Debes confirmar la nueva contraseña."
            pass_error.visible = True
            page.update()
            return
        if len(password_input.value) < 8:
            pass_error.value = "La contraseña debe tener al menos 8 caracteres."
            pass_error.visible = True
            page.update()
            return
        if password_input.value != password_confirm_input.value:
            pass_error.value = "Las contraseñas no coinciden."
            pass_error.visible = True
            page.update()
            return
        success, msg = auth_controller.restablecer_contrasena(code_input.value, password_input.value)
        pass_error.value = msg
        pass_error.visible = True
        page.update()
        if success:
            page.go("/")

    validar_btn = ft.ElevatedButton(
        "Validar código",
        on_click=validate_code,
        width=350,
        bgcolor=MoodDayTheme.SECONDARY,
        color=MoodDayTheme.TEXT_LIGHT,
        height=45,
        visible=True
    )
    restablecer_btn = ft.ElevatedButton(
        "Restablecer contraseña",
        on_click=change_password,
        width=350,
        bgcolor=MoodDayTheme.SECONDARY,
        color=MoodDayTheme.TEXT_LIGHT,
        height=45,
        visible=False
    )
    return ft.View(
        route="/reset",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Cambiar contraseña"),
            bgcolor=MoodDayTheme.SECONDARY,
            color=MoodDayTheme.TEXT_LIGHT
        ),
        controls=[
            ft.Container(
                width=420,
                padding=ft.Padding(30, 30, 30, 30),
                bgcolor=MoodDayTheme.BACKGROUND_CARD,
                border_radius=MoodDayTheme.BORDER_RADIUS,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                content=ft.Column(
                    [
                        ft.Text("Cambia tu contraseña", size=24, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        ft.Text("Usa el código que te enviamos por correo para restablecer tu acceso.", size=14, color=MoodDayTheme.TEXT_SECONDARY),
                        ft.Text("El código es válido por 15 minutos", size=12, color=MoodDayTheme.INFO, weight="bold"),
                        code_error,
                        code_input,
                        validar_btn,
                        password_input,
                        password_confirm_input,
                        pass_error,
                        restablecer_btn,
                        ft.TextButton(
                            "Volver al inicio de sesión",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color=MoodDayTheme.PRIMARY)
                        )
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )
