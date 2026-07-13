#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Installation script for Pi System Status OLED Display

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="pi-status"

echo "=== Pi System Status OLED Display Installer ==="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
fi

# Check for I2C
if ! lsmod | grep -q i2c; then
    echo "Warning: I2C module not loaded. Enable I2C with:"
    echo "  sudo raspi-config -> Interface Options -> I2C"
    echo ""
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-dev \
    libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5 \
    i2c-tools fonts-dejavu

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv "$SCRIPT_DIR/venv"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install --upgrade pip
"$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

# Detect I2C address
echo ""
echo "Scanning for I2C devices..."
if command -v i2cdetect &> /dev/null; then
    i2cdetect -y 1 || echo "Could not scan I2C bus. Make sure I2C is enabled."
fi

# Update service file with correct path
echo ""
echo "Configuring systemd service..."
sed -i "s|/opt/piSysStatus|$SCRIPT_DIR|g" "$SCRIPT_DIR/pi-status.service"

# Install systemd service
sudo cp "$SCRIPT_DIR/pi-status.service" /etc/systemd/system/
sudo systemctl daemon-reload

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To test the display manually:"
echo "  $SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/pi_status.py"
echo ""
echo "To start the service:"
echo "  sudo systemctl start $SERVICE_NAME"
echo ""
echo "To enable auto-start on boot:"
echo "  sudo systemctl enable $SERVICE_NAME"
echo ""
echo "To check service status:"
echo "  sudo systemctl status $SERVICE_NAME"
echo ""
echo "If you see nothing on the display, check:"
echo "1. I2C is enabled: sudo raspi-config -> Interface Options -> I2C"
echo "2. I2C address: sudo i2cdetect -y 1 (common: 0x3C or 0x3D)"
echo "3. Edit I2C_ADDRESS in pi_status.py if needed"
