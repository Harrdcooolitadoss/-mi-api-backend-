from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db
from app.models import Usuario
from app.auth import generar_token, generar_hash, verificar_contraseña
from app.dependencies import obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/")
async def registrar_usuario(usuario: Usuario):
    """Registra un nuevo usuario con contraseña encriptada."""
    existente = await db.usuarios.find_one({"email": usuario.email})
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    usuario.password = generar_hash(usuario.password)  # Encriptar la contraseña antes de guardarla
    resultado = await db.usuarios.insert_one(usuario.dict())
    return {"id": str(resultado.inserted_id)}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = await db.usuarios.find_one({"email": form_data.username})
    if not usuario or not verificar_contraseña(form_data.password, usuario["password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = generar_token({"sub": usuario["email"], "nombre": usuario["nombre"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/perfil")
async def obtener_perfil(usuario: dict = Depends(obtener_usuario_actual)):
    """Devuelve información del usuario autenticado."""
    return {"mensaje": f"Bienvenido, {usuario['nombre']}"}

@router.get("/")
async def obtener_todos_los_usuarios():
    """Obtiene la lista de todos los usuarios en la base de datos."""
    usuarios = await db.usuarios.find().to_list(length=100)
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])  # Convertir ObjectId a string
    return usuarios

@router.get("/{email}")
async def obtener_usuario(email: str):
    """Obtiene un usuario específico por su email."""
    usuario = await db.usuarios.find_one({"email": email})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario["_id"] = str(usuario["_id"])  # Convertir ObjectId a string
    return usuario

@router.put("/{email}")
async def actualizar_usuario(email: str, usuario: Usuario):
    """Actualiza toda la información de un usuario."""
    resultado = await db.usuarios.update_one({"email": email}, {"$set": usuario.dict()})
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario actualizado"}

@router.patch("/{email}")
async def modificar_parcial_usuario(email: str, datos: dict):
    """Modifica parcialmente un usuario por su email."""
    resultado = await db.usuarios.update_one({"email": email}, {"$set": datos})
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario modificado parcialmente"}

@router.delete("/{email}")
async def eliminar_usuario(email: str):
    """Elimina un usuario de la base de datos."""
    resultado = await db.usuarios.delete_one({"email": email})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario eliminado"}
