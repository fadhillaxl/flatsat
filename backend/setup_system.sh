#!/bin/bash
# Install system dependencies
sudo apt update
sudo apt install -y fswebcam python3-pip i2c-tools libopencv-dev python3-opencv

# Note: Some Python packages rely on system libraries (like opencv)
# The pip install command will handle the Python dependencies
