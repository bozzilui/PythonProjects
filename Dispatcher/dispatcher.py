"""Dispatcher for the simulation"""

from typing import Optional, List
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    drivers: List[Driver]
    waiting_list: list

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """

        self.drivers = []

        self.waiting_list = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return "Dispatcher ({} Drivers)".format(len(self.drivers))

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        """

        if len(self.drivers) == 0:
            self.waiting_list.append(rider)
            return None

        fastest = self.drivers[0]

        for driver in self.drivers:
            if driver.is_idle is True:
                curr = driver.get_travel_time(rider.origin)
                if curr < fastest.get_travel_time(rider.origin):
                    fastest = driver
        return fastest

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        """

        if driver not in self.drivers:
            self.drivers.append(driver)
        if len(self.waiting_list) == 0:
            return None

        rider = self.waiting_list[0]

        self.waiting_list.remove(self.waiting_list[0])
        return rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        """
        if rider in self.waiting_list:
            self.waiting_list.remove(rider)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
