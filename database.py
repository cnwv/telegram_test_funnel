from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import settings
from sqlalchemy import select, insert, update, func

from models import Users

database_url = settings.db_url
DATABASE_PARAMS = {}

engine = create_async_engine(database_url, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class BaseDAO:
    model = Users

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def today_user_count(cls, **filter_by):
        async with async_session_maker() as session:
            today = func.current_date()
            query = select(cls.model).where(func.date(cls.model.registration_time) == today)
            result = await session.execute(query)
            count = len(result.scalars().all())
            return count

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def add_or_none(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            try:
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                return None

    @classmethod
    async def update(cls, model_id, data: dict):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.user_id == model_id).values(**data)
            await session.execute(stmt)
            await session.commit()
