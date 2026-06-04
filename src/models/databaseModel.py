import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    @staticmethod
    def get_connection():
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT", "3306")

        if not host or not user or not database:
            raise RuntimeError(
                "Faltan variables de entorno de la base de datos. "
                "Revisa .env y asegúrate de definir DB_HOST, DB_USER y DB_NAME."
            )

        try:
            return mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=int(port),
                use_pure=True
            )
        except mysql.connector.Error as e:
            raise RuntimeError(
                f"Error al conectar con la base de datos: {e}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Error inesperado al conectar con la base de datos: {e}"
            ) from e