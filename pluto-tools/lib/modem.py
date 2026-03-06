import numpy as np

def text_to_bits(text):
    bits = []
    for c in text:
        bits.extend([int(b) for b in format(ord(c),'08b')])
    return bits


def bits_to_text(bits):

    chars = []

    for i in range(0,len(bits),8):

        byte = bits[i:i+8]

        val = int("".join(str(b) for b in byte),2)

        chars.append(chr(val))

    return "".join(chars)