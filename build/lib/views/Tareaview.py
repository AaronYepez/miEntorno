import flet as ft

# esta vista es la que muestra el dashboard de tareas
# y guarda nuevas tareas para el usuario que inició sesión

def TareaView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/", [ft.Text("redireccionando al login...")])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def refresh():
        lista_tareas.controls.clear()
        tareas = tarea_controller.obtener_lista(user["id_usuario"])
        if not tareas:
            lista_tareas.controls.append(ft.Text("no tienes tareas aún. agrega una nueva arriba."))
        else:
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t["titulo"], weight="bold"),
                                subtitle=ft.Text(
                                    f"{t.get('descripcion', '')}\nPrioridad: {t.get('prioridad', 'media')}"
                                ),
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
    txt_descripcion = ft.TextField(
        label="Descripción (opcional)",
        expand=True,
        multiline=True,
        max_lines=3
    )

    def add_task(e):
        success, msg = tarea_controller.guardar_nueva(
            user["id_usuario"], txt_titulo.value, txt_descripcion.value
        )
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        if success:
            txt_titulo.value = ""
            txt_descripcion.value = ""
            refresh()
        page.update()

    view = ft.View(
        route="/dashboard",
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
                        ft.Row([txt_titulo, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_task)]),
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
