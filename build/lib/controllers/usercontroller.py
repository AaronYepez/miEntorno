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
        
    def registrar_usuario(self, nombre, email, password, telefono=None):
        try:
            nuevo_usuario = UsuarioSchema(nombre=nombre, email=email, password=password, telefono=telefono)
            success = self.model.registrar(nuevo_usuario)
            return success, "Usuario registrado exitosamente."
        except ValidationError as e:
            return False, e.errors()[0]['msg']

    def enviar_email_recuperacion(self, email):
        token = self.model.crear_token_recuperacion(email)
        if not token:
            return False, "No existe ningún usuario registrado con ese correo."

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        email_from = os.getenv("EMAIL_FROM")

        if not smtp_host or not smtp_user or not smtp_password or not email_from:
            return False, "No está configurado el servidor SMTP. Actualiza las variables de entorno en .env."

        mensaje = EmailMessage()
        mensaje["Subject"] = "Recuperación de contraseña MoodDay"
        mensaje["From"] = email_from
        mensaje["To"] = email
        mensaje.set_content(
            f"Hola,\n\nSe ha solicitado restablecer tu contraseña de MoodDay.\n\n"
            f"Usa este código para recuperar tu cuenta:\n\n{token}\n\n"
            "El código es válido por 1 hora. Si no solicitaste este cambio, ignora este mensaje.\n\n"
            "Saludos,\nMoodDay"
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
            return False, "No se pudo enviar el correo. Revisa la configuración SMTP."

    def restablecer_contrasena(self, token, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."

        success = self.model.actualizar_password_por_token(token, password)
        if success:
            return True, "Contraseña restablecida con éxito."
        return False, "El código es inválido o ha expirado."
