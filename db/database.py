from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    text = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    repeat = Column(String, nullable=True)
    done = Column(Boolean, default=False)

engine = None
SessionLocal = None

async def init_db(db_url: str):
    global engine, SessionLocal
    engine = create_async_engine(db_url, echo=False)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_task(user_id: int, parsed) -> Task:
    async with SessionLocal() as session:
        task = Task(
            user_id=user_id,
            text=parsed.text,
            date_time=parsed.date_time,
            repeat=parsed.repeat
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

async def get_user_tasks(user_id: int) -> list[Task]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Task)
            .where(Task.user_id == user_id, Task.done == False)
        )
        return result.scalars().all()

async def remove_task(user_id: int, text: str) -> bool:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Task)
            .where(
                Task.user_id == user_id,
                Task.text == text,
                Task.done == False
            )
            .limit(1)
        )
        task = result.scalars().first()
        if not task:
            return False
        task.done = True
        await session.commit()
        return True

