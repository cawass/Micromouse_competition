# Hardware configuration
I2C_CONFIG = {
    'scl': 40,
    'sda': 41,
    'freq': 400000
}


MOTOR_PINS = {
    'ain1': 4,
    'ain2': 5,
    'pwma': 6,
    'bin1': 15,
    'bin2': 16,
    'pwmb': 17,
    'stby': 14
}
IR_PINS = {
    'ir1': 10,
    'ir2': 11,
    'ir3': 12,
    'ir4': 13
}

CONFIG_SWITCH = {
    'switch1': 47,
    'switch2': 21,
    'switch3': 20,
    'run_reset': 19,
    'led1': 45,
    'led2': 48
}
SENSOR_CONFIG = {
    #'address': 0x36,
    'address': 0x68,
    'resolution': 4096  # 12-bit resolution
}

TOF = {
    'address': 0x29,
}
