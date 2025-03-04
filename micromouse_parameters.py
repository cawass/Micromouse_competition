import math

class Micromouse:
    def __init__(self, wheel_diameter: float):
        """
        Initialize the Micromuse characteristics.
        :param wheel_diameter: Diameter of the wheel in meters.
        """
        self.wheel_diameter = wheel_diameter
        self.wheel_circumference = math.pi * wheel_diameter  # Compute circumference