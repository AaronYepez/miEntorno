"""
Script para inicializar la base de datos de MoodDay
Ejecutar: python setup_database.py
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Crea la base de datos y tablas si no existen"""
    
    try:
        # Conectarse sin especificar base de datos
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD") or "",
            port=os.getenv("DB_PORT", "3306")
        )
        
        cursor = conn.cursor()
        db_name = os.getenv("DB_NAME", "tareas")
        
        # Crear base de datos si no existe
        print(f"Creando base de datos '{db_name}' si no existe...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Seleccionar la base de datos
        cursor.execute(f"USE {db_name}")
        
        # Crear tabla de usuarios
        print("Creando tabla 'usuario'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(100) COLLATE utf8mb4_unicode_ci NOT NULL,
            apellido VARCHAR(100) COLLATE utf8mb4_unicode_ci,
            email VARCHAR(150) COLLATE utf8mb4_unicode_ci NOT NULL,
            password VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
            telefono VARCHAR(20) COLLATE utf8mb4_unicode_ci,
            reset_token VARCHAR(255) COLLATE utf8mb4_unicode_ci,
            reset_token_expires DATETIME,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso DATETIME,
            activo TINYINT(1) DEFAULT 1,
            foto_perfil VARCHAR(255) COLLATE utf8mb4_unicode_ci,
            PRIMARY KEY (id_usuario),
            UNIQUE KEY uk_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Crear tabla de tareas/emociones
        print("Creando tabla 'tareas'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id_tarea INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            titulo VARCHAR(200) COLLATE utf8mb4_unicode_ci NOT NULL,
            descripcion TEXT COLLATE utf8mb4_unicode_ci,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_limite DATE,
            hora_limite TIME,
            estado ENUM('pendiente','en_progreso','completada','cancelada') DEFAULT 'pendiente',
            clasificacion ENUM('personal','trabajo','estudio','hogar','salud','otro') DEFAULT 'personal',
            prioridad ENUM('baja','media','alta') DEFAULT 'media',
            completada TINYINT DEFAULT 0,
            fecha_completada DATETIME,
            PRIMARY KEY (id_tarea),
            KEY idx_usuario (id_usuario),
            KEY idx_estado (estado),
            KEY idx_clasificacion (clasificacion)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
        print("\n✅ Base de datos inicializada exitosamente!")
        print(f"Base de datos: {db_name}")
        print("Tablas creadas: usuario, tareas")
        
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
        print("   python src/main.py")
    else:
        print("\n⚠️  Por favor revisa los errores anteriores")
