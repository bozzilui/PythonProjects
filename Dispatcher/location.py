"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location."""

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.

        """
        # TODO
        self.m = row
        self.n = column

    def __str__(self) -> str:
        """Return a string representation.

        """
        # TODO
        m = self.m
        n = self.n
        return m.__str__() + ',' + n.__str__()

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        # TODO
        return self.n == other.n and self.m == other.m


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.

    """
    # TODO
    distx = abs(destination.m - origin.m)
    disty = abs(destination.n - origin.n)
    return distx + disty


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'
    """
    # TODO
    row = location_str[0]
    col = location_str[2]
    location = Location(int(row), int(col))
    return location


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
