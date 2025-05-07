from sqlalchemy import text, insert, select
from database import sync_engine, async_engine
from models import metadata_obj, workers_table


def get_sync():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")


async def get_async():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")


class SyncCore:
    # Для исперативного стиля
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            #     ('Bobr'),
            #     ('Volk');"""
            stmt = insert(workers_table).values(
                [
                    {"username": "Ivan"},
                    {"username": "John"}
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all()
            print(f"{workers=}")


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)