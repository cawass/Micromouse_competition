import time
import math
import micropython
from machine import SoftI2C, Pin, Timer, I2C
from drivers.AS5600 import AS5600
from drivers.tb6612 import MotorDriver
from utils.postion_calculator import PositionTracker
from utils.data_logger import DataLogger
import config 
from drivers.mpu6500 import MPU6500
from motor_controll import MotorController


# Initialize hardware

i2c = SoftI2C(scl=Pin(config.I2C_CONFIG['scl']), 
              sda=Pin(config.I2C_CONFIG['sda']))

from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin(config.I2C_CONFIG['scl']), sda=Pin(config.I2C_CONFIG['sda']))

print("Scanning I2C bus...")
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C devices found!")
else:
    print("I2C devices found:", [hex(device) for device in devices])
    
"""
sensor = AS5600(i2c, config.SENSOR_CONFIG['address'])

motor = MotorDriver(**config.MOTOR_PINS)
tracker = PositionTracker(wheel_diameter=35)
logger = DataLogger()

"""



# Initialize I2C
i2c = SoftI2C(scl=Pin(config.I2C_CONFIG['scl']), sda=Pin(config.I2C_CONFIG['sda']))

# Initialize the MPU6500 sensor
sensor = MPU6500(i2c)

def read_sensor(timer):
    print("Acceleration:", sensor.acceleration)
    print("Gyro:", sensor.gyro)
    print("Temperature:", sensor.temperature)

print("MPU6500 id: " + hex(sensor.whoami))

# Set up a timer to read the sensor periodically
timer_0 = Timer(0)
timer_0.init(period=1000, mode=Timer.PERIODIC, callback=read_sensor)


"""# Calibration
if sensor.scan():
    tracker.calibrate(sensor.raw_angle)
else:
    raise RuntimeError("AS5600 not found")

def read_sensor():
    raw = sensor.raw_angle
    angle = (raw / config.SENSOR_CONFIG['resolution']) * 360
    return raw, angle

def control_loop():
    last_time = time.ticks_ms()
    
    while True:
        raw, angle = read_sensor()
        delta_time = (time.ticks_ms() - last_time) / 1000
        last_time = time.ticks_ms()
        
        speed, distance = tracker.update(angle, delta_time)
    
        # Log data for plotting
        logger.log(
            time=time.ticks_ms(),
            raw_angle=raw,
            angle=angle,
            speed=speed,
            distance=distance
        )
        print(f"time {time} angle {angle}")
        
        # Motor control logic
        if distance < 100:  # Example condition
            motor.set_motor("left", 30000)
            motor.set_motor("right", 30000)
        else:
            motor.stop()
        
        time.sleep_ms(10)

# Run main loop
try:
    control_loop()
except KeyboardInterrupt:
    motor.stop()
    logger.save()
    print("Data saved to log.csv")

"""
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
