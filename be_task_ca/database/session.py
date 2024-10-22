from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine, AsyncEngine,
)

from be_task_ca.config import settings

from be_task_ca.database.models import Base

async_engine: AsyncEngine = None
async_session: AsyncSession = None


async def init_session():
    global async_engine, async_session
    async_engine = create_async_engine(settings.database_url)
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            # A commit here ensures that we're never losing anything although the inserts already need to independently
            # call commit() to retrieve the generated ID to return
            await session.commit()
        except exc.SQLAlchemyError as _:
            await session.rollback()
            raise


async def init_models():
    # Alembic would be used for migrations in a real service
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
