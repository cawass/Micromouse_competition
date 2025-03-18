# motor_control.py
import time
from drivers.tb6612 import MotorDriver
import config
class MotorController:
    def __init__(self, motor_driver, mm_per_sec=700.0, turn_90_time=0.5, default_speed=60000):
        """
        Initialize the motor controller.
        :param motor_driver: Instance of tb6612.MotorDriver controlling the motors.
        :param mm_per_sec: Calibrated speed (mm per second) at default_speed PWM for straight motion.
        :param turn_90_time: Calibrated time (seconds) to turn 90 degrees in place.
        :param default_speed: Default PWM value for motor speed (0 to 65535 on ESP32).
        """
        self.driver = motor_driver
        self.mm_per_sec = mm_per_sec
        self.turn_90_time = turn_90_time
        self.default_speed = default_speed

    def move_forward(self, distance_mm, speed=None):
        """
        Move the robot straight for the given distance in millimeters.
        Positive distance moves forward, negative moves backward.
        """
        if speed is None:
            speed = self.default_speed
        # Calculate how long to run the motors to cover the distance (if using time-based control)
        if self.mm_per_sec > 0:
            duration = abs(distance_mm) / self.mm_per_sec  # time in seconds
        else:
            duration = 0  # if mm_per_sec is zero (no calibration), we would rely on encoder feedback instead
        # Set motor directions based on sign of distance
        if distance_mm >= 0:
            # forward
            self.driver.set_motor("left", speed)
            self.driver.set_motor("right", speed)
        else:
            # backward
            self.driver.set_motor("left", -speed)
            self.driver.set_motor("right", -speed)
        # Run for the calculated duration (blocking)
        time.sleep(duration)
        # Stop motors after moving
        self.driver.stop()

    def turn_left(self, angle_deg=90, speed=None):
        """
        Turn in place to the left by the specified angle (degrees).
        """
        if speed is None:
            speed = self.default_speed
        # Left turn: left motor backward, right motor forward
        self.driver.set_motor("left", -speed)
        self.driver.set_motor("right", speed)
        # Calculate turn duration proportionally to angle
        duration = (angle_deg / 90.0) * self.turn_90_time
        time.sleep(duration)
        self.driver.stop()

    def turn_right(self, angle_deg=90, speed=None):
        """
        Turn in place to the right by the specified angle (degrees).
        """
        if speed is None:
            speed = self.default_speed
        # Right turn: left motor forward, right motor backward
        self.driver.set_motor("left", speed)
        self.driver.set_motor("right", -speed)
        duration = (angle_deg / 90.0) * self.turn_90_time
        time.sleep(duration)
        self.driver.stop()

# Independent testing of MotorController module
if __name__ == "__main__":
    # For testing, use a dummy MotorDriver if actual hardware is not available.
    class DummyMotorDriver:
        def set_motor(self, side, speed):
            print(f"[Dummy] {side} motor set to speed {speed}")
        def stop(self):
            print("[Dummy] Motors stopped")

    # Initialize MotorController with dummy driver and test movements
    dummy_driver = MotorDriver(**config.MOTOR_PINS)
    motor_ctrl = MotorController(dummy_driver)

    print("Testing forward movement 100mm:")
    motor_ctrl.move_forward(100)   # Expect motors forward then stop
    print("Testing backward movement 50mm:")
    motor_ctrl.move_forward(-50)   # Expect motors reverse then stop
    print("Testing turn left 90 degrees:")
    motor_ctrl.turn_left(90)       # Expect left motor reverse, right motor forward then stop
    print("Testing turn right 45 degrees:")
    motor_ctrl.turn_right(45)      # Expect left motor forward, right motor reverse then stop
