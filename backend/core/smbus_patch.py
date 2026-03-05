import sys
import smbus2

# Patch smbus module if not present, using smbus2
if 'smbus' not in sys.modules:
    sys.modules['smbus'] = smbus2
