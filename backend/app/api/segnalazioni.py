from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.segnalazione import SegnalazioneCreate, SegnalazioneResponse
from app.services.segnalazione_service import SegnalazioneService

router = APIRouter(prefix="/api/v1/segnalazioni", tags=["segnalazioni"])


@router.post("/", response_model=SegnalazioneResponse, status_code=status.HTTP_201_CREATED)
async def create_segnalazione(
    data: SegnalazioneCreate,
    db: AsyncSession = Depends(get_db),
):
    segnalazione = await SegnalazioneService.create(db, data)
    return SegnalazioneResponse.from_orm(segnalazione)


@router.get("/{unique_code}", response_model=SegnalazioneResponse)
async def get_segnalazione(
    unique_code: str,
    db: AsyncSession = Depends(get_db),
):
    segnalazione = await SegnalazioneService.get_by_code(db, unique_code)
    if segnalazione is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Segnalazione {unique_code} non trovata",
        )
    return SegnalazioneResponse.from_orm(segnalazione)