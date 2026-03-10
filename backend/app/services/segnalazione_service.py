import uuid
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.segnalazione import Segnalazione
from app.models.enums import StatoSegnalazione
from app.schemas.segnalazione import SegnalazioneCreate


class SegnalazioneService:

    @staticmethod
    def _generate_unique_code() -> str:
        chars = string.ascii_uppercase + string.digits
        random_part = "".join(random.choices(chars, k=6))
        return f"SEG-{random_part}"

    @staticmethod
    async def create(
        db: AsyncSession,
        data: SegnalazioneCreate,
    ) -> Segnalazione:
        from geoalchemy2.functions import ST_GeomFromText

        unique_code = SegnalazioneService._generate_unique_code()
        point_wkt = f"POINT({data.longitude} {data.latitude})"

        segnalazione = Segnalazione(
            id=uuid.uuid4(),
            unique_code=unique_code,
            category=data.category,
            description=data.description,
            position=ST_GeomFromText(point_wkt, 4326),
            status=StatoSegnalazione.APERTA,
            citizen_email=data.citizen_email,
        )

        db.add(segnalazione)
        await db.flush()
        await db.refresh(segnalazione)
        return segnalazione

    @staticmethod
    async def get_by_code(
        db: AsyncSession,
        unique_code: str,
    ) -> Segnalazione | None:
        result = await db.execute(
            select(Segnalazione).where(Segnalazione.unique_code == unique_code)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Segnalazione]:
        offset = (page - 1) * page_size
        result = await db.execute(
            select(Segnalazione)
            .order_by(Segnalazione.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return list(result.scalars().all())