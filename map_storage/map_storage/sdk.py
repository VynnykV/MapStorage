from typing import List, Tuple, Generator, Any
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import registry
from map_storage.features.map_layers.application.queries.tiles_queries import ListTilesInRectangleQuery, \
    TileResponse, ListTilesInRectangleQueryHandler, ListTilesOverlappingWithSquareQuery, \
    ListTilesOverlappingWithSquareQueryHandler
from map_storage.features.shared.models.coordinates import Coordinates
from map_storage.features.map_layers.data.sqlalchemy_config import configure_map_layers_orm


class MapStorageSDK:
    def __init__(self, db_url: str):
        self._db_engine = create_async_engine(db_url, echo=True)
        self._Session = async_sessionmaker(bind=self._db_engine)
        self._sqlalchemy_registry = registry()
        configure_map_layers_orm(self._sqlalchemy_registry)

    @asynccontextmanager
    async def session_scope(self):
        session = self._Session()
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    async def tiles_in_rectangle_area(
            self,
            layers_ids: List[int],
            start_coordinates: Tuple[float, float],
            end_coordinates: Tuple[float, float],
            offset: int, limit: int,
            select_img: bool, select_surf: bool, select_fast: bool) -> List[TileResponse]:
        async with self.session_scope() as session:
            query = ListTilesInRectangleQuery(
                layers_ids=layers_ids,
                start=Coordinates(*start_coordinates),
                end=Coordinates(*end_coordinates),
                offset=offset, limit=limit,
                select_img=select_img, select_surf=select_surf, select_fast=select_fast
            )
            handler = ListTilesInRectangleQueryHandler(session)
            return await handler(query)


    async def tiles_overlapping_with_square(
            self,
            layers_ids: List[int],
            square_center: Tuple[float, float],
            square_size_m: float,
            offset: int, limit: int,
            select_img: bool, select_surf: bool, select_fast: bool) -> List[TileResponse]:
        async with self.session_scope() as session:
            query = ListTilesOverlappingWithSquareQuery(
                layers_ids=layers_ids,
                square_center=Coordinates(*square_center),
                square_size=square_size_m,
                offset=offset, limit=limit,
                select_img=select_img, select_surf=select_surf, select_fast=select_fast
            )
            handler = ListTilesOverlappingWithSquareQueryHandler(session)
            return await handler(query)
