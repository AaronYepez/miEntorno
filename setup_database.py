"""
Script para inicializar la base de datos de MoodDay
Ejecutar: python setup_database.py
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def ensure_column(cursor, table, column, column_def):
    cursor.execute("SHOW COLUMNS FROM {table} LIKE %s".format(table=table), (column,))
    if cursor.fetchone() is None:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_def}")


def create_database():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD") or "",
            port=os.getenv("DB_PORT", "3306")
        )
        cursor = conn.cursor()
        db_name = os.getenv("DB_NAME", "tareas")

        print(f"Creando base de datos '{db_name}' si no existe...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {db_name}")

        print("Creando tabla 'usuario'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(100) COLLATE utf8mb4_unicode_ci NOT NULL,
            email VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
            password VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
            telefono VARCHAR(20) COLLATE utf8mb4_unicode_ci,
            numero_control VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL,
            grado VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL,
            grupo VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,
            edad INT,
            sexo VARCHAR(30) COLLATE utf8mb4_unicode_ci NOT NULL,
            reset_token VARCHAR(255) COLLATE utf8mb4_unicode_ci,
            reset_token_expires DATETIME,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso DATETIME,
            activo TINYINT(1) DEFAULT 1,
            PRIMARY KEY (id_usuario),
            UNIQUE KEY uk_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)

        print("Creando tabla 'tareas'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id_tarea INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            titulo VARCHAR(200) COLLATE utf8mb4_unicode_ci NOT NULL,
            descripcion TEXT COLLATE utf8mb4_unicode_ci,
            estado_animo VARCHAR(30) COLLATE utf8mb4_unicode_ci DEFAULT 'Neutral',
            intensidad TINYINT DEFAULT 5,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id_tarea),
            KEY idx_usuario (id_usuario)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)

        ensure_column(cursor, "usuario", "numero_control", "VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL")
        ensure_column(cursor, "usuario", "grado", "VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL")
        ensure_column(cursor, "usuario", "grupo", "VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL")
        ensure_column(cursor, "usuario", "edad", "INT")
        ensure_column(cursor, "usuario", "sexo", "VARCHAR(30) COLLATE utf8mb4_unicode_ci NOT NULL")
        ensure_column(cursor, "tareas", "estado_animo", "VARCHAR(30) COLLATE utf8mb4_unicode_ci DEFAULT 'Neutral'")
        ensure_column(cursor, "tareas", "intensidad", "TINYINT DEFAULT 5")

        conn.commit()
        print("\n✅ Base de datos inicializada exitosamente!")
        print(f"Base de datos: {db_name}")
        print("Tablas creadas o actualizadas: usuario, tareas")

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        if err.errno == 2003:
            print(f"❌ Error: No se puede conectar a MySQL en {os.getenv('DB_HOST')}")
            print("   Asegúrate de que MySQL esté ejecutándose")
        elif err.errno == 1045:
            print(f"❌ Error: Credenciales de MySQL incorrectas")
            print("   Verifica tu usuario y contraseña en .env")
        else:
            print(f"❌ Error en MySQL: {err}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("MoodDay - Inicialización de Base de Datos")
    print("=" * 50)

    if create_database():
        print("\n✨ ¡Listo! Ahora puedes ejecutar la aplicación:")
        print("   uv run .")
    else:
        print("\n⚠️  Por favor revisa los errores anteriores")
