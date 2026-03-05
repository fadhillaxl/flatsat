import time
import random
from core.bus import i2c_lock

try:
    from ina219 import INA219
except ImportError:
    INA219 = None

class EPS:
    def __init__(self, address=0x41):
        self.available = False
        if INA219:
            try:
                self.ina = INA219(shunt_ohms=0.1, max_expected_amps=2.0, address=address)
                self.ina.configure()
                self.available = True
            except Exception as e:
                print(f"[EPS] Hardware not found: {e}")
        else:
            print("[EPS] ina219 library not found")

    def read_power(self):
        if self.available:
            try:
                with i2c_lock:
                    return {
                        "voltage": self.ina.voltage(),
                        "current": self.ina.current()
                    }
            except Exception as e:
                print(f"[EPS] Read error: {e}")
        
        # Simulation / Mock Data
        return {
            "voltage": 4.1 + random.uniform(-0.1, 0.1),
            "current": 320.0 + random.uniform(-50, 50) # mA
        }
