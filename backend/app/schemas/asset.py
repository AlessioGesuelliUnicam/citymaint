import uuid
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel

from app.models.enums import TipoAsset


class AssetCreate(BaseModel):
    type: TipoAsset
    name: str
    latitude: float
    longitude: float
    installation_date: date | None = None
    useful_life_years: int | None = None
    notes: str | None = None


class AssetUpdate(BaseModel):
    name: str | None = None
    installation_date: date | None = None
    useful_life_years: int | None = None
    health_score: Decimal | None = None
    notes: str | None = None


class AssetResponse(BaseModel):
    id: uuid.UUID
    type: TipoAsset
    name: str
    latitude: float
    longitude: float
    installation_date: date | None
    useful_life_years: int | None
    health_score: Decimal | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}