import time
import random
from smbus2 import SMBus
from core.bus import i2c_lock

try:
    from bmp280 import BMP280
except ImportError:
    BMP280 = None

class Environment:
    def __init__(self, address=0x76):
        self.available = False
        self.bus = None
        self.sensor = None
        
        if BMP280:
            try:
                # BMP280 library often requires an SMBus object
                self.bus = SMBus(1)
                self.sensor = BMP280(i2c_dev=self.bus, i2c_addr=address)
                self.available = True
            except Exception as e:
                print(f"[Environment] BMP280 not found: {e}")
        else:
            print("[Environment] bmp280 library not found")

    def read_data(self):
        if self.available:
            try:
                with i2c_lock:
                    temp = self.sensor.get_temperature()
                    pressure = self.sensor.get_pressure()
                    # Altitude estimation: h = 44330 * (1 - (p/p0)^(1/5.255))
                    # p0 = 1013.25 hPa
                    altitude = 44330 * (1 - (pressure / 1013.25) ** (1 / 5.255))
                    
                return {
                    "temperature": temp,
                    "pressure": pressure,
                    "altitude": altitude,
                    "humidity": 0.0 # BMP280 doesn't have humidity (BME280 does)
                }
            except Exception as e:
                print(f"[Environment] Read error: {e}")

        # Simulation / Mock Data
        return {
            "temperature": 25.0 + random.uniform(-2, 2),
            "pressure": 1013.25 + random.uniform(-5, 5),
            "altitude": 0.0 + random.uniform(-1, 1),
            "humidity": 45.0 + random.uniform(-5, 5)
        }
