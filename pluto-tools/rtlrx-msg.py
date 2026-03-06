from rtlsdr import RtlSdr
import numpy as np
import time
from lib.modem import bits_to_text
from lib.framing import find_packet

CENTER_FREQ = 433500000
SAMPLE_RATE = 1000000
BAUD = 1000
# NOTE: With Manchester, baud rate effectively doubles for symbols, but we handle it in framing.py
# Actually, our simple approach sends 2 bits per original bit.
# To keep things simple, we keep the symbol rate the same, so effective data rate is halved.
# Transmitter sends 2 symbols for every 1 data bit.
# Receiver just demodulates symbols and passes them to find_packet which handles decoding.

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
        samples = sdr.read_samples(256*1024)
        
        # Calculate average power in dB
        power = 10 * np.log10(np.mean(np.abs(samples)**2) + 1e-20)
        
        if power > -20: 
            print(f"Signal detected! Power: {power:.2f} dB")
            
            # Quadrature Demodulation (FM Demod)
            # Calculates instantaneous frequency deviation
            # d_phase = angle(sample[n] * conj(sample[n-1]))
            
            # Create delayed version of samples
            samples_delay = np.concatenate(([0], samples[:-1]))
            
            # Calculate phase difference (Instantaneous Frequency)
            d_phase = np.angle(samples * np.conj(samples_delay))
            
            # AFC: Center the frequency
            freq_offset = np.mean(d_phase)
            d_phase -= freq_offset
            
            # --- CLOCK RECOVERY (Oversampling) ---
            # Instead of blindly averaging every BIT_SAMPLES, we need to find the optimal sampling point.
            # We look for the "eye opening" or maximum variance.
            # Simple approach: oversample by 8x (BIT_SAMPLES must be divisible)
            
            # Since BIT_SAMPLES = 1000 (1Msps / 1000 baud), we have plenty of samples.
            # Let's just decimate for now to a manageable rate, say 8 samples per bit
            
            samples_per_symbol = BIT_SAMPLES
            
            # Let's stick to the current block approach but try to align the phase.
            # We can try multiple offsets (0, BIT_SAMPLES/4, BIT_SAMPLES/2, 3*BIT_SAMPLES/4)
            
            offsets = [0, int(BIT_SAMPLES/4), int(BIT_SAMPLES/2), int(3*BIT_SAMPLES/4)]
            
            found_any = False
            
            for offset in offsets:
                 # Slice the phase array with offset
                 # Ensure we have enough data
                 if len(d_phase) <= offset:
                     break
                     
                 d_phase_shifted = d_phase[offset:]
                 
                 # Truncate to multiple of BIT_SAMPLES
                 num_bits = len(d_phase_shifted) // BIT_SAMPLES
                 if num_bits == 0:
                     continue
                     
                 d_phase_trunc = d_phase_shifted[:num_bits * BIT_SAMPLES]
                 
                 # Reshape and average
                 bit_chunks = d_phase_trunc.reshape(-1, BIT_SAMPLES)
                 bit_means = np.mean(bit_chunks, axis=1)
                 
                 # Try Normal Logic
                 demod_bits = (bit_means > 0).astype(int)
                 
                 found, payload = find_packet(demod_bits)
                 if found:
                     text = bits_to_text(payload)
                     print(f"SYNC FOUND! (Normal Polarity)")
                     print(f"DECODED: {text}")
                     found_any = True
                     break
                     
                 # Try Inverted Logic
                 demod_bits_inv = (bit_means < 0).astype(int)
                 
                 found, payload = find_packet(demod_bits_inv)
                 if found:
                     text = bits_to_text(payload)
                     print(f"SYNC FOUND! (Inverted Polarity)")
                     print(f"DECODED: {text}")
                     found_any = True
                     break
            
            if not found_any:
                 # Debug: Print first 32 bits of the best guess (offset 0)
                 # Re-calculate for offset 0 for debug print
                 num_bits = len(d_phase) // BIT_SAMPLES
                 d_phase_trunc = d_phase[:num_bits * BIT_SAMPLES]
                 bit_chunks = d_phase_trunc.reshape(-1, BIT_SAMPLES)
                 bit_means = np.mean(bit_chunks, axis=1)
                 demod_bits = (bit_means > 0).astype(int)
                 
                 debug_str = "".join(str(b) for b in demod_bits[:64])
                 print(f"Raw bits (offset 0): {debug_str}...")

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    sdr.close()
