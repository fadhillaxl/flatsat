import time
import random
from smbus2 import SMBus
from core.bus import i2c_lock

try:
    from bmp280 import BMP280
except ImportError:
    BMP280 = None

# Support for BME280 (which has ID 0x60)
try:
    import bme280
except ImportError:
    bme280 = None

class Environment:
    def __init__(self, address=0x76):
        self.available = False
        self.bus = None
        self.sensor = None
        self.type = "mock"
        
        # Try BME280 first (since user likely has ID 60)
        if bme280:
            try:
                # bme280 library usage: bme280.load_calibration_params(bus, address)
                # then bme280.sample(bus, address, params)
                self.bus = SMBus(1)
                self.calibration_params = bme280.load_calibration_params(self.bus, address)
                self.address = address
                self.available = True
                self.type = "bme280"
                print(f"[Environment] Found BME280/BMP280 via bme280 library")
                return
            except Exception as e:
                pass
                # print(f"[Environment] bme280 init failed: {e}")

        # Fallback to BMP280 library
        if BMP280:
            try:
                self.bus = SMBus(1)
                self.sensor = BMP280(i2c_dev=self.bus, i2c_addr=address)
                self.available = True
                self.type = "bmp280"
            except Exception as e:
                print(f"[Environment] BMP280 init failed: {e}")
        else:
            print("[Environment] Libraries not found")

    def read_data(self):
        if self.available:
            try:
                with i2c_lock:
                    if self.type == "bme280":
                        data = bme280.sample(self.bus, self.address, self.calibration_params)
                        return {
                            "temperature": data.temperature,
                            "pressure": data.pressure,
                            "humidity": data.humidity,
                            # Approx altitude
                            "altitude": 44330 * (1 - (data.pressure / 1013.25) ** (1 / 5.255))
                        }
                    elif self.type == "bmp280":
                        temp = self.sensor.get_temperature()
                        pressure = self.sensor.get_pressure()
                        altitude = 44330 * (1 - (pressure / 1013.25) ** (1 / 5.255))
                        return {
                            "temperature": temp,
                            "pressure": pressure,
                            "altitude": altitude,
                            "humidity": 0.0
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
