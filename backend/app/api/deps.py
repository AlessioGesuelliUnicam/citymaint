from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.operatore import Operatore
from app.services.operatore_service import OperatoreService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_operatore(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Operatore:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    operatore_id = decode_access_token(token)
    if operatore_id is None:
        raise credentials_exception
    try:
        operatore = await OperatoreService.get_by_id(
            db, uuid.UUID(operatore_id)
        )
    except ValueError:
        raise credentials_exception
    if operatore is None:
        raise credentials_exception
    return operatore