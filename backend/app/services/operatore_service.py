import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.operatore import Operatore
from app.core.security import hash_password, verify_password
from app.schemas.operatore import OperatoreCreate


class OperatoreService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: OperatoreCreate,
    ) -> Operatore:
        operatore = Operatore(
            id=uuid.uuid4(),
            name=data.name,
            surname=data.surname,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        db.add(operatore)
        await db.flush()
        await db.refresh(operatore)
        return operatore

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ) -> Operatore | None:
        result = await db.execute(
            select(Operatore).where(Operatore.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def authenticate(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> Operatore | None:
        operatore = await OperatoreService.get_by_email(db, email)
        if operatore is None:
            return None
        if not verify_password(password, operatore.hashed_password):
            return None
        return operatore
    
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        operatore_id: uuid.UUID,
    ) -> Operatore | None:
        result = await db.execute(
            select(Operatore).where(Operatore.id == operatore_id)
        )
        return result.scalar_one_or_none()