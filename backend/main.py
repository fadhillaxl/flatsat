from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import io
import logging
from backend.drivers.ina219 import INA219Driver
from backend.drivers.mpu6050 import MPU6050Driver
from backend.drivers.relays import RelayDriver
from backend.drivers.camera import CameraDriver
from backend.drivers.sdr import SDRDriver
from backend.drivers.system import SystemDriver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(title="FlatSat Mission Control API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Hardware Initialization ---
logger.info("Initializing hardware drivers...")
ina = INA219Driver()
imu = MPU6050Driver()
relays = RelayDriver()
cameras = CameraDriver()
sdr = SDRDriver()
system = SystemDriver()
logger.info("Hardware initialization complete.")

# --- Models ---
class RelayControl(BaseModel):
    id: int
    state: bool

class SDRConfig(BaseModel):
    frequency: int
    sample_rate: int
    gain: int
    tx_enabled: bool
    rx_enabled: bool

# --- Endpoints ---

@app.get("/")
async def root():
    stats = system.get_stats()
    return {"message": "FlatSat API is running", "uptime": stats["uptime"]}

@app.get("/status")
async def get_system_status():
    """Returns the initialization status (Real/Mock) of all subsystems."""
    return {
        "ina219": "MOCK" if ina.mock else "REAL",
        "mpu6050": "MOCK" if imu.mock else "REAL",
        "relays": "MOCK" if relays.mock else "REAL",
        "cameras": "MOCK" if cameras.mock else "REAL",
        "sdr": "MOCK" if sdr.mock else "REAL",
        "system": "MOCK" if system.mock else "REAL"
    }

@app.get("/telemetry")
async def get_telemetry():
    """Returns real telemetry data from sensors."""
    power_data = ina.read()
    imu_data = imu.read()
    sys_stats = system.get_stats()

    # Calculate environment data (using IMU temp for now as proxy for environment if no other sensor)
    # Ideally add BME280 for pressure/humidity/altitude
    # For now, we mock pressure/altitude/humidity based on system time or just constants if no sensor
    
    return {
        "timestamp": time.time(),
        "power": power_data,
        "imu": {
            "roll": imu_data["gyro"]["x"], # Simplified mapping for demo
            "pitch": imu_data["gyro"]["y"],
            "yaw": imu_data["gyro"]["z"],
            "accel": imu_data["accel"]
        },
        "system": {
            "cpu_temp": sys_stats["temp"],
            "cpu_usage": sys_stats["cpu_usage"],
            "ram_usage": sys_stats["ram_usage"],
            "disk_usage": sys_stats["disk_usage"],
            "uptime": sys_stats["uptime"]
        },
        "environment": {
            "temperature": imu_data["temp"], # Using MPU6050 temp
            "humidity": 45.0, # Placeholder (needs BME280)
            "pressure": 1013.25, # Placeholder (needs BME280)
            "altitude": 0.0 # Placeholder
        }
    }

@app.get("/relays")
async def get_relays():
    return {"relays": relays.get_all_states()}

@app.post("/relay/{relay_id}/{action}")
async def control_relay(relay_id: int, action: str):
    """Control relays. Action: 'on' or 'off'."""
    if relay_id < 1 or relay_id > 4:
        raise HTTPException(status_code=400, detail="Invalid relay ID (1-4)")
    
    is_on = action.lower() == "on"
    success = relays.set_state(relay_id - 1, is_on)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to control relay")
        
    return {"relay_id": relay_id, "state": "ON" if is_on else "OFF"}

@app.get("/sdr/status")
async def get_sdr_status():
    return {
        "frequency": sdr.frequency if sdr.mock else sdr.sdr.rx_lo,
        "sample_rate": sdr.sample_rate if sdr.mock else sdr.sdr.rx_rf_bandwidth,
        "gain": sdr.gain if sdr.mock else sdr.sdr.rx_hardwaregain_chan0,
        "tx_enabled": sdr.tx_enabled if sdr.mock else False, # TX logic simplified
        "rx_enabled": sdr.rx_enabled if sdr.mock else True
    }

@app.post("/sdr/config")
async def config_sdr(config: SDRConfig):
    success = sdr.set_config(
        config.frequency, 
        config.sample_rate, 
        config.gain, 
        config.tx_enabled, 
        config.rx_enabled
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to configure SDR")
        
    return {"status": "updated", "config": config}

@app.get("/camera/{camera_id}")
async def get_camera_image(camera_id: int):
    """Returns real camera frame."""
    frame = cameras.get_frame(camera_id)
    return StreamingResponse(io.BytesIO(frame), media_type="image/jpeg")

@app.get("/spectrum")
async def get_spectrum():
    """Returns FFT data from SDR."""
    data = sdr.get_spectrum()
    return {"data": data}

@app.on_event("shutdown")
def shutdown_event():
    cameras.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
