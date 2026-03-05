import numpy as np
import scipy.io.wavfile as wav

try:
    import adi
except ImportError:
    adi = None

class Comms:
    def __init__(self, uri="ip:192.168.2.1"):
        self.uri = uri
        self.available = False
        if adi:
            try:
                # Don't instantiate until needed or check connection
                # sdr = adi.Pluto(uri) 
                self.available = True
            except Exception:
                pass
    
    def transmit(self, wav_file="downlink.wav"):
        if not adi:
            print("[Comms] pyadi-iio not installed")
            return

        try:
            sdr = adi.Pluto(self.uri)
            rate, data = wav.read(wav_file)
            
            # Normalize data
            data = data.astype(np.float32)
            if np.max(np.abs(data)) > 0:
                data = data / np.max(np.abs(data))
            
            # Create IQ data (simple AM/SSB like modulation for demo, or just raw IQ if wav is IQ)
            # The prompt example: iq = data + 1j*data
            iq = data + 1j * data
            
            sdr.tx_cyclic_buffer = False # Send once
            sdr.tx(iq)
            print(f"[Comms] Transmitted {wav_file}")
        except Exception as e:
            print(f"[Comms] Transmission failed: {e}")
