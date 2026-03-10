from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.operatore import OperatoreCreate, OperatoreResponse
from app.services.operatore_service import OperatoreService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    operatore = await OperatoreService.authenticate(
        db, form_data.username, form_data.password
    )
    if operatore is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=str(operatore.id))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=OperatoreResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: OperatoreCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await OperatoreService.get_by_email(db, data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email già registrata",
        )
    operatore = await OperatoreService.create(db, data)
    return OperatoreResponse.model_validate(operatore)