---
title: FAQ and Troubleshooting
description: Find answers to frequently asked questions and step-by-step troubleshooting for AnkiDraft installation, Ollama, PDF OCR, and Anki .apkg exports.
---

Find answers to the most common questions about AnkiDraft.

## 1. General Questions

### Does AnkiDraft replace Anki?
No—AnkiDraft and Anki complement each other. **AnkiDraft** is the authoring and quality-auditing studio where you turn textbooks and lectures into atomic flashcards, while **Anki** (Desktop, AnkiWeb, AnkiMobile, AnkiDroid) is the spaced-repetition engine where you do your daily reviews.

### Can I use AnkiDraft for free and offline?
Yes. AnkiDraft is free, runs offline on your computer, and supports free local AI models via [Ollama](/en/ai-setup/local-models-ollama/) without any paid API subscription.

### Are my PDFs and flashcards uploaded to the cloud?
No. Your PDFs, SQLite database, and media files stay locally on your drive, isolated per profile (`~/.ankidraft/profiles/<profile_name>/`). If you configure a cloud AI provider (OpenAI, Gemini, Claude), only the text passages you explicitly select for card generation are sent directly to your API account.

## 2. Troubleshooting

### macOS shows a security prompt on first launch
Make sure you dragged **AnkiDraft** into your **Applications** folder from the `.dmg` disk image. Official macOS releases are notarized by Apple; if you test an unsigned or *nightly* build and Gatekeeper asks for confirmation, right-click the **AnkiDraft** icon > **Open** (or allow the app in **System Settings > Privacy & Security**).

### Ollama is not detected or no local model appears
Make sure **Ollama** is running locally and listening on the default address (`http://localhost:11434`; for SSRF protection, only local/loopback URLs are allowed under **Settings** (<kbd>Ctrl+,</kbd>) > **AI Engines** > **Local Ollama**). Also ensure you have pulled at least one model via `ollama pull <model>` before testing the connection.

### My scanned PDF has no text or LaTeX formulas look broken
Automatic fast extraction (PyMuPDF / pypdf) works for digital PDFs with selectable text. For scanned handouts or math-heavy lectures, click **`Marker OCR`** in the document toolbar ([PDF & Document Import](/en/sources/import-pdf/)). On first use, AnkiDraft installs PyTorch and local models (~5 GB free disk space and an internet connection required once), after which OCR runs 100% offline.

### How do I export cards to Anki Desktop without losing review history?
Use **Export Anki Cards (.apkg)** (<kbd>Ctrl+Alt+E</kbd>) to create a package for Anki: AnkiDraft never alters FSRS or SM-2 scheduling. Periodically export your full collection (`.colpkg`) from Anki Desktop and import it back into AnkiDraft (<kbd>Ctrl+Shift+I</kbd>) to refresh retention counters and purge deleted cards ([Distributed Lifecycle Guide](/en/guides/cycle_de_vie_distribue/)).

### My math formulas do not render in Anki
Verify that your equations use standard MathJax/KaTeX delimiters (`\( ... \)` for inline math and `\[ ... \]` for centered block equations).

### How do I report a bug or request a feature?
Inside AnkiDraft, open **Settings** (<kbd>Ctrl+,</kbd>) > **Help & Guides** > **Report an Idea or Bug**, click **Help & Feedback** in the sidebar footer, or open an issue on the [official GitHub repository](https://github.com/Skyl9/AnkiDraft/issues).
