from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    
class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    telefono: Optional[str] = None
    numero_control: str = Field(..., min_length=3, max_length=50)
    grado: str = Field(..., min_length=1, max_length=50)
    grupo: str = Field(..., min_length=1, max_length=20)
    edad: int = Field(..., ge=10, le=120)
    sexo: str = Field(..., min_length=4, max_length=30)
    
class TareaSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    estado_animo: str = Field(..., min_length=3, max_length=30)
    intensidad: int = Field(..., ge=1, le=10)
    clasificacion: str = "personal"
    prioridad: str = "media"
