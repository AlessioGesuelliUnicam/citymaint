from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.api.deps import get_current_operatore
from app.models.operatore import Operatore
from app.schemas.asset import AssetCreate, AssetResponse
from app.services.asset_service import AssetService

router = APIRouter(prefix="/api/v1/asset", tags=["asset"])


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    data: AssetCreate,
    db: AsyncSession = Depends(get_db),
    current_operatore: Operatore = Depends(get_current_operatore),
):
    asset = await AssetService.create(db, data)
    return AssetResponse.from_orm(asset)


@router.get("/", response_model=list[AssetResponse])
async def get_asset_list(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_operatore: Operatore = Depends(get_current_operatore),
):
    assets = await AssetService.get_list(db, page, page_size)
    return [AssetResponse.from_orm(a) for a in assets]


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_operatore: Operatore = Depends(get_current_operatore),
):
    asset = await AssetService.get_by_id(db, asset_id)
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset {asset_id} non trovato",
        )
    return AssetResponse.from_orm(asset)