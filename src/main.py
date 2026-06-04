import flet as ft
import os
import sys
from dotenv import load_dotenv 
from controllers.usercontroller import AuthController
from controllers.tareacontroller import TareaController
from views.loginView import LoginView
from views.dashboardView import RegisterView
from views.recoveryView import ForgotPasswordView, ResetPasswordView
from views.Tareaview import TareaView
from views.recommendationsView import RecommendationsView
from views.sleepView import SleepView
from views.quickHelpView import QuickHelpView

# Permite importar setup_database desde la raíz del proyecto cuando se ejecuta desde src
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from setup_database import create_database
from config.themes import MoodDayTheme

def start(page: ft.Page):
    # Configuración básica de la página
    page.title = "MoodDay - Diario Emocional"
    page.window_width = 500
    page.window_height = 750
    page.window_resizable = True
    page.window_min_width = 360
    page.theme_mode = ft.ThemeMode.LIGHT
    
    print("Iniciando aplicación MoodDay...")

    # Verificamos y creamos la base de datos si hace falta
    print("Verificando esquema de base de datos...")
    if not create_database():
        print("Error al inicializar la base de datos. Revisa .env y asegúrate de que MySQL está disponible.")
        return

    # Cargamos los controladores
    try:
        auth_ctrl = AuthController()
        task_ctrl = TareaController()
        print("Controladores cargados exitosamente.")
    except Exception as ex:
        print(f"Error al iniciar controladores: {ex}")
        return

    def route_change(e):
        print(f"Cambiando ruta a: {page.route}")
        page.views.clear()
        # Rutas de la app
        if page.route == "/" or page.route == "":
            print("Cargando LoginView...")
            page.views.append(LoginView(page, auth_ctrl))
            
        elif page.route == "/registro":
            print("Cargando RegisterView...")
            page.views.append(RegisterView(page, auth_ctrl))
            
        elif page.route == "/recuperar":
            print("Cargando ForgotPasswordView...")
            page.views.append(ForgotPasswordView(page, auth_ctrl))
            
        elif page.route == "/reset":
            print("Cargando ResetPasswordView...")
            page.views.append(ResetPasswordView(page, auth_ctrl))

        elif page.route == "/dashboard":
            print("Cargando TareaView (Dashboard)...")
            page.views.append(TareaView(page, task_ctrl))
        elif page.route == "/recomendaciones":
            print("Cargando RecommendationsView...")
            page.views.append(RecommendationsView(page, task_ctrl))
        elif page.route == "/sueno":
            print("Cargando SleepView...")
            page.views.append(SleepView(page, task_ctrl))
        elif page.route == "/ayuda-rapida":
            print("Cargando QuickHelpView...")
            page.views.append(QuickHelpView(page, task_ctrl))
        
        # Seguridad por si la ruta no existe
        if not page.views:
            page.views.append(
                ft.View("/", [ft.Text("Error 404: Ruta no encontrada")])
            )
        
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    # Configuramos los eventos de la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Cargar la primera vista
    route_change(None) 
    page.update()

def main():
    print("Arrancando Flet Engine...")
    ft.app(target=start)
    
if __name__ == "__main__":
    main()
