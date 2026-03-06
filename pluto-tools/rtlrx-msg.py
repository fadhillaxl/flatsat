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