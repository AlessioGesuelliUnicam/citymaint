import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from geoalchemy2.shape import to_shape

from app.models.enums import CategoriaSegnalazione, StatoSegnalazione


class SegnalazioneCreate(BaseModel):
    category: CategoriaSegnalazione = CategoriaSegnalazione.DA_VERIFICARE
    description: str
    latitude: float
    longitude: float
    citizen_email: str | None = None


class SegnalazioneUpdate(BaseModel):
    category: CategoriaSegnalazione | None = None
    status: StatoSegnalazione | None = None
    ai_suggested_category: str | None = None
    ai_priority_score: Decimal | None = None


class SegnalazioneResponse(BaseModel):
    id: uuid.UUID
    unique_code: str
    category: CategoriaSegnalazione
    description: str
    latitude: float
    longitude: float
    status: StatoSegnalazione
    ai_suggested_category: str | None
    ai_priority_score: Decimal | None
    citizen_email: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm(cls, obj):
        shape = to_shape(obj.position)
        return cls(
            id=obj.id,
            unique_code=obj.unique_code,
            category=obj.category,
            description=obj.description,
            latitude=shape.y,
            longitude=shape.x,
            status=obj.status,
            ai_suggested_category=obj.ai_suggested_category,
            ai_priority_score=obj.ai_priority_score,
            citizen_email=obj.citizen_email,
            created_at=obj.created_at,
        )