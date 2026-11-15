---
title: Managing Profiles and Your Collection
description: Create isolated study profiles in AnkiDraft, manage per-profile SQLite databases and media folders, and protect your local data with backups.
---

AnkiDraft lets you completely isolate multiple collections using **user profiles**.

## 1. Why Use Multiple Profiles?

Each profile has its own SQLite database (`ankidraft.db`), `media/` folder, `staging/` area, and `backups/` snapshots. This makes profiles ideal for **splitting your work into large, focused collections**:
- **Separate your personal notes from your academic years** (e.g., *Personal Notes / Languages*, *Year 1 Med School*, *Year 2 Med School*, *Exam Prep*).
- **Avoid getting lost in bulky documents**: imported study materials (PDF textbooks, lecture slides, video transcripts) can quickly become quite large. Isolating each major area in its own profile keeps your library clean, fast, and easy to navigate.

## 2. Creating, Transferring, or Switching Profiles

1. Click **`Profil : <name>`** at the bottom of the left sidebar (or use the startup *Workspaces & Profiles* dialog).
2. Enter a clear name and click **+ Create** to add a new independent space, or select an existing profile to switch.
3. AnkiDraft automatically locks the active profile (`ProfileLockService`) to prevent concurrent write conflicts across windows.
4. Click **Transfer...** to selectively copy decks, tags, note types, or image albums from another profile into the active one, or **Delete this space** to remove an unused unlocked profile.

## 3. Automatic Backups

AnkiDraft automatically saves timestamped SQLite snapshots inside the profile's `backups/` subfolder (retaining up to 5 recent backups on startup as well as creating a safety snapshot before sensitive actions like replacing your collection from a `.colpkg` archive).
