import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Enum as SAEnum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.enums import RuoloOperatore
from app.models.mixins import TimestampMixin


class Operatore(TimestampMixin, Base):
    __tablename__ = "operatori"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RuoloOperatore] = mapped_column(
        SAEnum(RuoloOperatore, name="ruolooperatore"),
        nullable=False,
        default=RuoloOperatore.OPERATORE,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)