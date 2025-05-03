from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.auth import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return payload
