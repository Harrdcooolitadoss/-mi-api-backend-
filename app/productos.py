from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Producto
from bson import ObjectId  # Para convertir ObjectId a string

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
async def crear_producto(producto: Producto):
    existente = await db.productos.find_one({"nombre": producto.nombre})
    if existente:
        raise HTTPException(status_code=400, detail="El producto ya existe")

    resultado = await db.productos.insert_one(producto.dict())
    return {"id": str(resultado.inserted_id)}

@router.get("/")
async def obtener_todos_los_productos():
    productos = await db.productos.find().to_list(length=100)
    for producto in productos:
        producto["_id"] = str(producto["_id"])  # Convertir ObjectId a string

    return productos

@router.get("/{nombre}")
async def obtener_producto(nombre: str):
    producto = await db.productos.find_one({"nombre": nombre})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto["_id"] = str(producto["_id"])  # Convertir ObjectId a string
    return producto

@router.put("/{nombre}")
async def actualizar_producto(nombre: str, producto: Producto):
    resultado = await db.productos.update_one({"nombre": nombre}, {"$set": producto.dict()})
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto actualizado"}

@router.patch("/{nombre}")
async def modificar_parcial_producto(nombre: str, datos: dict):
    resultado = await db.productos.update_one({"nombre": nombre}, {"$set": datos})
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto modificado parcialmente"}

@router.delete("/{nombre}")
async def eliminar_producto(nombre: str):
    resultado = await db.productos.delete_one({"nombre": nombre})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto eliminado"}
