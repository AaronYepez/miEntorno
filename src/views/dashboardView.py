import flet as ft
from controllers.tareacontroller import TareaController

def DashboardView(page, tarea_controller):
    # si el usuario no esta en session lo mando al login otra vez
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/", [ft.Text("redireccionando al login...")])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def refresh():
        lista_tareas.controls.clear()
        tareas = tarea_controller.obtener_lista(user["id_usuario"])
        if not tareas:
            lista_tareas.controls.append(ft.Text("no tienes tareas aún. agrega una nueva tarea arriba."))
        else:
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t["titulo"], weight="bold"),
                                subtitle=ft.Text(f"{t.get('descripcion', '')}\nPrioridad: {t.get('prioridad', 'media')}") if t.get("descripcion") else ft.Text(f"Prioridad: {t.get('prioridad', 'media')}"),
                                trailing=ft.Container(
                                    content=ft.Text(t.get("estado", "pendiente"), color="white", size=12),
                                    bgcolor=ft.Colors.ORANGE_300,
                                    padding=5,
                                    border_radius=3
                                )
                            ),
                            padding=10
                        )
                    )
                )
        page.update()

    txt_titulo = ft.TextField(label="Título de la tarea", expand=True)
    txt_descripcion = ft.TextField(label="Descripción (opcional)", expand=True, multiline=True, max_lines=3)

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
            title=ft.Text(f"Bienvenido, {user['nombre']}"),
            actions=[
                ft.IconButton(
                    ft.Icons.EXIT_TO_APP,
                    tooltip="Cerrar sesión",
                    on_click=lambda e: page.session.store.clear() or page.go("/")
                )
            ]
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            txt_titulo,
                            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_task)
                        ]),
                        txt_descripcion,
                        ft.Divider(),
                        ft.Text("mis tareas pendientes", size=20, weight="bold"),
                        lista_tareas
                    ],
                    expand=True,
                    spacing=15
                ),
                padding=20,
                expand=True
            )
        ]
    )
    refresh()
    return view


def RegisterView(page: ft.Page, auth_controller):
    # registro en el mismo archivo dashboardView para no usar registerView.py
    nombre_input = ft.TextField(
        label="Nombre completo",
        width=350,
        border_radius=10
    )

    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL
    )

    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10
    )

    password_confirm_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10
    )

    def register_click(e):
        if not nombre_input.value or not email_input.value or not password_input.value or not password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llene todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        if password_input.value != password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(
            nombre_input.value,
            email_input.value,
            password_input.value
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
        bgcolor="blue",
        color="white"
    )

    return ft.View(
        route="/registro",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("SIGE - Registro"),
            bgcolor="bluegrey900",
            color="white"
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Crear una cuenta nueva", size=24, weight="bold"),
                    nombre_input,
                    email_input,
                    password_input,
                    password_confirm_input,
                    register_button,
                    ft.TextButton(
                        "Volver al login",
                        on_click=lambda _: page.go("/")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=20
            )
        ]
    )
