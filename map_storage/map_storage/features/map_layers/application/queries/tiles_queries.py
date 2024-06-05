from typing import List, Optional, Sequence, Any, Callable, Tuple
import cv2
import geopy
import geopy.distance
import numpy as np
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dataclasses import dataclass

from map_storage.features.map_layers.models.map_tile import MapTile
from map_storage.features.shared.models.coordinates import Coordinates


class ListTilesQuery(BaseModel):
    layers_ids: List[int]
    offset: int
    limit: int
    select_img: bool
    select_surf: bool
    select_fast: bool


@dataclass
class TileResponse:
    latitude: float
    longitude: float
    vertices: List[Tuple[float, float]]
    azimuth: float
    img: Optional[np.ndarray]
    surf_keypoints: Sequence[cv2.KeyPoint]
    surf_descriptors: np.ndarray[Any, np.dtype[np.generic]]
    fast_keypoints: Optional[np.ndarray]
    img_shape: Tuple[int, int]


async def query_tiles_wrapper(
        db: AsyncSession,
        query: ListTilesQuery,
        db_query: Callable):

    select_attributes = [
        MapTile.center_lat, MapTile.center_long,
        MapTile.nw_lat, MapTile.nw_long,
        MapTile.ne_lat, MapTile.ne_long,
        MapTile.se_lat, MapTile.se_long,
        MapTile.sw_lat, MapTile.sw_long,
        MapTile.azimuth,
        MapTile.img_height,
        MapTile.img_width
    ]

    if query.select_img:
        select_attributes.append(MapTile.img)

    if query.select_surf:
        select_attributes.append(MapTile.surf_features)

    if query.select_fast:
        select_attributes.append(MapTile.fast_keypoints)

    res = (await db.execute(db_query(select_attributes))).all()

    return [TileResponse(
        latitude=row.center_lat,
        longitude=row.center_long,
        vertices=[(row.nw_lat, row.nw_long), (row.ne_lat, row.ne_long), (row.se_lat, row.se_long), (row.sw_lat, row.sw_long)],
        azimuth=row.azimuth,
        img=row.img if query.select_img else None,
        surf_keypoints=row.surf_features.keypoints if query.select_surf else None,
        surf_descriptors=row.surf_features.descriptors if query.select_surf else None,
        fast_keypoints=row.fast_keypoints if query.select_fast else None,
        img_shape=(row.img_height, row.img_width)
    ) for row in res]


class ListTilesInRectangleQuery(ListTilesQuery):
    start: Coordinates
    end: Coordinates

class ListTilesInRectangleQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self, query: ListTilesInRectangleQuery) -> List[TileResponse]:
        def db_query(select_attributes):
            lat_interval = sorted((query.start.latitude, query.end.latitude))
            long_interval = sorted((query.start.longitude, query.end.longitude))

            return ((select(*select_attributes)
                         .where(MapTile.map_layer_id.in_(query.layers_ids)))
                        .where(MapTile.center_lat.between(*lat_interval))
                        .where(MapTile.center_long.between(*long_interval))
                        .order_by(MapTile.center_lat.asc(), MapTile.center_long.asc())
                        .offset(query.offset).limit(query.limit))

        return await query_tiles_wrapper(self._db, query, db_query)


class ListTilesOverlappingWithSquareQuery(ListTilesQuery):
    square_center: Coordinates
    square_size: float


class ListTilesOverlappingWithSquareQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self, query: ListTilesOverlappingWithSquareQuery):
        def db_query(select_attributes):
            center = geopy.Point(*query.square_center)
            d = geopy.distance.distance(kilometers=query.square_size / 2 / 1000)

            limiting_points = [
                d.destination(point=center, bearing=0),
                d.destination(point=center, bearing=180),
                d.destination(point=center, bearing=90),
                d.destination(point=center, bearing=270)
            ]

            lat_interval = sorted(p.latitude for p in limiting_points[:2])
            long_interval = sorted(p.longitude for p in limiting_points[-2:])

            return ((select(*select_attributes)
                    .where(MapTile.map_layer_id.in_(query.layers_ids)))
                    .where((MapTile.nw_lat.between(*lat_interval) & MapTile.nw_long.between(*long_interval))
                           | (MapTile.ne_lat.between(*lat_interval) & MapTile.ne_long.between(*long_interval))
                           | (MapTile.se_lat.between(*lat_interval) & MapTile.se_long.between(*long_interval))
                           | (MapTile.sw_lat.between(*lat_interval) & MapTile.sw_long.between(*long_interval)))
                    .order_by(MapTile.center_lat.asc(), MapTile.center_long.asc())
                    .offset(query.offset).limit(query.limit))

        return await query_tiles_wrapper(self._db, query, db_query)