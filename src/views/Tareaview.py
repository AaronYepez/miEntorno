import flet as ft
from config.themes import MoodDayTheme


def TareaView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/", [ft.Text("Redireccionando al login...")])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    error_text = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)

    def refresh():
        lista_tareas.controls.clear()
        tareas = tarea_controller.obtener_lista(user["id_usuario"])
        if not tareas:
            lista_tareas.controls.append(
                ft.Container(
                    padding=20,
                    bgcolor=MoodDayTheme.BACKGROUND_CARD,
                    border_radius=MoodDayTheme.BORDER_RADIUS,
                    content=ft.Text("Aún no hay registros emocionales. Agrega uno nuevo arriba.", size=14, color=MoodDayTheme.TEXT_SECONDARY)
                )
            )
        else:
            for t in tareas:
                estado = t.get("estado_animo", "Neutral")
                intensidad = t.get("intensidad", 0)
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
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text(f"Estado: {estado}", size=12, color=MoodDayTheme.TEXT_LIGHT),
                                                bgcolor=MoodDayTheme.ACCENT,
                                                padding=ft.Padding(8, 5, 8, 5),
                                                border_radius=8
                                            ),
                                            ft.Container(
                                                content=ft.Text(f"Intensidad: {intensidad}/10", size=12, color=MoodDayTheme.TEXT_LIGHT),
                                                bgcolor=MoodDayTheme.INFO,
                                                padding=ft.Padding(8, 5, 8, 5),
                                                border_radius=8
                                            )
                                        ],
                                        spacing=10
                                    )
                                ],
                                spacing=10
                            )
                        )
                    )
                )
        page.update()

    txt_titulo = ft.TextField(
        label="Título del registro emocional",
        expand=True,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    txt_descripcion = ft.TextField(
        label="¿Cómo te sientes? Describe tu estado emocional",
        expand=True,
        multiline=True,
        max_lines=4,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    estado_animo = ft.Dropdown(
        label="¿Cómo te sientes hoy?",
        width=350,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        options=[
            ft.dropdown.Option("Feliz"),
            ft.dropdown.Option("Triste"),
            ft.dropdown.Option("Ansioso"),
            ft.dropdown.Option("Calmado"),
            ft.dropdown.Option("Enojado"),
            ft.dropdown.Option("Neutral"),
        ]
    )

    intensidad = ft.Slider(
        min=1,
        max=10,
        divisions=9,
        label="Intensidad: {value}",
        width=350,
        value=5
    )

    def add_task(e):
        error_text.visible = False
        success, msg = tarea_controller.guardar_nueva(
            user["id_usuario"],
            txt_titulo.value,
            txt_descripcion.value,
            estado_animo.value,
            intensidad.value
        )
        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.SUCCESS if success else MoodDayTheme.ERROR
        )
        page.snack_bar.open = True
        if success:
            txt_titulo.value = ""
            txt_descripcion.value = ""
            estado_animo.value = None
            intensidad.value = 5
            refresh()
        else:
            error_text.value = msg
            error_text.visible = True
        page.update()

    view = ft.View(
        route="/dashboard",
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        appbar=ft.AppBar(
            title=ft.Text(f"MoodDay - Bienvenido, {user['nombre']}", color=MoodDayTheme.TEXT_LIGHT),
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
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            padding=MoodDayTheme.PADDING_STANDARD,
                            bgcolor=MoodDayTheme.BACKGROUND_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Registra tu emoción", size=20, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                    error_text,
                                    txt_titulo,
                                    txt_descripcion,
                                    estado_animo,
                                    intensidad,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Guardar registro",
                                                on_click=add_task,
                                                bgcolor=MoodDayTheme.PRIMARY,
                                                color=MoodDayTheme.TEXT_LIGHT,
                                                height=40
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                spacing=MoodDayTheme.SPACING_STANDARD
                            )
                        ),
                        ft.Divider(height=2, color=MoodDayTheme.BORDER_COLOR),
                        ft.Text("Tus registros emocionales", size=18, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        lista_tareas
                    ],
                    expand=True,
                    spacing=MoodDayTheme.SPACING_STANDARD
                ),
                padding=MoodDayTheme.PADDING_STANDARD,
                expand=True
            )
        ]
    )
    refresh()
    return view
