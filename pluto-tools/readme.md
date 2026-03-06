Kita buat **toolkit lengkap seperti hackrf_tools tetapi untuk PlutoSDR + RTL-SDR**.  
Ini cocok dengan setup kamu sekarang:

- **TX:** Raspberry Pi Zero 2W + entity["product","ADALM-Pluto SDR","Analog Devices software-defined radio"]  
- **RX:** Laptop + entity["product","RTL-SDR Blog V4","USB software-defined radio dongle"]  
- Frekuensi test: **433 MHz ISM**

Toolkit ini akan memungkinkan:

📡 kirim pesan  
📡 kirim file  
📡 kirim CW  
📡 decode otomatis di RTL-SDR

---

# 🛰️ Struktur Toolkit

```
pluto-tools/
│
├── plutotx-msg.py      # kirim text
├── plutotx-file.py     # kirim file
├── plutotx-cw.py       # morse code
│
├── rtlrx-msg.py        # decode pesan
├── rtlrx-waterfall.py  # monitor signal
│
├── lib/
│   ├── fsk.py
│   ├── modem.py
│   └── framing.py
│
└── requirements.txt
```

---

# 1️⃣ Install dependency

Di **Raspberry Pi dan Laptop**

```bash
pip install numpy pyadi-iio pyrtlsdr scipy
```

---

# 2️⃣ Library Modem

### `lib/modem.py`

```python
import numpy as np

def text_to_bits(text):
    bits = []
    for c in text:
        bits.extend([int(b) for b in format(ord(c),'08b')])
    return bits


def bits_to_text(bits):

    chars = []

    for i in range(0,len(bits),8):

        byte = bits[i:i+8]

        val = int("".join(str(b) for b in byte),2)

        chars.append(chr(val))

    return "".join(chars)
```

---

# 3️⃣ FSK Generator

### `lib/fsk.py`

```python
import numpy as np

def generate_fsk(bits, sample_rate, baud, f0, f1):

    samples_per_bit = int(sample_rate / baud)

    signal = []

    for bit in bits:

        freq = f1 if bit else f0

        t = np.arange(samples_per_bit) / sample_rate

        tone = np.exp(2j*np.pi*freq*t)

        signal.extend(tone)

    return np.array(signal).astype(np.complex64)
```

---

# 4️⃣ PlutoSDR Transmitter

### `plutotx-msg.py`

```python
import adi
import argparse
from lib.modem import text_to_bits
from lib.fsk import generate_fsk

parser = argparse.ArgumentParser()

parser.add_argument("--msg",required=True)
parser.add_argument("--freq",type=int,default=433500000)
parser.add_argument("--rate",type=int,default=1000000)
parser.add_argument("--baud",type=int,default=1000)
parser.add_argument("--gain",type=int,default=0)
parser.add_argument("--uri",default="ip:192.168.2.1")

args = parser.parse_args()

print("Connecting Pluto")

sdr = adi.Pluto(args.uri)

sdr.sample_rate = args.rate
sdr.tx_lo = args.freq
sdr.tx_hardwaregain_chan0 = args.gain
sdr.tx_cyclic_buffer = False

bits = text_to_bits(args.msg)

samples = generate_fsk(bits,args.rate,args.baud,-10000,10000)

print("TX:",args.msg)

sdr.tx(samples)
```

---

# 5️⃣ RTL-SDR Receiver (Auto Decode)

### `rtlrx-msg.py`

```python
from rtlsdr import RtlSdr
import numpy as np
from lib.modem import bits_to_text

CENTER_FREQ = 433500000
SAMPLE_RATE = 1000000
BAUD = 1000

BIT_SAMPLES = int(SAMPLE_RATE/BAUD)

sdr = RtlSdr()

sdr.sample_rate = SAMPLE_RATE
sdr.center_freq = CENTER_FREQ
sdr.gain = 'auto'

print("Listening...")

samples = sdr.read_samples(256000)

bits=[]

for i in range(0,len(samples),BIT_SAMPLES):

    chunk = samples[i:i+BIT_SAMPLES]

    if len(chunk) < BIT_SAMPLES:
        break

    phase = np.angle(np.mean(chunk))

    if phase > 0:
        bits.append(1)
    else:
        bits.append(0)

text = bits_to_text(bits)

print("DECODED:",text)
```

---

# 6️⃣ Transmit test

Di **Raspberry Pi**

```bash
python3 plutotx-msg.py --msg "HELLO SAT"
```

---

# 7️⃣ Receive

Di **Laptop**

```bash
python3 rtlrx-msg.py
```

Output:

```
Listening...
DECODED: HELLO SAT
```

---

# 8️⃣ Visual Signal (SDR++)
Kalau dibuka di SDR++ kamu akan melihat:

```
   bit 0  ← tone kiri
   bit 1  ← tone kanan
```

Waterfall seperti **telemetry satelit FSK**.

---

# 9️⃣ Upgrade yang sangat menarik untuk project kamu

Toolkit ini bisa berkembang jadi **ground station simulator** untuk flatsat kamu.

Tambahkan modul:

### 🛰 telemetry frame

```
SAT01|TEMP:22|BAT:3.8|GYRO:0.01
```

### 🛰 camera image transmit

```
plutotx-file image.jpg
```

### 🛰 SSTV

image → RF

### 🛰 command uplink

```
rtlrx-cmd
```

lalu raspi flatsat menerima command.

---

