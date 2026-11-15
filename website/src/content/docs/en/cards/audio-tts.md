---
title: Text-to-Speech (TTS) and Audio Cards
description: Automatically generate natural offline audio pronunciation for language and terminology flashcards using Kokoro or Piper neural TTS voices locally.
---

When studying foreign languages, medical terminology, or music, attaching an audio clip to a flashcard dramatically boosts retention.

## 1. Install Offline TTS Engines and Voices

Open **Settings** (<kbd>Ctrl+,</kbd>) › **Audio & TTS** before generating offline audio for the first time:

- **Piper TTS (local & fast)**: expand **MOTEUR LOCAL PIPER**, click **Download Piper CLI (1-Click)**, then select and download one or more target-language voice packs under **Additional Voices** (French, English, Japanese, Spanish, German, etc.).
- **Kokoro-82M (optional high-fidelity local engine)**: expand **MOTEUR LOCAL KOKORO-82M (OPTIONNEL)** and click **Install Kokoro (1-Click)** to download the local runner and ONNX model files.
- **Zero-download options**: **Edge-TTS** works directly over an internet connection (free, no API key), and the **OS System Engine** uses native voices already installed on your computer.

Click **Test Selected Voice** to verify playback before running a batch job.

## 2. Generating Field Pronunciation in One Click

1. In **Editor & Browser** (<kbd>Alt+3</kbd>), place your cursor inside the field containing the word or sentence to pronounce.
2. Click the **Text-to-Speech (TTS)** icon in the toolbar.
3. Select the target language and installed or online voice.
4. The audio file is generated, normalized, and attached automatically as `[sound:filename.mp3]`, ready for Anki Desktop, AnkiWeb, and AnkiMobile.

## 3. Batch Audio Generation

Have an entire vocabulary deck without audio? Select multiple cards in the editor table and run **Batch TTS Generation**: AnkiDraft generates audio for all selected cards in the background.
