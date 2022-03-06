from abc import ABC, abstractmethod

from sqlalchemy.sql.schema import Table as SaTable

from .mixins import InsertMixin, SelectMixin, UpdateMixin


class Base(ABC, SelectMixin, InsertMixin, UpdateMixin):
    def __init__(self, database):
        self.database = database

    @property
    @abstractmethod
    def ilike_fields(self) -> tuple:
        """fields for ilike select filter"""

    @property
    @abstractmethod
    def exact_fields(self) -> tuple:
        """fields for exact select filter"""

    @property
    @abstractmethod
    def table(self) -> SaTable:
        ...

    async def select(self, multiple=False, **kwargs):
        query = self.prepare_select_query(**kwargs)
        return (
            await self.database.fetch_all(query)
            if multiple
            else await self.database.fetch_one(query)
        )

    async def insert(self, **kwargs):
        query = self.table.insert().values(**kwargs)
        record_id = await self.database.execute(query)
        return {"id": record_id}

    async def update(self, where, values):
        query = self.prepare_update_query(where, values)
        return await self.database.execute(query)
