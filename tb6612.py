from machine import Pin, PWM

class MotorDriver:
    def __init__(self, ain1, ain2, pwma, bin1, bin2, pwmb, stby):
        self.ain1 = Pin(ain1, Pin.OUT)
        self.ain2 = Pin(ain2, Pin.OUT)
        self.pwma = PWM(Pin(pwma), freq=1000)
        self.bin1 = Pin(bin1, Pin.OUT)
        self.bin2 = Pin(bin2, Pin.OUT)
        self.pwmb = PWM(Pin(pwmb), freq=1000)
        self.stby = Pin(stby, Pin.OUT)

        self.enable()  # Enable motor driver
        self.stop()

    def enable(self):
        """Enable motor driver by setting STBY high."""
        self.stby.value(1)

    def disable(self):
        """Put motor driver in standby mode (high impedance)."""
        self.stby.value(0)

    def set_motor(self, side, speed):
        """
        Control motor: 'left' or 'right'
        Speed range: -65535 to 65535 (ESP32 16-bit PWM)
        """
        if side == "left":
            in1, in2, pwm = self.ain1, self.ain2, self.pwma
        elif side == "right":
            in1, in2, pwm = self.bin1, self.bin2, self.pwmb
        else:
            raise ValueError("Invalid motor side")

        if speed > 0:
            in1.value(1)  # Forward
            in2.value(0)
        elif speed < 0:
            in1.value(0)  # Reverse
            in2.value(1)
        else:
            in1.value(1)  # Brake (Both high)
            in2.value(1)

        pwm.duty_u16(abs(speed))  # Set PWM duty cycle

    def stop(self):
        """Short brake (both inputs HIGH)."""
        self.ain1.value(1)
        self.ain2.value(1)
        self.bin1.value(1)
        self.bin2.value(1)
        self.pwma.duty_u16(0)
        self.pwmb.duty_u16(0)

    def standby(self):
        """Put the motor driver in standby mode."""
        self.disable()

