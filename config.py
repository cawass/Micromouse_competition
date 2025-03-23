# Hardware configuration
I2C_CONFIG = {
    'scl': 40,
    'sda': 41,
    'freq': 400000
}


MOTOR_PINS = {
    'ain1': 5,
    'ain2': 18,
    'pwma': 9,
    'bin1': 11,
    'bin2': 12,
    'pwmb': 10,
    'stby': 4
}

SENSOR_CONFIG = {
    #'address': 0x36,
    'address': 0x68,
    'resolution': 4096  # 12-bit resolution
}

TOF = {
    'address': 0x29,
}
