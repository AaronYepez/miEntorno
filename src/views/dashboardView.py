import flet as ft
from controllers.tareacontroller import TareaController
from config.themes import MoodDayTheme


def DashboardView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/", [ft.Text("Redireccionando al login...")])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def refresh():
        lista_tareas.controls.clear()
        tareas = tarea_controller.obtener_lista(user["id_usuario"])
        if not tareas:
            lista_tareas.controls.append(
                ft.Container(
                    padding=20,
                    bgcolor=MoodDayTheme.BACKGROUND_CARD,
                    border_radius=MoodDayTheme.BORDER_RADIUS,
                    content=ft.Text("Aún no hay registros emocionales. Crea tu primera entrada.", size=14, color=MoodDayTheme.TEXT_SECONDARY)
                )
            )
        else:
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=MoodDayTheme.BORDER_RADIUS),
                        content=ft.Container(
                            bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
                            padding=15,
                            content=ft.Column(
                                [
                                    ft.Text(t["titulo"], weight="bold", size=16, color=MoodDayTheme.TEXT_PRIMARY),
                                    ft.Text(t.get("descripcion", ""), size=13, color=MoodDayTheme.TEXT_SECONDARY),
                                ],
                                spacing=8
                            )
                        )
                    )
                )
        page.update()

    txt_titulo = ft.TextField(label="Título de la entrada emocional", expand=True, border_radius=MoodDayTheme.BORDER_RADIUS, border_color=MoodDayTheme.BORDER_COLOR)
    txt_descripcion = ft.TextField(label="Describe cómo te sientes", expand=True, multiline=True, max_lines=4, border_radius=MoodDayTheme.BORDER_RADIUS, border_color=MoodDayTheme.BORDER_COLOR)

    def add_task(e):
        success, msg = tarea_controller.guardar_nueva(user["id_usuario"], txt_titulo.value, txt_descripcion.value)
        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.SUCCESS if success else MoodDayTheme.ERROR
        )
        page.snack_bar.open = True
        if success:
            txt_titulo.value = ""
            txt_descripcion.value = ""
            refresh()
        page.update()

    view = ft.View(
        "/dashboard",
        appbar=ft.AppBar(
            title=ft.Text(f"MoodDay - Hola {user['nombre']}", color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.PRIMARY,
            color=MoodDayTheme.TEXT_LIGHT,
            actions=[
                ft.IconButton(
                    ft.Icons.EXIT_TO_APP,
                    tooltip="Cerrar sesión",
                    icon_color=MoodDayTheme.TEXT_LIGHT,
                    on_click=lambda e: (page.session.store.clear(), page.go("/"))
                )
            ]
        ),
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        controls=[
            ft.Container(
                width=700,
                padding=MoodDayTheme.PADDING_STANDARD,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=MoodDayTheme.PADDING_STANDARD,
                            bgcolor=MoodDayTheme.BACKGROUND_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Nueva entrada emocional", size=20, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                    txt_titulo,
                                    txt_descripcion,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton("Guardar entrada", on_click=add_task, bgcolor=MoodDayTheme.PRIMARY, color=MoodDayTheme.TEXT_LIGHT),
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                spacing=15
                            )
                        ),
                        ft.Divider(height=2, color=MoodDayTheme.BORDER_COLOR),
                        ft.Text("Mis registros emocionales", size=18, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        lista_tareas
                    ],
                    spacing=20
                )
            )
        ]
    )
    refresh()
    return view


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
        # Validaciones campo a campo
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
            telefono_input.value or None
        )
        if not success:
            error_text.value = msg
            error_text.visible = True
            page.update()
            return
        # Éxito
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
