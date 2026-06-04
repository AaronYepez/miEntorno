import flet as ft
from config.themes import MoodDayTheme


def get_recommendations_for_estado(estado_animo):
    estado_animo = (estado_animo or "Neutral").lower()

    recommendations_dict = {
        "triste": [
            {
                "icon": "🫁",
                "title": "Respiración consciente",
                "content": "Inhala profundamente por 4 segundos, mantén 4 y exhala 6. Repite 3 veces para calmar la mente.",
                "color": "#8B5CF6"
            },
            {
                "icon": "🎵",
                "title": "Conecta con algo agradable",
                "content": "Escucha una canción suave, escribe algo por lo que estés agradecido o da una caminata breve.",
                "color": "#EC4899"
            },
            {
                "icon": "💬",
                "title": "Habla con alguien de confianza",
                "content": "Compartir lo que sientes puede aliviar la carga emocional y ayudarte a sentirte más acompañado.",
                "color": "#3B82F6"
            }
        ],
        "ansioso": [
            {
                "icon": "🫁",
                "title": "Ejercicio 4-7-8",
                "content": "Coloca una mano en el pecho y otra en el abdomen. Respira lento y profundo juntos para bajar la ansiedad.",
                "color": "#F59E0B"
            },
            {
                "icon": "📱",
                "title": "Pausa digital",
                "content": "Toma unos minutos para desconectarte de las pantallas y enfócate en tu entorno.",
                "color": "#10B981"
            },
            {
                "icon": "🚶",
                "title": "Actividad breve",
                "content": "Haz algo pequeño y agradable como estirarte, caminar o beber agua.",
                "color": "#6366F1"
            }
        ],
        "estresado": [
            {
                "icon": "💪",
                "title": "Relajación muscular",
                "content": "Tensa y suelta cada grupo muscular de pies a cabeza durante 30 segundos.",
                "color": "#EF4444"
            },
            {
                "icon": "✅",
                "title": "Divide en pasos",
                "content": "Organiza tus tareas en pasos pequeños y avanza un paso a la vez.",
                "color": "#14B8A6"
            },
            {
                "icon": "🎨",
                "title": "Tiempo para ti",
                "content": "Dedica unos minutos a una actividad recreativa que te relaje.",
                "color": "#F97316"
            }
        ],
        "agotado": [
            {
                "icon": "😴",
                "title": "Descanso breve",
                "content": "Cierra los ojos un momento, relaja los hombros y respira profundo 5 veces.",
                "color": "#6366F1"
            },
            {
                "icon": "💧",
                "title": "Hidratación",
                "content": "Toma agua y permite que tu cuerpo recupere energía.",
                "color": "#06B6D4"
            },
            {
                "icon": "🏃",
                "title": "Movimiento suave",
                "content": "Haz un estiramiento lento o una caminata ligera para activar tu cuerpo sin forzarlo.",
                "color": "#10B981"
            }
        ]
    }
    
    if estado_animo in recommendations_dict:
        return recommendations_dict[estado_animo]
    else:
        return [
            {
                "icon": "🧘",
                "title": "Atención plena",
                "content": "Tómate unos segundos para notar cómo te sientes y respirar con calma.",
                "color": "#8B5CF6"
            },
            {
                "icon": "🎮",
                "title": "Actividad divertida",
                "content": "Haz algo que disfrutes, aunque sea breve: escucha música, dibuja o escribe una idea positiva.",
                "color": "#EC4899"
            },
            {
                "icon": "🤝",
                "title": "Mantén la conexión",
                "content": "Comparte tus pensamientos con alguien de confianza si lo deseas.",
                "color": "#3B82F6"
            }
        ]


