#!/bin/bash
# Install system dependencies
sudo apt update
sudo apt install -y fswebcam python3-pip i2c-tools libopencv-dev python3-opencv python3-smbus

# Enable I2C interface (if not already enabled)
sudo raspi-config nonint do_i2c 0

# Note: Some Python packages rely on system libraries (like opencv)
# The pip install command will handle the Python dependencies
pip install pi-ina219 mpu6050-raspberrypi bmp280 smbus2
