# FlatSat Mission Control - Installation & Usage Guide

This guide will help you set up and run the FlatSat Mission Control dashboard and backend. The system is designed to run on a **MacBook** (ground station) or a **Raspberry Pi** (flight computer).

## 🚀 Quick Start

If you have already cloned the repo, you can simply run:

```bash
./start_dev.sh
```

This will:
1. Start the Python Backend (FastAPI) on port **8000**
2. Start the Frontend Dashboard (Next.js) on port **3000**

---

## 🛠️ Manual Installation

### 1. Prerequisites

Ensure you have the following installed:
- **Python 3.9+**
- **Node.js 18+** & **npm**

### 2. Backend Setup (FastAPI)

The backend handles sensor drivers and the API.

1. Navigate to the project root:
   ```bash
   cd flatsat
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv backend/.venv
   source backend/.venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

   **Hardware Support:**
   The backend automatically detects if real hardware is connected. If not, it switches to **MOCK** mode.
   - **INA219** (Power Sensor)
   - **MPU6050** (IMU)
   - **GPIO Relays**
   - **ADALM-Pluto** (SDR)
   - **USB Cameras**

### 3. Frontend Setup (Next.js)

The frontend is the mission control dashboard.

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

---

## 🏃 Running the System

### Option A: Use the Helper Script (Recommended)

From the root directory:

```bash
chmod +x start_dev.sh
./start_dev.sh
```

### Option B: Run Manually

**Terminal 1 (Backend):**
```bash
source backend/.venv/bin/activate
python -m backend.main
```
*API will be available at: http://localhost:8000*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*Dashboard will be available at: http://localhost:3000*

---

## 📡 Usage

1. Open **http://localhost:3000** in your browser.
2. Check the **System Status** in the top right corner:
   - 🟢 **REAL**: Hardware is connected and active.
   - 🟡 **MOCK**: Simulation mode (hardware not found).
3. **Telemetry Panel**: View real-time graphs for voltage, current, and IMU data.
4. **Relay Control**: Toggle power relays on/off.
5. **Camera Payload**: View live feeds from connected USB cameras.
6. **SDR Payload**: Control the ADALM-Pluto radio and view spectrum analysis.

## ⚠️ Troubleshooting

- **Port in use error**:
  Run this to kill lingering processes:
  ```bash
  lsof -t -i:8000 | xargs kill -9
  lsof -t -i:3000 | xargs kill -9
  ```

- **Permission denied for hardware**:
  On Linux/Raspberry Pi, you may need to add your user to the `dialout`, `i2c`, and `video` groups.
  ```bash
  sudo usermod -a -G dialout,i2c,video $USER
  ```
