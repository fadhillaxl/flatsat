from rtlsdr import RtlSdr
import numpy as np
import time
from lib.modem import bits_to_text

CENTER_FREQ = 433500000
SAMPLE_RATE = 1000000
BAUD = 1000
SYNC_WORD = [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0] # 0x2DD4

BIT_SAMPLES = int(SAMPLE_RATE/BAUD)

sdr = RtlSdr()

sdr.sample_rate = SAMPLE_RATE
sdr.center_freq = CENTER_FREQ
sdr.gain = 'auto' # or set a fixed gain like 20

print(f"Listening on {CENTER_FREQ/1e6} MHz...")
print("Press Ctrl+C to stop")

def correlate_and_decode(bits):
    # Search for Sync Word
    # Simple sliding window correlation
    
    sync_len = len(SYNC_WORD)
    threshold = sync_len - 2 # Allow 2 bit errors
    
    # Convert bits to numpy array for easier matching
    bits_arr = np.array(bits)
    sync_arr = np.array(SYNC_WORD)
    
    # Check every possible start position
    for i in range(len(bits) - sync_len - 8):
        window = bits_arr[i : i+sync_len]
        
        # Count matching bits
        matches = np.sum(window == sync_arr)
        
        if matches >= threshold:
            # Sync found!
            # Next 8 bits are length (in bytes)
            len_start = i + sync_len
            len_bits = bits[len_start : len_start+8]
            
            # Decode length
            length_val = int("".join(str(b) for b in len_bits), 2)
            
            if length_val > 64: # Sanity check max length
                continue
                
            # Extract payload
            payload_start = len_start + 8
            payload_len_bits = length_val * 8
            payload_end = payload_start + payload_len_bits
            
            if payload_end <= len(bits):
                payload_bits = bits[payload_start:payload_end]
                text = bits_to_text(payload_bits)
                print(f"SYNC FOUND! Length: {length_val}")
                print(f"DECODED: {text}")
                return True
                
    return False

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
            # If there is a frequency offset, the mean of d_phase will not be 0.
            # Subtracting the mean centers the FSK signal around 0 Hz.
            freq_offset = np.mean(d_phase)
            d_phase -= freq_offset
            
            # Downsample / Integrate over bit period
            # Reshape array to (num_bits, samples_per_bit) and take mean
            
            # Ensure we have a multiple of BIT_SAMPLES
            num_bits = len(d_phase) // BIT_SAMPLES
            d_phase_trunc = d_phase[:num_bits * BIT_SAMPLES]
            
            # Reshape to 2D array: rows=bits, cols=samples_per_bit
            bit_chunks = d_phase_trunc.reshape(-1, BIT_SAMPLES)
            
            # Average phase change over each bit period
            # Positive average = Logic 1 (Positive Frequency Shift)
            # Negative average = Logic 0 (Negative Frequency Shift)
            bit_means = np.mean(bit_chunks, axis=1)
            
            # Threshold at 0
            # INVERTED LOGIC: If bit_means < 0 (Low Freq), it's a 1. If > 0 (High Freq), it's a 0.
            # This depends on whether the TX sends f1 for 1 or f0 for 1.
            # Currently TX sends f1 (+10kHz) for 1, and f0 (-10kHz) for 0.
            # But the receiver might be seeing an inverted spectrum or phase.
            # Let's try inverting the receiver logic first.
            demod_bits = (bit_means < 0).astype(int)
            
            # Try to find packet in the demodulated bits
            found = correlate_and_decode(demod_bits)
            
            if not found:
                 # Try normal logic if inverted failed
                 demod_bits_normal = (bit_means > 0).astype(int)
                 found_normal = correlate_and_decode(demod_bits_normal)
                 
                 if not found_normal:
                     # Debug: Print first 32 bits to see what we are receiving
                     debug_str = "".join(str(b) for b in demod_bits[:32])
                     print(f"Raw bits (first 32): {debug_str}...")

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    sdr.close()
