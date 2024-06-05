from typing import Optional

from pydantic import BaseModel, constr

from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.features.import_profiles.models.rectangle_import_profile import RectangleImportProfile
from map_storage.features.shared.contracts.repository import Repository
from map_storage.features.shared.models.coordinates import Coordinates


class CreateRectangleImportProfileCommand(BaseModel):
    name: constr(min_length=1, max_length=50)
    start: Coordinates
    end: Coordinates
    description: Optional[constr(min_length=1, max_length=200)] = None


class CreateRectangleImportProfileHandler:
    def __init__(self, import_profile_repo: Repository[ImportProfile]):
        self.import_profile_repo = import_profile_repo

    async def __call__(self, command: CreateRectangleImportProfileCommand):
        import_profile = ImportProfile(name=command.name, description=command.description)
        import_profile.set_rectangle_profile(
            RectangleImportProfile(start=command.start, end=command.end)
        )
        self.import_profile_repo.add(import_profile)
