from pydantic import BaseModel, conint

from map_storage.features.map_layers.models.map_layer import MapLayer
from map_storage.features.shared.contracts.repository import Repository
from map_storage.features.shared.exceptions import NotFoundException


class DeleteMapLayerCommand(BaseModel):
    id: conint(ge=1)


class DeleteMapLayerCommandHandler:
    def __init__(self, map_layer_repo: Repository[MapLayer]):
        self.map_layer_repo = map_layer_repo

    async def __call__(self, command: DeleteMapLayerCommand):
        map_layer = await self.map_layer_repo.get(command.id)

        if map_layer is None:
            raise NotFoundException()

        await self.map_layer_repo.delete(map_layer)
