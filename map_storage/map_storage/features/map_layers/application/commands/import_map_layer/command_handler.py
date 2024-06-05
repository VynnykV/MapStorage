import cv2
from sqlalchemy.ext.asyncio import AsyncSession

from map_storage.features.import_profiles.models.import_profile import ImportProfile
from map_storage.features.map_layers.models.map_layer import MapLayer
from map_storage.features.map_layers.models.map_tile import MapTile, TileSURFFeatures
from map_storage.features.shared.contracts.map_provider import MapProvider
from map_storage.features.shared.contracts.repository import Repository
from map_storage.features.shared.exceptions import MapProviderException, MapStorageException

from .features_detection import canny_hough_detect
from .command import ImportMapLayerCommand
from .map_tiles_grids import build_tiles_grid
from .response import ImportMapLayerResponse

class ImportMapLayerHandler:
    def __init__(self,
                 db: AsyncSession,
                 import_profile_repo: Repository[ImportProfile],
                 map_layer_repo: Repository[MapLayer],
                 map_provider: MapProvider):
        self._db = db
        self.import_profile_repo = import_profile_repo
        self.map_layer_repo = map_layer_repo
        self.map_provider = map_provider

    async def __call__(self, command: ImportMapLayerCommand):
        is_layer_name_exist = await self.map_layer_repo.any([MapLayer.name == command.layer_name])
        if is_layer_name_exist:
            raise MapStorageException("map layer with same name already exist")

        map_layer = MapLayer(
            name=command.layer_name,
            description=command.description,
            import_type=command.import_profile_type,
            zoom=command.zoom_lvl,
            has_surf_features=command.actions.compute_surf is not None,
            has_fast_features=command.actions.compute_fast is not None,
            has_images=command.actions.save_img
        )

        if map_layer.has_surf_features:
            map_layer._surf_min_hessian = command.actions.compute_surf.hessianThreshold

        if map_layer.has_fast_features:
            map_layer._fast_threshold = command.actions.compute_fast.threshold
            map_layer._fast_nonmax_suppression = command.actions.compute_fast.nonmaxSuppression
            map_layer._fast_type = command.actions.compute_fast.type

        zoom_m_per_px = (self.map_provider
                         .zoom_lvl_to_meters_per_px(command.zoom_lvl))

        tiles_grid = build_tiles_grid(
            zoom_m_per_px,
            self.map_provider.max_tile_size_px(),
            command.import_profile_type,
            command.import_profile_args
        )

        surf =cv2.xfeatures2d.SURF_create()
        if command.actions.compute_surf:
            surf = cv2.xfeatures2d.SURF_create(**dict(command.actions.compute_surf))

        fast = cv2.FastFeatureDetector_create()
        if command.actions.compute_fast:
            fast = cv2.FastFeatureDetector_create(
                threshold=command.actions.compute_fast.threshold,
                nonmaxSuppression=command.actions.compute_fast.nonmaxSuppression
            )

        for tile_coords in tiles_grid.tiles_coordinates:
            tile_res = await self.map_provider.load_tile(
                tile_coords[0], command.zoom_lvl,
                tiles_grid.tiles_width_px, tiles_grid.tiles_height_px
            )

            if tile_res.error:
                raise MapProviderException(tile_res.error)

            if tile_res.img is None:
                raise MapProviderException('Map provider returned no img')

            tile = MapTile(
                map_layer_id=map_layer.id,
                center_lat=tile_coords[0].latitude, center_long=tile_coords[0].longitude,
                nw_lat=tile_coords[1].latitude, nw_long=tile_coords[1].longitude,
                ne_lat=tile_coords[2].latitude, ne_long=tile_coords[2].longitude,
                se_lat=tile_coords[3].latitude, se_long=tile_coords[3].longitude,
                sw_lat=tile_coords[4].latitude, sw_long=tile_coords[4].longitude,
                azimuth=0,
            )
            tile.img_shape = tile_res.img.shape[:2]

            if command.actions.save_img:
                tile.img = tile_res.img

            img_gray = cv2.cvtColor(tile.img, cv2.COLOR_BGR2GRAY)

            if command.actions.compute_surf:
                keypoints, descriptors = surf.detectAndCompute(img_gray, None)
                tile.surf_features = TileSURFFeatures(keypoints, descriptors)

            if command.actions.compute_fast:
                kp_arr = canny_hough_detect(tile.img, 9, (300, 330), 30, 30, 5)
                tile.fast_keypoints = kp_arr

            map_layer.add_tile(tile)

        self.map_layer_repo.add(map_layer)
        await self._db.commit()
        await self._db.refresh(map_layer)
        return ImportMapLayerResponse(id=map_layer.id)
