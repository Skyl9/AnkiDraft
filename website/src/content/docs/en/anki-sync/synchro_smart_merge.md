---
title: Synchronization, Duplicates, and Smart Merge
description: Resolve conflicts during Anki imports with Smart Merge, preserve existing review schedules, and clean up duplicate flashcards automatically.
---

When collaborating on a shared deck or editing a flashcard in both Anki and AnkiDraft, **Smart Merge** protects your work.

## 1. When Smart Merge Triggers & 3-Pane Resolution

During an `.apkg` or `.txt` import, whenever an incoming note matches an existing **GUID** in AnkiDraft:
- **If the note has no local manual edits, merges, or version restores**: the incoming update is applied **silently** with no conflict prompt.
- **If content differs and the note has protected local edits**: **Smart Merge** opens with a **Similarity (%)** badge and **3 panes**:
  1. Left (red, read-only): **Local AnkiForge Base**;
  2. Center (blue, **editable**): **Merged Result (Interactive)** with per-field transfer arrows (`◀` / `▶`) and `Different` / `Identical` badges;
  3. Right (green, read-only): **Incoming Base (`.apkg`)**.

Built-in Smart Merge shortcuts: <kbd>Alt+Left</kbd> / <kbd>Alt+Right</kbd> (prev/next conflict), <kbd>Ctrl+Alt+Left</kbd> (**Keep All Local**), <kbd>Ctrl+Alt+Right</kbd> (**Keep All Incoming**), and <kbd>Ctrl+Enter</kbd> (**Confirm Merge**).

## 2. Duplicates, Merges, and Media Hygiene

- **Merges & Duplicates**: from **Analysis & AI Audit** (<kbd>Alt+4</kbd>) › **Merges & Duplicates**, the quick scan in **Editor & Browser** (<kbd>Alt+3</kbd>), or your connected [MCP assistant](/en/ai-setup/consultant_mcp/), detect exact and near-duplicates (Levenshtein similarity) to merge redundant cards safely.
- **Media & Storage**: imported media files are MD5-deduplicated and Zstandard-decompressed when needed; orphaned media and TTS audio cache can be purged under **Settings** (<kbd>Ctrl+,</kbd>) › **Storage**.
