import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import String, Integer, Date, Numeric, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry

from app.core.database import Base
from app.models.mixins import TimestampMixin
from app.models.enums import TipoAsset

class AssetUrbano(TimestampMixin, Base):
    __tablename__ = "asset_urbani"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    type: Mapped[TipoAsset] = mapped_column(
        SAEnum(TipoAsset, name="tipoasset"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    geometry: Mapped[bytes] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=4326),
        nullable=False,
    )
    installation_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    useful_life_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    health_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        default=100,
    )
    notes: Mapped[str | None] = mapped_column(nullable=True)