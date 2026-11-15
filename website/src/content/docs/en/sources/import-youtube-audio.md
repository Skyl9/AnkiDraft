---
title: Importing YouTube Videos and Audio Lectures
description: Turn any YouTube lecture, podcast, or classroom voice recording into timestamped transcripts and atomic Anki flashcards locally on your device.
---

AnkiDraft lets you turn online video lectures and recorded classroom audio directly into structured transcripts and flashcards.

## 1. Importing a YouTube Video

1. Open **My Documents** (`<kbd>Alt+7</kbd>`) and click **Import from Web / YouTube**.
2. Paste one or more YouTube links (supports batch URLs, one per line).
3. AnkiDraft retrieves official or auto-generated subtitles first and builds a clean, timestamped transcript.
4. If no subtitles exist, it can download the audio stream and run speech-to-text transcription.

## 2. Transcribing Local Audio Files

Recorded a lecture, seminar, or voice memo?
1. Drop any supported audio file (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.wma`, `.webm`) into **My Documents**.
2. Listen back inside the built-in **Audio Player** directly above the transcript.
3. Run **AI Structure** from the toolbar to reorganize raw speech into clear study sections before generating cards.

:::note[Prerequisites for Audio & No-Subtitle YouTube Transcription]
- **With YouTube subtitles**: works out of the box, no extra tool required.
- **Audio files or YouTube videos without subtitles**: requires **either a local Whisper binary** (`whisper` / `whisper-cli`) **or an OpenAI / Groq API key** configured in **Settings (`Ctrl+,`) > AI Engines**. Downloading YouTube audio streams also requires **`yt-dlp`** on your system.
:::
