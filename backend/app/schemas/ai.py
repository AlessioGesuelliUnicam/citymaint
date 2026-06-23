from pydantic import BaseModel, Field

from app.models.enums import CategoriaSegnalazione


class RispostaCategorizzazione(BaseModel):
    categoria: CategoriaSegnalazione
    confidence: float = Field(ge=0.0, le=1.0)
    motivazione: str


class RispostaPrioritizzazione(BaseModel):
    score: float = Field(ge=0.0, le=10.0)
    motivazione: str
