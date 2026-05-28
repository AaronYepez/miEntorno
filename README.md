# 🚀 Nombre de tu Proyecto Genial

## 📝 Descripción del Proyecto

El proyecto MoodDay+ tiene como propósito desarrollar una aplicación digital orientada al bienestar emocional de las personas, permitiéndoles registrar, monitorear y comprender su estado de ánimo en la vida diaria. La aplicación busca fomentar el autoconocimiento emocional mediante el seguimiento de emociones, niveles de energía y estrés, así como ofrecer recomendaciones prácticas que ayuden a mejorar el bienestar personal. Además, el sistema pretende funcionar como una herramienta de apoyo preventivo, identificando patrones emocionales frecuentes y generando alertas cuando se detecten indicadores de estrés elevado, tristeza constante o baja energía.MoodDay+ no realizará diagnósticos médicos, sino que ofrecerá orientación y sugerencias para promover hábitos saludables y el cuidado emocional.

---

## Alcance del Proyecto

El alcance del sistema contempla el desarrollo de una aplicación capaz de:

- MoodDay+ no realizará diagnósticos Registrar usuarios y administrar sus datos básicos.
- Permitir el registro diario del estado emocional.
- Guardar información relacionada con:
- emoción predominante,
- nivel de energía,
- nivel de estrés,
- Comentarios o razones del estado emocional.
- Generar un historial emocional para identificar patrones y estadísticas.
- Mostrar recomendaciones personalizadas según la emoción registrada.
- Generar alertas preventivas cuando se detecten varios registros emocionales negativos consecutivos.
- Incluir un “Modo de ayuda rápida” con ejercicios de respiración y mensajes de calma.
- Mantener la integridad y seguridad de la información mediante una base de datos relacional normalizada.

---

## 👥 Integrantes del Equipo

### 👤 Mi Compita

- **NOMBRE: JOSE RAFAEL RUIZ HERNANDEZ**
- **EDAD: 18**
- **GRADO: 6**
- **GRUPO: D**
- **ESPECIALIDAD: Programacion**
- **NUMERO DE CONTROL: 23308060610676 **
- **CORREO: 23308060610676@cetis61.edu.mx**
- **NOMBRE DE ESCUELA: CETis #61**

### 👤 Mis Datos

- **NOMBRE: AARON YEPEZ MENDEZ**
- **EDAD: 18**
- **GRADO: 6**
- **GRUPO: D**
- **ESPECIALIDAD: Programacion**
- **NUMERO DE CONTROL: 23308060610451**
- **CORREO: 23308060610451@cetis61.edu.mx**
- **NOMBRE DE ESCUELA: CETis #61**

---

## 📸 Foto del Equipo

<img src="assests/aaroncito.jpeg" alt="Foto de Aarón" width="150" />

<img src="assests/Rafita.jpeg.jpeg" alt="Foto de Rafael" width="150" />

> # Primera Parte
>
> powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
> git config --global user.name "AaronYepez"
> git config --global user.email "23308060610451@cetis61.edu.mx"
> cat pyproject.toml
> uv add flet
> crear DATABASE.PY
> schemas.py
> 23308060610451@cetis61.edu.mx
> uv sync
> python setup_database.py
> uv run app
> .\.venv\Scripts\python.exe -m src.main
> Si aún quieres que funcione por email real, reemplaza en .env:

SMTP_USER
SMTP_PASSWORD
EMAIL_FROM

---

## 🚀 Cómo ejecutar el proyecto después de clonar

1. Clona el repositorio:
   ```powershell
   git clone <URL_DEL_REPOSITORIO>
   cd miEntorno
   ```
2. Crea y activa el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   Si `pip` no está disponible, ejecuta:
   ```powershell
   python -m ensurepip --upgrade
   ```
