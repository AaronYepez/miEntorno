import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
from models.userModel import UsuarioModel
from models.schemasModely import UsuarioSchema
from pydantic import ValidationError

load_dotenv()

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        
    def login(self, email, password):
        user = self.model.validar_login(email, password)
        if user:
            return user, "Login exitoso"
        return None, "Email o contraseña incorrectos"
        
    def registrar_usuario(self, nombre, email, password, telefono=None, numero_control=None, grado=None, grupo=None, edad=None, sexo=None):
        if self.model.existe_email(email):
            return False, "Este correo electrónico ya está registrado."
        
        try:
            nuevo_usuario = UsuarioSchema(
                nombre=nombre,
                email=email,
                password=password,
                telefono=telefono,
                numero_control=numero_control,
                grado=grado,
                grupo=grupo,
                edad=edad,
                sexo=sexo
            )
            success = self.model.registrar(nuevo_usuario)
            if success:
                return success, "Usuario registrado exitosamente. Inicia sesión ahora."
            return False, "Error al registrar el usuario."
        except ValidationError as e:
            return False, e.errors()[0]['msg']

    def enviar_email_recuperacion(self, email):
        if not self.model.existe_email(email):
            return False, "No existe ningún usuario registrado con ese correo."

        code = self.model.crear_token_recuperacion(email)
        if not code:
            return False, "No se pudo generar el código de recuperación. Inténtalo de nuevo."

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        email_from = os.getenv("EMAIL_FROM")

        smtp_incompleto = (
            not smtp_host or
            not smtp_user or
            not smtp_password or
            not email_from or
            smtp_user.startswith("tu_") or
            smtp_password.startswith("tu_") or
            email_from.startswith("tu_")
        )

        if smtp_incompleto:
            # Si SMTP no está listo, devolver el código directamente para pruebas
            return True, (
                f"Código de recuperación: {code} (válido por 15 minutos). "
                "SMTP no configurado correctamente, usa este código para continuar."
            )

        mensaje = EmailMessage()
        mensaje["Subject"] = "MoodDay - Código de recuperación de contraseña"
        mensaje["From"] = email_from
        mensaje["To"] = email
        mensaje.set_content(
            f"Hola,\n\n"
            f"Se ha solicitado restablecer tu contraseña de MoodDay.\n\n"
            f"Usa este código para recuperar tu cuenta:\n\n"
            f"    {code}\n\n"
            f"Este código es válido por 15 minutos.\n"
            f"Si no solicitaste este cambio, ignora este mensaje.\n\n"
            f"Saludos,\nMoodDay"
        )

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                if smtp_port == 587:
                    server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(mensaje)
            return True, "Se envió un correo con el código de recuperación."
        except Exception as ex:
            print(f"Error SMTP: {ex}")
            return True, (
                f"No se pudo enviar el correo. Usa este código de recuperación: {code} "
                "(válido por 15 minutos)."
            )

    def restablecer_contrasena(self, token, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."

        success = self.model.actualizar_password_por_token(token, password)
        if success:
            return True, "Contraseña restablecida con éxito. Inicia sesión con tu nueva contraseña."
        return False, "El código es inválido o ha expirado. Solicita uno nuevo."
