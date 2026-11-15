---
title: Generating Flashcards with AI
description: Automatically turn textbook chapters and lecture notes into atomic Q&A or cloze flashcards with structured AI pipelines and human validation.
---

AnkiDraft helps you rapidly turn dense study chapters into atomic flashcards while keeping you in full control through human staging review.

## 1. Two Complementary Workspaces: Creation Studio vs. Batch Factory

AnkiDraft separates **interactive card crafting** (one excerpt or free-form note) from **batch production** (an entire book split into queued jobs):

### Option A — Creation Studio (<kbd>Alt+2</kbd>): Focused & Interactive
Best for working closely on **one section**, **a pasted excerpt**, or a **New Free Input** (<kbd>Ctrl+N</kbd>):
1. Open **Creation Studio** (<kbd>Alt+2</kbd>).
2. Pick a document section on the left or click **New Free Input** (<kbd>Ctrl+N</kbd>).
3. Select the note type (*Basic*, *Cloze Deletion*), destination deck, and AI agent/model, then press <kbd>Ctrl+Enter</kbd>.
4. Review generated cards one by one with live preview (<kbd>Space</kbd> to approve, <kbd>Delete</kbd> to reject), then press <kbd>Ctrl+S</kbd> to save.

### Option B — Batch Factory (<kbd>Alt+6</kbd>): Multi-Chapter Queue Processing
Best for processing **multiple chapters or whole textbooks** through a resumable queue:
1. Open **Batch Factory** (<kbd>Alt+6</kbd>).
2. Click **Batch Slice Composer** (<kbd>Ctrl+N</kbd>) to slice your sources ([Scope & Chapters](/en/sources/scope-and-slices/)):
   - **Direct Mode**: each checked section creates one generation task.
   - **Automatic Mode**: groups or splits sections automatically by length.
3. Set the note type and destination Anki deck, then launch the queue (<kbd>Ctrl+Enter</kbd>). If a single task fails, use **Resume Batch** without restarting from scratch.
4. Review all queued cards inside the **Staging** panel before saving to your collection.

## 2. Tailoring Card Style (Personas)

Adapt the AI extraction style to your discipline:
- **Sciences & Medicine**: precise definitions, physiological mechanisms, reference values.
- **Law & Humanities**: core concepts, conceptual distinctions, dates, and case law.
- **Languages & Vocabulary**: contextual examples, idioms, and pronunciation notes.

## 3. Human Review Before Saving (Staging)

No AI-generated card is ever added blindly to your collection: all proposals land in the **Staging Review** queue where you can accept, edit, or reject each card in one click.
