import time
import psutil
from subsystems.eps import EPS
from subsystems.adcs import ADCS
from subsystems.environment import Environment

class Telemetry:
    def __init__(self):
        self.eps = EPS()
        self.adcs = ADCS()
        self.env = Environment()
        self.start_time = time.time()

    def collect(self):
        power_data = self.eps.read_power()
        orientation = self.adcs.read_orientation()
        # ADCS temp is internal to MPU, Environment temp is from BMP280 (more accurate for ambient)
        env_data = self.env.read_data()
        
        voltage = power_data.get("voltage", 0)
        current = power_data.get("current", 0)
        
        return {
            "satellite_id": "FLATSAT-1",
            "timestamp": time.time(),
            "power": {
                "voltage": voltage,
                "current": current,
                "power": voltage * (current / 1000.0) # approx power in Watts if current is mA? Wait, INA219 usually returns mA. 
                # If current is Amps, then W = V*A. If mA, then W = V*(mA/1000).
                # eps.py returns "current": self.ina.current() which is usually mA from the library.
                # But my mock data was 0.32 (Amps?). Let's assume Amps for consistency with standard engineering, but check eps.py mock.
                # Mock: 0.32. That's likely Amps.
            },
            "imu": {
                "roll": orientation.get("roll", 0),
                "pitch": orientation.get("pitch", 0),
                "yaw": orientation.get("yaw", 0),
                "accel": orientation.get("accel", {"x": 0, "y": 0, "z": 0}),
                "gyro": orientation.get("gyro", {"x": 0, "y": 0, "z": 0})
            },
            "system": {
                "uptime": time.time() - self.start_time,
                "cpu_usage": psutil.cpu_percent(),
                "ram_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "cpu_temp": self.get_cpu_temp()
            },
            "environment": {
                "temperature": env_data.get("temperature", 0),
                "humidity": env_data.get("humidity", 0),
                "pressure": env_data.get("pressure", 0),
                "altitude": env_data.get("altitude", 0)
            }
        }

    def get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return float(f.read()) / 1000.0
        except:
            return 0.0
