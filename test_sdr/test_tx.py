import numpy as np
import adi
import time
import sys

def generate_sine_wave(freq, sample_rate, duration=1.0, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate complex sine wave (IQ)
    # frequency offset from center frequency
    iq = amplitude * (np.cos(2 * np.pi * freq * t) + 1j * np.sin(2 * np.pi * freq * t))
    return iq

def main():
    # Configuration
    CENTER_FREQ = 433500000  # 433.5 MHz
    SAMPLE_RATE = 1000000    # 1 MSPS
    TONE_FREQ = 10000        # 10 kHz offset (closer to center, easier to see)
    TX_GAIN = -10            # dB (max is usually 0 or 10 depending on firmware, min -80)
    
    # URI of the PlutoSDR
    # Default USB: ip:192.168.2.1
    # If using Ethernet on Pluto++, it might be different.
    # Try to detect or use default.
    uri = "ip:192.168.2.1"
    if len(sys.argv) > 1:
        uri = sys.argv[1]

    print(f"Connecting to PlutoSDR at {uri}...")
    try:
        sdr = adi.Pluto(uri=uri)
    except Exception as e:
        print(f"Error connecting to PlutoSDR: {e}")
        print("Make sure the device is connected and the URI is correct.")
        return

    # Configure TX
    print(f"Configuring TX: Freq={CENTER_FREQ/1e6} MHz, SR={SAMPLE_RATE/1e6} MSPS, Gain={TX_GAIN} dB")
    sdr.tx_lo = CENTER_FREQ
    sdr.tx_cyclic_buffer = True  # Enable cyclic buffer for continuous transmission
    sdr.tx_hardwaregain_chan0 = TX_GAIN
    
    # Create a sine wave
    print(f"Generating tone at +{TONE_FREQ/1e3} kHz offset...")
    samples = generate_sine_wave(TONE_FREQ, SAMPLE_RATE, duration=0.01, amplitude=0.5)
    
    # Scale to int16 if needed, but pyadi-iio handles complex64 (float) usually if using modern version
    # The example in backend.md used float32/32768, which implies it expects values <= 1.0
    # So we keep amplitude <= 1.0
    # samples = samples * 2**14 # REMOVED scaling, assuming normalized floats
    
    # Send data
    print("Transmitting... Press Ctrl+C to stop.")
    try:
        sdr.tx(samples)
        # Since cyclic buffer is enabled, it will keep transmitting this buffer
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping transmission...")
        sdr.tx_destroy_buffer()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup if needed
        pass

if __name__ == "__main__":
    main()
