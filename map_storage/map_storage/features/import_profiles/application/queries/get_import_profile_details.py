from typing import Optional
from pydantic import BaseModel, conint
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.features.shared.models.coordinates import Coordinates
from map_storage.features.shared.queries import FilteredQuery


class GetImportProfileDetailsQuery(FilteredQuery):
    id: conint(ge=1)

    def filter_by(self, select_expression: Select) -> Select:
        return select_expression.where(ImportProfile.id == self.id)


class RectangleImportProfile(BaseModel):
    start: Coordinates
    end: Coordinates


class GetImportProfileDetailsResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    shape: RectangleImportProfile


class GetImportProfileDetailsQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self,
                       query: GetImportProfileDetailsQuery) -> GetImportProfileDetailsResponse:
        db_query = query.db_query(ImportProfile)

        db_query.options(
            joinedload(ImportProfile._rectangle_import_profile)
        )

        res: ImportProfile = (await self._db.execute(db_query)).scalar_one()

        return GetImportProfileDetailsResponse(
            id=res.id,
            name=res.name,
            type=res.type,
            description=res.description,
            shape=RectangleImportProfile(
                start=res.rectangle_import_profile.start,
                end=res.rectangle_import_profile.end
            )
        )
