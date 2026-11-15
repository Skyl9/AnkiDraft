---
title: Smart Image Occlusion (Vision AI)
description: Create Image Occlusion Enhanced flashcards from anatomy or course diagrams using manual masks, Vision AI label detection, and Hide All or Hide One.
---

**Smart Image Occlusion** (`Image Occlusion AI`) turns anatomy plates, maps, flowcharts, and scientific diagrams into visual flashcards using the **`Image Occlusion Enhanced`** standard directly inside AnkiDraft.

## 1. Opening a Diagram in the Occlusion Studio

Several direct entry points feed into the occlusion canvas:
- From **My Documents** (<kbd>Alt+7</kbd>) › **Figures** tab on an imported PDF: launch image occlusion in one click on any extracted diagram.
- From an **Image Album**: open any scanned plate directly in the occlusion tool ([Image Albums](/en/sources/albums-images/)).
- Inside the occlusion dialog: click **Change Image…** (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.svg`) or **Paste Image** straight from your clipboard.

## 2. Manual Masking or Vision AI Auto-Detection

1. **Detect with AI**: automatically scans the diagram with a Vision-capable model to place occlusion boxes over labels and fill the **Masks & Labels** table.
2. **Manual Draw & Adjust**: switch between **Select / Move Mode** and **Draw Mode** to sketch, resize, or delete (<kbd>Delete</kbd>) mask rectangles freely.
3. Refine **`Text / Answer`** and **`Hint`** entries in the right-hand table and use the zoom controls as needed.

:::note[Vision AI Requirement]
Automatic label detection requires a **Vision-capable AI engine** (Gemini/OpenAI/Anthropic API or local multimodal Ollama model) configured in **Settings** (<kbd>Ctrl+,</kbd>). Manual mask drawing works 100% offline with zero API keys.
:::

## 3. Occlusion Modes and Note Generation

Before generating notes into your chosen **Target Deck** (with an optional card header and comma-separated tags such as `image-occlusion`), pick your study mode:
- **`Hide All, Reveal One (Hide All)`**: best when neighboring labels would otherwise give away the answer. Keep **`Keep other masks hidden on back`** checked to prevent contextual leaks while reviewing.
- **`Hide One, Reveal One (Hide One)`**: keeps surrounding labels visible when spatial context helps anchor a specific term.

On first use, AnkiDraft automatically provisions the **`Image Occlusion Enhanced`** note type in your collection, ready for `.apkg` export to Anki Desktop, AnkiWeb, and AnkiMobile.
