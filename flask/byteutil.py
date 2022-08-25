

byte_mask = 0xFF

def to_bytes(n, byte_number):
	return [((byte_mask << shift) & n) >> shift for shift in reversed(range(0, byte_number * 8, 8))]
