import flet as ft
import threading
from config.themes import MoodDayTheme


def TareaView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/", [ft.Text("Redireccionando al login...")])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    error_text = ft.Text("", color=MoodDayTheme.ERROR, size=13, visible=False)
    alerta_card = ft.Container(
        visible=False,
        padding=ft.Padding(16, 16, 16, 16),
        bgcolor=MoodDayTheme.WARNING,
        border_radius=MoodDayTheme.BORDER_RADIUS,
        content=ft.Text("", size=13, color=MoodDayTheme.TEXT_PRIMARY)
    )
    alert_timer = None

    def clear_alert():
        nonlocal alert_timer
        alerta_card.visible = False
        alert_timer = None
        page.update()

    def emotion_color(estado):
        mapping = {
            "Feliz": MoodDayTheme.EMOTION_HAPPY,
            "Triste": MoodDayTheme.EMOTION_SAD,
            "Ansioso": MoodDayTheme.EMOTION_ANXIOUS,
            "Calmado": MoodDayTheme.EMOTION_CALM,
            "Enojado": MoodDayTheme.EMOTION_ANGRY,
            "Estresado": MoodDayTheme.WARNING,
            "Agotado": MoodDayTheme.WARNING,
            "Neutral": MoodDayTheme.EMOTION_NEUTRAL,
        }
        return mapping.get(estado, MoodDayTheme.INFO)

    def open_dialog(dialog):
        page.dialog = dialog
        page.dialog.open = True
        page.update()



    def refresh():
        lista_tareas.controls.clear()
        tareas = tarea_controller.obtener_lista(user["id_usuario"])
        alerta_text = tarea_controller.evaluar_alerta(user["id_usuario"])

        # mensaje de alerta (5.5 seconds)
        nonlocal alert_timer
        if alerta_text:
            alerta_card.visible = True
            alerta_card.content = ft.Text(alerta_text, size=13, color=MoodDayTheme.TEXT_PRIMARY)
            page.snack_bar = ft.SnackBar(
                ft.Text(alerta_text, color=MoodDayTheme.TEXT_LIGHT),
                bgcolor=MoodDayTheme.WARNING,
                open=True
            )
            if alert_timer is not None:
                try:
                    alert_timer.cancel()
                except Exception:
                    pass
            alert_timer = threading.Timer(5.5, clear_alert)
            alert_timer.daemon = True
            alert_timer.start()
        else:
            alerta_card.visible = False

        if not tareas:
            lista_tareas.controls.append(
                ft.Container(
                    padding=20,
                    bgcolor=MoodDayTheme.BACKGROUND_CARD,
                    border_radius=MoodDayTheme.BORDER_RADIUS,
                    content=ft.Text(
                        "Aún no hay registros emocionales. Agrega uno nuevo arriba.",
                        size=14,
                        color=MoodDayTheme.TEXT_SECONDARY
                    )
                )
            )
        else:
            for t in tareas:
                estado = t.get("estado_animo", "Neutral")
                intensidad = t.get("intensidad", 0)
                mensaje_motivador = t.get("mensaje_motivador")
                lista_tareas.controls.append(
                    ft.Card(
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=MoodDayTheme.BORDER_RADIUS),
                        content=ft.Container(
                            bgcolor=MoodDayTheme.BACKGROUND_CARD,
                            padding=15,
                            content=ft.Column(
                                [
                                    ft.Text(t["titulo"], weight="bold", size=16, color=MoodDayTheme.TEXT_PRIMARY),
                                    ft.Text(t.get("descripcion", ""), size=13, color=MoodDayTheme.TEXT_SECONDARY),
                                    ft.Text(f"¿Por qué? {t.get('razon_emocion', '')}", size=13, color=MoodDayTheme.TEXT_SECONDARY),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text(f"Estado: {estado}", size=12, color=MoodDayTheme.TEXT_LIGHT),
                                                bgcolor=emotion_color(estado),
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
                                    ),
                                    ft.Text("Frase motivadora:", size=12, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                    ft.Text(mensaje_motivador or "Sin frase motivadora por el momento.", size=13, color=MoodDayTheme.TEXT_SECONDARY)
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

    txt_razon = ft.TextField(
        label="¿Por qué crees que te sientes así?",
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
            ft.dropdown.Option("Estresado"),
            ft.dropdown.Option("Agotado"),
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

    def show_motivational_message(text):
        dialog = ft.AlertDialog(
            title=ft.Text("Tu mensaje motivador", weight="bold"),
            content=ft.Text(text, size=14, color=MoodDayTheme.TEXT_SECONDARY),
            actions=[
                ft.ElevatedButton("Gracias", on_click=lambda e: (setattr(page.dialog, 'open', False), page.update()))
            ]
        )
        open_dialog(dialog)

    def add_task(e):
        error_text.visible = False
        success, msg, frase = tarea_controller.guardar_nueva(
            user["id_usuario"],
            txt_titulo.value,
            txt_descripcion.value,
            txt_razon.value,
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
            txt_razon.value = ""
            estado_animo.value = None
            intensidad.value = 5
            refresh()
            if frase:
                show_motivational_message(frase)
        else:
            error_text.value = msg
            error_text.visible = True
        page.update()

    view = ft.View(
        route="/dashboard",
        bgcolor=MoodDayTheme.BACKGROUND_LIGHT,
        scroll=ft.ScrollMode.AUTO,
        appbar=ft.AppBar(
            title=ft.Text(f"MoodDay - Bienvenido, {user['nombre']}", color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.PRIMARY,
            color=MoodDayTheme.TEXT_LIGHT,
            actions=[
                ft.IconButton(
                    ft.Icons.LIGHTBULB,
                    tooltip="Ver recomendaciones",
                    icon_color=MoodDayTheme.TEXT_LIGHT,
                    on_click=lambda e: page.go("/recomendaciones")
                ),
                ft.IconButton(
                    ft.Icons.HEALING,
                    tooltip="Ejercicios de relajación y sueño",
                    icon_color=MoodDayTheme.TEXT_LIGHT,
                    on_click=lambda e: page.go("/sueno")
                ),
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
                padding=MoodDayTheme.PADDING_STANDARD,
                expand=True,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Registra tu emoción", size=22, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                                        ft.Text(
                                            "Agrega cómo te sientes hoy y recibe una frase motivadora para apoyarte.",
                                            size=14,
                                            color=MoodDayTheme.TEXT_SECONDARY
                                        )
                                    ],
                                    expand=True
                                ),
                                ft.ElevatedButton(
                                    "Ver recomendaciones",
                                    on_click=lambda e: page.go("/recomendaciones"),
                                    bgcolor=MoodDayTheme.SECONDARY,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=40
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        alerta_card,
                        ft.Container(
                            padding=MoodDayTheme.PADDING_STANDARD,
                            bgcolor=MoodDayTheme.BACKGROUND_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    txt_titulo,
                                    txt_descripcion,
                                    txt_razon,
                                    estado_animo,
                                    intensidad,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Guardar registro",
                                                on_click=add_task,
                                                bgcolor=MoodDayTheme.PRIMARY,
                                                color=MoodDayTheme.TEXT_LIGHT,
                                                height=45
                                            ),

                                        ],
                                        spacing=15
                                    )
                                ],
                                spacing=15
                            )
                        ),
                        ft.Divider(height=2, color=MoodDayTheme.BORDER_COLOR),
                        ft.Text("Tus registros emocionales", size=18, weight="bold", color=MoodDayTheme.TEXT_PRIMARY),
                        lista_tareas
                    ],
                    spacing=MoodDayTheme.SPACING_STANDARD
                )
            )
        ]
    )
    refresh()
    return view
