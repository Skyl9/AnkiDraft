---
title: Note Editor, KaTeX Math, and Cloze Deletions
description: Write and format Anki flashcards with live KaTeX math preview, cloze deletions, rich media attachments, and full per-note revision history in AnkiDraft.
---

The **Editor & Browser** view (<kbd>Alt+3</kbd>) combines deck browsing and full note editing with live Anki card preview (<kbd>Ctrl+P</kbd> to toggle preview, <kbd>Ctrl+Alt+T</kbd> to switch between **📝 Notes** and **🗂️ Cards**).

## 1. Writing Math and Chemistry Formulas (KaTeX)

AnkiDraft renders your LaTeX equations live without waiting for an Anki export:
- **Quick insert**: click the **KaTeX Formula** toolbar icon or press <kbd>Ctrl+M</kbd>.
- **Inline formula**: wrap your expression in `\( ... \)` or `$ ... $` (e.g., `$E = mc^2$`).
- **Centered block formula**: use `\[ ... \]` or `$$ ... $$`.
- **LaTeX Autocompletion**: type `\` followed by the first letters of a symbol (`\alpha`, `\frac`, `\sum`) to open the completion popup.

## 2. Cloze Deletions, Media, and Customizable Toolbar

Cloze cards are ideal for memorizing precise definitions or key terms:
1. Highlight the word or phrase you want to hide.
2. Click **Cloze** or press <kbd>Ctrl+Shift+C</kbd> to insert the next index `{{c1::your text}}` (or with a hint `{{c1::answer::hint}}`).
3. The toolbar also includes HTML formatting, code blocks, links (<kbd>Ctrl+K</kbd>), image insertion (plus drag-and-drop directly into any field), and toolbar customization via `...`.
4. Each field header provides a **TTS** speaker button for audio pronunciation, and course-linked notes display **View Course ➔** to jump straight back to the source passage.

:::tip[Interactive Diagrams and Charts]
To mask labels directly on anatomy plates or technical diagrams, use [Smart Image Occlusion (Vision AI)](/en/cards/image-occlusion/).
:::

## 3. Group Editing, Flags, and Bulk Actions

- **Atomic Group Edit** (<kbd>Ctrl+Shift+E</kbd>) & **Targeted Find / Replace** (<kbd>Ctrl+Alt+F</kbd>): add/remove tags (while preserving `source:`, `section:`, `page:` provenance tags) or edit a field across selected notes (*Replace*, *Append*, *Prepend*, *Find and replace*).
- **Fast organization & AI bulk tools**: apply flags (<kbd>Ctrl+0</kbd> to <kbd>Ctrl+7</kbd>), suspend/unsuspend (<kbd>Ctrl+J</kbd> or <kbd>!</kbd>), move decks (<kbd>Ctrl+D</kbd>), change note type (<kbd>Ctrl+Shift+M</kbd>), clean up tags (**Tag Hygiene & Merge…**), or run **AI Batch Edit** / **Auto-Tagging** on a selection.

## 4. Revision History (Time Machine)

Edited a card by mistake? Every save (<kbd>Ctrl+S</kbd>) stores a local snapshot in the note history: click **History** or press <kbd>Ctrl+H</kbd> to open the **Time Machine**, compare snapshots, and restore previous wording in one click.
