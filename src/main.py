import flet as ft 
from controllers.usercontroller import AuthController
from controllers.tareacontroller import TareaController
from views.loginView import LoginView
from views.dashboardView import RegisterView
from views.recoveryView import ForgotPasswordView, ResetPasswordView
from views.Tareaview import TareaView
from config.themes import MoodDayTheme

def start(page: ft.Page):
    # Configuración básica de la página
    page.title = "MoodDay - Diario Emocional"
    page.window_width = 500
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    
    print("Iniciando aplicación MoodDay...")

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