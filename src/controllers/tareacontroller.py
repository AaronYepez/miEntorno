from models.tareasModel import TareasModel

class TareaController:
    def __init__(self):
        self.model = TareasModel()
    
    def obtener_lista(self, id_usuario):
        try:
            return self.model.listar_por_usuario(id_usuario)
        except Exception as e:
            print(f"Error al obtener tareas: {e}")
            return []
    
    def guardar_nueva(self, id_usuario, titulo, desc):
        if not titulo or not titulo.strip():
            return False, "El título es obligatorio."
        
        try:
            self.model.crear_tarea(id_usuario, titulo, desc or "")
            return True, "Entrada emocional guardada exitosamente."
        except Exception as e:
            print(f"Error al guardar tarea: {e}")
            return False, "Error al guardar la entrada. Intenta de nuevo."