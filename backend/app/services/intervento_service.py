import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.intervento import Intervento
from app.models.enums import StatoIntervento
from app.schemas.intervento import InterventoCreate


class InterventoService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: InterventoCreate,
    ) -> Intervento:
        intervento = Intervento(
            id=uuid.uuid4(),
            title=data.title,
            type=data.type,
            status=StatoIntervento.PIANIFICATO,
            asset_id=data.asset_id,
            squadra_id=data.squadra_id,
            planned_date=data.planned_date,
            estimated_cost=data.estimated_cost,
            notes=data.notes,
        )

        db.add(intervento)
        await db.flush()
        await db.refresh(intervento)
        return intervento

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        intervento_id: uuid.UUID,
    ) -> Intervento | None:
        result = await db.execute(
            select(Intervento).where(Intervento.id == intervento_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Intervento]:
        offset = (page - 1) * page_size
        result = await db.execute(
            select(Intervento)
            .order_by(Intervento.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return list(result.scalars().all())