from rtlsdr import RtlSdr
import numpy as np
import time
from lib.modem import bits_to_text

CENTER_FREQ = 433500000
SAMPLE_RATE = 1000000
BAUD = 1000

BIT_SAMPLES = int(SAMPLE_RATE/BAUD)

sdr = RtlSdr()

sdr.sample_rate = SAMPLE_RATE
sdr.center_freq = CENTER_FREQ
sdr.gain = 'auto' # or set a fixed gain like 20

print(f"Listening on {CENTER_FREQ/1e6} MHz...")
print("Press Ctrl+C to stop")

try:
    while True:
        # Read a chunk of samples
        # 256k samples @ 1Msps = ~0.25 seconds of audio
        samples = sdr.read_samples(256*1024)
        
        # Simple energy detection to avoid processing noise
        # Calculate average power in dB
        power = 10 * np.log10(np.mean(np.abs(samples)**2) + 1e-20)
        
        # Threshold (adjust based on your noise floor)
        # If signal is strong enough, try to decode
        if power > -20: 
            print(f"Signal detected! Power: {power:.2f} dB")
            
            bits = []
            for i in range(0, len(samples), BIT_SAMPLES):
                chunk = samples[i:i+BIT_SAMPLES]
                if len(chunk) < BIT_SAMPLES:
                    break
                
                # FSK Demodulation logic
                # For simple FSK, we can check phase changes or frequency content
                # The original code used phase > 0, which is very simple
                # Let's keep it consistent but maybe improve later
                phase = np.angle(np.mean(chunk))
                if phase > 0:
                    bits.append(1)
                else:
                    bits.append(0)
            
            text = bits_to_text(bits)
            # Filter out non-printable characters to reduce noise output
            clean_text = "".join([c for c in text if c.isprintable()])
            
            if len(clean_text) > 3: # Ignore very short noise
                print(f"DECODED: {clean_text}")
        else:
            # Optional: print a dot to show it's alive
            # print(".", end="", flush=True)
            pass

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    sdr.close()
