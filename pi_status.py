#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Raspberry Pi System Status Display for UCTRONICS Pi Rack OLED
Displays: Temperature, Hostname, IP, CPU Load, Memory, Disk Space
"""

import time
import socket
import subprocess
import psutil
from pathlib import Path

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

# Display configuration
I2C_PORT = 1
I2C_ADDRESS = 0x3C  # Common address for UCTRONICS displays
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32  # UCTRONICS Pi Rack typically uses 128x32

# Refresh interval in seconds
REFRESH_INTERVAL = 2


def get_ip_address():
    """Get the primary IP address of the Pi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No IP"


def get_hostname():
    """Get the hostname of the Pi."""
    return socket.gethostname()


def get_cpu_temperature():
    """Get CPU temperature in Celsius."""
    try:
        temp_path = Path("/sys/class/thermal/thermal_zone0/temp")
        if temp_path.exists():
            temp = int(temp_path.read_text().strip()) / 1000.0
            return f"{temp:.1f}C"
    except Exception:
        pass

    # Fallback to vcgencmd
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Output is like "temp=45.0'C"
            temp_str = result.stdout.strip()
            temp = temp_str.replace("temp=", "").replace("'C", "")
            return f"{float(temp):.1f}C"
    except Exception:
        pass

    return "N/A"


def get_cpu_load():
    """Get CPU load percentage."""
    return f"{psutil.cpu_percent(interval=None):.0f}%"


def get_memory_usage():
    """Get memory usage percentage."""
    mem = psutil.virtual_memory()
    return f"{mem.percent:.0f}%"


def get_disk_usage():
    """Get disk usage percentage for root filesystem."""
    disk = psutil.disk_usage("/")
    return f"{disk.percent:.0f}%"


def create_display():
    """Initialize and return the OLED display device."""
    serial = i2c(port=I2C_PORT, address=I2C_ADDRESS)
    device = ssd1306(serial, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
    return device


def get_font(size=10):
    """Load a font, falling back to default if needed."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except (IOError, OSError):
            continue

    # Fallback to default font
    return ImageFont.load_default()


def draw_status(device):
    """Draw system status on the OLED display."""
    font_small = get_font(8)
    font_medium = get_font(10)

    hostname = get_hostname()
    ip = get_ip_address()
    temp = get_cpu_temperature()
    cpu = get_cpu_load()
    mem = get_memory_usage()
    disk = get_disk_usage()

    with canvas(device) as draw:
        # Line 1: Hostname and Temperature
        draw.text((0, 0), f"{hostname}", font=font_medium, fill="white")
        draw.text((90, 0), f"{temp}", font=font_medium, fill="white")

        # Line 2: IP Address
        draw.text((0, 11), f"IP:{ip}", font=font_small, fill="white")

        # Line 3: CPU, Memory, Disk
        draw.text((0, 22), f"C:{cpu}", font=font_small, fill="white")
        draw.text((42, 22), f"M:{mem}", font=font_small, fill="white")
        draw.text((88, 22), f"D:{disk}", font=font_small, fill="white")


def draw_status_64(device):
    """Draw system status on 128x64 OLED display (alternative layout)."""
    font_small = get_font(10)
    font_medium = get_font(12)

    hostname = get_hostname()
    ip = get_ip_address()
    temp = get_cpu_temperature()
    cpu = get_cpu_load()
    mem = get_memory_usage()
    disk = get_disk_usage()

    with canvas(device) as draw:
        # Line 1: Hostname
        draw.text((0, 0), f"Host: {hostname}", font=font_medium, fill="white")

        # Line 2: IP Address
        draw.text((0, 14), f"IP: {ip}", font=font_small, fill="white")

        # Line 3: Temperature
        draw.text((0, 26), f"Temp: {temp}", font=font_small, fill="white")

        # Line 4: CPU Load
        draw.text((0, 38), f"CPU: {cpu}  Mem: {mem}", font=font_small, fill="white")

        # Line 5: Disk
        draw.text((0, 50), f"Disk: {disk}", font=font_small, fill="white")


def main():
    """Main loop to update the display."""
    print("Initializing Pi Status Display...")
    print(f"I2C Port: {I2C_PORT}, Address: 0x{I2C_ADDRESS:02X}")

    try:
        device = create_display()
        print(f"Display initialized: {DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
    except Exception as e:
        print(f"Error initializing display: {e}")
        print("\nTroubleshooting tips:")
        print("1. Enable I2C: sudo raspi-config -> Interface Options -> I2C")
        print("2. Check I2C address: sudo i2cdetect -y 1")
        print("3. Install dependencies: pip install -r requirements.txt")
        return 1

    # Initialize CPU percentage measurement
    psutil.cpu_percent(interval=None)

    print("Starting display loop (Ctrl+C to stop)...")

    try:
        while True:
            if DISPLAY_HEIGHT == 64:
                draw_status_64(device)
            else:
                draw_status(device)
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\nShutting down...")
        device.cleanup()

    return 0


if __name__ == "__main__":
    exit(main())
