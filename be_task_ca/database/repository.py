from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession
from be_task_ca.database.models import Base

Model = TypeVar("Model", bound=Base)


class SingletonMetaclass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if issubclass(args[0], Base):
            if args[0] not in cls._instances:
                cls._instances[args[0]] = super().__call__(*args, **kwargs)

            return cls._instances[args[0]]
        return super().__call__(*args, **kwargs)

class DBRepository(Generic[Model], metaclass=SingletonMetaclass):
    # This class is an implementation of the repository pattern, it makes use of the Generic class
    _session = None
    
    def __init__(self, model: type[Model]):
        self._model = model

    def with_session(self, session: AsyncSession):
        self._session = session
        return self

    async def insert(self, data: dict) -> Model:
        obj = self._model(**data)
        self._session.add(obj)

        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def update(self, id: int, data: dict) -> Model:
        obj = await self._session.get(self._model, id)

        for k, v in data.items():
            setattr(obj, k, v)

        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def get(self, id: int | UUID | None = None) -> Model | list[Model] | None:
        if id:
            return await self._session.get(self._model, id)
        else:
            return list(await self._session.scalars(select(self._model)))

    async def delete(self, id: int | None = None, obj: Model | None = None) -> Model | None:
        if id:
            obj = await self.get(id)

        if obj:
            return await self._session.delete(obj)
        else:
            return None

    async def filter(self, *expressions: BinaryExpression) -> list[Model]:
        query = select(self._model)

        if expressions:
            query = query.where(*expressions)

        return list(await self._session.scalars(query))

    async def filter_one(self, *expressions: BinaryExpression) -> Model:
        query = select(self._model)

        if expressions:
            query = query.where(*expressions)

        return (await self._session.scalars(query)).first()

