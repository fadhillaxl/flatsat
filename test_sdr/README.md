# PlutoSDR Transmission Test

This script transmits a continuous sine wave (tone) using the PlutoSDR.
It is designed to verify that the PlutoSDR is transmitting correctly.

## Prerequisites

### 1. Install System Dependencies

The default Raspberry Pi OS repositories often have an outdated version of `libiio`. You need to install the latest version from the Analog Devices repository.

**Step 1: Add the Analog Devices Repository**
```bash
# Install GPG if missing
sudo apt install -y gpg

# Download the key and save it to the keyring (modern method, apt-key is deprecated)
wget -O - https://swdownloads.analog.com/cse/apt/generic.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/adi-archive-keyring.gpg

# Add the repository to your sources list (forcing 'bookworm' as 'trixie' might not be supported yet)
echo "deb [signed-by=/usr/share/keyrings/adi-archive-keyring.gpg] https://swdownloads.analog.com/cse/apt bookworm main" | sudo tee /etc/apt/sources.list.d/analog.list

# Update package lists
sudo apt update
```

**Step 2: Install Libraries**
```bash
# Install libiio and libad9361
sudo apt install libiio0 libiio-utils libiio-dev libad9361-0 libad9361-dev python3-pip
```

### 2. Install Python Dependencies
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

- The script will configure the PlutoSDR to transmit at **433.5 MHz** (center frequency).
- It generates a tone at **+10 kHz** offset (so you should see a peak at **433.51 MHz**).
- Open your SDR receiver software (e.g., SDR Console, GQRX, SDR#) on your laptop and tune to 433.51 MHz to see the signal.
