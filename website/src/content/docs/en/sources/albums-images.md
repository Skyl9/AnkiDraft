---
title: Image Albums, Photo Scans, and Vision OCR
description: "Combine whiteboard photos, scanned handouts, and diagrams in an Image Album, transcribe pages with Vision AI, index in RAG, and forge flashcards."
---

Took photos of the lecture whiteboard, snapped handwritten study sheets, or collected loose anatomy plates? In **My Documents** (<kbd>Alt+7</kbd>), **Image Albums** keep your visuals organized page by page so you can clean, transcribe with Vision AI, and turn them into flashcards.

## 1. Creating and Organizing an Image Album

1. Open **My Documents** (<kbd>Alt+7</kbd>) and click **Create an Image Album** (or **Create album** on the empty view).
2. Enter a title, select a target folder, and pick the initial sort order:
   - **Natural alphanumeric sort** (`page_1`, `page_2`…)
   - **EXIF capture date** (camera chronological order)
   - **Raw import order**
3. Inside the album viewer, each plate includes quick actions: reorder left/right, **rotate 90°**, **inspect / crop**, delete, or append new files (**Add images**).

## 2. Transcribing the Album with Vision AI

1. Click **Transcribe album…** in the album toolbar.
2. Select a **multimodal Vision-capable engine** (such as `Google Gemini 3.5 Flash Lite` or a local Ollama vision model; AnkiDraft warns when a selected engine cannot read images).
3. Target the exact plates to process:
   - **Entire album**
   - **Untranscribed plates only**
   - **Stale plates** (modified or rotated since the last OCR pass)
   - **Custom range** (e.g., `1-5, 8, 12-15`)
4. Pick the **Image data type** and optional formatting guidance. If any page hits a network or quota limit, use **Retry failures** instead of re-running the whole album.

## 3. Visual RAG, PDF Compilation, and Flashcards

- **Visual RAG**: indexes your plates and diagrams in FAISS for multimodal semantic search.
- **Compile to PDF**: merges all album pages (preserving rotations and crops) into a single readable PDF.
- **Forge Cards**: opens the album directly in **Creation Studio** (<kbd>Alt+2</kbd>), or launch **Image Occlusion** from the inspector to mask diagram labels.

:::tip
Using Claude Code, Cursor, or Antigravity with zero API key? The `ingestion-albums-visuels` Skill in `~/ankiforge_agentique` can transcribe and structure album plates before staging flashcards in **Safeguard & Validation** (<kbd>Alt+5</kbd>).
:::
