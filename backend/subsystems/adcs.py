import random
import sys
# Patch smbus for mpu6050 library compatibility
import core.smbus_patch
from core.bus import i2c_lock

try:
    from mpu6050 import mpu6050
except ImportError as e:
    print(f"[ADCS] Import Error: {e}")
    mpu6050 = None

class ADCS:
    def __init__(self, address=0x68):
        self.available = False
        if mpu6050:
            try:
                # MPU6050 library usually defaults to bus 1, but we can be explicit if needed
                # However, mpu6050-raspberrypi library takes address in constructor
                self.sensor = mpu6050(address, bus=1)
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
                    gyro = self.sensor.get_gyro_data()
                return {
                    "roll": accel['x'],
                    "pitch": accel['y'],
                    "yaw": accel['z'],
                    "accel": accel,
                    "gyro": gyro
                }
            except Exception as e:
                print(f"[ADCS] Read error: {e}")

        # Simulation / Mock Data
        return {
            "roll": random.uniform(-5, 5),
            "pitch": random.uniform(-5, 5),
            "yaw": random.uniform(0, 360),
            "accel": {"x": random.uniform(-1, 1), "y": random.uniform(-1, 1), "z": 9.8},
            "gyro": {"x": random.uniform(-0.1, 0.1), "y": random.uniform(-0.1, 0.1), "z": random.uniform(-0.1, 0.1)}
        }

    def read_temperature(self):
        if self.available:
            try:
                with i2c_lock:
                    return self.sensor.get_temp()
            except Exception:
                pass
        return 25.0 + random.uniform(-2, 2)
