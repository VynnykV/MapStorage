from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from map_storage.features.map_layers.models.map_layer import MapLayer


class ListMapLayersQuery:
    pass


class ListMapLayer(BaseModel):
    id: int
    name: str
    import_type: str


ListMapLayersResponse = List[ListMapLayer]


class ListMapLayersQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self, request: ListMapLayersQuery) -> ListMapLayersResponse:
        query = select(MapLayer)
        map_layers = (await self._db.scalars(query)).unique().all()

        return [ListMapLayer(id=m.id, name=m.name, import_type=m.import_type) for m in map_layers]
