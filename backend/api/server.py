from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mission.mission_control import MissionControl
import uvicorn
import os
import random
import math

app = FastAPI(title="Flatsat API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Mission Control
mission = MissionControl()

# Mock Relay State
relay_states = [False, False, False, False]

# Mock SDR State
class SDRConfig(BaseModel):
    frequency: int
    sample_rate: int
    gain: int
    rx_enabled: bool
    tx_enabled: bool

sdr_state = SDRConfig(
    frequency=433000000,
    sample_rate=2000000,
    gain=10,
    rx_enabled=False,
    tx_enabled=False
)

@app.on_event("startup")
async def startup_event():
    # Start the mission scheduler
    mission.run()
    print("[API] Mission scheduler started")

@app.get("/")
def read_root():
    return {"status": "Flatsat Operational", "mode": "Headless"}

@app.get("/telemetry")
def get_telemetry():
    return mission.telemetry.collect()

@app.post("/capture")
def capture_image():
    filename = mission.payload.capture("manual_capture.jpg")
    if filename:
        return {"status": "success", "file": filename}
    return {"status": "failed"}

@app.get("/camera/{camera_id}")
def get_camera_image(camera_id: int):
    # In a real system, select the correct device based on camera_id
    # For now, return the latest captured image or a placeholder
    image_path = "image.jpg"
    if not os.path.exists(image_path):
        # Generate a dummy image if none exists
        mission.payload.capture(image_path)
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {"error": "Image not found"}

@app.get("/relays")
def get_relays():
    return {"relays": relay_states}

@app.post("/relay/{relay_id}/{state}")
def control_relay(relay_id: int, state: str):
    if relay_id < 1 or relay_id > 4:
        raise HTTPException(status_code=400, detail="Invalid relay ID")
    
    is_on = state.lower() == "on"
    relay_states[relay_id - 1] = is_on
    print(f"[Relay] Relay {relay_id} set to {state}")
    return {"status": "success", "relay_id": relay_id, "state": state}

@app.get("/sdr/status")
def get_sdr_status():
    return sdr_state

@app.post("/sdr/config")
def set_sdr_config(config: SDRConfig):
    global sdr_state
    sdr_state = config
    print(f"[SDR] Config updated: {config}")
    return sdr_state

@app.get("/spectrum")
def get_spectrum():
    # Generate mock spectrum data (FFT bins)
    # 256 bins, centered at frequency with some noise and a peak
    bins = 128
    data = []
    base_noise = -80
    
    for i in range(bins):
        val = base_noise + random.uniform(-5, 5)
        # Add a peak in the center if RX is enabled
        if sdr_state.rx_enabled:
            dist = abs(i - bins/2)
            if dist < 10:
                val += 50 * math.exp(-dist/2)
        data.append(val)
        
    return {"data": data}

@app.post("/transmit")
def transmit_telemetry():
    # Trigger a manual transmission sequence
    mission.mission_loop()
    return {"status": "mission_sequence_triggered"}

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
