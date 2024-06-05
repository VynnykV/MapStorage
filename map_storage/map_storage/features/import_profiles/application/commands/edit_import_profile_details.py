from pydantic import BaseModel, conint, constr

from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.features.shared.contracts.repository import Repository
from map_storage.features.shared.exceptions import NotFoundException


class EditImportProfileDetailsCommand(BaseModel):
    import_profile_id: conint(ge=1)
    name: constr(min_length=1, max_length=50)


class EditImportProfileDetailsHandler:
    def __init__(self, import_profile_repo: Repository[ImportProfile]):
        self.import_profile_repo = import_profile_repo
    
    async def __call__(self, command: EditImportProfileDetailsCommand):
        import_profile = await self.import_profile_repo.get(command.import_profile_id)

        if import_profile is None:
            raise NotFoundException()

        import_profile.name = command.name
