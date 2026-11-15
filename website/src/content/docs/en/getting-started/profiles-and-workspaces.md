---
title: Managing Profiles and Your Collection
description: Create isolated study profiles in AnkiDraft, manage per-profile SQLite databases and media folders, and protect your local data with backups.
---

AnkiDraft lets you completely isolate multiple collections using **user profiles**.

## 1. Why Use Multiple Profiles?

Each profile has its own SQLite database and dedicated media folder (images, audio). This makes profiles ideal for **splitting your work into large, focused collections**:
- **Separate your personal notes from your academic years** (e.g., *Personal Notes / Languages*, *Year 1 Med School*, *Year 2 Med School*, *Exam Prep*).
- **Avoid getting lost in bulky documents**: imported study materials (PDF textbooks, lecture slides, video transcripts) can quickly become quite large. Isolating each major area in its own profile keeps your library clean, fast, and easy to navigate.

## 2. Creating or Switching Profiles

1. Open the profile selector from the application header or at startup.
2. Click **New Profile** and give it a clear name.
3. Switch between profiles in one click: AnkiDraft automatically locks the active profile to prevent concurrent write conflicts.

## 3. Automatic Backups

Before any sensitive operation (such as replacing your collection from a `.colpkg` archive or applying an update), AnkiDraft automatically creates a timestamped backup of your local database inside your profile folder.
