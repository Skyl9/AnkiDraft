---
title: Note Types, Templates, and CSS Styling
description: Customize note types, HTML/Mustache card templates, AI Role guides, LaTeX headers, CSS snippets, and light/dark styling for Anki Desktop and Web.
---

The **Note Types** view (<kbd>Alt+8</kbd>) lets you design, style, preview, and share note types that remain 100% compatible with the Anki ecosystem.

## 1. Initial Model, Starter Pack, and Image Occlusion

- **Clean initial profile**: a blank AnkiDraft profile ships only with a single **`Basic` (`Basique`)** note type (`Front`/`Back` or `Recto`/`Verso`) so your first `.apkg` import never collides with pre-seeded templates.
- **On-demand Starter Pack**: open **Starter Pack** inside **Note Types** (<kbd>Alt+8</kbd>) to install **`Cloze Deletion`** (`{{cloze:Text}}`) and additional ready-made community models.
- **`Image Occlusion Enhanced`**: provisioned automatically the first time you open [Smart Image Occlusion](/en/cards/image-occlusion/).

## 2. HTML/Mustache Templates, CSS, LaTeX, and Snippets

Every note type features **4 sub-tabs** (*CSS Style*, *Front HTML*, *Back HTML*, and **LaTeX** preamble/footer for compilation) alongside a live preview (**light / dark mode** toggle using automatic sample values or a real witness note):
- Use standard **Anki Mustache** syntax (`{{Front}}`, `{{FrontSide}}`, `{{cloze:Text}}`) and the **Insertion Helpers** drawer (fields, cloze, CSS classes, structure).
- Browse the **Snippets** library (*Info*, *Warning*, *Error*, *Tip*, *Theorem* callouts, difficulty/exam badges, MCQ grids, code blocks, KaTeX boxes) with automatic CSS conflict detection.
- Fill in **AI Role** (or the structured **Prompt for AI** table) to tell AI agents exactly how each field should be populated during generation.

## 3. Import, Export, and Smart Reconciliation

- Import or export note types as `.afmodel` / `.json` (<kbd>Ctrl+Alt+O</kbd> / <kbd>Ctrl+Alt+E</kbd>), or import a model directly from another AnkiDraft profile.
- When importing an `.apkg` deck whose note type already exists in your collection, AnkiDraft reconciles it cleanly instead of creating duplicate `Basic-12345` models.
