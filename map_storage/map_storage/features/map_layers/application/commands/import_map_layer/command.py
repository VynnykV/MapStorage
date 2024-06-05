from enum import Enum
from pydantic import BaseModel, conint, constr, confloat
from typing import Optional, List

from map_storage.features.shared.models.coordinates import Coordinates


class ImportProfileType(str, Enum):
    POLYLINE = 'polyline'
    RECTANGLE = 'rectangle'


class RectangleProfileArgs(BaseModel):
    start: Coordinates
    end: Coordinates


class PolylineProfileArgs(BaseModel):
    waypoints: List[Coordinates]
    load_distance_m: confloat(ge=20) = 20


class SURFAction(BaseModel):
    hessianThreshold: conint(ge=1)


class FASTAction(BaseModel):
    threshold: conint(ge=0)
    nonmaxSuppression: bool
    type: Optional[conint(ge=0)] = None


class ImportActions(BaseModel):
    save_img: bool = True
    compute_surf: Optional[SURFAction] = None
    compute_fast: Optional[FASTAction] = None


class ImportMapLayerCommand(BaseModel):
    import_profile_type: ImportProfileType
    import_profile_args: PolylineProfileArgs|RectangleProfileArgs
    layer_name: constr(min_length=1, max_length=50)
    zoom_lvl: float
    actions: ImportActions
    description: Optional[constr(max_length=200)] = None