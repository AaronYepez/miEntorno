# 🚀 Guía Rápida - MoodDay

## Iniciar la Aplicación

```bash
cd c:\Users\SALA2-PC2\Desktop\miEntorno
python src/main.py
```

## Primeros Pasos

### 1️⃣ **Crear Cuenta**
- Click en "Crear una cuenta nueva"
- Llena todos los campos
- La contraseña debe tener mínimo 8 caracteres
- Confirma la contraseña
- Click "Registrar cuenta"
- Serás redirigido al login

### 2️⃣ **Iniciar Sesión**
- Ingresa tu email y contraseña
- Click "Entrar"
- ¡Bienvenido al dashboard!

### 3️⃣ **Registrar una Emoción**
- En el dashboard, ingresa un título
- Describe cómo te sientes
- Click "Guardar registro"
- Tu emoción se guardará automáticamente

### 4️⃣ **Cerrar Sesión**
- Click en el ícono de salida (⬜ arriba a la derecha)
- Volverás a la pantalla de login

### 5️⃣ **¿Olvidaste tu Contraseña?**
- En el login, click "¿Olvidaste tu contraseña?"
- Ingresa tu correo
- Recibirás un código de 6 dígitos (o en consola si SMTP no está configurado)
- Ingresa el código
- Crea tu nueva contraseña
- Click "Restablecer contraseña"

## 🎨 Colores de la Aplicación

- 🔵 **Azul suave** - Tranquilidad y confianza
- 🟢 **Verde azulado** - Serenidad y balance
- 🟢 **Verde menta** - Paz y calma
- 💡 **Interfaz clara** - Fácil de usar

## ⚙️ Configuración

### Variables de Entorno (.env)

```ini
# Base de Datos (ya configurado)
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=tareas
DB_PORT=3306

# SMTP (Opcional - para enviar correos reales)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tune@gmail.com
SMTP_PASSWORD=contraseña_app
EMAIL_FROM=tumail@gmail.com
```

## 📊 Base de Datos

- **Ubicación:** MySQL en 127.0.0.1
- **Base de datos:** tareas
- **Tablas:** usuario, tareas

## 🔐 Seguridad

✅ **Contraseñas encriptadas** con bcrypt  
✅ **Emails únicos** - No se permiten duplicados  
✅ **Códigos temporales** - Válidos solo 15 minutos  
✅ **Sesiones seguras** - Se limpian al cerrar sesión

## 🐛 Solución de Problemas

**"Error de conexión a la BD"**
```bash
# Reinicia MySQL
# Verifica .env sea correcto
python setup_database.py
```

**"Email ya registrado"**
- El email que intentas usar ya existe
- Usa otro email o recupera tu contraseña

**"Código expirado"**
- Los códigos solo duran 15 minutos
- Solicita un código nuevo

## 📝 Notas Importantes

- La aplicación se ejecuta localmente
- Necesitas MySQL corriendo en tu PC
- Los datos se guardan en BD MySQL
- La contraseña debe tener mínimo 8 caracteres
- Los códigos de recuperación son solo números

## 🆘 Ayuda Rápida

| Problema | Solución |
|----------|----------|
| No se abre la app | Revisa que Python y MySQL estén instalados |
| BD no existe | Ejecuta: `python setup_database.py` |
| Contraseña olvidada | Click "¿Olvidaste tu contraseña?" en login |
| Email duplicado | Usa otro email o recupera tu cuenta |
| Código no llega | Revisa la consola (si SMTP no está configurado) |

## 📞 Contacto

Para errores o sugerencias, revisa los logs de consola.

---

**¡Disfruta usando MoodDay! 🌟**
