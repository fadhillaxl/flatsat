import time
import logging

# Configure logging
logger = logging.getLogger("ina219")

class INA219Driver:
    def __init__(self, address=0x40):
        self.mock = False
        try:
            from ina219 import INA219
            self.ina = INA219(shunt_ohms=0.1, max_expected_amps=2.0, address=address)
            self.ina.configure()
            logger.info(f"INA219 initialized at address {hex(address)}")
        except (ImportError, OSError, ValueError) as e:
            logger.warning(f"Failed to initialize INA219: {e}. Using mock data.")
            self.mock = True
            self.start_time = time.time()

    def read(self):
        if self.mock:
            import random
            # Simulate some realistic values
            voltage = 5.0 + random.uniform(-0.1, 0.1)
            current = 150.0 + random.uniform(-10, 50) # mA
            power = voltage * current / 1000.0 # W
            return {
                "voltage": round(voltage, 2),
                "current": round(current, 2),
                "power": round(power, 2)
            }
        
        try:
            return {
                "voltage": round(self.ina.voltage(), 2),
                "current": round(self.ina.current(), 2),
                "power": round(self.ina.power() / 1000.0, 2)
            }
        except Exception as e:
            logger.error(f"Error reading INA219: {e}")
            return {"voltage": 0, "current": 0, "power": 0}
