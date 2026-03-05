import psutil
import time
import logging

# Configure logging
logger = logging.getLogger("system")

class SystemDriver:
    def __init__(self):
        self.mock = False
        try:
            psutil.cpu_percent(interval=0.1)
            logger.info("System monitoring initialized.")
        except Exception as e:
            logger.warning(f"Failed to initialize system monitoring: {e}. Using mock data.")
            self.mock = True

    def get_stats(self):
        if self.mock:
            import random
            return {
                "cpu_usage": round(random.uniform(0, 100), 1),
                "ram_usage": round(random.uniform(0, 100), 1),
                "disk_usage": round(random.uniform(0, 100), 1),
                "uptime": time.time(),
                "temp": 45.0 + random.uniform(-1, 1)
            }
        
        try:
            return {
                "cpu_usage": psutil.cpu_percent(),
                "ram_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "uptime": time.time() - psutil.boot_time(),
                "temp": self.get_cpu_temp()
            }
        except Exception as e:
            logger.error(f"Error reading system stats: {e}")
            return {
                "cpu_usage": 0,
                "ram_usage": 0,
                "disk_usage": 0,
                "uptime": 0,
                "temp": 0
            }

    def get_cpu_temp(self):
        try:
            # Raspberry Pi specific
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return round(float(f.read()) / 1000.0, 1)
        except:
            # Fallback for other systems (e.g. Mac/Linux)
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if "coretemp" in temps:
                    return temps["coretemp"][0].current
            return 0.0
