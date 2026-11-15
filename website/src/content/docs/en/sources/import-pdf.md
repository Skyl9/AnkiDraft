---
title: Importing PDFs, Slides, and Ebooks
description: Cleanly extract PDF textbooks, DOCX documents, PPTX slides, and EPUB books with Marker OCR, preserving diagrams, tables, and LaTeX formulas.
---

The **My Documents** view (`<kbd>Alt+7</kbd>`) turns your static files into structured courses ready for flashcard generation, with batch multi-file drag-and-drop and folder organization.

## 1. Supported File Formats

Drag and drop one or more files directly into **My Documents** (or click **Import**):
- **PDF Documents (`.pdf`)**: lecture handouts, academic papers, and textbooks, preserving tables, figures, and LaTeX math equations.
- **Word Documents (`.docx`) and Slides (`.pptx`)**: extracts headings, bullet points, tables, and speaker notes.
- **Ebooks (`.epub`) and Markdown / Plain Text (`.md`, `.txt`)**.
- **Jupyter Notebooks (`.ipynb`) and Python Code (`.py`)**: keeps code blocks and markdown annotations structured.

:::tip[Photos or Scans Without Selectable Text?]
If your source consists of raw images (book pages, whiteboard photos, handwritten notes), use an **Image Album** directly rather than assembling a PDF manually — [see Image Albums & Vision OCR](/en/sources/albums-images/).
:::

## 2. PDF Extraction Modes (`PyMuPDF` / `pypdf` vs `Marker OCR`)

During import, AnkiDraft uses **Marker OCR** automatically if it is already installed on your machine; otherwise, it performs fast local extraction via **PyMuPDF** (with **pypdf** as fallback).

After import, the top toolbar lets you switch between **`PDF` / `MD` / `Logs`**, run **Format** or **AI Structure** to refine headings, or launch **Marker OCR** on demand for scanned or math-heavy handouts.

:::note[Marker OCR Installation Prerequisite]
Marker OCR is optional and installed on demand from the toolbar button. Its local models require approximately **5 GB of free disk space** and an active internet connection for the initial download.
:::

## 3. Diagrams, Figures, and 1-Click Image Occlusion

Extracted figures and diagrams appear in the **Figures** tab of the right-hand Inspector, which automatically filters out tiny decorative icons. From there, you can attach any figure to a flashcard or launch **Image Occlusion** in a single click.
