import time
import logging
import numpy as np

# Configure logging
logger = logging.getLogger("sdr")

class SDRDriver:
    def __init__(self, frequency=437000000, sample_rate=2400000, gain=30):
        self.mock = False
        try:
            import adi
            self.sdr = adi.Pluto()
            self.sdr.rx_lo = frequency
            self.sdr.rx_rf_bandwidth = sample_rate
            self.sdr.rx_buffer_size = 1024
            self.sdr.gain_control_mode_chan0 = "manual"
            self.sdr.rx_hardwaregain_chan0 = gain
            logger.info("PlutoSDR initialized successfully.")
        except Exception as e:
            logger.warning(f"Failed to initialize PlutoSDR: {e}. Using mock data.")
            self.mock = True
            self.frequency = frequency
            self.sample_rate = sample_rate
            self.gain = gain
            self.rx_enabled = False
            self.tx_enabled = False

    def read_samples(self):
        if self.mock:
            # Simulate noise + signal
            n_points = 1024
            noise = np.random.normal(0, 0.1, n_points) + 1j * np.random.normal(0, 0.1, n_points)
            
            if self.rx_enabled:
                # Add a carrier
                t = np.arange(n_points)
                signal = 0.5 * np.exp(1j * 2 * np.pi * 0.1 * t)
                return noise + signal
            
            return noise
        
        try:
            return self.sdr.rx()
        except Exception as e:
            logger.error(f"Error reading SDR: {e}")
            return np.zeros(1024, dtype=np.complex64)

    def set_config(self, frequency, sample_rate, gain, tx_enabled, rx_enabled):
        if self.mock:
            self.frequency = frequency
            self.sample_rate = sample_rate
            self.gain = gain
            self.tx_enabled = tx_enabled
            self.rx_enabled = rx_enabled
            return True
        
        try:
            self.sdr.rx_lo = int(frequency)
            self.sdr.rx_rf_bandwidth = int(sample_rate)
            self.sdr.rx_hardwaregain_chan0 = int(gain)
            # TX logic would be here
            return True
        except Exception as e:
            logger.error(f"Error configuring SDR: {e}")
            return False

    def get_spectrum(self):
        samples = self.read_samples()
        
        # Calculate FFT
        spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))
        spectrum = 20 * np.log10(spectrum + 1e-9) # Convert to dB
        
        return spectrum.tolist()
