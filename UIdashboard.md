## Mission-Control Style Dashboard UI (for your FlatSat)

This dashboard will run on **your laptop (MacBook Air)** and control/monitor the FlatSat running on **Raspberry Pi Zero 2 W** with sensors, cameras, relays, and **ADALM-Pluto SDR**.

Goal: look like a **satellite mission control panel** with telemetry, camera feeds, RF status, and subsystem control.

---

# 1. Dashboard Architecture

```text
Laptop (Mission Control)
 ├── Web Dashboard (React / Next.js)
 ├── Telemetry Graphs (Grafana)
 ├── RF Tools (SatDump / GNU Radio)
 └── API client

            WIFI / LAN

Raspberry Pi Zero 2 W
 └── FastAPI server
      ├─ sensors
      ├─ cameras
      ├─ relay control
      └─ Pluto SDR control
```

The browser connects directly to the **FlatSat API**.

---

# 2. UI Layout (Mission Control)

Example screen layout:

```text
┌──────────────────────────────────────────────┐
│ FLATSAT MISSION CONTROL                      │
├───────────────┬──────────────────────────────┤
│ Telemetry     │ Camera Payload               │
│               │                              │
│ Voltage       │  Camera 1  Camera 2 Camera 3 │
│ Current       │                              │
│ IMU           │                              │
│ CPU Temp      │                              │
├───────────────┼──────────────────────────────┤
│ Relay Control │ SDR Payload                  │
│               │                              │
│ Relay1 ON/OFF │ Frequency                    │
│ Relay2 ON/OFF │ RX/TX status                 │
│ Relay3 ON/OFF │ Signal power                 │
│ Relay4 ON/OFF │ Spectrum preview             │
└───────────────┴──────────────────────────────┘
```

Panels:

### Telemetry

Data from:

* **INA219 High Side DC Current Sensor**
* **MPU6050 IMU Sensor**

Display:

* voltage
* current
* power
* acceleration
* gyro

---

### Camera Panel

Displays 3 USB cameras:

```
/dev/video0
/dev/video1
/dev/video2
```

Buttons:

```
CAPTURE
START STREAM
STOP STREAM
```

---

### Relay Control

Control **4 Channel Relay Module 5V Optocoupler**

Example UI:

```
Relay 1  [ON] [OFF]
Relay 2  [ON] [OFF]
Relay 3  [ON] [OFF]
Relay 4  [ON] [OFF]
```

---

### SDR Payload Panel

Control **ADALM-Pluto SDR**

Display:

```
Frequency
RX power
TX state
sample rate
```

Buttons:

```
START RX
START TX
STOP
```

---

# 3. Tech Stack (Dashboard)

Frontend

```
Next.js
React
TailwindCSS
Chart.js
```

Backend

```
FastAPI (on Raspberry Pi)
```

Communication

```
REST API
WebSocket (optional)
```

---

# 4. Example Dashboard Code

Simple telemetry viewer.

```html
<!DOCTYPE html>
<html>

<head>
<title>FlatSat Mission Control</title>
</head>

<body>

<h1>FlatSat Dashboard</h1>

<h2>Power</h2>

Voltage: <span id="v"></span><br>
Current: <span id="c"></span><br>

<h2>IMU</h2>

AX: <span id="ax"></span><br>
AY: <span id="ay"></span><br>
AZ: <span id="az"></span><br>

<button onclick="relay(1,1)">Relay1 ON</button>
<button onclick="relay(1,0)">Relay1 OFF</button>

<script>

const api="http://RASPI_IP:8000"

async function update(){

let r=await fetch(api+"/telemetry")
let d=await r.json()

document.getElementById("v").innerText=d.voltage
document.getElementById("c").innerText=d.current

document.getElementById("ax").innerText=d.accel.x
document.getElementById("ay").innerText=d.accel.y
document.getElementById("az").innerText=d.accel.z

}

async function relay(id,state){

await fetch(api+"/relay/"+id+"/"+state,{
method:"POST"
})

}

setInterval(update,1000)

</script>

</body>

</html>
```

---

# 5. Camera Viewer

Example image viewer:

```
http://RASPI_IP:8000/camera/0
http://RASPI_IP:8000/camera/1
http://RASPI_IP:8000/camera/2
```

Embed:

```html
<img src="http://RASPI_IP:8000/camera/0">
```

---

# 6. Telemetry Graphs (Mission Control Style)

Use **Grafana**.

Graphs:

```
Voltage over time
Current consumption
IMU motion
RF power
CPU temperature
```

Database:

```
InfluxDB
```

---

# 7. SDR Spectrum Panel

You can embed spectrum from:

* **GNU Radio**
* **SatDump**

or stream IQ data.

---

# 8. Advanced UI (Recommended)

Add these panels:

### Satellite Orientation

3D model showing IMU data.

Libraries:

```
three.js
```

---

### Spectrum Waterfall

Like SDR software.

Libraries:

```
WebGL
d3.js
```

---

# 9. Final System

You will have:

FlatSat

* avionics
* payload
* SDR
* cameras

Ground station

* mission control dashboard
* telemetry graphs
* RF tools
* payload control

Very similar to **CubeSat lab systems**.

---
