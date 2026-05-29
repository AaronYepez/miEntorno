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
    
    def guardar_nueva(self, id_usuario, titulo, desc, estado_animo, intensidad):
        if not titulo or not titulo.strip():
            return False, "El título es obligatorio."
        if not desc or not desc.strip():
            return False, "Describe cómo te sientes antes de guardar."
        if not estado_animo:
            return False, "Selecciona cómo te sientes."
        if intensidad is None or intensidad < 1 or intensidad > 10:
            return False, "Selecciona la intensidad de tu emoción entre 1 y 10."
        
        try:
            self.model.crear_tarea(id_usuario, titulo, desc, estado_animo, intensidad)
            return True, "Registro emocional guardado exitosamente."
        except Exception as e:
            print(f"Error al guardar tarea: {e}")
            return False, "Error al guardar la entrada. Intenta de nuevo."
