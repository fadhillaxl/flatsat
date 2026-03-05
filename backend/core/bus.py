from threading import Lock

# Global lock for I2C bus access to prevent collisions between threads
i2c_lock = Lock()
