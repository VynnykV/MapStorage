from typing import List

from pydantic import BaseModel

from map_storage.features.shared.models.coordinates import Coordinates


class AntColonyOptimizationCommand(BaseModel):
    polyline_points: List[Coordinates]
