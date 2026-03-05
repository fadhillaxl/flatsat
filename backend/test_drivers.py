import sys
import time
import smbus2

def check_i2c_devices():
    print("Scanning I2C bus...")
    try:
        bus = smbus2.SMBus(1)
        found = []
        for device in range(128):
            try:
                bus.write_byte(device, 0)
                found.append(hex(device))
            except Exception:
                pass
        bus.close()
        print(f"Found I2C devices: {found}")
        return found
    except Exception as e:
        print(f"Error scanning I2C: {e}")
        return []

def test_ina219():
    print("\n[TEST] INA219 Power Sensor (0x40)...")
    try:
        from subsystems.eps import EPS
        eps = EPS()
        if eps.available:
            data = eps.read_power()
            print(f"✅ PASS: Voltage={data['voltage']}V, Current={data['current']}mA")
        else:
            print("❌ FAIL: EPS module not initialized (Library missing or I2C error)")
    except Exception as e:
        print(f"❌ FAIL: Exception {e}")

def test_mpu6050():
    print("\n[TEST] MPU6050 IMU (0x68)...")
    try:
        from subsystems.adcs import ADCS
        adcs = ADCS()
        if adcs.available:
            orient = adcs.read_orientation()
            temp = adcs.read_temperature()
            print(f"✅ PASS: Roll={orient['roll']:.2f}, Pitch={orient['pitch']:.2f}, Temp={temp:.2f}C")
        else:
            print("❌ FAIL: ADCS module not initialized")
    except Exception as e:
        print(f"❌ FAIL: Exception {e}")

def test_bmp280():
    print("\n[TEST] BMP280 Environment Sensor (0x76)...")
    try:
        from subsystems.environment import Environment
        env = Environment()
        if env.available:
            data = env.read_data()
            print(f"✅ PASS: Temp={data['temperature']:.2f}C, Pressure={data['pressure']:.2f}hPa, Alt={data['altitude']:.2f}m")
        else:
            print("❌ FAIL: Environment module not initialized")
    except Exception as e:
        print(f"❌ FAIL: Exception {e}")

def test_camera():
    print("\n[TEST] USB Camera...")
    try:
        from subsystems.payload import Payload
        import os
        payload = Payload()
        filename = "test_capture.jpg"
        if os.path.exists(filename):
            os.remove(filename)
            
        result = payload.capture(filename)
        if result and os.path.exists(result):
            size = os.path.getsize(result)
            print(f"✅ PASS: Image captured ({size} bytes)")
            # Clean up
            os.remove(result)
        else:
            print("⚠️ WARNING: Capture failed (Camera might be busy or missing)")
    except Exception as e:
        print(f"❌ FAIL: Exception {e}")

if __name__ == "__main__":
    print("=== FLATSAT HARDWARE DIAGNOSTICS ===")
    
    # Check I2C Bus first
    devices = check_i2c_devices()
    
    # Test individual drivers
    test_ina219()
    test_mpu6050()
    test_bmp280()
    test_camera()
    
    print("\n=== DIAGNOSTICS COMPLETE ===")
