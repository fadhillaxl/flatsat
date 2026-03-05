import time
import psutil
from subsystems.eps import EPS
from subsystems.adcs import ADCS

class Telemetry:
    def __init__(self):
        self.eps = EPS()
        self.adcs = ADCS()

    def collect(self):
        power = self.eps.read_power()
        orientation = self.adcs.read_orientation()
        temperature = self.adcs.read_temperature()
        
        return {
            "satellite_id": "FLATSAT-1",
            "timestamp": time.time(),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "temperature": temperature,
            "voltage": power.get("voltage", 0),
            "current": power.get("current", 0),
            "roll": orientation.get("roll", 0),
            "pitch": orientation.get("pitch", 0),
            "yaw": orientation.get("yaw", 0)
        }
