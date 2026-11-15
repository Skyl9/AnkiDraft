---
title: Installing AnkiDraft
description: "Download, install, and update AnkiDraft on macOS, Windows, and Linux from the latest official GitHub release with Ed25519 signature verification."
---

AnkiDraft is a standalone desktop application. You do not need to install Python or any developer tools on your computer.

## 1. Download the Installer (Latest Release)

Visit the [AnkiDraft homepage](https://ankidraft.app/en/#download) or go straight to the [latest GitHub release](https://github.com/Skyl9/AnkiDraft/releases/latest) to automatically fetch the package for your system:

| Operating System | Published Formats (`releases/latest`) | System Requirements |
| :--- | :--- | :--- |
| **macOS** | Disk image `.dmg` (Apple Silicon) or `.zip` archive | macOS 13 (Ventura) or newer, Apple Silicon chip (M1/M2/M3/M4) |
| **Windows** | Standalone `.exe` installer or portable `.zip` archive | Windows 10 or Windows 11 (64-bit) |
| **Linux** | Portable `.AppImage` executable or `.tar.gz` archive | Modern 64-bit Linux distribution (Ubuntu 22.04+, Fedora, Arch) |

## 2. Step-by-Step Setup

### On macOS
1. Double-click the `.dmg` disk image downloaded from the [latest release](https://github.com/Skyl9/AnkiDraft/releases/latest).
2. Drag the application icon into your **Applications** folder.
3. Launch the app from Launchpad or Spotlight.

### On Windows
1. If you download the `.exe` installer, double-click it and follow the wizard (no administrator rights required for a user-level installation).
2. If you download the portable `.zip` archive, extract it and run the main executable.

### On Linux (AppImage)
1. Make the downloaded `.AppImage` file executable:
   ```bash
   chmod +x *.AppImage
   ```
2. Launch the application by double-clicking it or executing it in your terminal.

## 3. Where Is Your Data Stored?

All your study data stays locally on your drive inside `~/.ankidraft/profiles/<profile_name>/`:
- `ankidraft.db`: your local SQLite database of cards, documents, and history.
- `media/`: images and audio clips attached to your flashcards.

## 4. Automatic Updates

AnkiDraft automatically checks for official releases and verifies both the cryptographic signature (Ed25519) and SHA-256 checksum before installing any update.
