import bcrypt
import secrets
from datetime import datetime, timedelta
from models.databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def registrar(self, data):
        hashed = self._hash_password(data.password)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuario (nombre, apellido, email, password, telefono) VALUES (%s, %s, %s, %s, %s)",
                (data.nombre, "", data.email, hashed.decode('utf-8'), data.telefono)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            user.pop('password', None)
            return user
        return None

    def crear_token_recuperacion(self, email):
        token = secrets.token_urlsafe(32)
        expires = datetime.utcnow() + timedelta(hours=1)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET reset_token = %s, reset_token_expires = %s WHERE email = %s",
            (token, expires.strftime('%Y-%m-%d %H:%M:%S'), email)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return token if success else None

    def obtener_usuario_por_token(self, token):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuario WHERE reset_token = %s AND reset_token_expires >= %s",
            (token, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        )
        user = cursor.fetchone()
        conn.close()
        return user

    def actualizar_password_por_token(self, token, new_password):
        user = self.obtener_usuario_por_token(token)
        if not user:
            return False
        hashed = self._hash_password(new_password)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET password = %s, reset_token = NULL, reset_token_expires = NULL WHERE id_usuario = %s",
            (hashed.decode('utf-8'), user['id_usuario'])
        )
        conn.commit()
        rows = cursor.rowcount
        conn.close()
        return rows > 0

class TareasModel:
    def __init__(self):
        self.db = Database()

    def crear_tarea(self, data, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tareas (titulo, descripcion, prioridad, clasificacion, usuario_id) VALUES (%s, %s, %s, %s, %s)",
                (data.titulo, data.descripcion, data.prioridad, data.clasificacion, usuario_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_tareas(self, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tareas WHERE usuario_id = %s", (usuario_id,))
        tareas = cursor.fetchall()
        conn.close()
        return tareas