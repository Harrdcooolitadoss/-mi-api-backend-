from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    nombre: str
    email: EmailStr
    password: str  # Se añade el campo de contraseña para la autenticación
    edad: Optional[int] = None

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int
