from pydantic import BaseModel, conint

from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.features.shared.contracts.repository import Repository
from map_storage.features.shared.exceptions import NotFoundException


class DeleteImportProfileCommand(BaseModel):
    id: conint(ge=1)


class DeleteImportProfileCommandHandler:
    def __init__(self, import_profile_repo: Repository[ImportProfile]):
        self.import_profile_repo = import_profile_repo

    async def __call__(self, command: DeleteImportProfileCommand):
        import_profile = await self.import_profile_repo.get(command.id)

        if import_profile is None:
            raise NotFoundException()

        await self.import_profile_repo.delete(import_profile)
