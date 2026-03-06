import numpy as np

# Preamble: 0xAA (10101010) repeated 4 times
PREAMBLE = [1, 0] * 16

# Sync Word: 0x2DD4 (0010 1101 1101 0100)
SYNC_WORD = [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0]

def create_packet(bits):
    """
    Wraps payload bits with Preamble + Sync Word + Length + Payload
    """
    # Calculate length (in bytes)
    length = len(bits) // 8
    length_bits = [int(b) for b in format(length, '08b')]
    
    return PREAMBLE + SYNC_WORD + length_bits + bits

def find_packet(demodulated_bits):
    """
    Searches for Sync Word in the bit stream and extracts the packet.
    Returns: (found_bool, payload_bits)
    """
    bits = np.array(demodulated_bits)
    sync = np.array(SYNC_WORD)
    
    # Simple correlation
    # We look for where the bits match the sync word
    # This is not efficient for huge streams but fine for short bursts
    
    threshold = len(SYNC_WORD) - 2 # Allow up to 2 bit errors in sync word
    
    for i in range(len(bits) - len(SYNC_WORD) - 8):
        window = bits[i : i+len(SYNC_WORD)]
        matches = np.sum(window == sync)
        
        if matches >= threshold:
            # Sync found!
            # Next 8 bits are length
            len_start = i + len(SYNC_WORD)
            len_bits = bits[len_start : len_start+8]
            
            # Decode length
            length_val = int("".join(str(b) for b in len_bits), 2)
            
            # Extract payload
            payload_start = len_start + 8
            payload_end = payload_start + (length_val * 8)
            
            if payload_end <= len(bits):
                return True, list(bits[payload_start:payload_end])
                
    return False, []
