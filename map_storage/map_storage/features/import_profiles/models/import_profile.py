from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .rectangle_import_profile import RectangleImportProfile


class ImportProfileTypeId(str, Enum):
    rectangle = 'rect'


@dataclass
class ImportProfile:
    name: str
    description: str
    _rectangle_import_profile: Optional[RectangleImportProfile] = None
    id: int = None
    type: ImportProfileTypeId = None

    @property
    def rectangle_import_profile(self) -> Optional[RectangleImportProfile]:
        return self._rectangle_import_profile

    def is_rectangle(self) -> bool:
        return self.type == ImportProfileTypeId.rectangle

    def set_rectangle_profile(self, profile: RectangleImportProfile):
        self.type = ImportProfileTypeId.rectangle
        self._rectangle_import_profile = profile
