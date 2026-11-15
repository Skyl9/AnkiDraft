---
title: Importing a Deck (.apkg) or Collection (.colpkg)
description: Load your existing Anki .apkg or .colpkg decks into AnkiDraft to enrich notes, audit card quality, and track textbook coverage across chapters.
---

Already using Anki for months or years? You can bring your existing flashcards into AnkiDraft anytime.

## 1. Opening the Import Wizard (<kbd>Ctrl+Shift+I</kbd>)

Press <kbd>Ctrl+Shift+I</kbd> (or click **Import Anki Package (.apkg)** in **Editor & Browser**) and drop your file: AnkiDraft supports **`.apkg`**, **`.colpkg`** (including Anki 23.10+ **Zstandard** `collection.anki21b` and `media.zstd`), as well as tab-separated **`.txt`** exports (with `#guid` column support).

## 2. `.apkg` / `.txt` vs. `.colpkg`

- **`.apkg` Package or `.txt` Export (Incremental Merge)**: choose whether to **Keep original deck hierarchy** or **Merge into target deck**. Unknown notes are added, while locally edited notes trigger [Smart Merge](/en/anki-sync/synchro_smart_merge/) on conflict.
- **`.colpkg` Collection Archive (`Full Anki Collection Replacement`)**: **atomically replaces** the entire *Anki Scope* (all decks, notes, note types, cards, and stats) with the incoming archive while **strictly preserving** your source documents, RAG chunks, AI agents, personas, and pipelines—and automatically creating a **SQLite backup** beforehand.

:::note[Anti-Zip-Bomb Size Safeguards]
By default, archive decompression is capped at **1 GiB** for `.apkg` packages and **5 GiB** for `.colpkg` collections.
:::

For a visual walkthrough of how AnkiDraft and Anki work together, read the [Visual Guide to the Distributed Lifecycle](/en/guides/cycle_de_vie_distribue/).
