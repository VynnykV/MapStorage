from dataclasses import dataclass
from typing import Protocol, Optional

import numpy as np

from map_storage.features.shared.models.coordinates import Coordinates


@dataclass
class GetTileResult:
    error: Optional[str] = None
    img: Optional[np.ndarray] = None


class MapProvider(Protocol):
    async def load_tile(self,
                        center: Coordinates,
                        zoom: float,
                        with_px: int, height_px: int) -> GetTileResult:
        ...

    @staticmethod
    def zoom_lvl_to_meters_per_px(zoom_lvl: float) -> float:
        ...

    @staticmethod
    def max_tile_size_px() -> int:
        ...
