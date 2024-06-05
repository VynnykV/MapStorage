from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from map_storage.features.import_profiles.models.import_profile import ImportProfile


class ListImportProfilesQuery:
    pass


class ListImportProfile(BaseModel):
    id: int
    name: str
    type: str


class ListImportProfilesResponse(BaseModel):
    import_profiles: List[ListImportProfile]


class ListImportProfilesQueryHandler:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self,
                       request: ListImportProfilesQuery) -> ListImportProfilesResponse:
        query = select(ImportProfile)
        import_profiles = (await self._db.scalars(query)).all()

        return ListImportProfilesResponse(
            import_profiles=[ListImportProfile(id=p.id, name=p.name, type=p.type)
                             for p in import_profiles]
        )
