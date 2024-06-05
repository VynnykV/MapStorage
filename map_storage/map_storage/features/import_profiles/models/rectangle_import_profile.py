from dataclasses import dataclass, field

from map_storage.features.shared.models.coordinates import Coordinates


@dataclass
class RectangleImportProfile:
    import_profile_id: int = None
    start: Coordinates = field(default_factory=Coordinates)
    end: Coordinates = field(default_factory=Coordinates)
