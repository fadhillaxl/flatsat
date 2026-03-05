import random
import sys
# Patch smbus for mpu6050 library compatibility
import core.smbus_patch
from core.bus import i2c_lock
from subsystems.wt901 import WT901C485

try:
    from mpu6050 import mpu6050
except ImportError as e:
    print(f"[ADCS] Import Error: {e}")
    mpu6050 = None

class ADCS:
    def __init__(self, address=0x68, use_wt901=True):
        self.available = False
        self.use_wt901 = use_wt901
        self.wt901 = None

        # Try WT901C485 first if enabled
        if self.use_wt901:
            try:
                self.wt901 = WT901C485(port="/dev/ttyUSB0", baud=9600)
                if self.wt901.available:
                    self.available = True
                    print("[ADCS] Using WT901C485 via USB")
                    return
            except Exception as e:
                print(f"[ADCS] WT901C485 init failed: {e}")

        # Fallback to MPU6050
        if mpu6050:
            try:
                self.sensor = mpu6050(address, bus=1)
                self.available = True
                print("[ADCS] Using MPU6050 via I2C")
            except Exception as e:
                print(f"[ADCS] Hardware not found: {e}")
        else:
            print("[ADCS] mpu6050 library not found")

    def read_orientation(self):
        if self.available:
            try:
                if self.wt901 and self.wt901.available:
                    data = self.wt901.get_data()
                    return {
                        "roll": data["angleX"],
                        "pitch": data["angleY"],
                        "yaw": data["angleZ"],
                        "accel": {"x": data["accX"], "y": data["accY"], "z": data["accZ"]},
                        "gyro": {"x": data["gyroX"], "y": data["gyroY"], "z": data["gyroZ"]},
                        "mag": {"x": data["magX"], "y": data["magY"], "z": data["magZ"]}
                    }
                else:
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
                if self.wt901 and self.wt901.available:
                    return self.wt901.get_data()["temp"]
                else:
                    with i2c_lock:
                        return self.sensor.get_temp()
            except Exception:
                pass
        return 25.0 + random.uniform(-2, 2)
