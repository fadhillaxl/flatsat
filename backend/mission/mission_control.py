import json
import os
from services.telemetry import Telemetry
from services.sstv import SSTV
from subsystems.payload import Payload
from subsystems.comms import Comms
from core.scheduler import Scheduler

class MissionControl:
    def __init__(self):
        self.telemetry = Telemetry()
        self.sstv = SSTV()
        self.payload = Payload()
        self.comms = Comms()
        self.scheduler = Scheduler()
        
        # Ensure logs directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def mission_loop(self):
        print("[Mission] Starting mission sequence...")
        
        # 1. Capture Image
        image_file = self.payload.capture("image.jpg")
        
        # 2. Collect Telemetry
        data = self.telemetry.collect()
        print(f"[Mission] Telemetry: {data}")
        
        # Log telemetry
        with open("logs/telemetry.json", "a") as f:
            f.write(json.dumps(data) + "\n")

        # 3. Encode SSTV
        if image_file:
            print("[Mission] Encoding SSTV...")
            success = self.sstv.encode(image_file, "downlink.wav")
            
            # 4. Transmit
            if success:
                print("[Mission] Transmitting...")
                self.comms.transmit("downlink.wav")
        
        print("[Mission] Sequence complete.")

    def run(self):
        # For standalone running
        self.scheduler.add_task(300, self.mission_loop)
        self.scheduler.start()
