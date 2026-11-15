---
title: "Language Learning & Audio Workflow: Offline TTS Flashcards"
description: "Build language vocabulary decks in AnkiDraft with offline neural text-to-speech audio (Kokoro or Piper), instant preview, and MCP batch enrichment."
---

This workflow shows how to build language decks (Japanese, Spanish, French, German, Mandarin, and more) with contextual sentence examples, 100% offline neural pronunciation audio, and clean bilingual formatting.

## 1. Bring In Your Vocabulary List or Study Material

You can start from any of three sources:
- A **source document** (grammar handout, vocabulary sheet, article, or subtitle file dropped into **My Documents**).
- An **existing Anki deck** imported with <kbd>Ctrl+Shift+I</kbd> ([Import .apkg / .colpkg](/en/anki-sync/import-colpkg/)).
- **Direct entry** inside **Editor & Browser** (<kbd>Alt+3</kbd>).

For higher long-term retention, prefer a **short contextual sentence** on the front card highlighting the target word rather than an isolated one-word translation.

## 2. Generate Offline Pronunciation Audio (Kokoro / Piper)

AnkiDraft supports local neural TTS engines that create standard `[sound:tts_xxx.mp3]` audio clips without internet access or cloud quotas ([Text-to-Speech & Audio](/en/cards/audio-tts/)):

1. Open **Settings** (<kbd>Ctrl+,</kbd>) > **Audio & TTS** and select a local engine (**Kokoro-82M** or **Piper ONNX**) along with the voice matching your target language.
2. **Single-card audio**: in **Editor & Browser** (<kbd>Alt+3</kbd>), click inside the target-language field and press the speaker/microphone button to synthesize and preview audio immediately.
3. **Batch deck audio**: select multiple notes in the browser and trigger **Batch TTS Generation** to synthesize missing audio clips in the background.

![AnkiDraft Card Browser and Editor](assets/screen_edition.png)

## 3. Enrich and Clean Up Language Decks via MCP

A frequent failure mode in language decks is **Type 3 Pathology (Bilingual Glue)**: cards mixing two languages in one prompt or pairing literal glosses with zero natural context. Your MCP agent can audit and fix this safely:

- **Add audio across an entire language deck**:
  - Tools used: `get_cards_by_deck_or_tag`, `generate_card_audio`, `generate_cards_batch_audio`.
  - Sample prompt: *"Fetch notes in deck `Languages::Japanese` (with `recursive=True`) missing `[sound:...]` tags and run `generate_cards_batch_audio` on the Expression field using a Japanese voice."*
- **Fix bilingual glue and add natural example sentences**:
  - Tools used: `diagnose_domain_knowledge_gaps`, `propose_card_refactor`.
  - Sample prompt: *"Inspect `Languages::Spanish` with `diagnose_domain_knowledge_gaps`, find cards with Type 3 bilingual glue or overloaded synonyms, and stage clean contextual rewrites via `propose_card_refactor`."*

## 4. Export with Deduplicated Audio Media

Press <kbd>Ctrl+Alt+E</kbd> to export your `.apkg`: AnkiDraft packages MD5-deduplicated audio files automatically so playback works smoothly on Anki Desktop, AnkiWeb, and AnkiMobile.
