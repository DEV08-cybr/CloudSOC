# ☁ CloudSOC

CloudSOC is a Terminal-based Cloud Security Operations Center built with Python and Textual.

It monitors cloud storage providers, detects security events, and provides a real-time dashboard.

---

# Features

- Dynamic Plugin System
- OneDrive Monitoring
- Google Drive Monitoring
- Storage Detection
- Event Logger
- Live Dashboard
- Cross Platform (Windows / Linux / macOS)

---

# Requirements

- Python 3.10+
- Git

Optional:

- rclone (Recommended)

---

# Installation

## Requirements

- Python 3.10+
- Git

Optional:

- rclone

## Windows

```powershell
git clone https://github.com/DEV08-cybr/CloudSOC.git
cd CloudSOC
python install.py
```

## Linux / macOS

```bash
git clone https://github.com/DEV08-cybr/CloudSOC.git
cd CloudSOC
python3 install.py
```

The installer automatically

- verifies project integrity
- checks Python
- checks pip
- installs dependencies
- installs CloudSOC
- checks rclone
- launches CloudSOC

No administrator privileges are required.

---

# Running CloudSOC

If you skipped launching during installation:

```bash
python -m cloudsoc.app
```

---

# Supported Platforms

- Windows 10
- Windows 11
- Ubuntu
- Fedora
- Debian
- Kali Linux
- Arch Linux
- Linux Mint
- macOS

---

# License

MIT License