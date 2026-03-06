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