import flet as ft
from config.themes import MoodDayTheme

# Vista del dashboard principal después de iniciar sesión
# Muestra las emociones registradas del usuario

def TareaView(page, tarea_controller):
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
                    content=ft.Text("No tienes registros emocionales aún. Agrega uno nuevo arriba.", size=14, color=MoodDayTheme.TEXT_SECONDARY)
                )
            )
        else:
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=MoodDayTheme.BORDER_RADIUS),
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t["titulo"], weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                subtitle=ft.Text(
                                    f"{t.get('descripcion', '')}\nPrioridad: {t.get('prioridad', 'media')}",
                                    color=MoodDayTheme.TEXT_SECONDARY,
                                    size=12
                                ),
                                trailing=ft.Container(
                                    content=ft.Text(t.get("estado", "pendiente"), color=MoodDayTheme.TEXT_LIGHT, size=12, weight="bold"),
                                    bgcolor=MoodDayTheme.ACCENT,
                                    padding=8,
                                    border_radius=5
                                )
                            ),
                            padding=10
                        )
                    )
                )
        page.update()

    txt_titulo = ft.TextField(
        label="Título del registro",
        expand=True,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        border_color=MoodDayTheme.BORDER_COLOR
    )
    
    txt_descripcion = ft.TextField(
        label="¿Cómo te sientes? Describe tu estado emocional",
        expand=True,
        multiline=True,
        max_lines=3,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        border_color=MoodDayTheme.BORDER_COLOR
    )

    def add_task(e):
        success, msg = tarea_controller.guardar_nueva(
            user["id_usuario"], txt_titulo.value, txt_descripcion.value
        )
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
                                    ft.Text("Registra tu emoción", size=18, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                    ft.Row([txt_titulo], spacing=10),
                                    txt_descripcion,
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
                                expand=False,
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
