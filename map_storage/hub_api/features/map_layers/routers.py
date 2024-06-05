from typing import Callable, Any

from fastapi import FastAPI, APIRouter, Depends

import hub_api.features.map_layers.dependencies as dep
from map_storage.features.map_layers.application.commands.delete_map_layer import DeleteMapLayerCommand
from map_storage.features.map_layers.application.commands.import_map_layer import ImportMapLayerCommand
from map_storage.features.map_layers.application.commands.import_map_layer.response import ImportMapLayerResponse
from map_storage.features.map_layers.application.queries.list_map_layer_tiles import MapLayerDetailsQuery, \
    MapLayerDetailsResponse
from map_storage.features.map_layers.application.queries.list_map_layers import ListMapLayersResponse, \
    ListMapLayersQuery


def add_map_layers_router(app: FastAPI):
    router = APIRouter(prefix="/mapLayers", tags=["map_layers"])

    @router.get(
        "/",
        response_model=ListMapLayersResponse)
    async def list_map_layers(
            request: ListMapLayersQuery = Depends(),
            handler: Callable[[ListMapLayersQuery], ListMapLayersResponse]
            = Depends(dep.list_map_layers_handler)):
        return await handler(request)

    @router.get(
        "/{map_layer_id}",
        response_model=MapLayerDetailsResponse)
    async def map_layer_details(
            map_layer_id: int,
            handler: Callable[[MapLayerDetailsQuery], MapLayerDetailsResponse]
            = Depends(dep.map_layer_details)):
        request = MapLayerDetailsQuery(id=map_layer_id)
        return await handler(request)

    @router.delete("/{map_layer_id}")
    async def delete_map_layer(
            map_layer_id: int,
            handler: Callable[[DeleteMapLayerCommand], Any]
            = Depends(dep.delete_map_layer_handler)):
        request = DeleteMapLayerCommand(id=map_layer_id)
        return await handler(request)

    @router.post("/import", response_model=ImportMapLayerResponse)
    async def import_map_layer(
            request: ImportMapLayerCommand,
            handler: Callable[[ImportMapLayerCommand], ImportMapLayerResponse]
            = Depends(dep.import_map_layer_handler)):
        return await handler(request)

    app.include_router(router)
