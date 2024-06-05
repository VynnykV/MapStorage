from typing import List

from pydantic import BaseModel, conint
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from map_storage.features.map_layers.models.map_layer import MapLayer
from map_storage.features.shared.queries import FilteredQuery


class MapLayerDetailsQuery(FilteredQuery):
    id: conint(ge=1)

    def filter_by(self, select_expression: Select) -> Select:
        return select_expression.where(MapLayer.id == self.id)


class ListMapLayerTiles(BaseModel):
    id: int
    center_lat: float
    center_long: float
    nw_lat: float
    nw_long: float
    ne_lat: float
    ne_long: float
    se_lat: float
    se_long: float
    sw_lat: float
    sw_long: float


class MapLayerDetailsResponse(BaseModel):
    id: int
    name: str
    import_type: str
    tiles: List[ListMapLayerTiles]


class MapLayerDetailsQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self,
                       query: MapLayerDetailsQuery) -> MapLayerDetailsResponse:
        db_query = query.db_query(MapLayer)

        db_query = db_query.options(joinedload(MapLayer._tiles))

        map_layer = await self._db.scalar(db_query)

        tiles = [ListMapLayerTiles(
            id=t.id,
            center_lat=t.center_lat,
            center_long=t.center_long,
            nw_lat=t.nw_lat,
            nw_long=t.nw_long,
            ne_lat=t.ne_lat,
            ne_long=t.ne_long,
            se_lat=t.se_lat,
            se_long=t.se_long,
            sw_lat=t.sw_lat,
            sw_long=t.sw_long
        ) for t in map_layer.tiles]

        return MapLayerDetailsResponse(
            id=map_layer.id,
            name=map_layer.name,
            import_type=map_layer.import_type,
            tiles=tiles
        )
