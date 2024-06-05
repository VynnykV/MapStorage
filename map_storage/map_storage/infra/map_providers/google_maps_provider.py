from typing import List

import cv2
import numpy as np
from pydantic import confloat, conint

import map_storage.infra as infra
from map_storage.features.shared.contracts.map_provider import GetTileResult
from map_storage.features.shared.models.coordinates import Coordinates


_zoom_lvl_table: List[float] = [
    156543.03392,
    78271.51696,
    39135.75848,
    19567.87924,
    9783.93962,
    4891.96981,
    2445.98490,
    1222.99245,
    611.49622,
    305.74811,
    152.87405,
    76.43702,
    38.21851,
    19.10925,
    9.55462,
    4.77731,
    2.38865,
    1.19432,
    0.59716,
    0.2435625,
    0.12453125
]

_googlemaps_api_url = 'https://maps.googleapis.com/maps/api/staticmap'

class GoogleMapsProvider:
    def __init__(self, googlemaps_api_key: str):
        self._api_key = googlemaps_api_key

    async def load_tile(self,
                        center: Coordinates,
                        zoom: confloat(ge=0, le=20),
                        with_px: conint(gt=10), height_px: conint(gt=10)) -> GetTileResult:

        params = {
            'center': f'{center.latitude}, {center.longitude}',
            'zoom': round(zoom),
            'size': f'{with_px}x{height_px}',
            'maptype': 'satellite',
            'key': self._api_key
        }

        async with infra.http_session.get(_googlemaps_api_url, params=params) as res:
            res_bytes = await res.read()

            if res.status != 200:
                return GetTileResult(error=res_bytes.decode())

            if len(res_bytes) == 0:
                return GetTileResult(error='Google map_layers fastapi returned empty response body')

            image_array = np.frombuffer(res_bytes, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return GetTileResult(img=img)

    @staticmethod
    def zoom_lvl_to_meters_per_px(zoom_lvl: float) -> float:
        return _zoom_lvl_table[int(zoom_lvl)]

    @staticmethod
    def max_tile_size_px() -> int:
        return 640
