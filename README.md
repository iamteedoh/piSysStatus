# piSysStatus

A small system-status display for Raspberry Pi rack OLED screens (such as the
UCTRONICS Pi Rack's SSD1306 I2C display). It shows, on a loop:

- Hostname and CPU temperature
- IP address
- CPU load, memory usage, and disk usage

It supports 128x32 displays (default, compact three-line layout) and 128x64
displays (five-line layout).

## Requirements

- A Raspberry Pi with I2C enabled
  (`sudo raspi-config` → Interface Options → I2C)
- An SSD1306-compatible I2C OLED display (commonly at address `0x3C`)
- Python 3 with the packages in `requirements.txt`
  (`luma.oled`, `luma.core`, `psutil`, `Pillow`)

## Install

Clone the repository onto the Pi and run the installer:

```bash
git clone https://github.com/iamteedoh/piSysStatus.git
cd piSysStatus
./install.sh
```

The installer:

1. Installs the required apt packages (Python tooling, image libraries,
   `i2c-tools`, fonts).
2. Creates a `venv/` virtual environment in the repository directory and
   installs `requirements.txt` into it.
3. Scans the I2C bus so you can confirm the display address.
4. Rewrites `pi-status.service` to point at wherever you cloned the
   repository, then installs it to `/etc/systemd/system/`.

It does not start the service for you. To run and enable it:

```bash
sudo systemctl start pi-status
sudo systemctl enable pi-status   # start on boot
sudo systemctl status pi-status
```

The service runs as `root` so it can access the I2C bus without extra group
setup.

## Run manually

```bash
./venv/bin/python pi_status.py
```

Press Ctrl+C to stop; the display is cleaned up on exit.

## Configuration

Settings are constants at the top of `pi_status.py`:

| Constant | Default | Meaning |
|---|---|---|
| `I2C_PORT` | `1` | I2C bus number (bus 1 on modern Pis) |
| `I2C_ADDRESS` | `0x3C` | Display address; some displays use `0x3D` |
| `DISPLAY_WIDTH` | `128` | Display width in pixels |
| `DISPLAY_HEIGHT` | `32` | Display height; set to `64` for the 128x64 layout |
| `REFRESH_INTERVAL` | `2` | Seconds between screen refreshes |

Edit the constants and restart the service
(`sudo systemctl restart pi-status`) to apply changes.

## Troubleshooting

If nothing appears on the display:

1. Confirm I2C is enabled: `sudo raspi-config` → Interface Options → I2C.
2. Find the display address: `sudo i2cdetect -y 1` (common: `0x3C` or `0x3D`).
3. Update `I2C_ADDRESS` in `pi_status.py` if it differs.

## License

piSysStatus is licensed under the
[GNU General Public License v3](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, the validation suite,
and the pull request process.

## Security

Please report vulnerabilities privately as described in
[SECURITY.md](SECURITY.md).
