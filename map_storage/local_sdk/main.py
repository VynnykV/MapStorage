import asyncio
import cv2
from map_storage import MapStorageSDK
from config import local_map_storage_config

async def main():
    cfg = local_map_storage_config()
    sdk = MapStorageSDK(cfg.db_url)

    res = await sdk.tiles_overlapping_with_square(
        layers_ids=[6],
        square_center=(33.031680, -117.169785),
        square_size_m=50,
        offset=0, limit=9,
        select_img=True, select_surf=False, select_fast=True
    )

    for tile in res:
        cv2.imwrite(f'{tile.latitude},{tile.longitude}.png', tile.img)


if __name__ == "__main__":
    asyncio.run(main())
