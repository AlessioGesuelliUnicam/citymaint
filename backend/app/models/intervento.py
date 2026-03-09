import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import String, Text, Date, Numeric, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.mixins import TimestampMixin
from app.models.enums import TipoIntervento, StatoIntervento

class Intervento(TimestampMixin, Base):
    __tablename__ = "interventi"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    type: Mapped[TipoIntervento] = mapped_column(
        SAEnum(TipoIntervento, name="tipointervento"),
        nullable=False,
    )
    status: Mapped[StatoIntervento] = mapped_column(
        SAEnum(StatoIntervento, name="statointervento"),
        nullable=False,
        default=StatoIntervento.PIANIFICATO,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("asset_urbani.id", ondelete="RESTRICT"),
        nullable=False,
    )
    squadra_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("squadre.id", ondelete="SET NULL"),
        nullable=True,
    )
    planned_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimated_cost: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    actual_cost: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)