from typing import Callable, Any

from fastapi import FastAPI, APIRouter, Depends

import hub_api.features.import_profiles.dependencies as dep
from map_storage.features.import_profiles.application.commands.create_rectangle_import_profile import *
from map_storage.features.import_profiles.application.commands.delete_import_profile import *
from map_storage.features.import_profiles.application.commands.edit_import_profile_details import *
from map_storage.features.import_profiles.application.queries.get_import_profile_details import *
from map_storage.features.import_profiles.application.queries.list_import_profiles import *


def add_import_profiles_router(app: FastAPI):
    router = APIRouter(prefix="/importProfiles", tags=["import_profiles"])

    @router.post("/rectangle")
    async def create_import_profile(
            request: CreateRectangleImportProfileCommand,
            handler: Callable[[CreateRectangleImportProfileCommand], Any]
            = Depends(dep.create_rectangle_import_profile_handler)):
        return await handler(request)

    @router.delete("/{import_profile_id}")
    async def delete_import_profile(
            import_profile_id: int,
            handler: Callable[[DeleteImportProfileCommand], Any]
            = Depends(dep.delete_import_profile_handler)):
        request = DeleteImportProfileCommand(id=import_profile_id)
        return await handler(request)

    @router.put("/")
    async def edit_import_profile(
            request: EditImportProfileDetailsCommand,
            handler: Callable[[EditImportProfileDetailsCommand], Any]
            = Depends(dep.edit_import_profile_details_handler)):
        return await handler(request)

    @router.get(
        "/{import_profile_id}",
        response_model=GetImportProfileDetailsResponse)
    async def get_import_profile_details(
            import_profile_id: int,
            handler: Callable[[GetImportProfileDetailsQuery], GetImportProfileDetailsResponse]
            = Depends(dep.get_import_profile_details_handler)):
        request = GetImportProfileDetailsQuery(id=import_profile_id)
        return await handler(request)

    @router.get(
        "/",
        response_model=ListImportProfilesResponse)
    async def list_import_profiles(
            request: ListImportProfilesQuery = Depends(),
            handler: Callable[[ListImportProfilesQuery], ListImportProfilesResponse]
            = Depends(dep.list_import_profiles_handler)):
        return await handler(request)

    app.include_router(router)
