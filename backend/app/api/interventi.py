from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.schemas.intervento import InterventoCreate, InterventoResponse
from app.services.intervento_service import InterventoService

router = APIRouter(prefix="/api/v1/interventi", tags=["interventi"])


@router.post("/", response_model=InterventoResponse, status_code=status.HTTP_201_CREATED)
async def create_intervento(
    data: InterventoCreate,
    db: AsyncSession = Depends(get_db),
):
    intervento = await InterventoService.create(db, data)
    return InterventoResponse.model_validate(intervento)


@router.get("/", response_model=list[InterventoResponse])
async def get_intervento_list(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    interventi = await InterventoService.get_list(db, page, page_size)
    return [InterventoResponse.model_validate(i) for i in interventi]


@router.get("/{intervento_id}", response_model=InterventoResponse)
async def get_intervento(
    intervento_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    intervento = await InterventoService.get_by_id(db, intervento_id)
    if intervento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intervento {intervento_id} non trovato",
        )
    return InterventoResponse.model_validate(intervento)