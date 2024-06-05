from fastapi import Request

from map_storage.features.import_profiles.application.commands.create_rectangle_import_profile import *
from map_storage.features.import_profiles.application.commands.delete_import_profile import *
from map_storage.features.import_profiles.application.commands.edit_import_profile_details import *
from map_storage.features.import_profiles.application.queries.get_import_profile_details import *
from map_storage.features.import_profiles.application.queries.list_import_profiles import *
from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.infra.db.repository import SqlAlchemyRepository


def create_rectangle_import_profile_handler(request: Request) -> CreateRectangleImportProfileHandler:
    return CreateRectangleImportProfileHandler(
        SqlAlchemyRepository(request.state.db, ImportProfile)
    )


def delete_import_profile_handler(request: Request) -> DeleteImportProfileCommandHandler:
    return DeleteImportProfileCommandHandler(
        SqlAlchemyRepository(request.state.db, ImportProfile)
    )


def edit_import_profile_details_handler(request: Request) -> EditImportProfileDetailsHandler:
    return EditImportProfileDetailsHandler(
        SqlAlchemyRepository(request.state.db, ImportProfile)
    )


def get_import_profile_details_handler(request: Request) -> GetImportProfileDetailsQueryHandler:
    return GetImportProfileDetailsQueryHandler(request.state.db)


def list_import_profiles_handler(request: Request) -> ListImportProfilesQueryHandler:
    return ListImportProfilesQueryHandler(request.state.db)

