import threading
import time
import platform
from wit_lib import device_model
from wit_lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
from wit_lib.protocol_resolver.roles.protocol_485_resolver import Protocol485Resolver

class WT901C485:
    def __init__(self, port="/dev/ttyUSB0", baud=9600, addr=0x50):
        self.port = port
        self.baud = baud
        self.addr = addr
        self.device = None
        self.available = False
        self.data = {
            "accX": 0, "accY": 0, "accZ": 0,
            "gyroX": 0, "gyroY": 0, "gyroZ": 0,
            "angleX": 0, "angleY": 0, "angleZ": 0,
            "temp": 0,
            "magX": 0, "magY": 0, "magZ": 0
        }
        self.running = False
        self.thread = None

        try:
            self.device = device_model.DeviceModel(
                "WT901C485",
                Protocol485Resolver(),
                JY901SDataProcessor(),
                "51_0"
            )
            self.device.ADDR = addr
            self.device.serialConfig.portName = port
            self.device.serialConfig.baud = baud
            self.device.openDevice()
            self.device.dataProcessor.onVarChanged.append(self._on_update)
            self.available = True
            
            # Start background reading thread
            self.running = True
            self.thread = threading.Thread(target=self._loop_read)
            self.thread.daemon = True
            self.thread.start()
            print(f"[WT901] Initialized on {port}@{baud} ADDR={hex(addr)}")
        except Exception as e:
            print(f"[WT901] Initialization failed: {e}")
            self.available = False

    def _on_update(self, device_model):
        try:
            self.data["accX"] = device_model.getDeviceData("accX")
            self.data["accY"] = device_model.getDeviceData("accY")
            self.data["accZ"] = device_model.getDeviceData("accZ")
            self.data["gyroX"] = device_model.getDeviceData("gyroX")
            self.data["gyroY"] = device_model.getDeviceData("gyroY")
            self.data["gyroZ"] = device_model.getDeviceData("gyroZ")
            self.data["angleX"] = device_model.getDeviceData("angleX")
            self.data["angleY"] = device_model.getDeviceData("angleY")
            self.data["angleZ"] = device_model.getDeviceData("angleZ")
            self.data["temp"] = device_model.getDeviceData("temperature")
            self.data["magX"] = device_model.getDeviceData("magX")
            self.data["magY"] = device_model.getDeviceData("magY")
            self.data["magZ"] = device_model.getDeviceData("magZ")
        except Exception:
            pass

    def _loop_read(self):
        while self.running:
            try:
                # 0x30 starts the register block for acceleration, angular velocity, angle, etc.
                # Reading 41 registers covers most data
                self.device.readReg(0x30, 41)
            except Exception:
                pass
            time.sleep(0.1)

    def get_data(self):
        return self.data

    def close(self):
        self.running = False
        if self.device:
            self.device.closeDevice()
