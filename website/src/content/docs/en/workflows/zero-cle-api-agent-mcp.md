---
title: "Zero API Key Workflow: Drive AnkiDraft from Claude or Cursor"
description: "Connect Claude, Cursor, or Antigravity to AnkiDraft's local MCP server, load your Skills workspace, and review every flashcard batch in Safeguard."
---

Already using **Claude Desktop**, **Claude Code**, **Cursor**, or **Antigravity**? AnkiDraft pairs a local MCP connector with a **dedicated Skills workspace** so you can generate flashcards, audit courses, and clean up decks with **zero additional API keys**. Every change waits for your manual approval before being saved.

![Two-phase human approval in AnkiDraft](assets/mcp_two_phase_commit.svg)

## 1. Enable the Local Server and Skills Workspace

1. Open **MCP Server & Agents** (<kbd>Alt+5</kbd>) from the sidebar.
2. Under **Supervision & Configuration**, verify the server is **Active** on port `8765` (or click **Start**), then copy the ready-to-use JSON snippet for **Claude**, **Antigravity (agy)**, or **Cursor**.
3. Switch to **Guides & Workspaces** to check your agent workspace (`~/ankiforge_agentique` by default) with **Check Drift** (or create it via **Initialize Workspace**).
4. Open that workspace folder in Claude Code, Cursor, or Antigravity: your assistant automatically reads the active profile context and loads its **dedicated MCP Skills** ([browse the full Skills reference](/en/ai-setup/consultant_mcp/)).

![AnkiDraft MCP Server Supervision and Config](assets/screen_consultant.png)

## 2. Five Everyday Prompts That Trigger Your Skills

With the workspace open, write natural requests — your assistant picks the right Skill and underlying MCP tools automatically:

### Case A — Sync Context & Get a 360° Collection Overview
- **Skills triggered**: `synchronisation-ankiforge`, `exploration-collection`.
- **Prompt**: *"Sync the workspace with my active AnkiDraft profile and give me a 360° overview of my decks, flagged cards, and imported study documents."*

### Case B — Create Cards from a Lecture or OCR Scan
- **Skills triggered**: `generation-cours-markdown`, `ingestion-albums-visuels` (automatic backup, Markdown structuring, staged insertion, and card preview).
- **Prompt**: *"Read the glycemic regulation sections of document #3, draft 12 short KaTeX flashcards in deck `Biochemistry::Metabolism`, check their rendered preview, and send the batch to Safeguard."*

### Case C — Spot Concepts Missing Between Course and Deck
- **Skill triggered**: `audit-couverture-rag` (plus `diagnose_domain_knowledge_gaps`).
- **Prompt**: *"Compare my Immunology textbook against all my decks, list every missing concept, and stage cards to close the coverage gaps."*

### Case D — Modernize Card Templates and Dark-Mode CSS
- **Skills triggered**: `audit-pertinence-modele`, `refacto-modeles`.
- **Prompt**: *"Audit whether every field in `Medical Cloze` is actually used, improve hint contrast in dark mode, preview the HTML output, and stage the template refactor for my review."*

### Case E — Clean Up Failing Cards, Duplicates, and Tags
- **Skills triggered**: `refactorisation-cartes`, `chasse-sangsues`, `deduplication-consolidation`, `hygiene-taxonomie-tags`.
- **Prompt**: *"Pull my red-flagged cards and recent leeches, split dense cards into shorter ones, merge clear duplicates, and stage a reviewable cleanup bundle."* (See [Anki Collection Rescue & Hygiene](/en/workflows/sauvetage-et-hygiene-anki-mcp/)).

:::tip
To automate repeatable multi-step extractions, your assistant can also trigger your saved [DAG & RAG Pipelines](/en/cards/dag_et_rag/) (`list_pipelines`, `trigger_pipeline_run`).
:::

## 3. Review and Approve Before Saving

No card is ever modified behind your back:
1. Open the **Safeguard & Validation** sub-tab under **MCP Server & Agents** (<kbd>Alt+5</kbd>).
2. Review the **Before / After diff**, explanation for each change, and deletion or split impact.
3. Click **Apply** to save the bundle into AnkiDraft, or **Reject** to discard everything cleanly.
