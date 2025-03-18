import math
import time
from machine import I2C, Pin
from drivers.mpu6500 import MPU6500

class MPU6500Fusion:
    def __init__(self, i2c, address=0x68, accel_sf=9.80665, gyro_sf=0.0174533):
        """
        Initialize the MPU6500 sensor and set up fusion variables.
        :param i2c: I2C bus object.
        :param address: I2C address of the MPU6500 (default is 0x68).
        :param accel_sf: Scale factor for acceleration (default is 9.80665 for m/s²).
        :param gyro_sf: Scale factor for gyroscope (default is 0.0174533 for rad/s).
        """
        self.sensor = MPU6500(i2c, address=address, accel_sf=accel_sf, gyro_sf=gyro_sf)
        self.gyro_offset = (0, 0, 0)  # Gyroscope offset for calibration
        self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0  # Roll, pitch, and yaw angles (start at 0)
        self.update_frequency = 100  # Update frequency in Hz
        self.sample_delay = 10  # Delay between samples in milliseconds
        self.gyro_filter_alpha = 0.90  # Low-pass filter coefficient for gyroscope
        self.gx_prev, self.gy_prev, self.gz_prev = 0.0, 0.0, 0.0  # For low-pass filter
        self.last_update_time = time.ticks_ms()  # Initialize last update time

    def calibrate_gyro(self, samples=100, delay=10):
        """
        Calibrate the gyroscope by calculating the average offset.
        :param samples: Number of samples to average (default is 100).
        :param delay: Delay between samples in milliseconds (default is 10 ms).
        """
        print("Calibrating gyroscope...")
        gx, gy, gz = 0.0, 0.0, 0.0

        for _ in range(samples):
            gx += self.sensor.gyro[0]
            gy += self.sensor.gyro[1]
            gz += self.sensor.gyro[2]
            time.sleep_ms(delay)

        self.gyro_offset = (gx / samples, gy / samples, gz / samples)
        print(f"Calibration complete. Offsets: {self.gyro_offset}")

    def low_pass_filter(self, current, previous, alpha):
        """
        Apply a low-pass filter to the sensor data.
        :param current: Current sensor reading.
        :param previous: Previous filtered value.
        :param alpha: Filter coefficient (0 < alpha < 1).
        :return: Filtered value.
        """
        return alpha * previous + (1 - alpha) * current

    def update(self):
        """
        Update roll, pitch, and yaw using gyroscope data.
        """
        # Read gyroscope data
        gx, gy, gz = self.sensor.gyro

        # Apply gyroscope calibration offsets
        gx -= self.gyro_offset[0]
        gy -= self.gyro_offset[1]
        gz -= self.gyro_offset[2]

        # Convert gyroscope data to degrees per second
        gx = math.degrees(gx)
        gy = math.degrees(gy)
        gz = math.degrees(gz)

        # Apply low-pass filter to gyroscope data
        gx = self.low_pass_filter(gx, self.gx_prev, self.gyro_filter_alpha)
        gy = self.low_pass_filter(gy, self.gy_prev, self.gyro_filter_alpha)
        gz = self.low_pass_filter(gz, self.gz_prev, self.gyro_filter_alpha)
        self.gx_prev, self.gy_prev, self.gz_prev = gx, gy, gz

        # Calculate time step (dt) in seconds
        current_time = time.ticks_ms()
        dt = time.ticks_diff(current_time, self.last_update_time) / 1000.0
        self.last_update_time = current_time

        # Integrate gyroscope data to update angles
        self.roll += gx * dt
        self.pitch += gy * dt
        self.yaw += gz * dt

        # Optional: Bound yaw to 0-360 degrees
        self.yaw = self.yaw % 360

    def get_angles(self):
        """
        Get the current roll, pitch, and yaw angles.
        :return: Tuple of (roll, pitch, yaw) in degrees.
        """
        return self.roll, self.pitch, self.yaw

    def reset_angles(self):
        """
        Reset roll, pitch, and yaw angles to 0.
        """
        self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0

# Example usage
if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(40), sda=Pin(41))  # Adjust pins for your hardware
    fusion = MPU6500Fusion(i2c)

    # Calibrate the gyroscope
    fusion.calibrate_gyro()

    # Reset angles to 0, 0, 0
    fusion.reset_angles()

    # Main loop to update and print angles
    while True:
        fusion.update()
        roll, pitch, yaw = fusion.get_angles()
        print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")
        time.sleep_ms(10)  # Adjust the delay for your desired update rate