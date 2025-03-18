from machine import I2C, Pin
from ustruct import unpack, pack
from collections import namedtuple

class AS5600:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        
    @property
    def raw_angle(self):
        return self._read_register(0x0C, 2)
    
    @property
    def angle(self):
        return self._read_register(0x0E, 2)
    
    def _read_register(self, reg, length):
        data = self.i2c.readfrom_mem(self.address, reg, length)
        return unpack('>H', data)[0] & 0x0FFF

    def scan(self):
        devices = self.i2c.scan()
        return self.address in devices