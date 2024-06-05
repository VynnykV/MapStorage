from dataclasses import dataclass
from typing import List, Optional

from map_storage.features.map_layers.models.map_tile import MapTile


@dataclass
class MapLayer:
    id: int = None

    def __init__(self,
                 name: str,
                 zoom: float,
                 import_type: str,
                 has_images: bool,
                 has_surf_features: bool,
                 has_fast_features: bool,
                 surf_min_hessian: Optional[int] = None,
                 fast_threshold: Optional[float] = None,
                 fast_nonmax_suppression: Optional[bool] = None,
                 fast_type: Optional[int] = None,
                 description: Optional[str] = None):
        self._tiles: List[MapTile] = []
        self.name = name
        self.import_type = import_type
        self.description = description
        self._zoom = zoom
        self._has_images = has_images
        self._has_surf_features = has_surf_features
        self._surf_min_hessian = surf_min_hessian
        self._has_fast_features = has_fast_features
        self._fast_threshold = fast_threshold
        self._fast_nonmax_suppression = fast_nonmax_suppression
        self._fast_type = fast_type

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def has_images(self) -> bool:
        return self._has_images

    @property
    def has_surf_features(self) -> bool:
        return self._has_surf_features

    @property
    def surf_min_hessian(self) -> int:
        return self._surf_min_hessian

    @property
    def has_fast_features(self) -> bool:
        return self._has_fast_features

    @property
    def tiles(self) -> List[MapTile]:
        return self._tiles
    
    def add_tile(self, tile: MapTile):
        if self._has_images and tile.img is None:
            raise ValueError('MapTile.img expected but not provided.')

        if not self._has_images and tile.img is not None:
            raise ValueError("MapTile.img provided when none is expected.")

        if self._has_surf_features and not bool(tile.surf_features):
            raise ValueError('MapTile.surf_features expected but not provided.')

        if not self._has_surf_features and bool(tile.surf_features):
            raise ValueError("MapTile.surf_features provided when none is expected.")

        if self._has_fast_features and tile.fast_keypoints is None:
            raise ValueError('MapTile.fast_keypoints expected but not provided')

        if not self._has_fast_features and tile.fast_keypoints is not None:
            raise ValueError('MapTile.fast_keypoints provided but none is expected')

        tile.map_layer_id = self.id

        self._tiles.append(tile)
