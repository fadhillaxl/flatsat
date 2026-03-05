import random
from core.bus import i2c_lock

try:
    from mpu6050 import mpu6050
except ImportError:
    mpu6050 = None

class ADCS:
    def __init__(self, address=0x68):
        self.available = False
        if mpu6050:
            try:
                self.sensor = mpu6050(address)
                self.available = True
            except Exception as e:
                print(f"[ADCS] Hardware not found: {e}")
        else:
            print("[ADCS] mpu6050 library not found")

    def read_orientation(self):
        if self.available:
            try:
                with i2c_lock:
                    accel = self.sensor.get_accel_data()
                # Basic mapping, in real usage would need sensor fusion
                return {
                    "roll": accel['x'],
                    "pitch": accel['y'],
                    "yaw": accel['z']
                }
            except Exception as e:
                print(f"[ADCS] Read error: {e}")

    def read_temperature(self):
        if self.available:
            try:
                with i2c_lock:
                    return self.sensor.get_temp()
            except Exception:
                pass
        return 25.0 + random.uniform(-2, 2)

        # Simulation / Mock Data
        return {
            "roll": random.uniform(-5, 5),
            "pitch": random.uniform(-5, 5),
            "yaw": random.uniform(0, 360)
        }
