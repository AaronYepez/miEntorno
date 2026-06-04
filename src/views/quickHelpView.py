import flet as ft
import asyncio
from config.themes import MoodDayTheme


def QuickHelpView(page, tarea_controller):
    user = page.session.store.get("user")
    if not user:
        page.go("/")
        return ft.View("/ayuda-rapida", [ft.Text("Redireccionando al login...")])

    # Estados del cronómetro
    breathing_state = {
        "phase": "inhale", 
        "seconds": 0, 
        "total_cycles": 0, 
        "active": False, 
        "paused": False,
        "task": None
    }
    timer_display = ft.Text("0", size=80, weight="bold", color=MoodDayTheme.PRIMARY)
    phase_text = ft.Text("Presiona iniciar para comenzar", size=18, color=MoodDayTheme.TEXT_LIGHT_SECONDARY)
    cycle_counter = ft.Text("Ciclo 0 de 5", size=14, color=MoodDayTheme.TEXT_LIGHT_SECONDARY)
    
    # Animación de círculo respiratorio
    circle_indicator = ft.Container(
        width=200,
        height=200,
        bgcolor=MoodDayTheme.PRIMARY,
        border_radius=200,
        shadow=ft.BoxShadow(blur_radius=30, color=MoodDayTheme.PRIMARY + "40"),
        opacity=0.3,
        scale=1.0,
        animate_scale=ft.Animation(500, "easeInOut")
    )
    
    def update_display():
        """Actualiza la pantalla con los valores actuales"""
        seconds = breathing_state["seconds"]
        phase = breathing_state["phase"]
        
        timer_display.value = str(seconds)
        
        if phase == "inhale":
            phase_text.value = "🫁 Inhala lentamente"
            phase_text.color = MoodDayTheme.PRIMARY
            timer_display.color = MoodDayTheme.PRIMARY
            circle_indicator.bgcolor = MoodDayTheme.PRIMARY
            circle_indicator.shadow = ft.BoxShadow(blur_radius=40, color=MoodDayTheme.PRIMARY + "60", spread_radius=2)
            circle_indicator.opacity = 0.6
            circle_indicator.scale = 1.2  # Expande al inhalar
        elif phase == "hold":
            phase_text.value = "⏸️ Mantén la respiración"
            phase_text.color = MoodDayTheme.SECONDARY
            timer_display.color = MoodDayTheme.SECONDARY
            circle_indicator.bgcolor = MoodDayTheme.SECONDARY
            circle_indicator.shadow = ft.BoxShadow(blur_radius=35, color=MoodDayTheme.SECONDARY + "50", spread_radius=1)
            circle_indicator.opacity = 0.75
            circle_indicator.scale = 1.15  # Ligeramente más pequeño que inhalar
        elif phase == "exhale":
            phase_text.value = "💨 Exhala lentamente"
            phase_text.color = MoodDayTheme.ERROR
            timer_display.color = MoodDayTheme.ERROR
            circle_indicator.bgcolor = MoodDayTheme.ERROR
            circle_indicator.shadow = ft.BoxShadow(blur_radius=25, color=MoodDayTheme.ERROR + "40", spread_radius=0)
            circle_indicator.opacity = 0.4
            circle_indicator.scale = 0.9  # Contrae al exhalar
        
        try:
            page.update()
        except Exception as e:
            print(f"Error actualizando pantalla: {e}")
    
    async def breathing_timer():
        """Ejecuta los ciclos de respiración 4-7-8"""
        phases = [
            ("inhale", 4),   # Inhala 4 segundos
            ("hold", 7),     # Mantén 7 segundos
            ("exhale", 8)    # Exhala 8 segundos
        ]
        
        try:
            for cycle in range(5):  # 5 ciclos completos
                if not breathing_state["active"]:
                    break
                    
                breathing_state["total_cycles"] = cycle + 1
                cycle_counter.value = f"Ciclo {cycle + 1} de 5"
                try:
                    page.update()
                except Exception:
                    pass
                
                for phase, duration in phases:
                    if not breathing_state["active"]:
                        break
                        
                    breathing_state["phase"] = phase
                    
                    # Cuenta hacia atrás desde duration hasta 1
                    for second in range(duration, 0, -1):
                        # Esperar mientras esté pausado
                        while breathing_state["paused"] and breathing_state["active"]:
                            await asyncio.sleep(0.1)
                        
                        if not breathing_state["active"]:
                            break
                        
                        breathing_state["seconds"] = second
                        update_display()
                        await asyncio.sleep(1)  # Espera 1 segundo
            
            # Ejercicio completado
            if breathing_state["active"]:
                breathing_state["active"] = False
                timer_display.value = "✓"
                phase_text.value = "¡Excelente! Respira naturalmente ahora"
                cycle_counter.value = "Ejercicio completado"
                try:
                    page.update()
                except Exception:
                    pass
                
        except Exception as e:
            print(f"Error en breathing_timer: {e}")
            breathing_state["active"] = False

    def start_breathing(e):
        """Inicia o reanuda el cronómetro de respiración"""
        if not breathing_state["active"]:
            breathing_state["active"] = True
            breathing_state["paused"] = False
            breathing_state["seconds"] = 0
            update_display()
            
            # Crear y ejecutar la tarea asincrónica
            breathing_state["task"] = asyncio.create_task(breathing_timer())
        else:
            # Si está pausado, reanuda
            breathing_state["paused"] = False
            update_display()

    def stop_breathing(e):
        """Pausa el cronómetro"""
        breathing_state["paused"] = True

    view = ft.View(
        route="/ayuda-rapida",
        bgcolor=MoodDayTheme.DARK_BACKGROUND,
        appbar=ft.AppBar(
            title=ft.Text("Ayuda Rápida - Respiración 4-7-8", color=MoodDayTheme.TEXT_LIGHT),
            bgcolor=MoodDayTheme.DARK_SURFACE,
            color=MoodDayTheme.TEXT_LIGHT,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="Volver",
                icon_color=MoodDayTheme.TEXT_LIGHT,
                on_click=lambda e: page.go("/dashboard")
            ),
        ),
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    [
                        # Sección intro
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=20, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("¿Te sientes ansioso?", size=24, weight="bold", color=MoodDayTheme.PRIMARY),
                                    ft.Text(
                                        "Esta técnica de respiración 4-7-8 es perfecta para calmar la ansiedad en momentos de crisis. Te guiaremos paso a paso.",
                                        size=14,
                                        color=MoodDayTheme.TEXT_LIGHT_SECONDARY
                                    )
                                ],
                                spacing=12
                            )
                        ),

                        # Cronómetro visual
                        ft.Container(
                            padding=ft.Padding(30, 30, 30, 30),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=20, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Column(
                                        [
                                            ft.Container(
                                                content=circle_indicator,
                                                alignment=ft.Alignment.CENTER,
                                            ),
                                            ft.Container(
                                                content=timer_display,
                                                alignment=ft.Alignment.CENTER,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=0
                                    ),
                                    phase_text,
                                    cycle_counter,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20
                            )
                        ),

                        # Instrucciones
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("¿Cómo funciona?", size=16, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Row(
                                        [
                                            ft.Text("1️⃣", size=20),
                                            ft.Column(
                                                [
                                                    ft.Text("Inhala", weight="bold", color=MoodDayTheme.PRIMARY),
                                                    ft.Text("4 segundos lentamente", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY)
                                                ]
                                            )
                                        ],
                                        spacing=10
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("2️⃣", size=20),
                                            ft.Column(
                                                [
                                                    ft.Text("Mantén", weight="bold", color=MoodDayTheme.SECONDARY),
                                                    ft.Text("7 segundos sin movimiento", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY)
                                                ]
                                            )
                                        ],
                                        spacing=10
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("3️⃣", size=20),
                                            ft.Column(
                                                [
                                                    ft.Text("Exhala", weight="bold", color=MoodDayTheme.ERROR),
                                                    ft.Text("8 segundos completamente", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY)
                                                ]
                                            )
                                        ],
                                        spacing=10
                                    ),
                                ],
                                spacing=15
                            )
                        ),

                        # Botones de control
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Iniciar",
                                    on_click=start_breathing,
                                    bgcolor=MoodDayTheme.PRIMARY,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=50,
                                    expand=True,
                                    icon=ft.Icons.PLAY_ARROW,
                                ),
                                ft.ElevatedButton(
                                    "Pausa",
                                    on_click=stop_breathing,
                                    bgcolor=MoodDayTheme.ERROR,
                                    color=MoodDayTheme.TEXT_LIGHT,
                                    height=50,
                                    expand=True,
                                    icon=ft.Icons.PAUSE,
                                )
                            ],
                            spacing=12
                        ),

                        # Consejos adicionales
                        ft.Container(
                            padding=ft.Padding(20, 20, 20, 20),
                            bgcolor=MoodDayTheme.DARK_CARD,
                            border_radius=MoodDayTheme.BORDER_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
                            content=ft.Column(
                                [
                                    ft.Text("💡 Consejos para mejores resultados", size=14, weight="bold", color=MoodDayTheme.TEXT_LIGHT),
                                    ft.Text("✓ Busca un lugar tranquilo", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("✓ Mantén una postura cómoda", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("✓ Relaja los hombros", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("✓ Repite 5 ciclos completos", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                    ft.Text("✓ Repite cuando lo necesites", size=12, color=MoodDayTheme.TEXT_LIGHT_SECONDARY),
                                ],
                                spacing=8
                            )
                        ),

                        # Botón volver mejorado
                        ft.Container(
                            expand=False,
                            alignment=ft.Alignment.CENTER,
                            padding=ft.Padding(0, 20, 0, 0),
                            content=ft.ElevatedButton(
                                "Ir a la Página Principal",
                                on_click=lambda e: page.go("/dashboard"),
                                bgcolor=MoodDayTheme.SECONDARY,
                                color=MoodDayTheme.TEXT_LIGHT,
                                height=60,
                                width=300,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    text_style=ft.TextStyle(size=16, weight="bold")
                                )
                            )
                        ),
                    ],
                    spacing=20
                )
            )
        ]
    )

    return view
