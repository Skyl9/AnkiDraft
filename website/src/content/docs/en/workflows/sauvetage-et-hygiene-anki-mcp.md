---
title: "Anki Collection Rescue: Duplicates, Leeches, and MCP Hygiene"
description: "Clean up an existing Anki collection (.colpkg): detect duplicates and leeches, run an MCP hygiene campaign, and split overloaded cards safely."
---

# Anki Collection Rescue: Duplicates, Leeches, and MCP Hygiene

Stuck with an older Anki deck full of stubborn leeches, near-duplicate cards, messy tags, or bloated paragraphs? This workflow helps you rescue and normalize your collection without ever losing your spaced-repetition scheduling history (FSRS / SM-2).

## 1. Safely Import Your Anki Collection (`.colpkg`)

1. From Anki Desktop, export a full archive: **File > Export > Anki Collection Package (`.colpkg`)** including media and scheduling info.
2. In AnkiDraft, press <kbd>Ctrl+Shift+I</kbd> and drop your `.colpkg` file ([Import .apkg or .colpkg](/en/anki-sync/import-colpkg/)).
3. AnkiDraft automatically creates a backup SQLite snapshot and isolates your **Anki Collection Scope** from your **Studio Scope** (your PDFs, RAG indexes, and app settings remain untouched).

## 2. Spot Duplicates and Overloaded Cards in the Audit Hospital

1. Open **Analysis & AI Audit** (<kbd>Alt+4</kbd>).
2. Under **Audit & Wozniak Linter**, pick a deck and click **Run Audit**: verbose, ambiguous, or multi-concept cards receive targeted cognitive diagnostics ([Wozniak Linter](/en/cards/linter_wozniak/)).
3. Open **Merges & Duplicates** to detect near-identical notes with the native C Levenshtein matcher and resolve duplicates cleanly.

![AnkiDraft Wozniak Analysis and Linter View](assets/screen_analysis.png)

## 3. Run an Assisted Collection Hygiene Campaign via MCP

To clean hundreds of cards across multiple decks systematically, connect your MCP client (**Claude**, **Cursor**, **Antigravity**) on port `8765` and follow these four stages:

### Stage A — Fix Cards Flagged During Daily Reviews
While reviewing in Anki, flag painful cards (Red = split needed, Orange = fact-check), then re-import your `.colpkg` into AnkiDraft:
- **MCP tools**: `get_flagged_cards`, `get_note_full_profile_360`, `set_card_flag`.
- **Prompt**: *"Fetch all my red-flagged cards using `get_flagged_cards`, diagnose why they keep failing with `audit_card_wozniak`, and stage atomic rewrites for each."*

### Stage B — Break Down Deck Silos and Diagnose 3 Pathologies
- **MCP tools**: `diagnose_domain_knowledge_gaps`, `diagnose_deck_weaknesses`, `audit_deck_wozniak`, `find_duplicate_cards`.
- **Prompt**: *"Run `diagnose_domain_knowledge_gaps` on Renal Physiology across every deck: surface related orphan cards, Type 1 missing concepts, Type 2 non-atomic cards, and Type 3 bilingual glue."*

### Stage C — Clean Up Tags and Empty Cards
- **MCP tools**: `audit_tag_hygiene`, `merge_tag_clusters`, `list_empty_cards`, `delete_empty_cards`.
- **Prompt**: *"Audit tag consistency with `audit_tag_hygiene`, merge typo/plural clusters via `merge_tag_clusters`, and check for empty front cards via `list_empty_cards`."*

### Stage D — Batch Split and Refactor Behind the Safeguard
- **MCP tools**: `begin_staged_bundle`, `propose_card_split`, `propose_card_refactor`, `propose_cards_batch_refactor`, `commit_staged_bundle`.
- **Prompt**: *"Start a bundle (`begin_staged_bundle`), split the 8 cards exceeding 40 words into 2–3 atomic notes using `propose_card_split`, tighten vague wording with `propose_card_refactor`, and finalize via `commit_staged_bundle`."*

![AnkiDraft MCP Server Supervision & Configuration (open Safeguard & Validation beside it)](assets/screen_consultant.png)

## 4. Approve in Safeguard and Export Back Without Losing SRS

1. Open **MCP Server & Agents** (<kbd>Alt+5</kbd>) > **Safeguard & Validation** and review every Before / After split and rewrite visually.
2. Click **Apply** to commit the bundle atomically into AnkiDraft.
3. Export the cleaned deck via <kbd>Ctrl+Alt+E</kbd> (or MCP tool `export_deck_apkg`) and open the `.apkg` in Anki: thanks to stable note GUIDs and [Smart Merge](/en/anki-sync/synchro_smart_merge/), updated wording lands cleanly while preserving your FSRS intervals.
