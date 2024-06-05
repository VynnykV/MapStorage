from dataclasses import dataclass
from typing import List, Tuple
from geopy.distance import geodesic
from pydantic import BaseModel
import numpy as np

from map_storage.features.shared.models.coordinates import Coordinates
from .command import RectangleProfileArgs, PolylineProfileArgs, ImportProfileType

@dataclass
class MapTilesGrid:
    tiles_width_px: int
    tiles_height_px: int
    tiles_coordinates: List[Tuple[Coordinates, Coordinates, Coordinates, Coordinates, Coordinates]]


def build_tiles_grid(
        zoom_m_per_px: float,
        max_tile_size_px: float,
        import_profile_type: ImportProfileType,
        import_profile_args: BaseModel
) -> MapTilesGrid:
    if import_profile_type == ImportProfileType.RECTANGLE:
        return build_rectangle_area_grid(
            RectangleProfileArgs(**import_profile_args.model_dump()),
            zoom_m_per_px, max_tile_size_px
        )
    if import_profile_type == ImportProfileType.POLYLINE:
        return build_polyline_area_grid(
            PolylineProfileArgs(**import_profile_args.model_dump()),
            zoom_m_per_px, max_tile_size_px
        )
    raise NotImplementedError()

def build_rectangle_area_grid(
        rectangle_profile: RectangleProfileArgs,
        zoom_m_per_px: float,
        max_tile_size_px: float) -> MapTilesGrid:
    start, end = rectangle_profile.start, rectangle_profile.end

    if start.latitude == end.latitude or start.longitude == end.longitude:
        raise Exception('start and end points must lie on different latitude and longitude')

    if start.latitude < end.latitude:
        start.latitude, end.latitude = end.latitude, start.latitude

    if start.longitude > end.longitude:
        start.longitude, end.longitude = end.longitude, start.longitude

    lat_size_m = geodesic(tuple(start), (end.latitude, start.longitude)).meters
    long_size_m = geodesic(tuple(start), (start.latitude, end.longitude)).meters

    max_tile_size_m = max_tile_size_px * zoom_m_per_px

    lat_cells = int(lat_size_m // max_tile_size_m) + 1
    long_cells = int(long_size_m // max_tile_size_m) + 1

    lat_step_degrees = (end.latitude - start.latitude) / lat_cells
    long_step_degrees = (end.longitude - start.longitude) / long_cells

    tile_size_pxs = (int(long_size_m / zoom_m_per_px / long_cells),
                     int(lat_size_m / zoom_m_per_px / lat_cells))

    tiles_coordinates = [
        (Coordinates(northern_lat + lat_step_degrees / 2, western_long + long_step_degrees / 2),
         Coordinates(northern_lat, western_long),
         Coordinates(northern_lat, western_long + long_step_degrees),
         Coordinates(northern_lat + lat_step_degrees, western_long + long_step_degrees),
         Coordinates(northern_lat + lat_step_degrees, western_long))
         for northern_lat in [start.latitude + lat_step_degrees * i for i in range(lat_cells)]
         for western_long in [start.longitude + long_step_degrees * i for i in range(long_cells)]
    ]

    return MapTilesGrid(tile_size_pxs[0], tile_size_pxs[1], tiles_coordinates)


def distance_to_line_segment(
        point_coordinates: Coordinates,
        line: Tuple[Coordinates, Coordinates]
) -> float:
    # Calculate distances from the point to each endpoint
    start, end = line[0].to_tuple(), line[1].to_tuple()
    point = point_coordinates.to_tuple()

    d_start = geodesic(point, start).meters
    d_end = geodesic(point, end).meters

    # Calculate vector representations of the segment and point
    segment_vector = np.array([end[0] - start[0], end[1] - start[1]])
    point_vector = np.array([point[0] - start[0], point[1] - start[1]])

    # Calculate the projection of the point onto the line segment
    projection = start + np.dot(point_vector, segment_vector) / np.dot(segment_vector, segment_vector) * segment_vector

    # Check if the projection falls within the bounds of the segment
    if 0 <= np.dot(projection - start, segment_vector) <= np.dot(segment_vector, segment_vector):
        # Calculate distance between the point and the projection
        d_projection = geodesic(point, (projection[0], projection[1])).meters
        return d_projection

    # If the projection is outside the segment bounds, return the distance to the nearest endpoint
    return min(d_start, d_end)


def tile_line_distance(
        tile_edges_coordinates: Tuple[Coordinates, Coordinates, Coordinates, Coordinates],
        line: Tuple[Coordinates, Coordinates]
) -> float:
    return min(distance_to_line_segment(p, line) for p in tile_edges_coordinates)


def build_polyline_area_grid(
        polyline_profile: PolylineProfileArgs,
        zoom_m_per_px: float,
        max_tile_size_px: float
) -> MapTilesGrid:
    # get rectangle grid that covers entire area
    start = Coordinates(
        latitude=min(polyline_profile.waypoints, key=lambda p: p.latitude).latitude,
        longitude=min(polyline_profile.waypoints, key=lambda p: p.longitude).longitude
    )
    end = Coordinates(
        latitude=max(polyline_profile.waypoints, key=lambda p: p.latitude).latitude,
        longitude=max(polyline_profile.waypoints, key=lambda p: p.longitude).longitude
    )

    rectangle_grid = build_rectangle_area_grid(
        RectangleProfileArgs(start=start, end=end),
        zoom_m_per_px, max_tile_size_px
    )

    line_segments = [(polyline_profile.waypoints[i], polyline_profile.waypoints[i+1])
             for i in range(len(polyline_profile.waypoints) - 1)]

    tile_size_px = (rectangle_grid.tiles_width_px, rectangle_grid.tiles_height_px)
    min_load_distance_m = max(tile_size_px) * zoom_m_per_px / 2
    load_distance_m = max(min_load_distance_m, polyline_profile.load_distance_m)

    result_coordinates = []
    for coords in rectangle_grid.tiles_coordinates:
        if any(tile_line_distance(coords[1:5], l) < load_distance_m
                for l in line_segments):
            result_coordinates.append(coords)

    return MapTilesGrid(
        tiles_width_px=rectangle_grid.tiles_width_px,
        tiles_height_px=rectangle_grid.tiles_height_px,
        tiles_coordinates=result_coordinates
    )
