---
title: Generation Pipelines and Smart Coverage
description: Automate multi-step flashcard creation with DAG pipelines and fill knowledge gaps across your textbooks using local RAG and Smart Coverage tools.
---

For large textbooks and courses, AnkiDraft combines the **DAG Pipelines** editor (directed acyclic workflows) and **Smart Coverage** (local RAG & alignment).

## 1. Chaining Up to 6 Step Types in a DAG Pipeline

In the **Pipelines** view, each workflow chains reusable, inspectable steps with cycle safeguards and conditional jumps (`↳ step`):
- **`RAG_RETRIEVAL` (Vector RAG Search)**: fetches top matching chunks (`top_k`) from an indexed course.
- **`LLM_PROMPT` (AI Agent)**: generates or audits flashcards with an agent (plus optional **per-step prompt override** without altering the global agent).
- **`MAP_REDUCE` (Parallel Batch Generation)**: splits and processes dense documents in parallel batches.
- **`HUMAN_VALIDATION` (Copilot Pause)**: pauses execution so you can approve or refine an intermediate outline before card generation.
- **`PYTHON_TOOL` (Deterministic Python Tool)**: runs non-LLM transforms (e.g., `clean_html_latex`, `validate_json_schema`, `deduplicate_cards_levenshtein`).
- **`AUDIO_TTS` (TTS Audio Generation)**: automatically attaches `[sound:...]` pronunciation tags to generated cards.

Three ready-to-use templates (*Standard Course Pipeline*, *Copilot Pipeline with Human Validation*, *High-Precision Map-Reduce & RAG*) are available under **Preset Templates…**, with **step-by-step simulation** (<kbd>Ctrl+Enter</kbd>) and JSON or cross-profile import/export.

## 2. Spotting Uncovered Chapters (Smart Coverage)

Using local semantic indexing and provenance links (`NoteChunkLinkModel`), AnkiDraft compares your existing flashcards against your entire course:
- In **My Documents** (<kbd>Alt+7</kbd>) › **Coverage** or **Analysis & AI Audit** (<kbd>Alt+4</kbd>) › **Documents**, it highlights orphan sections that have zero flashcards yet.
- Click **Forge Section** (or <kbd>Ctrl+Alt+F</kbd>) to generate only the missing cards without duplicating concepts you already covered.
