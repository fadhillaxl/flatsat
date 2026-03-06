import numpy as np
import adi
import argparse

def text_to_bits(text):
    bits = []
    for c in text:
        b = format(ord(c), '08b')
        bits.extend([int(x) for x in b])
    return bits

def generate_fsk(bits, sample_rate, baud, f0, f1):
    samples_per_bit = int(sample_rate / baud)
    signal = []

    for bit in bits:
        freq = f1 if bit else f0
        t = np.arange(samples_per_bit) / sample_rate
        tone = np.exp(2j * np.pi * freq * t)
        signal.extend(tone)

    return np.array(signal).astype(np.complex64)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--msg", required=True)
    parser.add_argument("--freq", default=433500000, type=int)
    parser.add_argument("--rate", default=1000000, type=int)
    parser.add_argument("--baud", default=1000, type=int)
    parser.add_argument("--gain", default=0, type=int)
    parser.add_argument("--uri", default="ip:192.168.2.1")

    args = parser.parse_args()

    print("Connecting PlutoSDR...")
    sdr = adi.Pluto(args.uri)

    sdr.sample_rate = args.rate
    sdr.tx_lo = args.freq
    sdr.tx_hardwaregain_chan0 = args.gain
    sdr.tx_cyclic_buffer = False

    print("Encoding message:", args.msg)

    bits = text_to_bits(args.msg)

    samples = generate_fsk(
        bits,
        args.rate,
        args.baud,
        f0 = -10000,
        f1 = 10000
    )

    print("Transmitting...")
    sdr.tx(samples)

    print("Done")

if __name__ == "__main__":
    main()