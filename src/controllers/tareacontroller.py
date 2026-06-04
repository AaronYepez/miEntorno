import os
import json
import urllib.error
import urllib.request
from models.tareasModel import TareasModel

class TareaController:
    def __init__(self):
        self.model = TareasModel()
    
    def obtener_lista(self, id_usuario):
        try:
            return self.model.listar_por_usuario(id_usuario)
        except Exception as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def obtener_frase_motivadora(self, descripcion, razon_emocion=None):
        api_key = os.getenv("GOOGLE_API_KEY")
        model = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

        if not api_key:
            return (
                "Recuerda que cada día es una nueva oportunidad para cuidarte. "
                "Respira profundo y sigue avanzando con calma."
            )

        razon_text = f" Razón: {razon_emocion.strip()}." if razon_emocion else ""
        prompt = (
            "Eres MoodDay, un asistente de salud mental empático, cálido y compasivo. "
            "Tu tarea es leer el estado de ánimo del usuario y responder con una sola frase "
            "corta (máximo 2 líneas), reconfortante, alentadora y en español. "
            "Adapta tu respuesta exactamente a lo que le duele o le alegra al usuario. "
            "Sé directo, no uses introducciones como 'Lamento escuchar eso' o 'Aquí tienes tu frase'. "
            "El usuario describe su estado: \"" + descripcion.strip() + "\"." + razon_text
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-goog-api-key": api_key
        }

        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    candidate = candidates[0]
                    content = candidate.get("content") or {}
                    parts = content.get("parts", [])
                    if parts:
                        first_part = parts[0]
                        text = first_part.get("text")
                        if isinstance(text, str) and text.strip():
                            return text.strip()
                    if isinstance(content, dict):
                        return json.dumps(content, ensure_ascii=False)
                return "Mantente presente y recuerda que cada paso cuenta."
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if hasattr(e, "read") else ""
            print(f"Error API Gemini HTTP: {e.code} {e.reason}. {error_body}")
        except urllib.error.URLError as e:
            print(f"Error API Gemini URL: {e.reason}")
        except Exception as e:
            print(f"Error al generar frase motivadora: {e}")

        return (
            "Tu voz importa y estás haciendo lo correcto al registrar cómo te sientes. "
            "Date un momento para respirar."
        )

    def evaluar_alerta(self, id_usuario):
        # Considerar sólo los últimos 3 registros (más recientes)
        tareas = self.obtener_lista(id_usuario)[:3]
        if not tareas:
            return None

        # Conteo específico para tristeza: si al menos 2 de los últimos 3 son 'triste', mostrar alerta
        triste_count = 0
        for tarea in tareas:
            estado = (tarea.get("estado_animo") or "").lower()
            if estado == "triste":
                triste_count += 1

        if triste_count >= 2:
            return (
                "Hemos detectado varios registros recientes de tristeza. "
                "Si te sientes abrumado, habla con alguien de confianza, practica ejercicios de respiración "
                "o busca apoyo profesional. Esto no es un diagnóstico médico, solo una recomendación de bienestar."
            )

        # Fallback: no mostrar alerta por defecto
        return None

    def guardar_nueva(self, id_usuario, titulo, desc, razon_emocion, estado_animo, intensidad):
        if not titulo or not titulo.strip():
            return False, "El título es obligatorio.", None
        if not desc or not desc.strip():
            return False, "Describe cómo te sientes antes de guardar.", None
        if not razon_emocion or not razon_emocion.strip():
            return False, "Cuéntanos por qué te sientes así para entender mejor tu experiencia.", None
        if not estado_animo:
            return False, "Selecciona cómo te sientes.", None
        if intensidad is None or intensidad < 1 or intensidad > 10:
            return False, "Selecciona la intensidad de tu emoción entre 1 y 10.", None
        
        try:
            frase = self.obtener_frase_motivadora(desc, razon_emocion)
            self.model.crear_tarea(id_usuario, titulo, desc, razon_emocion, estado_animo, intensidad, frase)
            return True, "Registro emocional guardado exitosamente.", frase
        except Exception as e:
            print(f"Error al guardar tarea: {e}")
            return False, "Error al guardar la entrada. Intenta de nuevo.", None
