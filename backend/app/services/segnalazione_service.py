import logging
import uuid
import random
import string
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.segnalazione import Segnalazione
from app.models.enums import StatoSegnalazione
from app.schemas.segnalazione import SegnalazioneCreate, SegnalazioneUpdate
from app.services.email_service import EmailService
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


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

        # Conta segnalazioni entro 50m negli ultimi 30gg (EPSG:32633 = UTM 33N, usa metri)
        try:
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            nearby_result = await db.execute(
                select(func.count(Segnalazione.id)).where(
                    func.ST_DWithin(
                        func.ST_Transform(Segnalazione.position, 32633),
                        func.ST_Transform(
                            func.ST_GeomFromText(point_wkt, 4326), 32633
                        ),
                        50.0,
                    ),
                    Segnalazione.created_at >= thirty_days_ago,
                    Segnalazione.id != segnalazione.id,
                )
            )
            numero_vicine = nearby_result.scalar() or 0
        except Exception as e:
            logger.warning("[AI] Query PostGIS segnalazioni vicine fallita: %s", e)
            numero_vicine = 0

        ai = AIService()
        cat = await ai.categorizza(data.description)
        prio = await ai.calcola_priorita(
            descrizione=data.description,
            categoria=cat.categoria.value,
            numero_segnalazioni_vicine=numero_vicine,
            giorni_apertura=0,
            vicino_zona_sensibile=False,
        )

        segnalazione.ai_suggested_category = cat.categoria.value
        segnalazione.ai_priority_score = prio.score
        await db.flush()
        await db.refresh(segnalazione)

        if data.citizen_email:
            await EmailService.send_conferma_segnalazione(
                to=data.citizen_email,
                unique_code=unique_code,
                description=data.description,
            )

        return segnalazione

    @staticmethod
    async def update(
        db: AsyncSession,
        segnalazione: Segnalazione,
        data: SegnalazioneUpdate,
    ) -> Segnalazione:
        vecchio_stato = segnalazione.status

        if data.category is not None:
            segnalazione.category = data.category
        if data.status is not None:
            segnalazione.status = data.status
        if data.ai_suggested_category is not None:
            segnalazione.ai_suggested_category = data.ai_suggested_category
        if data.ai_priority_score is not None:
            segnalazione.ai_priority_score = data.ai_priority_score

        await db.flush()
        await db.refresh(segnalazione)

        if (
            data.status is not None
            and data.status != vecchio_stato
            and segnalazione.citizen_email
        ):
            await EmailService.send_aggiornamento_stato(
                to=segnalazione.citizen_email,
                unique_code=segnalazione.unique_code,
                nuovo_stato=data.status.value,
            )

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