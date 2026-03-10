import uuid
from decimal import Decimal
from sqlalchemy import String, Text, Numeric, Enum as SAEnum, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry

from app.core.database import Base
from app.models.mixins import TimestampMixin
from app.models.enums import CategoriaSegnalazione, StatoSegnalazione


class Segnalazione(TimestampMixin, Base):
    __tablename__ = "segnalazioni"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    unique_code: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    category: Mapped[CategoriaSegnalazione] = mapped_column(
        SAEnum(CategoriaSegnalazione, name="categoriasegnalazione"),
        nullable=False,
        default=CategoriaSegnalazione.DA_VERIFICARE,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[bytes] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False,
    )
    status: Mapped[StatoSegnalazione] = mapped_column(
        SAEnum(StatoSegnalazione, name="statosegnalazione"),
        nullable=False,
        default=StatoSegnalazione.APERTA,
    )
    ai_suggested_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ai_priority_score: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    citizen_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        Index("idx_segnalazioni_position", "position", postgresql_using="gist"),
    )