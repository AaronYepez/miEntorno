import flet as ft
from controllers.tareacontroller import TareaController


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
                    bgcolor="#FFFFFF",
                    border_radius=15,
                    content=ft.Text("Aún no hay registros emocionales. Crea tu primera entrada.", size=14)
                )
            )
        else:
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=18),
                        content=ft.Container(
                            bgcolor="#F7FBFF",
                            padding=15,
                            content=ft.Column(
                                [
                                    ft.Text(t["titulo"], weight="bold", size=16),
                                    ft.Text(t.get("descripcion", ""), size=13),
                                ],
                                spacing=8
                            )
                        )
                    )
                )
        page.update()

    txt_titulo = ft.TextField(label="Título de la entrada emocional", expand=True, border_radius=15)
    txt_descripcion = ft.TextField(label="Describe cómo te sientes", expand=True, multiline=True, max_lines=4, border_radius=15)

    def add_task(e):
        success, msg = tarea_controller.guardar_nueva(user["id_usuario"], txt_titulo.value, txt_descripcion.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        if success:
            txt_titulo.value = ""
            txt_descripcion.value = ""
            refresh()
        page.update()

    view = ft.View(
        "/dashboard",
        appbar=ft.AppBar(
            title=ft.Text(f"MoodDay - Hola {user['nombre']}"),
            bgcolor="#5E97D1",
            color="white",
            actions=[
                ft.IconButton(
                    ft.Icons.EXIT_TO_APP,
                    tooltip="Cerrar sesión",
                    on_click=lambda e: page.session.store.clear() or page.go("/")
                )
            ]
        ),
        bgcolor="#E9F2FF",
        controls=[
            ft.Container(
                width=700,
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=20,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            content=ft.Column(
                                [
                                    ft.Text("Nueva entrada emocional", size=20, weight="bold"),
                                    txt_titulo,
                                    txt_descripcion,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton("Guardar entrada", on_click=add_task, bgcolor="#5E97D1", color="white"),
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                spacing=15
                            )
                        ),
                        ft.Divider(height=2),
                        ft.Text("Mis registros emocionales", size=18, weight="bold"),
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
        border_radius=15,
        text_size=16
    )

    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=15,
        keyboard_type=ft.KeyboardType.EMAIL,
        text_size=16
    )

    telefono_input = ft.TextField(
        label="Teléfono (opcional)",
        width=350,
        border_radius=15,
        keyboard_type=ft.KeyboardType.PHONE,
        text_size=16
    )

    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=15,
        text_size=16
    )

    password_confirm_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=15,
        text_size=16
    )

    def register_click(e):
        if not nombre_input.value or not email_input.value or not password_input.value or not password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios."))
            page.snack_bar.open = True
            page.update()
            return

        if password_input.value != password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden."))
            page.snack_bar.open = True
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(
            nombre_input.value,
            email_input.value,
            password_input.value,
            telefono_input.value or None
        )

        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

        if success:
            page.go("/")

    register_button = ft.ElevatedButton(
        "Registrar cuenta",
        on_click=register_click,
        width=350,
        bgcolor="#5E97D1",
        color="white"
    )

    return ft.View(
        route="/registro",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("MoodDay | Registro"),
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
                        ft.Text("Crea tu diario emocional", size=24, weight="bold"),
                        ft.Text("Regístrate para empezar a seguir tu estado de ánimo.", size=14),
                        nombre_input,
                        email_input,
                        telefono_input,
                        password_input,
                        password_confirm_input,
                        register_button,
                        ft.TextButton("Volver al inicio de sesión", on_click=lambda _: page.go("/"))
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )
