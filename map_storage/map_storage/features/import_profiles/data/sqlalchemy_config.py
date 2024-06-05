from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import registry, composite, relationship

from map_storage.features.import_profiles.models.import_profile import *
from map_storage.features.shared.models.coordinates import Coordinates


def configure_import_profiles_orm(orm_registry: registry):

    import_profiles_table = Table(
        'import_profiles', orm_registry.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('type', String(20), nullable=False),
        Column('name', String(50), nullable=False),
        Column('description', String(200), nullable=True)
    )
    orm_registry.map_imperatively(
        ImportProfile, import_profiles_table,
        properties={
            '_rectangle_import_profile': relationship(
                RectangleImportProfile, uselist=False, cascade='all', lazy='joined'),
        }
    )

    rectangle_import_profiles_table = Table(
        'rectangle_import_profiles', orm_registry.metadata,
        Column('import_profile_id', Integer,
               ForeignKey('import_profiles.id', ondelete='CASCADE'), primary_key=True),
        Column('start_lat', Float, nullable=False),
        Column('start_long', Float, nullable=False),
        Column('end_lat', Float, nullable=False),
        Column('end_long', Float, nullable=False)
    )
    orm_registry.map_imperatively(
        RectangleImportProfile, rectangle_import_profiles_table,
        properties={
            'start': composite(
                Coordinates,
                rectangle_import_profiles_table.c.start_lat,
                rectangle_import_profiles_table.c.start_long
            ),
            'end': composite(
                Coordinates,
                rectangle_import_profiles_table.c.end_lat,
                rectangle_import_profiles_table.c.end_long
            )
        }
    )
