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
3. **First launch:** official macOS releases are notarized by Apple; if you install a nightly or unsigned build and macOS shows a Gatekeeper warning:
   - Open **System Settings** → **Privacy & Security**, scroll to **Security**, and click **Open Anyway** for AnkiDraft (or **Right-click** → **Open** on the app in Applications).
   - You only need to do this **once** for that installation.

### On Windows *(not yet tested in production)*
1. If you download the `.exe` installer, double-click it and follow the wizard (no administrator rights required for a user-level installation).
2. If you download the portable `.zip` archive, extract it and run the main executable.

### On Linux (AppImage) *(not yet tested in production)*
1. Make the downloaded `.AppImage` file executable:
   ```bash
   chmod +x *.AppImage
   ```
2. Launch the application by double-clicking it or executing it in your terminal.

## 3. Where Is Your Data Stored?

All your study data stays locally on your drive inside your user folder:
- **macOS:** `/Users/<your-name>/.ankidraft/profiles/<profile_name>/`
- **Windows:** `C:\Users\<YourName>\.ankidraft\profiles\<profile_name>\`
- **Linux:** `/home/<your-name>/.ankidraft/profiles/<profile_name>/`

Each profile contains:
- `ankidraft.db`: your local SQLite database of cards, documents, and history.
- `media/`: images and audio clips attached to your flashcards.
- `backups/`: automatic local snapshots (up to 5 recent backups kept on startup and before sensitive operations).
- `staging/`: isolated temporary workspace for staged transfers and MCP file staging.

## 4. Automatic Updates

AnkiDraft automatically checks for official releases and verifies both the SHA-256 manifest (`checksums.txt`) and its Ed25519 cryptographic signature (`checksums.txt.sig`) when provided.

## 5. Report an Issue or Suggest Improvements

If you run into a bug, if your operating system is not yet available, or if you have ideas for improvements, please open an issue on [GitHub Issues](https://github.com/Skyl9/AnkiDraft/issues).