3. Actualiza pip e instala uv:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install uv
   uv sync
   ```
4. Copia el archivo de ejemplo de variables de entorno y configura tu base de datos y correo:
   ```powershell
   copy .env.example .env
   ```
5. Ajusta los valores en `.env`:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `DB_PORT`
   - `SMTP_HOST` (opcional)
   - `SMTP_PORT` (opcional)
   - `SMTP_USER` (opcional)
   - `SMTP_PASSWORD` (opcional)
   - `EMAIL_FROM` (opcional)

   > Si no completas la configuración SMTP o usas valores de ejemplo, la app seguirá funcionando y mostrará el código de recuperación en la pantalla para testing.

   Para enviar el código real por correo con Gmail:
   - `SMTP_HOST=smtp.gmail.com`
   - `SMTP_PORT=587`
   - `SMTP_USER=tu_email@gmail.com`
   - `EMAIL_FROM=tu_email@gmail.com`
   - `SMTP_PASSWORD` debe ser una contraseña de aplicación de Gmail, no tu contraseña normal.

   Pasos para crear la contraseña de aplicación en Gmail:
   1. Activa la verificación en dos pasos en tu cuenta de Google.
   2. Ve a "Seguridad" y luego a "Contraseñas de aplicación".
   3. Crea una contraseña para "Correo" o "Otro".
   4. Copia esa contraseña y pégala en `SMTP_PASSWORD`.
   5. Guarda el archivo `.env` y reinicia la app con `uv run app`.

6. Inicializa la base de datos si aún no existe:
   - Ejecuta `python setup_database.py`
   - Esto crea o actualiza las tablas `usuario` y `tareas` con los campos necesarios para MoodDay.
7. Ejecuta la aplicación con uv:
   ```powershell
   uv run app
   ```

> Si `uv run app` no funciona, también puedes ejecutar directamente:
>
> ```powershell
> .\.venv\Scripts\python.exe -m src.main
> ```

## 🌟 Nuevas funciones de MoodDay

- El registro ahora pide número de control, grado, grupo, edad y sexo para personalizar mejor la experiencia.
- El dashboard es un diario emocional: puedes ingresar cómo te sientes, seleccionar tu estado y añadir la intensidad de la emoción.
- Todos los campos principales tienen validaciones en la interfaz para evitar datos incompletos o inválidos.

## 🔐 Recuperación de contraseña

- Las contraseñas se guardan en la base de datos con cifrado `bcrypt`.
- Si el usuario olvida su contraseña, el sistema genera un token seguro y envía un correo de recuperación.
- En la pantalla de login, hay un botón `¿Olvidaste tu contraseña?` para iniciar el proceso.

## 🎨 Diseño MoodDay

- El proyecto ahora tiene una apariencia más suave y amigable, con colores pastel y mensajes de diario emocional.
- La pantalla principal se enfoca en el registro de estados de ánimo como un diario personal.
- El flujo de registro, inicio y recuperación está diseñado para una experiencia clara y segura.

## 📚 Documentación compacta incluida

Este README ahora contiene un resumen de toda la documentación extra del proyecto. Los archivos adicionales fueron consolidados para reducir el número de archivos y mantener toda la información importante en un solo lugar.

### Contenido resumido

- ✅ **Objetivo del proyecto:** MoodDay es un diario emocional para registrar y monitorear el estado de ánimo.
- ✅ **Alcance:** autenticación segura, registros emocionales, recuperación de contraseña, historial, validaciones y una interfaz calmante.
- ✅ **Equipo:** información de los integrantes y datos de contacto.
- ✅ **Instalación:** pasos rápidos para clonar, crear el entorno, instalar dependencias, configurar `.env`, inicializar la base de datos y ejecutar con `uv run .`.
- ✅ **Guía rápida:** creación de cuenta, inicio de sesión, registro de emociones, cierre de sesión y recuperación de contraseña.
- ✅ **Implementación:** lista de vistas, modelos, controladores y mejoras aplicadas al proyecto.
- ✅ **Seguridad:** bcrypt para contraseñas, validación de emails únicos, códigos de recuperación de 6 dígitos y sesiones seguras.
- ✅ **Base de datos:** tablas `usuario` y `tareas`, con campos ampliados para número de control, grado, grupo, edad, sexo, estado emocional e intensidad.
- ✅ **Mejoras UX:** colores calmantes, estilo consistente, mensajes claros y validaciones de formulario.
- ✅ **Notas de mantenimiento:** si el proyecto ya no necesita los archivos Markdown adicionales, puedes confiar en esta documentación consolidada.

---

Cómo configurar .env para enviar el código por email real
Abre el archivo .env en .env y reemplaza las líneas de SMTP así:

Si usas Gmail
Entra a tu cuenta de Google.
Activa la verificación en dos pasos.
Crea una contraseña de aplicación.
Usa esa contraseña en SMTP_PASSWORD.
Ejemplo real correcto
Si usas otro proveedor
Cambia SMTP_HOST y SMTP_PORT por los valores de tu proveedor:

Outlook/Office 365: smtp.office365.com, puerto 587
Yahoo: smtp.mail.yahoo.com, puerto 587
Host local o SMTP propio: el host y puerto que te haya dado tu servicio
Importante
SMTP_USER debe ser tu cuenta de email real.
SMTP_PASSWORD debe ser la contraseña o la contraseña de aplicación, no el texto tu_contraseña_aplicacion.
EMAIL_FROM debe ser el mismo correo que envía el mensaje.
Después de guardar el .env, reinicia la app con:
