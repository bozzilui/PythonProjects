"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""
from location import Location


WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    """A rider for a ride-sharing service.

    """
    id: str
    patience: int
    origin: Location
    destination: Location
    status: str
    curr_wait: int

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Rider.

        """

        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING
        self.curr_wait = 0

    def __str__(self) -> str:
        """Return a string representation.

        """
        return self.id

    def __eq__(self, other: object) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        s_id = self.id
        o_id = other.id

        return s_id == o_id


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['location']})
