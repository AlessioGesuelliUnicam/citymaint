import uuid
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel

from app.models.enums import TipoIntervento, StatoIntervento


class InterventoCreate(BaseModel):
    title: str
    type: TipoIntervento
    asset_id: uuid.UUID
    squadra_id: uuid.UUID | None = None
    planned_date: date | None = None
    estimated_cost: Decimal | None = None
    notes: str | None = None


class InterventoUpdate(BaseModel):
    title: str | None = None
    type: TipoIntervento | None = None
    status: StatoIntervento | None = None
    squadra_id: uuid.UUID | None = None
    planned_date: date | None = None
    estimated_cost: Decimal | None = None
    actual_cost: Decimal | None = None
    notes: str | None = None


class InterventoResponse(BaseModel):
    id: uuid.UUID
    title: str
    type: TipoIntervento
    status: StatoIntervento
    asset_id: uuid.UUID
    squadra_id: uuid.UUID | None
    planned_date: date | None
    estimated_cost: Decimal | None
    actual_cost: Decimal | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}