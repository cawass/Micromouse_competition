from tb6612 import MotorDriver
import time

# Define motor control pins (adjust for your ESP32 wiring)
motor = MotorDriver(ain1=5, ain2=18, pwma=9, bin1=11, bin2=12, pwmb=10, stby=4)

print("Motor driver initialized.")

# Move forward at 50% speed
print("Moving forward at 50% speed.")
motor.set_motor("left", 32767)
motor.set_motor("right", 32767)
time.sleep(2)

# Stop with braking
print("Stopping with braking.")
motor.stop()
time.sleep(0)

# Move backward at 25% speed
print("Moving backward at 25% speed.")
motor.set_motor("left", -16384)
motor.set_motor("right", -16384)
time.sleep(2)

# Standby mode (high impedance)
print("Entering standby mode.")
motor.standby()
time.sleep(2)

print("Stopping motors.")
motor.stop()
