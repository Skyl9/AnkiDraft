---
title: Generating Flashcards with AI
description: Automatically turn textbook chapters and lecture notes into atomic Q&A or cloze flashcards with structured AI pipelines and human validation.
---

AnkiDraft helps you rapidly turn dense study chapters into atomic flashcards while keeping you in full control through human staging review.

## 1. Two Complementary Workspaces: Creation Studio vs. Batch Factory

AnkiDraft separates **interactive card crafting** (one excerpt or free-form note) from **batch production** (an entire book split into queued jobs):

### Option A — Creation Studio (<kbd>Alt+2</kbd>): Focused & Interactive
Best for working closely on **one section**, **a pasted excerpt**, or a **New Input** (<kbd>Ctrl+N</kbd>):
1. Open **Creation Studio** (<kbd>Alt+2</kbd>).
2. Pick a document section on the left (with its scope) or click **New Input** (<kbd>Ctrl+N</kbd>).
3. Under **Anki Targets** and **AI Orchestration**, select the deck, note type, **AI Engine**, and **Agent Pipeline**; optionally enable **Multimodal Vision** (`ON`/`OFF` badge based on engine capability) and **Advanced Settings** (*Temperature*, *Max Tokens*), then press <kbd>Ctrl+Enter</kbd>.
4. Review cards with live preview (<kbd>Space</kbd> or <kbd>V</kbd> to approve, <kbd>Delete</kbd> / <kbd>Backspace</kbd> / <kbd>R</kbd> to reject, <kbd>E</kbd> to edit, <kbd>Alt+Left</kbd> / <kbd>Alt+Right</kbd> to navigate, or **Accept All** in 1 click), then press <kbd>Ctrl+S</kbd> to save.

### Option B — Batch Factory (<kbd>Alt+6</kbd>): Multi-Chapter Queue Processing
Best for processing **multiple chapters or whole textbooks** through a resumable queue:
1. Open **Batch Factory** (<kbd>Alt+6</kbd>).
2. Click **Compose Batch…** (<kbd>Ctrl+N</kbd>) to slice your sources ([Scope & Chapters](/en/sources/scope-and-slices/)):
   - **Direct Mode**: each checked section creates one generation task.
   - **Automatic Mode**: groups or splits sections automatically by length.
3. Configure targets and toggles (**Vision (PDF)**, **Auto Validation**, **Full Document by Chunks**, *Advanced Settings*), then launch the queue (<kbd>Ctrl+Enter</kbd>). If a single task fails, use **Resume Batch** without restarting from scratch.
4. Review generated cards in the bottom **Review** tab (<kbd>Alt+Up</kbd> / <kbd>Alt+Down</kbd> to switch slices) before saving to your collection.

## 2. Tailoring AI Behavior (Agents & Pipelines)

Extraction style is driven by the **Agent Pipeline** chosen in Studio or Batch Factory and customized in **Agent Editor** (<kbd>Alt+9</kbd>). AnkiDraft includes built-in presets ready to clone and refine:
- **Wozniak Atomic Generator** and **Auto-Cloze Generator** (focused cloze cards);
- **Medical & Anatomy Specialist** (mechanisms, clinical concepts, anatomical relations);
- **Scientific Formulas & KaTeX** (derivations and mathematical notation);
- **Languages & Vocabulary Tutor** (contextual examples, idioms, pronunciation);
- **Law, Standards & Case Law** (core concepts, distinctions, rulings).

:::tip[Per-Note-Type AI Instructions]
You can also define an **AI Role** (or structured table via **Prompt for AI**) directly on any note type under **Note Types** (<kbd>Alt+8</kbd>) to guide how AI populates each field.
:::

## 3. Human Review Before Saving (Staging)

No AI-generated card is ever added blindly to your collection: all proposals land in the review queue (**Studio** or Batch Factory's **Review** tab) where you can accept, edit, or reject each card before saving (<kbd>Ctrl+S</kbd>).
