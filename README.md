# 🚀 Shift OS 26.03.1 "Harmonia"

![OS](https://img.shields.io/badge/OS-Linux-orange.svg)
![Base](https://img.shields.io/badge/Base-Ubuntu_24.04_LTS-E95420.svg)
![Desktop](https://img.shields.io/badge/Desktop-GNOME_46-4A86E8.svg)
![Display Server](https://img.shields.io/badge/Display-Wayland-0078D7.svg)
![Kernel](https://img.shields.io/badge/Kernel-6.8-333333.svg)
![Architecture](https://img.shields.io/badge/Arch-amd64-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> *"An OS that gets out of your way and lets you create."*

**Shift OS** is a custom, high-performance Linux distribution built for developers, creators, and gamers. Based on the rock-solid foundation of Ubuntu 24.04 LTS, Shift OS strips away the bloatware and delivers a pure, blazing-fast GNOME 46 experience out of the box.

---

## 📋 Table of Contents

- [Why Shift OS?](#-why-shift-os)
- [Exclusive Features](#-exclusive-features)
- [Screenshots](#-screenshots)
- [System Requirements](#-system-requirements)
- [What's Included](#-whats-included)
- [Download & Installation](#-download--installation)
- [Building from Source](#-building-from-source)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Community & Support](#-community--support)
- [License](#-license)

---

## ✨ Why Shift OS?

Most Linux distributions either ship bloated with software you never asked for, or strip things down so much they're unusable out of the box. **Harmonia** hits the sweet spot:

- 🚀 **Blazing Fast:** Idles at just ~700MB RAM. Optimized systemd services mean no hidden background processes eating your resources.
- 🛡️ **Rock-Solid Base:** Built on Ubuntu 24.04 LTS with Linux Kernel 6.8. You get 5 years of security updates and maximum hardware compatibility.
- 🎨 **Pure GNOME 46:** Unmodified, stock GNOME desktop running on Wayland by default for tear-free rendering and beautiful animations.
- 🛠️ **Creator-Ready:** Whether you use Godot, VS Code, Docker, or OBS Studio, your workflow starts the moment you log in.
- 🔒 **Privacy First:** Zero telemetry. Zero ads. Your machine, your data.
- 📦 **Full Ubuntu Compatibility:** Access millions of packages via APT, plus Flatpak support with Flathub pre-configured.

---

## 🌟 Exclusive Features

### 🎉 Shift Welcome App
A custom-built, interactive GTK3 onboarding wizard written in Python. Features include:
- **System Health Monitor** — live checks for system updates, firewall status, and network connectivity
- **Developer Setup Wizard** — select your tech stack (Python, Node.js, Go, Rust, Docker, databases, and more) and generate a one-click install script
- **Keyboard Shortcuts Cheatsheet** — searchable reference for Navigation, System, Terminal, and Text shortcuts
- **Privacy & Security Tools** — quick access to UFW firewall, GNOME Privacy Settings, and security tips
- **Theme & Appearance** — shortcuts to Wallpaper, Color Scheme, GNOME Tweaks, and recommended extensions
- **System Information + CPU Benchmark** — auto-detected hardware info with a built-in benchmark tool
- **Getting Started Checklist** — trackable progress checklist for post-install setup steps
- **App Recommendations** — curated app list with live install status detection

### 🖥️ Other Highlights
- **Pre-configured Flatpak + Flathub** — sandboxed apps ready from day one
- **Calamares Graphical Installer** — get up and running in under 10 minutes
- **Full Live Session** — try before you install, no data touched
- **Out-of-the-box Codecs** — play any media format instantly without hunting for decoders
- **Clean Boot** — no snap, no Amazon lens, no unnecessary background daemons

---

## 📸 Screenshots

> *(Add your screenshots here)*

| Desktop Overview | Shift Welcome App |
|---|---|
| *(screenshot)* | *(screenshot)* |

| App Grid | Terminal |
|---|---|
| *(screenshot)* | *(screenshot)* |

---

## 💻 System Requirements

| | Minimum | Recommended |
|---|---|---|
| **Processor** | 64-bit dual-core, 2 GHz | 64-bit quad-core, 2.5 GHz+ |
| **Memory** | 4 GB RAM | 8 GB RAM or more |
| **Storage** | 25 GB free space | 50 GB SSD |
| **Graphics** | VGA 1024×768 | Intel / AMD / NVIDIA GPU |
| **Network** | Optional | Broadband for updates |
| **Architecture** | amd64 (x86_64) | amd64 (x86_64) |

---

## 📦 What's Included

### Pre-installed Software
| Category | Apps |
|---|---|
| Browser | Firefox (via Flatpak) |
| Code Editor | Visual Studio Code |
| Game Engine | Godot 4 |
| Version Control | Git |
| Terminal | GNOME Terminal |
| Text Editor | GNOME Text Editor |
| Files | GNOME Files (Nautilus) |
| Package Manager | APT + Flatpak |
| Installer | Calamares |

### Technical Specs
| Component | Version |
|---|---|
| Base | Ubuntu 24.04 LTS "Noble Numbat" |
| Kernel | Linux 6.8 |
| Desktop Environment | GNOME 46 (unmodified) |
| Display Server | Wayland (default) · X11 (fallback) |
| Init System | systemd |
| Package Manager | APT · dpkg · Flatpak |
| Default Filesystem | ext4 |
| Default Shell | bash |
| Installer | Calamares (graphical) |

---

## 📥 Download & Installation

### Step 1 — Download the ISO
Download the latest ISO from the releases page:

👉 **[Download Shift OS Harmonia ISO](https://github.com/Kharisdestianmaulana/shift-os/releases)**

> ISO size: ~4.2 GB | Codename: Harmonia | Architecture: amd64

### Step 2 — Verify the ISO *(optional but recommended)*
```bash
sha256sum shift-os-26.03.1-amd64.iso
# Compare with the SHA256 checksum posted on the releases page
```

### Step 3 — Flash to USB
Use any of these tools to flash the ISO to a USB drive (minimum 8 GB):
- **[Rufus](https://rufus.ie/)** — Windows
- **[BalenaEtcher](https://balena.io/etcher/)** — Windows / macOS / Linux
- **[Ventoy](https://www.ventoy.net/)** — Multi-boot USB

```bash
# Or on Linux via terminal (replace /dev/sdX with your USB device):
sudo dd if=shift-os-26.03.1-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

### Step 4 — Boot & Install
1. Restart your PC and boot from the USB drive (usually F12, F2, or Del to enter boot menu)
2. Choose **"Try or Install Shift OS"**
3. Once in the live session, click the **"Install Shift OS"** icon on the desktop
4. Follow the Calamares installer — the whole process takes around 10 minutes
5. Reboot, remove the USB, and enjoy Shift OS! 🎉

---

## 🔧 Building from Source

Shift OS is built using **[Cubic](https://github.com/PJ-Singh-001/Cubic)** (Custom Ubuntu ISO Creator).

### Prerequisites
```bash
sudo apt-add-repository ppa:cubic-wizard/release
sudo apt update
sudo apt install cubic
```

### Build Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/Kharisdestianmaulana/shift-os.git
   cd shift-os
   ```
2. Open Cubic and point it to the `cubic-project/` directory in this repo
3. The `custom-disk/` folder contains all customizations applied to the base Ubuntu ISO
4. Generate the ISO from within Cubic

### Installing the Welcome App
```bash
# Copy the welcome app to the system
sudo cp welcome/shift-welcome.py /usr/local/bin/shift-welcome
sudo chmod +x /usr/local/bin/shift-welcome

# Set it to run on first login (autostart)
mkdir -p ~/.config/autostart
cp welcome/shift-welcome.desktop ~/.config/autostart/
```

> **Dependencies:** `python3`, `python3-gi`, `gir1.2-gtk-3.0`

---

## 📁 Project Structure

```
shift-os/
├── cubic-project/          # Cubic project directory
│   └── custom-disk/        # All ISO customizations
│       ├── etc/            # System config files
│       ├── usr/            # Custom user-space additions
│       └── casper/         # Live session config
├── welcome/                # Shift Welcome App source
│   ├── shift-welcome.py    # Main GTK3 app
│   ├── shift-welcome.desktop  # Autostart entry
│   └── logo.png            # App icon
├── assets/                 # Wallpapers, icons, branding
├── docs/                   # Documentation
└── README.md
```

---

## 🗺️ Roadmap

| Version | Codename | Status | Highlights |
|---|---|---|---|
| v26.03.1 | Harmonia | ✅ Released | Initial release, pure GNOME 46, Wayland, Calamares |
| v26.09 | Serenity | 🔄 In Progress | NVIDIA driver integration, Shift Welcome App v2, GNOME 47 |
| v27.03 | Aurora | 📋 Planned | ARM support, Shift App Center, online accounts manager |
| Future | Shift OS Pro | 💡 Concept | Enterprise edition, LTS kernel, commercial support |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** — Open an [issue](https://github.com/Kharisdestianmaulana/shift-os/issues)
2. **Suggest features** — Use the [feature request template](https://github.com/Kharisdestianmaulana/shift-os/issues/new)
3. **Improve the Welcome App** — Fork the repo, make changes to `welcome/shift-welcome.py`, and open a pull request
4. **Translations** — Help translate the Welcome App to other languages
5. **Documentation** — Improve this README or add wiki pages

### Development Setup for the Welcome App
```bash
git clone https://github.com/Kharisdestianmaulana/shift-os.git
cd shift-os/welcome

# Install dependencies
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-gdkpixbuf-2.0

# Run the app
python3 shift-welcome.py
```

---

## 🌐 Community & Support

- **Developer:** Kharis Destian Maulana ([@riray-hub](https://github.com/riray-hub))
- **Website:** [shift-os.netlify.app](https://shift-os.netlify.app)
- **Email:** kharisdestian862@gmail.com
- **Telegram:** [t.me/shiftos](https://t.me/shiftos)
- **Discord:** [discord.gg/shiftos](https://discord.gg/shiftos)

Found a bug? Please [open an issue](https://github.com/Kharisdestianmaulana/shift-os/issues) — don't email security vulnerabilities publicly.

---

## 📜 License

Shift OS is an open-source project.

- **Custom tools** (Welcome App, scripts, configs): [MIT License](LICENSE)
- **Ubuntu/Debian packages**: [GNU GPL and various open-source licenses](https://ubuntu.com/legal)
- **GNOME Desktop Environment**: [GPL v2+](https://www.gnome.org/licensing/)
- **Linux Kernel**: [GPL v2](https://www.kernel.org/doc/html/latest/process/license-rules.html)

---

<div align="center">

Made with ❤️ in Indonesia by **Kharis Destian Maulana**

*Shift OS — Elegance Meets Pure Performance*

</div>
