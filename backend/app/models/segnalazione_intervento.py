import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class SegnalazioneIntervento(Base):
    __tablename__ = "segnalazione_interventi"

    segnalazione_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("segnalazioni.id", ondelete="CASCADE"),
        primary_key=True,
    )
    intervento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interventi.id", ondelete="CASCADE"),
        primary_key=True,
    )