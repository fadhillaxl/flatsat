🛰️ 1. FULL SYSTEM ARCHITECTURE
                    FLATSAT SYSTEM

         ┌──────────────────────────┐
         │        Ground Station    │
         │                          │
         │  GPredict (Tracking)     │
         │  SDR Console (RX)        │
         │  MMSSTV (Image Decode)   │
         │  Dashboard               │
         └──────────────┬───────────┘
                        │
                        │ RF
                        │
                ┌───────▼────────┐
                │    PlutoSDR     │
                │   COMMS SYSTEM  │
                └───────┬────────┘
                        │ USB
                        │
           ┌────────────▼────────────┐
           │ Raspberry Pi Zero 2 W   │
           │       OBC (Flight SW)   │
           │                         │
           │  Payload  → USB Camera  │
           │  ADCS     → MPU6050     │
           │  EPS      → INA219      │
           │  COMMS    → PlutoSDR    │
           │                         │
           │  Mission Scheduler     │
           │  Telemetry Generator   │
           │  SSTV Encoder          │
           └─────────────────────────┘
🧩 2. Wiring Hardware
Raspberry Pi → Sensors
Device	Pin
INA219 VCC	3.3V
INA219 GND	GND
INA219 SDA	GPIO2
INA219 SCL	GPIO3
MPU6050 VCC	3.3V
MPU6050 GND	GND
MPU6050 SDA	GPIO2
MPU6050 SCL	GPIO3

I2C bisa share bus.

USB Devices
Device	Port
USB Camera	USB
PlutoSDR	USB OTG
📁 3. Project Folder Structure
flatsat/
│
├── core
│   ├── scheduler.py
│   ├── bus.py
│
├── subsystems
│   ├── eps.py
│   ├── adcs.py
│   ├── payload.py
│   ├── comms.py
│
├── services
│   ├── telemetry.py
│   ├── sstv.py
│   ├── command.py
│
├── mission
│   ├── mission_control.py
│
├── api
│   ├── server.py
│
└── logs
⚙️ 4. Software Installation
sudo apt update

sudo apt install

fswebcam
python3-pip
python3-numpy
python3-opencv
i2c-tools

pip3 install

pysstv
psutil
pyadi-iio
pillow
fastapi
uvicorn
smbus2
🧠 5. Flight Software Modules
EPS (Power Monitoring)

Sensor:

INA219

from ina219 import INA219

def read_power():

    return {
        "voltage":4.1,
        "current":0.32
    }
ADCS (Orientation)

Sensor:

MPU-6050

def read_orientation():

    return {
        "roll":0,
        "pitch":0,
        "yaw":0
    }
Payload (Camera)
import os

def capture():

    os.system("fswebcam -r 320x240 image.jpg")

    return "image.jpg"
Telemetry Generator
import psutil

def collect():

    return {

        "cpu":psutil.cpu_percent(),

        "ram":psutil.virtual_memory().percent
    }
SSTV Encoder
from pysstv.color import Robot36
from PIL import Image

def encode():

    img = Image.open("image.jpg")

    sstv = Robot36(img, 44100, 16)

    with open("downlink.wav","wb") as f:

        sstv.write_wav(f)
COMMS (PlutoSDR TX)

Radio:

ADALM-Pluto

import adi
import numpy as np
import scipy.io.wavfile as wav

def transmit():

    sdr = adi.Pluto()

    rate,data = wav.read("downlink.wav")

    data = data.astype(np.float32)/32768

    iq = data + 1j*data

    sdr.tx(iq)
Mission Control
while True:

    capture()

    telemetry = collect()

    encode()

    transmit()

    sleep(300)
🌐 6. Local API (Headless Control)

Server:

from fastapi import FastAPI

app = FastAPI()

@app.get("/capture")

def capture():

    run_capture()

    return {"status":"done"}

run:

uvicorn server:app --host 0.0.0.0 --port 8000
🖥️ 7. Dashboard

Laptop bisa akses:

http://raspberrypi:8000

atau push ke MQTT.

Broker:

EMQX

📡 8. Ground Station

Software stack:

Function	Software
tracking	GPredict
SDR receiver	SDR Console
SSTV decode	MMSSTV

Flow:

SDR Console
↓
Virtual Audio Cable
↓
MMSSTV
↓
Image decode
🤖 9. MASTER AI PROMPT (Generate Entire Project)

Ini prompt yang bisa kamu pakai di AI coding tool untuk generate seluruh kode otomatis.

Create a complete Flatsat flight software project for Raspberry Pi Zero 2 W.

The system must simulate a CubeSat architecture with these subsystems:

OBC:
Raspberry Pi Zero 2 W running Python

EPS:
INA219 power monitoring over I2C

ADCS:
MPU6050 IMU over I2C

Payload:
USB camera capturing images using fswebcam

COMMS:
PlutoSDR (ADALM Pluto) used for radio transmission using pyadi-iio

The software architecture must follow this structure:

core
subsystems
services
mission
api

Functions required:

capture image
collect telemetry
overlay telemetry on image
encode SSTV using Robot36
generate wav audio
transmit wav via PlutoSDR
receive RF command
mission scheduler loop
JSON telemetry logging
REST API using FastAPI
MQTT telemetry publish

Telemetry packet format JSON:

satellite_id
timestamp
cpu
ram
temperature
voltage
current
roll
pitch
yaw

The system must run headless and automatically execute a mission loop every 5 minutes.

Use Python libraries:

pysstv
pyadi-iio
psutil
pillow
fastapi
numpy
smbus2

Also generate:

hardware wiring diagram
module documentation
command uplink handler
ground station decoder instructions