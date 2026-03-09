import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.mixins import TimestampMixin

class Squadra(TimestampMixin, Base):
    __tablename__ = "squadre"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class SquadraOperatore(Base):
    __tablename__ = "squadra_operatori"

    squadra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("squadre.id", ondelete="CASCADE"),
        primary_key=True,
    )
    operatore_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("operatori.id", ondelete="CASCADE"),
        primary_key=True,
    )
    is_team_leader: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)