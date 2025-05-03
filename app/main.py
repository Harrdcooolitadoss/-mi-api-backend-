from fastapi import FastAPI
from app.usuarios import router as usuarios_router
from app.productos import router as productos_router

app = FastAPI(title="FastAPI con MongoDB + JWT Autenticación")

# Registrar los routers en la aplicación
app.include_router(usuarios_router)
app.include_router(productos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
