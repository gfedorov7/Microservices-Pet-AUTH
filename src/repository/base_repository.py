from abc import ABC
from typing import Type, Sequence, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Select

from src.repository.repository import Repository
from src.util.type.model import ModelType


class BaseRepository(Repository):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        return await self._get_one_or_none_by_stmt(stmt)

    async def get(self, limit: int, offset: int) -> Sequence[ModelType] | None:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, model: Dict[str, Any]) -> ModelType:
        record = self.model(**model)
        self.session.add(record)
        await self.session.commit()
        return record

    async def update(self, id: int, model: Dict[str, Any]) -> ModelType:
        instance = await self.get_by_id(id)
        instance = self._update_instance(instance, model)
        await self.session.commit()
        return instance

    async def delete(self, id: int) -> None:
        instance = await self.get_by_id(id)
        if not instance:
            return
        
        await self.session.delete(instance)
        await self.session.commit()
        
    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        return await self._get_one_or_none_by_stmt(stmt) or 0

    async def _get_one_or_none_by_stmt(self, stmt: Select) -> Any | None:
        record = await self.session.execute(stmt)
        return record.scalar_one_or_none()

    @staticmethod
    def _update_instance(instance: ModelType, model: Dict[str, Any]) -> ModelType:
        for key, value in model.items():
            if value is None:
                continue
            setattr(instance, key, value)
        return instance