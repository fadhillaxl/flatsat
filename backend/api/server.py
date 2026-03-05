from fastapi import FastAPI
from mission.mission_control import MissionControl
import uvicorn
import os

app = FastAPI(title="Flatsat API", version="1.0.0")

# Initialize Mission Control
mission = MissionControl()

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

@app.post("/transmit")
def transmit_telemetry():
    # Trigger a manual transmission sequence
    mission.mission_loop()
    return {"status": "mission_sequence_triggered"}

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
