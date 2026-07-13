# Contributing to piSysStatus

Thanks for helping improve piSysStatus. This guide covers local setup,
validation, and the pull request process.

## Ways to contribute

- **Report a bug** using the repository's bug report form.
- **Request a feature** using the feature request form.
- **Send a pull request** after opening an issue for non-trivial changes.
- **Report a vulnerability privately** by following [SECURITY.md](SECURITY.md).

## Prerequisites

- Python 3.12
- `shellcheck`
- gitleaks 8.30.1 or newer
- A Raspberry Pi with an SSD1306 I2C OLED display only when exercising the
  display loop end to end (development and validation work anywhere)

## Set up from a clean clone

```bash
git clone https://github.com/iamteedoh/piSysStatus.git
cd piSysStatus

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Never commit secrets, private hostnames, or paths and addresses specific to
your own network.

## Run the validation suite

Run the same checks that protect `main`:

```bash
python -m compileall -q .
python -c "import pi_status"
git ls-files '*.sh' | xargs -r shellcheck
bash -n install.sh
gitleaks git . --config .gitleaks.toml --redact --no-banner
```

When changing display behavior, test on real hardware where practical and
note the display size (128x32 or 128x64) and Pi model in the pull request.

## Project layout

- `pi_status.py` — the status display loop (temperature, hostname, IP, CPU,
  memory, disk) for SSD1306 OLED displays
- `install.sh` — dependency install, virtualenv creation, and systemd setup
- `pi-status.service` — systemd unit template installed by `install.sh`
- `requirements.txt` — Python dependencies
- `.github/workflows/` — source validation and source-only release automation

## Pull request process

1. Create a branch from `main`.
2. Make the smallest complete change and update documentation.
3. Run the full validation suite above.
4. Use a [Conventional Commit](https://www.conventionalcommits.org/) PR title:
   `feat:`, `fix:`, `docs:`, `refactor:`, `ci:`, `test:`, or `chore:`.
5. Complete the pull request template and link the related public issue.
6. Wait for all required checks to pass, then squash-merge.

The PR title becomes the squash commit subject and drives release-please:
`fix:` creates a patch release, `feat:` creates a minor release, and a `!` or
`BREAKING CHANGE:` footer creates a breaking release.

## License

By contributing, you agree that your contributions are licensed under the
project's [GNU General Public License v3](LICENSE).
