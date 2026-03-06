#!/bin/bash

# Assign IP address to eth0 (interface for PlutoSDR)
echo "Configuring eth0 for PlutoSDR connection..."
sudo ifconfig eth0 192.168.2.10 netmask 255.255.255.0 up

# Check status
echo "Checking eth0 status:"
ifconfig eth0

# Ping PlutoSDR
echo "Pinging PlutoSDR (192.168.2.1)..."
ping -c 3 192.168.2.1
