# Security Policy

## Reporting a vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

Use GitHub's private vulnerability reporting instead:

1. Open the repository's **Security** tab.
2. Select **Report a vulnerability**.
3. Provide the details requested below.

If private reporting is unavailable, contact the maintainer through the
[iamteedoh GitHub profile](https://github.com/iamteedoh).

## What to include

- A description of the issue and its potential impact
- Reproduction steps or a minimal proof of concept
- The affected release, commit, platform, and component
- A suggested remediation, if known

Never include passwords, SSH keys, private hostnames, private IP addresses,
or unredacted logs in a report.

## Security-sensitive areas

piSysStatus runs as a privileged system service on the host it monitors, so
the most sensitive surfaces are:

- `install.sh`, which runs `apt-get`, writes to `/etc/systemd/system/`, and
  reloads systemd via `sudo`
- `pi-status.service`, which runs the display loop as `root` for I2C access
- Subprocess execution in `pi_status.py` (the `vcgencmd` temperature fallback)
- Reads of `/sys/class/thermal` and the outbound UDP socket used to discover
  the local IP address
- Third-party dependency handling in `requirements.txt`

## Supported versions

Security fixes land on `main` and ship in the next tagged source release. Test
against the latest release or `main` before reporting an issue.
