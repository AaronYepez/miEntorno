import flet as ft
from config.themes import MoodDayTheme


def RegisterView(page: ft.Page, auth_controller):
    nombre_input = ft.TextField(
        label="Nombre completo",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.TEXT,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    numero_control_input = ft.TextField(
        label="Número de control",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    grado_input = ft.TextField(
        label="Grado",
        width=190,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.TEXT,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    grupo_input = ft.TextField(
        label="Grupo",
        width=190,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.TEXT,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    edad_input = ft.TextField(
        label="Edad",
        width=190,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR,
        input_filter=ft.NumbersOnlyInputFilter()
    )

    sexo_input = ft.Dropdown(
        label="Sexo",
        width=190,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        options=[
            ft.dropdown.Option("Femenino"),
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Otro"),
            ft.dropdown.Option("Prefiero no decirlo"),
        ]
    )

    telefono_input = ft.TextField(
        label="Teléfono (opcional)",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        keyboard_type=ft.KeyboardType.PHONE,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    password_input = ft.TextField(
        label="Contraseña (mínimo 8 caracteres)",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    password_confirm_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        text_size=16,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    error_text = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)

    def register_click(e):
        error_text.visible = False
        if not nombre_input.value:
            error_text.value = "El nombre es obligatorio."
            error_text.visible = True
            page.update()
            return
        if len(nombre_input.value) < 3:
            error_text.value = "El nombre debe tener al menos 3 caracteres."
            error_text.visible = True
            page.update()
            return
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
        if not numero_control_input.value:
            error_text.value = "El número de control es obligatorio."
            error_text.visible = True
            page.update()
            return
        if not grado_input.value:
            error_text.value = "El grado es obligatorio."
            error_text.visible = True
            page.update()
            return
        if not grupo_input.value:
            error_text.value = "El grupo es obligatorio."
            error_text.visible = True
            page.update()
            return
        if not edad_input.value:
            error_text.value = "La edad es obligatoria."
            error_text.visible = True
            page.update()
            return
        try:
            edad_valor = int(edad_input.value)
        except ValueError:
            error_text.value = "Ingresa una edad válida."
            error_text.visible = True
            page.update()
            return
        if edad_valor < 10 or edad_valor > 120:
            error_text.value = "La edad debe estar entre 10 y 120 años."
            error_text.visible = True
            page.update()
            return
        if not sexo_input.value:
            error_text.value = "Selecciona tu sexo."
            error_text.visible = True
            page.update()
            return
        if not password_input.value:
            error_text.value = "La contraseña es obligatoria."
            error_text.visible = True
            page.update()
            return
        if len(password_input.value) < 8:
            error_text.value = "La contraseña debe tener al menos 8 caracteres."
            error_text.visible = True
            page.update()
            return
        if not password_confirm_input.value:
            error_text.value = "Debes confirmar la contraseña."
            error_text.visible = True
            page.update()
            return
        if password_input.value != password_confirm_input.value:
            error_text.value = "Las contraseñas no coinciden."
            error_text.visible = True
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(
            nombre_input.value,
            email_input.value,
            password_input.value,
            telefono_input.value or None,
            numero_control_input.value,
            grado_input.value,
            grupo_input.value,
            edad_valor,
            sexo_input.value
        )
        if not success:
            error_text.value = msg
            error_text.visible = True
            page.update()
            return

        page.snack_bar = ft.SnackBar(ft.Text(msg, color=MoodDayTheme.TEXT_LIGHT), bgcolor=MoodDayTheme.SUCCESS)
        page.snack_bar.open = True
        page.update()
        page.go("/")

    register_button = ft.ElevatedButton(
        "Registrar cuenta",
        on_click=register_click,
        width=350,
        bgcolor=MoodDayTheme.PRIMARY,
        color=MoodDayTheme.TEXT_LIGHT,
        height=45
    )

    return ft.View(
        route="/registro",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        scroll=ft.ScrollMode.AUTO,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Registro"),
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
                        ft.Text("Crea tu diario emocional", size=24, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        ft.Text("Regístrate para empezar a seguir tu estado de ánimo.", size=14, color=MoodDayTheme.TEXT_SECONDARY),
                        error_text,
                        nombre_input,
                        email_input,
                        numero_control_input,
                        ft.Row([grado_input, grupo_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=20, wrap=True),
                        ft.Row([edad_input, sexo_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=20, wrap=True),
                        telefono_input,
                        password_input,
                        password_confirm_input,
                        register_button,
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
