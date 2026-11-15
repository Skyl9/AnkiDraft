---
title: Using a Free Local Model with Ollama
description: Generate atomic Anki flashcards 100% offline and for free on your computer using local Ollama models with automatic capability detection and zero API keys.
---

Prefer not to use paid cloud APIs, or studying confidential documents offline? AnkiDraft integrates natively with **Ollama**.

## 1. Install Ollama in 2 Minutes

1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Open a terminal and pull a model suited to your computer's RAM:
   - **8 GB RAM**: `ollama pull llama3.2:3b` or `ollama pull qwen2.5:3b`
   - **16 GB+ RAM (e.g., Apple Silicon M1/M2/M3/M4)**: `ollama pull qwen2.5:7b` or `ollama pull mistral`

## 2. Connect and Scan Ollama in AnkiDraft

1. Open **Settings** (<kbd>Ctrl+,</kbd>) › **AI Engines**.
2. Under **LOCAL SERVERS & ACCESS GATEWAYS**, locate **Local Ollama:** (`http://localhost:11434` by default; only local/loopback URLs are allowed as an anti-SSRF safeguard).
3. Click **Scan Models**: AnkiDraft queries Ollama (`/api/tags`), detects each model's capabilities automatically (Vision, Thinking/CoT, JSON output, context window), and imports new models into your catalog marked as **Free / included / local**.
4. You can also add or fine-tune a local model manually via **Add a model ▾** › **Popular quick presets** › **`Ollama Local (llama3)`** or **Custom model...** (useful to enable **Multimodal vision** or adjust **Context Limit** and **Default Temperature**).

:::tip
If local inference runs slowly on CPU or modest hardware, increase **Max generation timeout** and **Default request timeout** in **Settings** (<kbd>Ctrl+,</kbd>) › **AI Engines** so long chapters do not time out prematurely.
:::
