import math

class DistanceDeterminator:
    def __init__(self, micromouse):
        """
        Initialize the DistanceDeterminator with a Micromouse instance.
        :param micromouse: An instance of the Micromouse class.
        """
        self.micromouse = micromouse
        self.previous_angle = 0
        self.total_distance = 0
        self.speed = 0
        self.calibrated_offset = 0

        # Store previous values for interpolation
        self.prev_measurement = {'speed': 0, 'total_distance': 0, 'angle': 0}

    def calibrate(self, initial_angle: float):
        """
        Calibrate the sensor by setting the initial angle as zero.
        :param initial_angle: The starting angle of the sensor in degrees.
        """
        self.calibrated_offset = initial_angle
        self.previous_angle = initial_angle
        self.total_distance = 0
        print("Calibration complete. Initial angle set to 0.")

    def unwrap_angle(self, prev_angle, curr_angle):
        """Adjust curr_angle so that the difference from prev_angle is minimal."""
        diff = curr_angle - prev_angle
        if diff > 180:
            curr_angle -= 360
        elif diff < -180:
            curr_angle += 360
        return curr_angle

    def interpolate_value(self, prev, curr, factor, is_angle=False):
        """
        Linearly interpolate between prev and curr.
        If is_angle is True, unwrap the angle to avoid discontinuities.
        'factor' should be between 0 (prev) and 1 (curr).
        """
        if is_angle:
            curr = self.unwrap_angle(prev, curr)
        return prev + factor * (curr - prev)

    def update(self, current_angle: float, time_interval: float, interpolation_factor=0.5):
        """
        Update the distance and speed based on the change in angle.
        :param current_angle: The new angle reading in degrees.
        :param time_interval: Time interval in seconds between readings.
        :param interpolation_factor: Factor (0 to 1) for interpolation.
        :return: speed (m/s), distance_travelled (m)
        """
        # Adjust for calibration offset
        adjusted_angle = current_angle - self.calibrated_offset
        previous_adjusted_angle = self.previous_angle - self.calibrated_offset
        
        # Compute angular displacement (in radians)
        angle_change = math.radians(adjusted_angle - previous_adjusted_angle)
        
        # Compute linear displacement
        distance_travelled = (angle_change / (2 * math.pi)) * self.micromouse.wheel_circumference
        self.total_distance += abs(distance_travelled)
        
        # Compute speed
        self.speed = abs(distance_travelled) / time_interval if time_interval > 0 else 0

        # Store current values
        current_measurement = {
            'speed': self.speed,
            'total_distance': self.total_distance,
            'angle': adjusted_angle
        }

        # Interpolate measurements
        interp_speed = self.interpolate_value(self.prev_measurement['speed'], current_measurement['speed'], interpolation_factor)
        interp_distance = self.interpolate_value(self.prev_measurement['total_distance'], current_measurement['total_distance'], interpolation_factor)
        interp_angle = self.interpolate_value(self.prev_measurement['angle'], current_measurement['angle'], interpolation_factor, is_angle=True)

        # Store interpolated values as the previous measurement for the next update
        self.prev_measurement = current_measurement

        # Store the current angle for the next update
        self.previous_angle = current_angle

        return interp_speed, interp_distance, interp_angle

