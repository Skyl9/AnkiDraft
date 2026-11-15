---
title: Document Hub and Multimodal Formats
description: Overview of supported sources in AnkiDraft — PDF, Web, YouTube, audio, DOCX, PPTX, EPUB, notebooks, code, and Image Albums with full source tracing.
---

The **My Documents** view (`<kbd>Alt+7</kbd>`) centralizes all your study materials in one place, lets you organize them into folders (via drag-and-drop), import documents from another profile, and preserves a direct link between every flashcard and its exact source passage.

## 1. Supported Study Sources

| Source Type | Formats | What AnkiDraft Extracts |
| :--- | :--- | :--- |
| **PDF Textbooks & Handouts** | `.pdf` | Chapter outline, text, tables, figures, and LaTeX math (PyMuPDF / pypdf, or Marker OCR on demand) |
| **Image Albums & Scans** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.gif` | Visual spreads, Vision AI transcription, and visual RAG — [see dedicated guide](/en/sources/albums-images/) |
| **Online Videos** | YouTube URLs | Timestamped subtitles, or audio transcription (`yt-dlp` + Whisper) |
| **Audio Recordings** | `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.wma`, `.webm` | Paragraph-segmented transcript (local Whisper or OpenAI/Groq API) + built-in player |
| **Web Articles & Wikipedia** | `http://`, `https://` | Clean article body (multi-page merge, MathML → LaTeX, SPA JavaScript rendering) |
| **Office, Ebooks & Text** | `.docx`, `.pptx`, `.epub`, `.md`, `.txt` | Heading hierarchy, lists, tables, and slide speaker notes |
| **Notebooks & Source Code** | `.ipynb`, `.py` | Code cells, markdown explanations, docstrings, and structured blocks |

## 2. Jump Back to the Source in One Click

While reviewing or editing any flashcard in the editor, click **View Course ➔** (`DocumentSourceBadge`) to jump straight back to the corresponding chapter and paragraph in **My Documents**. From the **Coverage** inspector tab, you can also click **Synchronize Cards** to refresh source-to-card coverage alignment.
