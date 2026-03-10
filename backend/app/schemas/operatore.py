import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.models.enums import RuoloOperatore

class OperatoreCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: RuoloOperatore = RuoloOperatore.OPERATORE


class OperatoreUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    role: RuoloOperatore | None = None
    is_active: bool | None = None


class OperatoreResponse(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    role: RuoloOperatore
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}