def RecommendationsView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/recomendaciones", [ft.Text("Redireccionando al login...")])

    tareas = tarea_controller.obtener_lista(user["id_usuario"])
    ultimo_estado = tareas[0].get("estado_animo") if tareas else "Neutral"
    recomendaciones = get_recommendations_for_estado(ultimo_estado)
    
    # Emojis para estados de ánimo
    mood_emojis = {
        "triste": "😔",
        "ansioso": "😰",
        "estresado": "😟",
        "agotado": "😴",
        "neutral": "😐",
        "feliz": "😊"
    }
    mood_emoji = mood_emojis.get(ultimo_estado.lower(), "😐")
    estado_resumen = f"{mood_emoji} Tu último registro muestra que te sientes: {ultimo_estado}"

    # Crear tarjetas mejoradas
    cards = []
    for idx, item in enumerate(recomendaciones):
        cards.append(
            ft.Container(
                padding=ft.Padding(20, 20, 20, 20),
                bgcolor=MoodDayTheme.DARK_CARD,
                border_radius=MoodDayTheme.BORDER_RADIUS,
                shadow=ft.BoxShadow(blur_radius=15, color="#00000020", offset=ft.Offset(0, 2)),

                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(item["icon"], size=36),
                                ft.Column(
                                    [
                                        ft.Text(item["title"], size=16, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ]
                                )
                            ],
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Text(item["content"], size=13, color=MoodDayTheme.TEXT_LIGHT_SECONDARY, selectable=True),
                    ],
                    spacing=12
                )
            )
        )

    view = ft.View(
        route="/recomendaciones",
        bgcolor=MoodDayTheme.DARK_BACKGROUND,
        appbar=ft.AppBar(
            title=ft.Text("Consejos de Bienestar", color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.DARK_SURFACE,
            color=MoodDayTheme.TEXT_LIGHT,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: page.go("/dashboard"),
                icon_color=MoodDayTheme.TEXT_LIGHT,
                tooltip="Volver al dashboard"
            ),
            actions=[]
        ),
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    [
                        # Encabezado mejorado
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=20, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("Consejos Personalizados de Bienestar", size=24, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text(
                                        "Encuentra ejercicios prácticos diseñados especialmente para tu estado emocional actual.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    ),
                                    ft.Divider(color=MoodDayTheme.TEXT_LIGHT_SECONDARY + "30", height=20),
                                    ft.Text(estado_resumen, size=16, weight="bold", color=MoodDayTheme.PRIMARY),
                                ],
                                spacing=12
                            )
                        ),

                        # Sección de Ayuda Rápida destacada
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.SECONDARY + "20",
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=15, color=MoodDayTheme.SECONDARY + "30"),
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text("🫁", size=40),
                                            ft.Column(
                                                [
                                                    ft.Text("Necesitas Ayuda Rápida?", size=16, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                                    ft.Text(
                                                        "Usa la técnica de respiración 4-7-8 con cronómetro visual para calmar la ansiedad.",
                                                        size=13,
                                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                                    ),
                                                ],
                                                expand=True,
                                                spacing=5
                                            )
                                        ],
                                        spacing=15,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.ElevatedButton(
                                        "Ir a Ayuda Rápida",
                                        on_click=lambda e: page.go("/ayuda-rapida"),
                                        bgcolor=MoodDayTheme.SECONDARY,
                                        color=MoodDayTheme.TEXT_LIGHT,
                                        height=45,
                                        expand=True,
                                        icon=ft.Icons.PLAY_ARROW
                                    )
                                ],
                                spacing=15
                            )
                        ),

                        # Título de recomendaciones
                        ft.Text(
                            "Ejercicios Recomendados",
                            size=18,
                            weight="bold",
                            color=MoodDayTheme.TEXT_LIGHT
                        ),

                        # Columna de tarjetas
                        ft.Column(cards, spacing=15),

                        # Contacto de emergencia mejorado
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.ERROR + "15",
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text("🆘", size=32),
                                            ft.Text("Contacto de Emergencia", size=16, weight="bold", color=MoodDayTheme.ERROR)
                                        ],
                                        spacing=12,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.Text(
                                        "Si necesitas ayuda inmediata, comunica a un familiar o amigo de confianza. "
                                        "Llama a emergencias (911) o a la línea de crisis de tu país. "
                                        "No estás solo y está bien pedir apoyo cuando lo necesitas.",
                                        size=13,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    )
                                ],
                                spacing=12
                            )
                        ),

                        # Botones de navegación
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Dormir Mejor 🌙",
                                    on_click=lambda e: page.go("/sueno"),
                                    bgcolor=MoodDayTheme.PRIMARY,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=45,
                                    expand=True,
                                    icon=ft.Icons.HOTEL
                                ),
                                ft.ElevatedButton(
                                    "Volver al Dashboard",
                                    on_click=lambda e: page.go("/dashboard"),
                                    bgcolor=MoodDayTheme.DARK_CARD,
                                    color=MoodDayTheme.PRIMARY,
                                    height=45,
                                    expand=True,
                                    icon=ft.Icons.HOME
                                )
                            ],
                            spacing=12
                        ),
                    ],
                    spacing=20
                )
            )
        ]
    )

    return view