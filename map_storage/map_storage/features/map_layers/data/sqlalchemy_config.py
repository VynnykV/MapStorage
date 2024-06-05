from typing import Tuple
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, Index, Boolean
from sqlalchemy.orm import registry, composite, relationship

from map_storage.features.map_layers.models.map_layer import MapLayer
from map_storage.features.map_layers.models.map_tile import MapTile, TileSURFFeatures
from map_storage.features.shared.custom_db_types import NumpyArray, SURFKeyPoints


def configure_map_layers_orm(orm_registry: registry):
    map_layers_table = Table(
        'map_layers', orm_registry.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        Column('description', String(200), nullable=True),
        Column('import_type', String(20), nullable=False, server_default='rectangle'),
        Column('zoom', Float, nullable=False),
        Column('has_images', Boolean, nullable=False),
        Column('has_surf_features', Boolean, nullable=False),
        Column('surf_min_hessian', Integer, nullable=True),
        Column('has_fast_features', Boolean, nullable=False, server_default='0'),
        Column('fast_threshold', Float, nullable=True),
        Column('fast_nonmax_suppression', Boolean, nullable=True),
        Column('fast_type', Integer, nullable=True)
    )
    orm_registry.map_imperatively(
        MapLayer, map_layers_table,
        properties={
            '_zoom': map_layers_table.c.zoom,
            '_has_images': map_layers_table.c.has_images,
            '_has_surf_features': map_layers_table.c.has_surf_features,
            '_surf_min_hessian': map_layers_table.c.surf_min_hessian,
            '_has_fast_features': map_layers_table.c.has_fast_features,
            '_fast_threshold': map_layers_table.c.fast_threshold,
            '_fast_nonmax_suppression': map_layers_table.c.fast_nonmax_suppression,
            '_tiles': relationship(MapTile, uselist=True, cascade='all'),
        }
    )

    map_tiles_table = Table(
        'map_tiles', orm_registry.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('center_lat', Float, nullable=False),
        Column('center_long', Float, nullable=False),
        Column('nw_lat', Float, nullable=False),
        Column('nw_long', Float, nullable=False),
        Column('ne_lat', Float, nullable=False),
        Column('ne_long', Float, nullable=False),
        Column('se_lat', Float, nullable=False),
        Column('se_long', Float, nullable=False),
        Column('sw_lat', Float, nullable=False),
        Column('sw_long', Float, nullable=False),
        Column('azimuth', Float, nullable=False),
        Column('map_layer_id', Integer,
               ForeignKey('map_layers.id', ondelete='CASCADE')),
        Column('img', NumpyArray, nullable=True),
        Column('img_width', Integer, nullable=False, server_default='0'),
        Column('img_height', Integer, nullable=False, server_default='0'),
        Column('surf_keypoints', SURFKeyPoints, nullable=True),
        Column('surf_descriptors', NumpyArray, nullable=True),
        Column('fast_keypoints', NumpyArray, nullable=True),
        Index('idx_map_layer_id', 'map_layer_id', unique=False),
        Index('idx_coordinates', 'center_lat', 'center_long', unique=False)
    )
    orm_registry.map_imperatively(
        MapTile, map_tiles_table,
        properties={
            'surf_features': composite(
                TileSURFFeatures,
                map_tiles_table.c.surf_keypoints,
                map_tiles_table.c.surf_descriptors,
                default=None
            )
        }
    )

    