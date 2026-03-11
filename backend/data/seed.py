import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_GeomFromText

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.enums import (
    RuoloOperatore, TipoAsset, CategoriaSegnalazione,
    StatoSegnalazione, TipoIntervento, StatoIntervento
)
from app.models.operatore import Operatore
from app.models.squadra import Squadra, SquadraOperatore
from app.models.asset import AssetUrbano
from app.models.segnalazione import Segnalazione
from app.models.intervento import Intervento
import app.models

async def seed():
    async with AsyncSessionLocal() as db:
        # Operatori
        admin = Operatore(
            id=uuid.uuid4(),
            name="Luca",
            surname="Bianchi",
            email="luca.bianchi@comune.tolentino.mc.it",
            hashed_password=hash_password("admin123"),
            role=RuoloOperatore.ADMIN,
        )
        tecnico = Operatore(
            id=uuid.uuid4(),
            name="Sara",
            surname="Mancini",
            email="sara.mancini@comune.tolentino.mc.it",
            hashed_password=hash_password("tecnico123"),
            role=RuoloOperatore.TECNICO,
        )
        operatore1 = Operatore(
            id=uuid.uuid4(),
            name="Marco",
            surname="Gentili",
            email="marco.gentili@comune.tolentino.mc.it",
            hashed_password=hash_password("operatore123"),
            role=RuoloOperatore.OPERATORE,
        )
        db.add_all([admin, tecnico, operatore1])
        await db.flush()

        # Squadra
        squadra = Squadra(
            id=uuid.uuid4(),
            name="Squadra Manutenzione Strade",
        )
        db.add(squadra)
        await db.flush()

        # Assegna operatore alla squadra
        db.add(SquadraOperatore(
            squadra_id=squadra.id,
            operatore_id=operatore1.id,
            is_team_leader=True,
        ))

        # Asset urbani di Tolentino
        lampione = AssetUrbano(
            id=uuid.uuid4(),
            type=TipoAsset.LAMPIONE,
            name="Lampione Piazza della Libertà",
            geometry=ST_GeomFromText("POINT(13.2833 43.2097)", 4326),
            useful_life_years=20,
        )
        strada = AssetUrbano(
            id=uuid.uuid4(),
            type=TipoAsset.STRADA,
            name="Via Indipendenza",
            geometry=ST_GeomFromText("POINT(13.2841 43.2103)", 4326),
            useful_life_years=30,
        )
        parco = AssetUrbano(
            id=uuid.uuid4(),
            type=TipoAsset.PARCO,
            name="Parco della Roverella",
            geometry=ST_GeomFromText("POINT(13.2819 43.2088)", 4326),
            useful_life_years=50,
        )
        db.add_all([lampione, strada, parco])
        await db.flush()

        # Segnalazioni
        seg1 = Segnalazione(
            id=uuid.uuid4(),
            unique_code="SEG-TOL001",
            category=CategoriaSegnalazione.STRADALE,
            description="Buca profonda in Via Indipendenza altezza civico 12",
            position=ST_GeomFromText("POINT(13.2841 43.2103)", 4326),
            status=StatoSegnalazione.IN_LAVORAZIONE,
            citizen_email="cittadino1@email.it",
        )
        seg2 = Segnalazione(
            id=uuid.uuid4(),
            unique_code="SEG-TOL002",
            category=CategoriaSegnalazione.ILLUMINAZIONE,
            description="Lampione spento in Piazza della Libertà",
            position=ST_GeomFromText("POINT(13.2833 43.2097)", 4326),
            status=StatoSegnalazione.APERTA,
            citizen_email="cittadino2@email.it",
        )
        db.add_all([seg1, seg2])
        await db.flush()

        # Intervento
        intervento = Intervento(
            id=uuid.uuid4(),
            title="Riparazione buca Via Indipendenza",
            type=TipoIntervento.ORDINARIO,
            status=StatoIntervento.IN_CORSO,
            asset_id=strada.id,
            squadra_id=squadra.id,
            estimated_cost=500,
        )
        db.add(intervento)
        await db.flush()

        await db.commit()
        print("Seed completato con successo!")


if __name__ == "__main__":
    asyncio.run(seed())