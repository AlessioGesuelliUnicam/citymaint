import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.functions import ST_GeomFromText

from app.models.asset import AssetUrbano
from app.schemas.asset import AssetCreate, AssetUpdate

class AssetService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: AssetCreate,
    ) -> AssetUrbano:
        point_wkt = f"POINT({data.longitude} {data.latitude})"

        asset = AssetUrbano(
            id=uuid.uuid4(),
            type=data.type,
            name=data.name,
            geometry=ST_GeomFromText(point_wkt, 4326),
            installation_date=data.installation_date,
            useful_life_years=data.useful_life_years,
            notes=data.notes,
        )

        db.add(asset)
        await db.flush()
        await db.refresh(asset)
        return asset

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        asset_id: uuid.UUID,
    ) -> AssetUrbano | None:
        result = await db.execute(
            select(AssetUrbano).where(AssetUrbano.id == asset_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
    ) -> list[AssetUrbano]:
        offset = (page - 1) * page_size
        result = await db.execute(
            select(AssetUrbano)
            .order_by(AssetUrbano.name)
            .offset(offset)
            .limit(page_size)
        )
        return list(result.scalars().all())