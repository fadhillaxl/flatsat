# PlutoSDR Transmission Test

This script transmits a continuous sine wave (tone) using the PlutoSDR.
It is designed to verify that the PlutoSDR is transmitting correctly.

## Prerequisites

### 1. Install System Dependencies

On Raspberry Pi (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install libiio-utils libad9361-iio-dev python3-pip
```

On macOS (if running from Mac):
```bash
brew install libiio
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

## Usage

1. Connect the PlutoSDR via USB or Ethernet.
2. Run the script:

```bash
python3 test_tx.py [uri]
```

- Default URI is `ip:192.168.2.1` (standard USB connection).
- If using Ethernet or a different IP, provide the URI as an argument, e.g.:
  ```bash
  python3 test_tx.py ip:192.168.2.10
  ```

## What to Expect

- The script will configure the PlutoSDR to transmit at **437.0 MHz** (center frequency).
- It generates a tone at **+100 kHz** offset (so you should see a peak at **437.1 MHz**).
- Open your SDR receiver software (e.g., SDR Console, GQRX, SDR#) on your laptop and tune to 437.1 MHz to see the signal.
