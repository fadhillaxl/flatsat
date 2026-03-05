Great — if you want a **real CubeSat-style FlatSat architecture**, we should design it like an actual satellite bus system. Since you plan to use **Raspberry Pi Zero 2 W** and **ADALM-Pluto SDR**, we can build a **modular satellite stack** similar to what university CubeSat teams use.

Below is a **more advanced architecture** with scheduler, telemetry system, and payload management.

---

# 1. Full CubeSat-Style Architecture

```text
                     Ground Station (Laptop)
           ┌─────────────────────────────────────┐
           │ Mission Control Dashboard           │
           │                                     │
           │ Grafana / Web UI / SatDump          │
           │ GNU Radio / Data Recorder           │
           └───────────────┬─────────────────────┘
                           │
                       REST API
                           │
                ┌──────────▼──────────┐
                │  Flight Computer     │
                │ Raspberry Pi Zero 2W │
                │  (OBC)               │
                └─────────┬────────────┘
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
    Telemetry        Payload Bus        Power Bus
        │                 │                  │
   INA219 sensor      Cameras           Relay system
   MPU6050 IMU        Pluto SDR
```

Key idea:

* **OBC controls everything**
* Payloads are **separate modules**
* Communication through **internal APIs**

---

# 2. Software Stack

## Operating System

On the **Raspberry Pi Zero 2 W**

```
Raspberry Pi OS Lite
```

Minimal OS → better stability.

---

# 3. Satellite Software Layers

### Layer 1 — Hardware Drivers

Responsible for sensors and devices.

Modules:

```
drivers/
    ina219.py
    imu_mpu6050.py
    camera.py
    relay.py
    pluto_sdr.py
```

Libraries:

* smbus2
* OpenCV
* pyadi-iio

---

### Layer 2 — Satellite Services

Core satellite logic.

Modules:

```
services/
    telemetry_service.py
    payload_service.py
    scheduler_service.py
    health_monitor.py
```

Responsibilities:

Telemetry service

* collect sensor data
* package telemetry

Payload service

* manage cameras
* control Pluto SDR

Health monitor

* CPU
* voltage
* temperature

---

### Layer 3 — Mission Scheduler

Real satellites use **task scheduling**.

Example tasks:

```
tasks/

capture_image
rf_scan
beacon_transmit
power_check
health_report
```

Example scheduler loop:

```python
while True:

    run_task("health_check")

    if satellite_over_target():
        run_task("capture_image")

    if time_to_beacon():
        run_task("transmit_beacon")
```

---

# 4. Telemetry System

Real satellites constantly send telemetry.

Example telemetry packet:

```json
{
 "timestamp": 1710000000,
 "power": {
   "voltage": 5.12,
   "current": 380
 },
 "imu": {
   "roll": 0.2,
   "pitch": 1.3,
   "yaw": 90
 },
 "payload": {
   "camera_active": true,
   "pluto_freq": 437000000
 }
}
```

Source sensors:

* **INA219 High Side DC Current Sensor**
* **MPU6050 IMU Sensor**

---

# 5. Payload System

Payloads are separate modules.

## Camera Payload

Tasks:

```
capture_image
capture_timelapse
stream_preview
```

Storage:

```
/data/images/
```

---

## SDR Payload

Using **ADALM-Pluto SDR**

Capabilities:

Receive

* satellite signals
* spectrum monitoring

Transmit

* beacon signal
* telemetry test packets

Example SDR task:

```
payload/pluto_rx.py
payload/pluto_tx.py
```

Example Python:

```python
import adi

sdr = adi.Pluto()

sdr.rx_lo = 437e6
samples = sdr.rx()
```

---

# 6. Command System (Ground → Satellite)

Ground station sends commands.

Example commands:

```
CMD_CAPTURE_IMAGE
CMD_START_RF_SCAN
CMD_ENABLE_RELAY_1
CMD_REBOOT
```

Command API:

```
POST /command
```

Example payload:

```json
{
 "command":"capture_image",
 "camera":1
}
```

---

# 7. Ground Station Stack

Runs on your **MacBook Air**.

### Telemetry Dashboard

Options:

* **Grafana**
* **Node-RED**
* Custom React dashboard

---

### RF Analysis

* **SatDump**
* **GNU Radio**

These will interact with **ADALM-Pluto SDR**.

---

# 8. Data Storage

FlatSat data storage:

```
/data/

telemetry/
images/
rf_recordings/
logs/
```

Example logs:

```
telemetry_2026_03_04.json
rf_capture_437mhz.iq
image_001.jpg
```

---

# 9. Suggested Folder Structure

```
flatsat/

drivers/
services/
payload/
tasks/
api/
logs/
data/

main.py
scheduler.py
config.yaml
```

---

# 10. Development Roadmap

### Step 1

Basic avionics

✔ read INA219
✔ read MPU6050
✔ relay control

---

### Step 2

Payload system

✔ camera capture
✔ data storage

---

### Step 3

SDR integration

✔ Pluto control
✔ receive signals

---

### Step 4

Mission scheduler

✔ autonomous tasks
✔ telemetry streaming

---

### Step 5

Ground station

✔ dashboard
✔ command interface

---

# 11. Final Result

You will have a **complete CubeSat development platform**:

Features

✔ avionics simulation
✔ payload management
✔ SDR experiments
✔ telemetry system
✔ mission scheduler
✔ ground station control

