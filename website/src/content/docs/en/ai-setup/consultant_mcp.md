---
title: MCP Server, External Agents & Skills
description: "Connect Claude, Cursor, or Antigravity to AnkiDraft via MCP, load dedicated Skills in your agent workspace, and review every batch in Safeguard."
---

AnkiDraft includes a built-in local **MCP (Model Context Protocol)** server (`127.0.0.1:8765`) so you can steer your collection directly from **Claude Desktop**, **Claude Code**, **Cursor**, **Antigravity**, or **Gemini CLI**, with **zero additional API keys**.

To make your assistant immediately reliable with Anki collections, AnkiDraft pairs with a dedicated **agent workspace** (`~/ankiforge_agentique`) containing **ready-to-use MCP Skills**.

## 1. Inside MCP Server & Agents (<kbd>Alt+5</kbd>)

The **MCP Server & Agents** view (<kbd>Alt+5</kbd>) organizes everything across **5 sub-tabs**:

1. **Supervision & Configuration**: start or stop the local server, rotate your access token, and copy one-click JSON configs for **Claude**, **Antigravity (agy)**, **Cursor**, or **cURL**.
2. **Safeguard & Validation**: mandatory two-phase human review gate where every creation, edit, split, or deletion waits for your click (**Apply** or **Reject**).
3. **Tool Catalog**: searchable reference of every MCP tool exposed by the local server.
4. **Activity**: live log of tool calls executed by your external assistant and their status.
5. **Guides & Workspaces**: manages your local agent workspace (`~/ankiforge_agentique` by default) with a compliance matrix, drift detection (**Check Drift**), safe updates (**Resync**), and initialization (**Initialize Workspace**).

## 2. Agent Workspace & Dedicated MCP Skills

Connecting the MCP server gives your client access to raw tools; **opening your agent workspace (`~/ankiforge_agentique`)** in Claude Code, Cursor, or Antigravity equips the assistant with clear guidelines, your active profile context, and **specialized Skills** under `.agents/skills/`:

### General Collection & Authoring Skills (`.agents/skills/general/`)

| User goal | Triggered Skill | What it does |
| :--- | :--- | :--- |
| **Start a session** | `synchronisation-ankiforge` | Detects the active profile, checks MCP tools, and refreshes profile metrics |
| **Get a 360° overview** | `exploration-collection` | Summarizes decks, flags, coverage status, and top priorities |
| **Audit card clarity** | `audit-qualite` | Flags overly long, vague, duplicate, or multi-fact cards |
| **Check note types** | `audit-pertinence-modele` | Measures real field usage and spots redundant card models |
| **Fix failing cards** | `chasse-sangsues` | Diagnoses *leech* cards with repeated lapses and proposes splits or hints |
| **Enrich a deck** | `amelioration-deck` | Proposes wording fixes, clues, enrichments, and atomic splits |
| **Handle flagged cards** | `refactorisation-cartes` | Collects cards flagged during reviews and stages clean rewrite batches |
| **Modernize templates** | `refacto-modeles` | Refactors HTML/CSS note types and fixes styling issues safely |
| **Clean up tags** | `hygiene-taxonomie-tags` | Audits and merges near-duplicate or inconsistent tag clusters |
| **Merge duplicates** | `deduplication-consolidation` | Finds duplicate notes and preserves the one with stronger review history |
| **Find missing concepts** | `audit-couverture-rag` | Compares an imported course document against your deck to fill coverage gaps |
| **Create from notes** | `generation-cours-markdown` | Backs up your profile, structures Markdown courses, generates short cards with previews |
| **Extract from scans** | `ingestion-albums-visuels` | Uses OCR pages and visual plates to build grounded cards from scanned books |

### Profile Context, Shared Domain Rules & Meta Skills

- **Protected profile & subject rules**: `.agents/profiles/<profile>/profile-context.md` tracks your decks and study context, while `.agents/rules/_shared_models/` and `.agents/skills/_shared_domain/` (such as `extraction-japonais`) store reusable subject-specific workflows.
- **Continuous improvement (`meta/`)**: `evolution-skills` refines existing skills after a complex session, and `feedback-dev-ankiforge` captures workflow edge cases.

:::note
When updating from **Guides & Workspaces > Resync**, AnkiDraft refreshes system files (`AGENT.md`, `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.agents/active-profile.md`, `.agents/mcp-catalog.md`) **without ever overwriting** your protected `profiles/`, `_shared_models/`, or `_shared_domain/` skills.
:::

## 3. Safety Safeguard: Two-Phase Human Validation

Neither an external MCP agent nor any workspace skill can alter or delete cards behind your back:
1. The assistant stages proposed changes inside a **Staged Bundle**.
2. Under **MCP Server & Agents** > **Safeguard & Validation**, you inspect a clear before/after diff of every added, edited, split, or deleted card.
3. Click **Apply** or **Reject**: you remain in complete control of your collection.

## 4. Practical Step-by-Step Guides

- **[Zero API Key Workflow: Drive AnkiDraft from Claude or Cursor](/en/workflows/zero-cle-api-agent-mcp/)**: quick setup and ready-to-use prompts that trigger your Skills.
- **[Anki Collection Rescue: Duplicates, Leeches, and MCP Hygiene](/en/workflows/sauvetage-et-hygiene-anki-mcp/)**: clean up an imported `.apkg` deck or `.colpkg` collection without losing review progress.
