import time
import logging

# Configure logging
logger = logging.getLogger("mpu6050")

class MPU6050Driver:
    def __init__(self, address=0x68):
        self.mock = False
        try:
            from mpu6050 import mpu6050
            self.sensor = mpu6050(address)
            logger.info(f"MPU6050 initialized at address {hex(address)}")
        except (ImportError, OSError, ValueError) as e:
            logger.warning(f"Failed to initialize MPU6050: {e}. Using mock data.")
            self.mock = True
            self.start_time = time.time()

    def read(self):
        if self.mock:
            import random
            import math
            t = time.time() - self.start_time
            return {
                "accel": {
                    "x": round(math.sin(t*0.5)*0.5, 2),
                    "y": round(math.cos(t*0.5)*0.5, 2),
                    "z": round(9.8 + random.uniform(-0.1, 0.1), 2)
                },
                "gyro": {
                    "x": round(random.uniform(-1, 1), 2),
                    "y": round(random.uniform(-1, 1), 2),
                    "z": round(random.uniform(-1, 1), 2)
                },
                "temp": round(25 + random.uniform(-1, 1), 1)
            }
        
        try:
            accel = self.sensor.get_accel_data()
            gyro = self.sensor.get_gyro_data()
            temp = self.sensor.get_temp()
            
            return {
                "accel": {
                    "x": round(accel['x'], 2),
                    "y": round(accel['y'], 2),
                    "z": round(accel['z'], 2)
                },
                "gyro": {
                    "x": round(gyro['x'], 2),
                    "y": round(gyro['y'], 2),
                    "z": round(gyro['z'], 2)
                },
                "temp": round(temp, 1)
            }
        except Exception as e:
            logger.error(f"Error reading MPU6050: {e}")
            return {
                "accel": {"x": 0, "y": 0, "z": 0},
                "gyro": {"x": 0, "y": 0, "z": 0},
                "temp": 0
            }
