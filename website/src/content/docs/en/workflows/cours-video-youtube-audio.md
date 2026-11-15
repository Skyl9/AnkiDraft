---
title: "YouTube Video & Audio Lectures: Transcription to Cards"
description: "Turn YouTube video lectures or classroom audio recordings into structured, atomic Anki flashcards using local transcription, slicing, and AI tools."
---

Recorded university lectures, YouTube explainers, and seminar audio files pack hours of spoken insight that are slow to review manually. This workflow turns speech into structured, atomic flashcards.

## 1. Import a YouTube URL or Local Audio Recording

1. Open **My Documents** (<kbd>Alt+7</kbd>).
2. Choose your source type ([Import YouTube & Audio](/en/sources/import-youtube-audio/)):
   - **YouTube lecture**: click **Import from Web** and paste the video URL. AnkiDraft downloads official captions when present or falls back to local speech-to-text transcription.
   - **Recorded lecture or voice memo** (`.mp3`, `.wav`, `.m4a`, `.mp4`, `.ogg`): drag and drop the file into **My Documents**. Local **Whisper** transcription runs on your machine without uploading your recordings to third-party servers.

![AnkiDraft Documents View](assets/screen_documents.png)

## 2. Turn Raw Transcripts into Clear Chapters

Spoken transcripts naturally contain filler words and tangents. Clean and outline the transcript before drafting flashcards:

- **In Creation Studio**: run a [generation workflow](/en/cards/dag_et_rag/) that first summarizes and structures the transcript into chapters before creating cards.
- **With Claude or Cursor**: ask your assistant to call `structure_transcript_for_ai` followed by `structure_document_sections` so timestamped speech becomes a crisp outline.

## 3. Slice by Topic and Review Your Cards

![AnkiDraft Creation Studio](assets/screen_creation.png)

1. To craft and review cards from a specific passage, open **Creation Studio** (<kbd>Alt+2</kbd>). To split a long lecture into queued chapter jobs, open **Batch Factory** (<kbd>Alt+6</kbd>) › **Batch Slice Composer** (<kbd>Ctrl+N</kbd>).
2. Pick your note type (*Basic* or *Cloze*) and writing style ([AI Card Generation](/en/cards/ai-generation/)).
3. Review every draft in the review queue before saving to catch spoken ambiguities or misheard technical terms.

## 4. Automate Structuring and Drafting (Zero API Key)

When driving AnkiDraft from Claude Code, Claude Desktop, or Cursor in [zero API key mode](/en/workflows/zero-cle-api-agent-mcp/):

- **Tools used**: `structure_transcript_for_ai`, `get_document_outline`, `create_notes_batch`, `begin_staged_bundle`, `commit_staged_bundle`.
- **Sample prompt**: *"Clean up raw transcript document #9 using `structure_transcript_for_ai` (didactic profile, keep timestamps), then stage clear definitions and causal questions via `create_notes_batch` into deck `Lectures::Neuroscience` for my approval."*
