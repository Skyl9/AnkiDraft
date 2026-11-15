---
title: Exporting Your Decks to Anki (.apkg)
description: Generate a clean, ready-to-study .apkg deck for Anki Desktop, AnkiWeb, and AnkiMobile with stable IDs and without losing your review history.
---

Once your flashcards are created and reviewed in AnkiDraft, transfer them to Anki in seconds using the `.apkg` exporter.

## 1. Exporting a Deck or Selection (.apkg)

1. Press <kbd>Ctrl+Alt+E</kbd> (globally, outside **Note Types**) or click **Export Anki Cards (.apkg)** in **Editor & Browser** (<kbd>Alt+3</kbd>).
2. Pick a specific deck (including `Subject::Chapter` sub-decks) or **All Decks (Entire Collection)**.
3. Choose the scope (**All cards in deck** or **New cards only (`new` status)**) and keep checked as needed:
   - **Include all associated media (images and audio)**;
   - **Sync flags and suspensions as tags (`flag::color`, `is::suspended`)**.
4. Click **Export Package** to save the `.apkg` file.

:::tip[Native Flags & Suspended Cards in Anki Desktop]
AnkiDraft exports each note's stable GUID alongside native card flags and suspended status. To restore native flags and suspensions in Anki Desktop on import, check **"Import any scheduling information"** in Anki Desktop; otherwise `flag::...` and `is::suspended` tags remain immediately filterable.
:::

## 2. Updating Cards in Anki Without Overwriting FSRS / SM-2

AnkiDraft **never** injects FSRS or SM-2 review history/scheduling into `.apkg` files. Because each note retains a stable **GUID**, re-importing an updated `.apkg` into Anki Desktop refreshes card text and media **while leaving your existing FSRS / SM-2 review history and intervals intact inside Anki**.

## 3. Quick Multi-Format Export (JSON, JSONL, Text, Markdown)

Inside **Editor & Browser** (<kbd>Alt+3</kbd>), the **Export as Text or JSON (quick analysis)** button also exports your selection, active filter, or full collection to **`.json`**, **`.jsonl`**, **`.txt` (Anki TSV)**, or **`.md`**, as a single file or one file per card (with optional `id`, `guid`, and `chunk_id`).
