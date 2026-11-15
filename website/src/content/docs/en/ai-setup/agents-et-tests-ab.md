---
title: Agent Editor (Alt+9) and A/B Testing Lab
description: Build and version custom personas in Agent Editor (Alt+9), tailor Jinja2 prompts and model overrides, and compare models or pipelines side by side in A/B.
---

The **AI Lab** section in the sidebar brings together the **Agent Editor** (<kbd>Alt+9</kbd>), [DAG Pipelines](/en/cards/dag_et_rag/), and **A/B Tests** so you can tune how the AI drafts and audits cards for each subject.

## 1. Customizing Personas in Agent Editor (<kbd>Alt+9</kbd>)

Open **AI Lab › Agent Editor** (<kbd>Alt+9</kbd>) to create, organize in folders, and refine your agents:

- **Scope and Output Format**:
  - **Agent Scope / Usage**: `Forge Pipeline (DAG)`, `AI Consultant (MCP Server)`, or `Universal (Forge & MCP)` (filterable in the tree via **All**, **Pipeline**, **MCP**, **Universal**).
  - **Output Format**: `json`, `cloze`, `markdown`, or `text`.
- **Dedicated AI Engine (optional)**: pin a specific engine to the agent (for instance a fast or Vision-capable model), or keep inheritance enabled so it follows the **global default AI model** configured in **Settings** (<kbd>Ctrl+,</kbd>).
- **Jinja2 Instructions & Prompt**:
  - Start fast using **Templates...** (ready-made Cloze, Wozniak, or Language starter frameworks).
  - Insert runtime variables at cursor position (`{{ text_source }}`, `{{ last_output }}`, `{{ fields }}`, `{{ retrieved_chunks }}`, `{{ item }}`, `{{ initial_prompt }}`, `{{ state.variables.xxx }}`), browse **Variables**, and check the live interpolated prompt via **Preview**.
- **Tools & Role Presets**: select allowed tools manually or apply built-in presets (*Wozniak Auditor*, *Model & CSS Architect*, *SRS & Leech Analyst*, *RAG & Document Researcher*, *DB & Scripts Admin*, *Universal Consultant*).
- **Unit Testing & Version History**:
  - Click **Test** (<kbd>Ctrl+Enter</kbd>) to run the agent in isolation on a sample snippet before wiring it into a pipeline.
  - Open **History** (Time Machine) to inspect prompt revisions with visual diffs, or duplicate an existing agent before experimenting.

## 2. Comparing Configurations in A/B Tests

Open **AI Lab › A/B Tests** to evaluate two setups objectively on the same source document (or snippet) and target note type:

- **3 Comparison Modes**:
  1. **Compare two AI Engines** (for example `Gemini 3.5 Flash Lite` vs. a local Ollama or free OpenRouter model).
  2. **Compare two Prompts / Personas** using a shared engine.
  3. **Compare two DAG Pipelines** end to end.
- **Inference Controls**: keep shared Temperature and Max Tokens, or check **Independent A/B Settings** to vary parameters per branch, then click **Run A/B Test** (<kbd>Ctrl+Enter</kbd>).
- **4 Side-by-Side Inspection Views**:
  - **Visual Render** (interactive Front/Back preview with **Desktop 100%**, **Tablet 768px**, and **Mobile 375px** toggles plus **Sync Navigation A ↔ B**).
  - **Fields Table** (structured field-by-field breakdown).
  - **Raw JSON** (direct model payloads).
  - **Diff A↔B** (line-by-line comparison), paired with card counts, token totals, latency, and estimated USD cost per branch.
