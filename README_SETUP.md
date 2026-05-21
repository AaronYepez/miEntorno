# MoodDay - Diario Emocional

MoodDay es una aplicación de escritorio construida con Flet que permite a los usuarios registrar y seguir sus emociones diarias, gestionar su bienestar emocional y crear hábitos saludables.

## Características

- ✅ **Registro seguro de usuarios** con encriptación de contraseñas
- ✅ **Sistema de recuperación de contraseña** con códigos de 6 dígitos válidos por 15 minutos
- ✅ **Diario emocional** para registrar tus sentimientos y emociones
- ✅ **Interfaz intuitiva** con paleta de colores calmantes
- ✅ **Autenticación segura** con sesiones de usuario
- ✅ **Gestión de emociones** con categorización y prioridades

## Requisitos

- Python 3.13 o superior
- MySQL/MariaDB configurado y en ejecución
- pip para instalar dependencias

## Instalación

1. **Clonar el repositorio**
```bash
git clone <url-repo>
cd miEntorno
```

2. **Crear y activar entorno virtual** (opcional pero recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -e .
```

4. **Configurar la base de datos**

- Crea una base de datos MySQL llamada `tareas`
- Importa el esquema SQL:
```bash
mysql -u root -p tareas < src/database/tareas.sql
```

5. **Configurar variables de entorno**

- Copia el archivo `.env.example` a `.env`
```bash
cp .env.example .env
```

- Edita `.env` con tus credenciales:
```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=tareas
DB_PORT=3306

# Opcional: Configurar SMTP para envío de correos
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_app
EMAIL_FROM=tu_email@gmail.com
```

## Uso

Para ejecutar la aplicación:

```bash
python -m flet src.main
```

O si tienes pip instalado:

```bash
python src/main.py
```

## Flujo de la aplicación

1. **Inicio de sesión**: Ingresa tu email y contraseña
2. **Registro**: Si no tienes cuenta, crea una nueva
3. **Recuperación de contraseña**: Si olvidas tu contraseña, recibe un código por correo
4. **Dashboard**: Una vez autenticado, accede a tu diario emocional
5. **Registrar emociones**: Crea nuevos registros de tus sentimientos
6. **Cerrar sesión**: Usa el botón de salida en la esquina superior derecha

## Estructura del proyecto

```
src/
├── main.py                 # Punto de entrada de la aplicación
├── config/
│   ├── __init__.py
│   └── themes.py          # Configuración de colores y temas
├── controllers/
│   ├── usercontroller.py  # Lógica de autenticación
│   └── tareacontroller.py # Lógica de tareas/emociones
├── models/
│   ├── databaseModel.py   # Conexión a BD
│   ├── userModel.py       # Modelo de usuario
│   ├── tareasModel.py     # Modelo de tareas
│   └── schemasModely.py   # Esquemas de validación
├── views/
│   ├── loginView.py       # Vista de inicio de sesión
│   ├── dashboardView.py   # Vista de registro y dashboard
│   ├── recoveryView.py    # Vista de recuperación de contraseña
│   └── Tareaview.py       # Vista principal del diario
└── database/
    └── tareas.sql         # Esquema de la base de datos
```

## Paleta de colores

La aplicación utiliza una paleta de colores diseñada para calmar y transmitir paz:

- **Azul suave (#5B9FBF)**: Color primario - calma
- **Verde azulado (#6DB5A9)**: Color secundario - serenidad
- **Verde menta (#A8D5BA)**: Acentos - paz
- **Emociones**: Colores específicos para alegría, tristeza, enojo, ansiedad, calma

## Características de seguridad

- ✅ Contraseñas encriptadas con bcrypt
- ✅ Validación de email único
- ✅ Códigos de recuperación temporales (15 minutos)
- ✅ Sesiones de usuario seguras
- ✅ Manejo de errores robusto

## Solución de problemas

### "Error de conexión a la base de datos"
- Verifica que MySQL esté ejecutándose
- Comprueba que los credenciales en `.env` sean correctos
- Asegúrate de que la base de datos `tareas` existe

### "No se envían correos de recuperación"
- SMTP no está configurado (esperado para testing - el código aparecerá en consola)
- Verifica que las variables SMTP en `.env` sean correctas
- Para Gmail, usa una "contraseña de aplicación" en lugar de tu contraseña normal

### "Error de validación de email"
- Asegúrate de ingresar un email válido
- Algunos emails especiales pueden no pasar validación

## Contribuir

Para contribuir al proyecto, por favor crea un pull request con tus cambios.

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.
