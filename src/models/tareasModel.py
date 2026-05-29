from models.databaseModel import Database

class TareasModel:
    def __init__(self):
        self.db = Database()

    def listar_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM tareas WHERE id_usuario = %s ORDER BY fecha_creacion DESC",
            (id_usuario,)
        )
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    def crear_tarea(self, id_usuario, titulo, descripcion, estado_animo, intensidad):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = (
            "INSERT INTO tareas (id_usuario, titulo, descripcion, estado_animo, intensidad) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (id_usuario, titulo, descripcion, estado_animo, intensidad))
        conn.commit()
        conn.close()
