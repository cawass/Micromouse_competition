import math

class PositionTracker:
    def __init__(self, wheel_diameter):
        self.wheel_circumference = math.pi * wheel_diameter
        self.prev_angle = 0
        self.total_distance = 0
        self._calibration_offset = 0
        
    def calibrate(self, current_angle):
        self._calibration_offset = current_angle
        
    def update(self, current_angle, delta_time):
        # Handle angle wrapping
        current_angle = self._unwrap_angle(self.prev_angle, current_angle)
        
        # Convert to radians and calculate delta
        delta_rad = math.radians((current_angle - self.prev_angle) / self._calibration_offset)
        
        # Calculate distance
        distance = (delta_rad / (2 * math.pi)) * self.wheel_circumference
        self.total_distance += abs(distance)
        
        # Calculate speed
        speed = distance / delta_time if delta_time > 0 else 0
        
        self.prev_angle = current_angle
        return speed, self.total_distance
        
    def _unwrap_angle(self, prev, curr):
        diff = curr - prev
        if diff > 2048:  # Handle 12-bit wrap-around
            curr -= 4096
        elif diff < -2048:
            curr += 4096
        return curr