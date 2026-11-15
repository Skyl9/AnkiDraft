---
title: Quality Audit and Wozniak's 20 Rules
description: Detect and split overloaded, vague, or hard-to-remember flashcards with the Wozniak 20-Rules Linter to boost long-term Anki retention daily.
---

A poorly formulated flashcard (too long, testing multiple facts at once, or lacking context) quickly turns into a "leech" that you repeatedly fail in Anki.

AnkiDraft includes a built-in **Pedagogical Linter** based on **Piotr Wozniak's 20 rules of formulating knowledge** (creator of SuperMemo).

## 1. Wozniak Audit in Analysis & AI Audit (<kbd>Alt+4</kbd>)

Open **Analysis & AI Audit** (<kbd>Alt+4</kbd>) › **Wozniak Audit & Linter**, pick a deck, and run the audit (<kbd>Ctrl+Enter</kbd>). AnkiDraft scores the deck out of 100 across **4 weighted categories** (with customizable settings under **Rules**):
- **Atomicity & Restructuring**: overloaded answers or cards testing multiple independent facts.
- **Cloze & Unambiguity**: vague prompts or overly broad clozes (plus a dedicated toggle to keep or convert clozes into Q&A).
- **Disambiguation & Context**: interfering cards that look too similar during recall.
- **KaTeX Formulas & Clarity**: ambiguous or malformed math expressions.

A quick linter dialog can also be launched directly on selected notes inside **Editor & Browser** (<kbd>Alt+3</kbd>).

## 2. Splitting Leeches and Merging Duplicates

- **Split into Atomic Cards**: under **Analysis & AI Audit** (<kbd>Alt+4</kbd>) › **Tokens & SRS** › **Leech Cards Diagnostic**, locate high-lapse cards and click **Split** to generate and apply (via *Two-Phase Commit* preview) a breakdown into 2 or 3 atomic cards.
- **Duplicate Detection & Merge**: the **Merges & Duplicates** tab (<kbd>Alt+4</kbd>, as well as the quick duplicate scan in `Editor & Browser`) clusters near-identical notes using Levenshtein similarity so you can merge redundant cards safely without losing review history.
