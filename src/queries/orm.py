from sqlalchemy import text, insert
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm, ResumesOrm, Workload


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_ivan = WorkersOrm(username="Ivan")
            worker_john = WorkersOrm(username="John")
            session.add_all([worker_ivan, worker_john])
            # flush отправляет запрос в базу данных
            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()



class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_data():
        async with async_session_factory() as session:
            worker_ivan = WorkersOrm(username="Ivan")
            worker_john = WorkersOrm(username="John")
            session.add_all([worker_ivan, worker_john])
            await session.commit()