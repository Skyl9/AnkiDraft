---
title: Configuring AI Providers (OpenAI, Gemini, Claude)
description: Securely connect OpenAI, Anthropic, Gemini, Groq, OpenCode, or OpenRouter API keys and configure generation token limits, RAG settings, and MCP budgets.
---

AnkiDraft is **provider-agnostic**: you are free to use the AI service of your choice or switch models depending on the task.

## 1. Supported Providers and Gateways

In **Settings** (<kbd>Ctrl+,</kbd>) › **AI Engines**, you can configure:

- **Dedicated Cloud API Keys (`CLOUD PROVIDER API KEYS`)**:
  - **OpenAI** (`GPT-4o`, `GPT-4o-mini`, `o3-mini`, `o1`, `o1-mini`)
  - **Anthropic** (`Claude 3.7 Sonnet`, `Claude 3.5 Sonnet`, `Claude 3.5 Haiku`)
  - **Google Gemini** (`Gemini 3.5 Flash Lite`, `Gemini 2.0 Flash`, `Gemini 1.5 Pro`)
  - **Groq** (`Llama 3.3 70B`, `DeepSeek-R1 70B` on LPU hardware)
  - **OpenCode** (`DeepSeek V4 Flash`, `Gemini 3.5 Flash Lite`, `GPT-5.4 Mini`, `Qwen 3.8 Flash`)
  - **OpenRouter** (`:free` models including `Qwen 3.8 27B`, `Gemma 4 31B`, `Nemotron 3.5 Lightning`, plus hundreds of paid models)
- **Configurable Local Servers & Gateways (`LOCAL SERVERS & ACCESS GATEWAYS`)**:
  - **Local Ollama** (`http://localhost:11434` by default) — see [Using a Free Local Model with Ollama](/en/ai-setup/local-models-ollama/)
  - **OpenCode Gateway** (`https://opencode.ai/zen/v1` by default)
  - **OpenRouter API** (`https://openrouter.ai/api/v1` by default)
- **Custom Models (`Add a model ▾` › `Custom model...`)**: register any model ID or OpenAI-compatible provider and configure its **Context Limit**, **Generation Cap (max tokens)**, **Default Temperature**, and capabilities (**Multimodal vision**, **Deep reasoning (Thinking / CoT)**, **JSON structured outputs**, **Free / included / local model**).

## 2. Getting a Free API Key (Student Guide)

| Free option | Credit card | How to obtain a key | Recommended preset in AnkiDraft | Caveats to keep in mind |
| :--- | :--- | :--- | :--- | :--- |
| **Google AI Studio** | No | Google account at [aistudio.google.com](https://aistudio.google.com/) → *Create API key* (`AIzaSy...`) | `Google Gemini 3.5 Flash Lite` (vision + PDF) | Rate limits/min & /day; free-tier prompts may be reviewed to improve Google products |
| **OpenRouter (`:free`)** | No | Account at [openrouter.ai](https://openrouter.ai/) → *Keys* (`sk-or-...`) | `OpenRouter Gratuit (Qwen 3.8 27B)` | ~20 req/min & ~50 req/day (or 1,000/day after a one-time $10 credit top-up) |
| **Groq Console** | No | Account at [console.groq.com](https://console.groq.com/) → *API Keys* (`gsk_...`) | `Llama 3.3 70B` / `DeepSeek-R1 70B` | Strict tokens-per-minute caps on very long chapters |
| **GitHub / Campus / OpenCode** | No | **GitHub Student Pack** (`models.github.ai`), **OpenCode** gateway, or university endpoint | **Custom model…** / **OpenCode Gateway** | Depends on student verification or gateway limits |

**Activate it in 30 seconds inside AnkiDraft:**
1. Open **Settings** (<kbd>Ctrl+,</kbd>) › **AI Engines**, paste the key next to the provider, and click **Test**.
2. Below the **ENGINES & MODELS CATALOG**, click **Add a model ▾** › **Popular quick presets** (for example `Google Gemini 3.5 Flash Lite` or `OpenRouter Gratuit (Qwen 3.8 27B)`), or open **Explore catalog & comparator...**.
3. Make sure **Free / included / local model** is checked in the model settings so the top-bar cost counter stays at `$0.00`.

:::note
For confidential medical notes or unlimited offline generation during exam season, prefer [local Ollama](/en/ai-setup/local-models-ollama/) or your existing assistant via [MCP Server (<kbd>Alt+5</kbd>)](/en/workflows/zero-cle-api-agent-mcp/).
:::

## 3. API Key & MCP Server Security

- **Strict OS Keychain Storage**: API keys are stored in your **operating system's secure keychain** (service `AnkiForge`: macOS Keychain, Windows Credential Manager, Linux Secret Service). If no OS keyring is available, keys are never saved in plaintext on disk.
- **Direct Connection**: keys never pass through any middleman server—AnkiDraft connects directly from your computer to your chosen provider.
- **Automatic Log Redaction**: the async logging filter automatically masks secret keys (`sk-*`, `AIza*`) and `Bearer` tokens before writing logs to disk.
- **Local MCP Server (`LOCAL MCP SERVER`)**: in the same **AI Engines** tab, toggle the background server, adjust its **Listening port** (`8765` by default) under **Advanced MCP & diagnostics**, rotate the 256-bit Bearer token (**Rotate token**), and pick the default destination for contextual prompts.

## 4. Global AI Preferences, RAG & Token Caps

- **Global Default AI Model**: choose the default engine inherited by [Agents](/en/ai-setup/agents-et-tests-ab/) or pipeline steps when no override is set.
- **Global Feature Toggles**: control **Streaming responses**, **Vision capabilities enabled**, **Automatic card validation**, and **Automatic Linter audit**.
- **Generation Token Caps, CoT & Timeouts**:
  - Under **Advanced generation & RAG options**: adjust **Temperature**, **Max Tokens Cap** (`4,096` to `128,000`, default `16,384`), **Thinking Budget (CoT)** (`0` to `32,768` tokens), **Max generation timeout**, and semantic retrieval parameters (**RAG Chunks (Top-K)** from `1` to `20`, **Min similarity threshold** from `40%` to `95%`).
  - Under **DEFAULT GENERATION PARAMETERS**: set **Default temperature** (`0.30`), **Default max token budget** (`4,000`), and **Default request timeout** (`60 s`).
- **Consultant Budget Safeguard (`Consultant Token Budget` & `Consultant Cost Budget (USD)`)**: set dedicated caps for Consultant runs (up to `200,000 tokens` and `$5.00`, defaulting to `50,000 tokens` / `$0.50`), with a **preventive stop at 80% of the quota**.
- **Estimations & Spend Tracking**: document pickers and slice composers show an estimated token count (`~X tokens`) for your selected text, DAG pipeline steps accept per-step token budgets, **A/B Tests** estimate USD run cost, and the top-bar counter tracks cumulative consumption.
