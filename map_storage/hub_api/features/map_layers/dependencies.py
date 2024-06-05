from fastapi import Request

from hub_api import map_storage_hub_config
from map_storage.features.map_layers.application.commands.delete_map_layer import *
from map_storage.features.map_layers.application.commands.import_map_layer import *
from map_storage.features.map_layers.application.queries.list_map_layer_tiles import MapLayerDetailsQueryHandler
from map_storage.features.map_layers.application.queries.list_map_layers import ListMapLayersQueryHandler
from map_storage.infra.db.repository import SqlAlchemyRepository
from map_storage.infra.map_providers.google_maps_provider import GoogleMapsProvider
from map_storage.features.import_profiles.models.import_profile import ImportProfile


def map_layer_details(request: Request) -> MapLayerDetailsQueryHandler:
    return MapLayerDetailsQueryHandler(request.state.db)


def list_map_layers_handler(request: Request) -> ListMapLayersQueryHandler:
    return ListMapLayersQueryHandler(request.state.db)


def delete_map_layer_handler(request: Request) -> DeleteMapLayerCommandHandler:
    return DeleteMapLayerCommandHandler(
        SqlAlchemyRepository(request.state.db, MapLayer)
    )


def import_map_layer_handler(request: Request) -> ImportMapLayerHandler:
    return ImportMapLayerHandler(
        request.state.db,
        SqlAlchemyRepository(request.state.db, ImportProfile),
        SqlAlchemyRepository(request.state.db, MapLayer),
        GoogleMapsProvider(map_storage_hub_config('hub_api/.env').googlemaps_api_key)
    )
