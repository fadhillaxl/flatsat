import time
import logging

# Configure logging
logger = logging.getLogger("relays")

class RelayDriver:
    def __init__(self, relay_pins=[17, 27, 22, 23]):
        self.mock = False
        try:
            from gpiozero import OutputDevice
            self.relays = []
            for pin in relay_pins:
                # Active LOW for most relay modules
                relay = OutputDevice(pin, active_high=False, initial_value=False)
                self.relays.append(relay)
            logger.info(f"Relays initialized on pins {relay_pins}")
        except (ImportError, OSError, ValueError) as e:
            logger.warning(f"Failed to initialize GPIO for relays: {e}. Using mock data.")
            self.mock = True
            self.relays = [False] * len(relay_pins)

    def set_state(self, index, state):
        if self.mock:
            if 0 <= index < len(self.relays):
                self.relays[index] = state
                return True
            return False

        if 0 <= index < len(self.relays):
            if state:
                self.relays[index].on()
            else:
                self.relays[index].off()
            return True
        return False

    def get_state(self, index):
        if self.mock:
            if 0 <= index < len(self.relays):
                return self.relays[index]
            return False

        if 0 <= index < len(self.relays):
            return self.relays[index].is_active
        return False

    def get_all_states(self):
        if self.mock:
            return self.relays
        return [r.is_active for r in self.relays]
