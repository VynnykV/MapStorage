from dataclasses import dataclass
from typing import Tuple

@dataclass
class CoordinatesDelta:
    lat_diff: float = 0
    long_diff: float = 0


@dataclass
class Coordinates:
    latitude: float = 0
    longitude: float = 0

    def __composite_values__(self):
        return self.latitude, self.longitude

    def __repr__(self):
        return f"({self.latitude!r}, {self.longitude!r})"

    def __eq__(self, other):
        return isinstance(other, Coordinates) and other.latitude == self.latitude and other.longitude == self.longitude

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other) -> CoordinatesDelta:
        if not isinstance(other, Coordinates):
            raise ValueError('Second operand must be Coordinates type')

        return CoordinatesDelta(
            lat_diff=self.latitude - other.latitude,
            long_diff=self.longitude - other.longitude
        )

    def __iter__(self):
        return iter((self.latitude, self.longitude))

    def to_tuple(self) -> Tuple[float, float]:
        return self.latitude, self.longitude
