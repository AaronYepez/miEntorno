import bcrypt
import random
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
                "INSERT INTO usuario (nombre, email, password, telefono, numero_control, grado, grupo, edad, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.nombre,
                    data.email,
                    hashed.decode('utf-8'),
                    data.telefono,
                    data.numero_control,
                    data.grado,
                    data.grupo,
                    data.edad,
                    data.sexo
                )
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

    def existe_email(self, email):
        """Verifica si un email ya está registrado"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def crear_token_recuperacion(self, email):
        # Generar código de 6 dígitos
        code = f"{random.randint(0, 999999):06d}"
        expires = datetime.utcnow() + timedelta(minutes=15)  # Válido por 15 minutos
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuario SET reset_token = %s, reset_token_expires = %s WHERE email = %s",
                (code, expires.strftime('%Y-%m-%d %H:%M:%S'), email)
            )
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                return code
            return None
        except Exception as e:
            print(f"Error al crear token: {e}")
            return None
        finally:
            conn.close()

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