import uuid
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel
from geoalchemy2.shape import to_shape

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

    @classmethod
    def from_orm(cls, obj):
        shape = to_shape(obj.geometry)
        return cls(
            id=obj.id,
            type=obj.type,
            name=obj.name,
            latitude=shape.y,
            longitude=shape.x,
            installation_date=obj.installation_date,
            useful_life_years=obj.useful_life_years,
            health_score=obj.health_score,
            notes=obj.notes,
            created_at=obj.created_at,
        )