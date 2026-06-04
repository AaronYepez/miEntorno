from models.databaseModel import Database

class TareasModel:
    def __init__(self):
        self.db = Database()
        self._ensure_motivational_column()

    def _ensure_motivational_column(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM tareas LIKE %s", ("mensaje_motivador",))
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE tareas ADD COLUMN mensaje_motivador TEXT COLLATE utf8mb4_unicode_ci"
            )
            conn.commit()
        cursor.execute("SHOW COLUMNS FROM tareas LIKE %s", ("razon_emocion",))
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE tareas ADD COLUMN razon_emocion TEXT COLLATE utf8mb4_unicode_ci"
            )
            conn.commit()
        cursor.close()
        conn.close()

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

    def crear_tarea(self, id_usuario, titulo, descripcion, razon_emocion, estado_animo, intensidad, mensaje_motivador=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = (
            "INSERT INTO tareas (id_usuario, titulo, descripcion, razon_emocion, estado_animo, intensidad, mensaje_motivador) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (id_usuario, titulo, descripcion, razon_emocion, estado_animo, intensidad, mensaje_motivador))
        conn.commit()
        conn.close()
