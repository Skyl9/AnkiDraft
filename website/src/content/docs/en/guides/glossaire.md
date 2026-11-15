---
title: "User Glossary: Key AnkiDraft Concepts Explained Simply"
description: "Understand every core AnkiDraft concept (Wozniak rules, Cloze, Smart Coverage, DAG, RAG, MCP, Safeguard) with clear Before / After study examples."
---

AnkiDraft combines spaced-repetition best practices with local AI tools. This glossary explains every technical term in plain English, paired with a concrete **Before / After** example.

---

## 1. Atomic Knowledge & Wozniak's 20 Rules

A core principle from Piotr Wozniak (creator of SuperMemo): a great flashcard tests **one short, unambiguous fact** at a time (minimum information principle). AnkiDraft's linter automatically spots bloated or vague prompts.

- **Before**: *Front:* "Explain the Krebs cycle (steps, rate-limiting enzymes, ATP/NADH/FADH2 yield)." ➔ Too dense to grade honestly during reviews.
- **After**: 3 crisp, independent cards: (1) "Which enzyme catalyzes the rate-limiting step of the Krebs cycle?", (2) "How many NADH molecules are produced per turn of the Krebs cycle?", (3) "Where in the cell does the Krebs cycle take place?".

---

## 2. Cloze Deletion

A fill-in-the-blank card (`{{c1::hidden term}}`) that hides one key word or phrase inside a clear sentence so you recall it directly in context (<kbd>Ctrl+Shift+C</kbd>).

- **Before**: "Define osmosis?" / "Movement of solvent across a semipermeable membrane from lower to higher solute concentration."
- **After**: "During osmosis, solvent moves across a semipermeable membrane from a {{c1::hypotonic (lower solute)}} solution to a {{c2::hypertonic (higher solute)}} solution."

---

## 3. Smart Coverage

A traceability tracker linking each generated card back to its exact source heading or page. It shows which chapters of your PDF already have flashcards and which sections are still uncovered.

- **Before**: Manually flipping through a 180-page textbook wondering whether you forgot subsection 3.4.
- **After**: The *Smart Coverage* gauge reports `Chapter 3: 82% covered — Section 3.4 (0 cards)` and lets you draft cards solely for that gap.

---

## 4. Scoping: Exclude vs. Neutralize

Two non-destructive actions to filter a textbook without deleting pages ([Scope & Chapters](/en/sources/scope-and-slices/)):
- **Exclude**: temporarily hides an off-syllabus chapter from AI generation.
- **Neutralize**: removes structural boilerplate (cover, table of contents, acknowledgments) from the *Smart Coverage* denominator.

- **Before**: A 300-page book with 30 pages of index and bibliography caps your coverage at 90% or generates useless cards about publisher copyrights.
- **After**: Index neutralized, bibliography excluded ➔ coverage accurately reaches **100% of active chapters** with zero junk cards.

---

## 5. Generation Pipeline (DAG)

An automated multi-step workflow (e.g., retrieve key passages ➔ synthesize clean Markdown ➔ draft cards ➔ add TTS audio ➔ stage for human review).

- **Before**: Copying a chapter into a chat box, generating cards, fixing broken LaTeX manually, then creating audio one card at a time.
- **After**: Clicking **Run Pipeline** executes the full workflow automatically and delivers clean drafts ready to review.

---

## 6. Local Semantic Search (RAG)

100% local indexing on your computer that lets AI retrieve relevant sections of your textbooks by **meaning** (not just exact keywords) before drafting or auditing cards.

- **Before**: Stuffing an entire textbook into a prompt (slow, expensive, and prone to hallucinations).
- **After**: Local RAG pulls only the 3 paragraphs relevant to the concept and keeps exact page provenance.

---

## 7. MCP Server (Model Context Protocol)

An open standard built into AnkiDraft that lets your external AI assistant (Claude Desktop, Claude Code, Cursor, Antigravity) read your courses and decks locally with zero extra API keys.

- **Before**: Copy-pasting notes back and forth between Anki, PDFs, and a browser chat window.
- **After**: Asking Claude directly *"Audit my Cardiology deck and draft missing cards for Chapter 4"* queries AnkiDraft live.

---

## 8. Safeguard & Staged Bundle (Two-Phase Human Approval)

A mandatory safety buffer: no AI proposal (create, edit, split, or delete) ever modifies your database directly. Every change enters a **Staged Bundle** with a Before / After diff until you click **Apply**.

- **Before**: Worrying that an automated prompt or script might accidentally overwrite 200 cards.
- **After**: You inspect every proposed card change side-by-side in the Safeguard and stay in 100% control.

---

## 9. Domain Gap Diagnosis & the 3 Cognitive Pathologies

A neuro-symbolic audit (`diagnose_domain_knowledge_gaps`) scanning all your decks together against a study topic to catch 3 pathologies:
- **Type 1 (Missing concepts)**: textbook concepts with zero matching flashcards.
- **Type 2 (Non-atomicity)**: bloated multi-fact cards needing splitting.
- **Type 3 (Bilingual glue)**: two languages mixed awkwardly in one card or bare word translations lacking context.

- **Before**: Realizing right before finals that 3 core topics are missing or scattered across unrelated decks.
- **After**: The audit collects related orphan cards across decks and pinpoints exact gaps and splits needed.

---

## 10. Studio Scope vs. Anki Collection Scope (`.apkg` vs. `.colpkg`)

AnkiDraft isolates authoring assets (**Studio Scope**: PDFs, transcripts, RAG indexes, prompts) from synced cards (**Anki Collection Scope**).
- `.apkg`: adds or merges a targeted deck.
- `.colpkg`: mirrors your complete Anki collection (removes cards deleted in Anki while keeping all PDFs intact).

- **Before**: Importing a full Anki backup risked wiping study notes or resurrecting deleted cards ("zombie cards").
- **After**: `.colpkg` sync updates your collection cleanly while keeping Studio sources safe and preventing zombie cards ([Distributed Lifecycle Guide](/en/guides/cycle_de_vie_distribue/)).

---

## 11. Smart Merge

A 3-way visual diff (**Local**, **Common Base**, **Incoming**) inspired by developer merge tools: when importing an updated `.apkg` from a classmate, only true text conflicts require your decision.

- **Before**: Blindly overwriting your personal edits or losing a teammate's additions when importing a shared deck.
- **After**: Pick the exact version per field while preserving media and review scheduling.

---

## 12. Leech Card

Anki's term for a card you repeatedly fail during reviews—almost always because it is too verbose, poorly phrased, or interferes with a sibling card.

- **Before**: Seeing the same frustrating card fail 8 times a month without sticking.
- **After**: AnkiDraft spots leeches from synced lapse counters and suggests splitting or clarifying them with distinctive cues.
