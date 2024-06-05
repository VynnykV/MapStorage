from dataclasses import dataclass
from typing import Sequence, Any, Optional, Tuple

import cv2
import numpy as np


@dataclass
class TileSURFFeatures:
    keypoints: Sequence[cv2.KeyPoint]
    descriptors: np.ndarray[Any, np.dtype[np.generic]] | np.ndarray


@dataclass
class MapTile:
    center_lat: float
    center_long: float
    nw_lat: float
    nw_long: float
    ne_lat: float
    ne_long: float
    se_lat: float
    se_long: float
    sw_lat: float
    sw_long: float
    id: Optional[int] = None
    map_layer_id: int = 0
    azimuth: float = 0
    surf_features: Optional[TileSURFFeatures] = None
    fast_keypoints: Optional[np.ndarray] = None
    img: Optional[np.ndarray] = None
    img_height: int = 0
    img_width: int = 0

    @property
    def img_shape(self) -> Tuple[int, int]:
        return self.img_height, self.img_width

    @img_shape.setter
    def img_shape(self, value: Tuple[int, int]):
        if len(value) < 2:
            raise ValueError('width and height values expected')
        self.img_height, self.img_width = value
