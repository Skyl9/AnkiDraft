---
title: Configuring AI Providers (OpenAI, Gemini, Claude)
description: Securely connect your OpenAI, Anthropic, or Gemini API keys, configure local providers, and track your token budget per pipeline in AnkiDraft.
---

AnkiDraft is **provider-agnostic**: you are free to use the AI service of your choice or switch models depending on the task.

## 1. Supported Providers

In **Settings** (<kbd>Ctrl+,</kbd>) > **AI Engines**, you can configure:
- **Google Gemini** (`Gemini 3.5 Flash Lite`, `Gemini 2.0 Flash`, `Gemini 1.5 Pro`)
- **OpenRouter** (`:free` models including `Qwen 3.8 27B`, `Gemma 4 31B`, `Nemotron 3.5 Lightning`, plus hundreds of paid models)
- **Groq** (`Llama 3.3 70B`, `DeepSeek-R1 70B` on LPU hardware)
- **OpenAI** (`GPT-4o`, `GPT-4o-mini`, `o3-mini`) and **Anthropic Claude** (`Claude Sonnet`, `Claude Haiku`)
- **OpenCode** and **any OpenAI-compatible endpoint** (Mistral, university server)
- **Ollama (100% Free & Offline)**: see [Using a Free Local Model with Ollama](/en/ai-setup/local-models-ollama/).

## 2. Getting a Free API Key (Student Guide)

| Free option | Credit card | How to obtain a key | Recommended preset in AnkiDraft | Caveats to keep in mind |
| :--- | :--- | :--- | :--- | :--- |
| **Google AI Studio** | No | Google account at [aistudio.google.com](https://aistudio.google.com/) → *Create API key* (`AIzaSy...`) | `Google Gemini 3.5 Flash Lite` (vision + PDF) | Rate limits/min & /day; free-tier prompts may be reviewed to improve Google products |
| **OpenRouter (`:free`)** | No | Account at [openrouter.ai](https://openrouter.ai/) → *Keys* (`sk-or-...`) | `OpenRouter Free (Qwen 3.8 27B)` | ~20 req/min & ~50 req/day (or 1,000/day after a one-time $10 credit top-up) |
| **Groq Console** | No | Account at [console.groq.com](https://console.groq.com/) → *API Keys* (`gsk_...`) | `Llama 3.3 70B` / `DeepSeek-R1 70B` | Strict tokens-per-minute caps on very long chapters |
| **Mistral / GitHub / Campus** | No | Free tier on [Mistral](https://console.mistral.ai/), **GitHub Student Pack** (`models.github.ai`), **Google AI student offers**, or campus gateway | **Custom model…** (OpenAI-compatible URL) | Depends on student verification or university limits |

**Activate it in 30 seconds inside AnkiDraft:**
1. Open **Settings** (<kbd>Ctrl+,</kbd>) > **AI Engines**, paste the key next to the provider, and click **Test**.
2. In the engine list below, click **Add a model** > **Popular quick presets** (for example `Google Gemini 3.5 Flash Lite` or `OpenRouter Free (Qwen 3.8 27B)`), or browse **Explore Catalog & Comparator...**.
3. Make sure **Free / included / local model** is checked so the top-bar cost counter stays at `$0.00`.

:::note
For confidential medical notes or unlimited offline generation during exam season, prefer [local Ollama](/en/ai-setup/local-models-ollama/) or your existing assistant via [MCP Server (<kbd>Alt+5</kbd>)](/en/workflows/zero-cle-api-agent-mcp/).
:::

## 3. API Key Security

- Your API keys are stored in your **operating system's secure keychain** (macOS Keychain, Windows Credential Manager, Linux Secret Service).
- Keys never pass through any middleman server: AnkiDraft connects directly from your computer to your chosen provider.
- Application logs automatically redact any secret key (`sk-*`, `AIza*`).

## 4. Token Budget Control

Before running a batch generation across a large textbook, AnkiDraft estimates the required token count and lets you set a strict per-run token cap to prevent unexpected API bills.
