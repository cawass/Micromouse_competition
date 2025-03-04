# File imports
from tb6612 import *
from AS5600 import *
from micromouse_parameters import *
from position_calculator import *
from machine import I2C, Pin
from math import pi
import math
import time

# Setup
i2c = I2C(0, scl=Pin(40), sda=Pin(41), freq=400000)
z = AS5600(i2c, AS5600_id)
motor = MotorDriver(ain1=5, ain2=18, pwma=9, bin1=11, bin2=12, pwmb=10, stby=4)

# Initialize micromouse and distance determinator
micromouse = Micromouse(wheel_diameter=35)  # Example wheel size in mm
distance_determinator = DistanceDeterminator(micromouse)

z.scan()
i = 0
previous_angle = z.ANGLE

def update_motion(i):
    global previous_angle
    raw_angle = z.ANGLE  # Read the raw 12-bit angle value
    angle_radians = (raw_angle / 4096) * 2 * pi  # Convert to radians
      # Print with 4 decimal places

    # Calculate distance and speed
    distance_determinator.update(previous_angle, raw_angle)

    print("Speed: {:.2f} mm/s".format(distance_determinator.speed))
    print("Total Distance: {:.2f} mm".format(distance_determinator.total_distance))
    print("Angle: {:.4f} rad".format(angle_radians))
        
    previous_angle = raw_angle

while True:
    update_motion(i)
    i += 1
    if i > 5:
        motor.set_motor("left", 50000)
        motor.set_motor("right", 50000)
    time.sleep(0.01)


