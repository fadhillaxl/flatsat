import adi
import argparse
from lib.modem import text_to_bits
from lib.fsk import generate_fsk
from lib.framing import create_packet

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

# Convert text to bits
payload_bits = text_to_bits(args.msg)

# Wrap in packet (Preamble + Sync + Length + Payload)
packet_bits = create_packet(payload_bits)

# Generate FSK samples
samples = generate_fsk(packet_bits, args.rate, args.baud, -10000, 10000)

print(f"TX: {args.msg} (Total bits: {len(packet_bits)})")

# Repeat transmission a few times to ensure reception
# (Since we don't have a continuous TX stream)
for i in range(3):
    sdr.tx(samples)
