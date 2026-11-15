---
title: Quickstart Guide
description: "Create, review, and export your first Anki flashcard deck in 5 minutes with AnkiDraft, and pick the step-by-step workflow tailored to your subject."
---

This guide walks you through creating your first Anki flashcard deck in minutes and helps you pick the end-to-end workflow that matches your study material and AI setup.

## Which workflow fits your goal?

![AnkiDraft workflow decision tree](assets/arbre_decision_workflow.svg)

Pick the step-by-step guide that matches your study material:

1. **[Written Docs & STEM: PDFs, formulas, and diagrams](/en/workflows/medecine-sciences-pdf/)** — pick the relevant chapters from a textbook, keep equations and figures, and check that every card is clear.
2. **[Languages & Pronunciation: vocabulary and offline audio](/en/workflows/langues-et-audio-tts/)** — add natural offline voice pronunciation to your vocabulary cards and fix ambiguous wording.
3. **[Video & Audio: YouTube lectures and recordings](/en/workflows/cours-video-youtube-audio/)** — transcribe recorded lectures and turn key explanations into flashcards.
4. **[Collection Cleanup & Hygiene for an existing Anki deck](/en/workflows/sauvetage-et-hygiene-anki-mcp/)** — import an `.apkg` deck or `.colpkg` collection, remove duplicates, split overly long cards, and export back without losing your review progress.
5. **[Fill knowledge gaps against a textbook](/en/cards/dag_et_rag/)** — link existing cards to textbook chapters to spot missed concepts right away.

- **[Cross-cutting mode — Work with zero API key using Claude or Cursor](/en/workflows/zero-cle-api-agent-mcp/)** — applies to any of the workflows above if you prefer driving AnkiDraft from your existing AI plan.

## Two Ways to Work with AI

AnkiDraft works both on its own and connected to your existing AI assistant (Claude, Cursor).

| Dimension | Built-in Studio (inside the app) | With Your AI Assistant (Claude, Cursor) |
| :--- | :--- | :--- |
| **What you need** | Free offline model ([Ollama](/en/ai-setup/local-models-ollama/)) or an [API key](/en/ai-setup/ia_fournisseurs/) | Your existing plan (Claude Desktop/Code, Cursor) — **zero API key** |
| **How it works** | Visual buttons, chapter selection, and batch generation | Chat naturally in your AI assistant connected to AnkiDraft |
| **Best suited for** | Extracting PDF chapters, adding voice audio, editing formulas | Spotting gaps across decks, bulk cleanup, and card rewrites |
| **Your control** | Review every card before saving | **Approval required**: nothing changes until you click **Apply** |

## How to Get a Free API Key (Student Guide)

You do not need a credit card or paid subscription to use the built-in Studio — here are the easiest ways to get a free API key that works right inside AnkiDraft:

1. **Google AI Studio (`Gemini`) — easiest starting point**: sign in with a Google account at [aistudio.google.com](https://aistudio.google.com/) and click **Create API key** (no credit card required). Paste the key (`AIzaSy...`) under **Settings > AI Engines > Gemini**, click **Test**, and pick the built-in **`Google Gemini 3.5 Flash Lite`** preset (great for PDFs and diagrams within daily rate limits; avoid sending sensitive private data on the free tier).
2. **OpenRouter (`:free`) — multiple free models from one key**: create a free account at [openrouter.ai](https://openrouter.ai/) with no credit card, generate a key (`sk-or-...`), and use built-in `$0` models ending in `:free` such as **`OpenRouter Free (Qwen 3.8 27B)`** (subject to per-minute and daily rate caps).
3. **Groq Console — ultra-fast open models**: generate a free key (`gsk_...`) at [console.groq.com](https://console.groq.com/) with no credit card for high-speed card drafting and auditing (subject to tokens-per-minute limits).
4. **Student perks & campus access**: use your university email to check eligibility for the **GitHub Student Developer Pack** (including **GitHub Models** access), **Google AI student offers**, **Mistral's** free experimentation tier ([console.mistral.ai](https://console.mistral.ai/)), or university-hosted AI endpoints / academic cloud credits (configurable via **Custom model…**).

:::tip
See exact UI presets, privacy tips, and budget caps in [Configuring AI Providers](/en/ai-setup/ia_fournisseurs/).
:::

## Get Started in 4 Simple Steps

### Step 1: Select or Create Your Profile

On first launch, AnkiDraft opens the `default` profile. To keep bulky course files separate from personal decks, create a dedicated profile from the selector at the top of the window ([Manage profiles](/en/getting-started/profiles-and-workspaces/)).

### Step 2: Choose an AI Engine (Optional)

Open **Settings** (<kbd>Ctrl+,</kbd>) and switch to **AI Engines**:
- **Free & 100% offline**: install [Ollama](/en/ai-setup/local-models-ollama/) locally and pick a model.
- **With an API key (free or paid)**: paste a [free-tier key from the options above](#how-to-get-a-free-api-key-student-guide) (Google Gemini, OpenRouter `:free`, Groq…) or a paid OpenAI / Anthropic key, stored encrypted in your OS keychain.
- **Zero API key**: turn on the local connection in **MCP Server & Agents** (<kbd>Alt+5</kbd>) to use your [Claude or Cursor plan](/en/workflows/zero-cle-api-agent-mcp/).

### Step 3: Import Your First Study Material

1. Open **My Documents** (<kbd>Alt+7</kbd>) from the sidebar.
2. Drag and drop a PDF, Word, PowerPoint, or EPUB file, or paste a YouTube video link.
3. For a focused excerpt or free-form note, switch to **Creation Studio** (<kbd>Alt+2</kbd>); to split and queue an entire textbook by chapter, open **Batch Factory** (<kbd>Alt+6</kbd>) › **Batch Slice Composer**.

### Step 4: Review, Improve, and Export to Anki

Review the generated cards, run a quick check in **Analysis & AI Audit** (<kbd>Alt+4</kbd>) to catch overly long or vague cards, then press <kbd>Ctrl+Alt+E</kbd> (**Export Anki Cards (.apkg)**). Double-click the exported `.apkg` file to add your cards directly into Anki.

> Want plain-language definitions with concrete Before / After examples? Read the [User Glossary](/en/guides/glossaire/).
