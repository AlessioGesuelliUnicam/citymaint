from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_operatore
from app.models.operatore import Operatore
from app.schemas.segnalazione import SegnalazioneCreate, SegnalazioneUpdate, SegnalazioneResponse
from app.services.segnalazione_service import SegnalazioneService

router = APIRouter(prefix="/api/v1/segnalazioni", tags=["segnalazioni"])


@router.post("/", response_model=SegnalazioneResponse, status_code=status.HTTP_201_CREATED)
async def create_segnalazione(
    data: SegnalazioneCreate,
    db: AsyncSession = Depends(get_db),
):
    segnalazione = await SegnalazioneService.create(db, data)
    return SegnalazioneResponse.from_orm(segnalazione)


@router.get("/", response_model=list[SegnalazioneResponse])
async def get_segnalazione_list(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_operatore: Operatore = Depends(get_current_operatore),
):
    segnalazioni = await SegnalazioneService.get_list(db, page, page_size)
    return [SegnalazioneResponse.from_orm(s) for s in segnalazioni]


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


@router.patch("/{unique_code}", response_model=SegnalazioneResponse)
async def update_segnalazione(
    unique_code: str,
    data: SegnalazioneUpdate,
    db: AsyncSession = Depends(get_db),
    current_operatore: Operatore = Depends(get_current_operatore),
):
    segnalazione = await SegnalazioneService.get_by_code(db, unique_code)
    if segnalazione is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Segnalazione {unique_code} non trovata",
        )
    segnalazione = await SegnalazioneService.update(db, segnalazione, data)
    return SegnalazioneResponse.from_orm(segnalazione)