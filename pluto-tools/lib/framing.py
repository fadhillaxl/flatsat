import numpy as np

# Preamble: 0xAA (10101010) repeated 4 times
# Note: In Manchester, 1 -> 10, 0 -> 01 (or vice versa).
# 0xAA (10101010) in bits becomes 1001100110011001 in Manchester
PREAMBLE = [1, 0] * 16

# Sync Word: 0x2DD4 (0010 1101 1101 0100)
SYNC_WORD = [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0]

def manchester_encode(bits):
    """
    Encodes bits using Manchester encoding (IEEE 802.3 convention):
    0 -> 01
    1 -> 10
    Returns list of bits (2x length)
    """
    encoded = []
    for b in bits:
        if b == 1:
            encoded.extend([1, 0])
        else:
            encoded.extend([0, 1])
    return encoded

def manchester_decode(bits):
    """
    Decodes Manchester encoded bits.
    Expects aligned bits.
    01 -> 0
    10 -> 1
    Returns list of decoded bits (0.5x length)
    """
    decoded = []
    # Process in pairs
    for i in range(0, len(bits)-1, 2):
        pair = (bits[i], bits[i+1])
        if pair == (0, 1):
            decoded.append(0)
        elif pair == (1, 0):
            decoded.append(1)
        else:
            # Error (00 or 11) - valid Manchester must transition
            # For simplicity, we can guess or mark error. 
            # Here we just treat 11 as 1 and 00 as 0 (effectively NRZ fallback)
            # or better, skip/abort. Let's append the first bit as fallback.
            decoded.append(bits[i]) 
    return decoded

def create_packet(bits):
    """
    Wraps payload bits with Preamble + Sync Word + Length + Payload
    Applies Manchester Encoding to the Payload + Length (Preamble/Sync are raw)
    """
    # Calculate length (in bytes)
    length = len(bits) // 8
    length_bits = [int(b) for b in format(length, '08b')]
    
    # We want to Manchester encode the data part to ensure transitions
    data_to_encode = length_bits + bits
    encoded_data = manchester_encode(data_to_encode)
    
    # Preamble and Sync are sent RAW (NRZ) to allow easy detection
    # Ideally Sync should also be Manchester but kept unique, 
    # but mixing NRZ header with Manchester body is a common simple protocol.
    
    return PREAMBLE + SYNC_WORD + encoded_data

def find_packet(demodulated_bits):
    """
    Searches for Sync Word in the bit stream and extracts the packet.
    Returns: (found_bool, payload_bits)
    """
    bits = np.array(demodulated_bits)
    sync = np.array(SYNC_WORD)
    
    threshold = len(SYNC_WORD) - 2 
    
    for i in range(len(bits) - len(SYNC_WORD) - 16): # Extra buffer
        window = bits[i : i+len(SYNC_WORD)]
        matches = np.sum(window == sync)
        
        if matches >= threshold:
            # Sync found!
            # The rest of the packet is Manchester encoded.
            
            # Start of encoded data
            data_start = i + len(SYNC_WORD)
            
            # Decode length first (8 bits data = 16 bits encoded)
            len_encoded = bits[data_start : data_start+16]
            len_decoded = manchester_decode(len_encoded)
            
            # Decode length value
            if len(len_decoded) < 8: return False, []
            length_val = int("".join(str(b) for b in len_decoded), 2)
            
            if length_val > 64: continue # Sanity check
            
            # Calculate total encoded payload length
            # length_val bytes * 8 bits/byte * 2 symbols/bit
            payload_encoded_len = length_val * 8 * 2
            
            payload_start = data_start + 16
            payload_end = payload_start + payload_encoded_len
            
            if payload_end <= len(bits):
                encoded_payload = bits[payload_start:payload_end]
                decoded_payload = manchester_decode(encoded_payload)
                return True, decoded_payload
                
    return False, []
