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

## 2. Generating and Playing Field Pronunciation in One Click

1. In **Editor & Browser** (<kbd>Alt+3</kbd>), open a note and click the **Generate Audio Pronunciation (TTS)** speaker icon in the target field's header. If text is highlighted, only the selection is synthesized; otherwise the full field is read (with Cloze tags `{{c1::word}}` cleanly expanded first).
2. Audio is synthesized using the engine and voice configured in **Settings** (<kbd>Ctrl+,</kbd>) › **Audio & TTS**, cached in your media folder, and appended as an Anki sound tag ready for Anki Desktop, AnkiWeb, and AnkiMobile:
   - **Edge-TTS**: generates an **`.mp3`** file (`[sound:tts_xxx.mp3]`);
   - **Piper TTS** and **Kokoro-82M**: generate a **`.wav`** file (`[sound:tts_xxx.wav]`);
   - **OS System Engine**: generates a **`.wav`** file (or **`.m4a`** on macOS).
3. Whenever a field contains a `[sound:...]` tag, a **Play / Stop** button appears in its header for instant playback.

## 3. Batch Audio Generation via a DAG Pipeline

To attach audio automatically across a batch of newly generated cards, add an **`Audio Generation (TTS)`** (`AUDIO_TTS`) step at the end of your workflow in **Pipelines** (see [Generation Pipelines](/en/cards/dag_et_rag/)). You can configure the source field, target field (append or replace), TTS engine, and voice.
