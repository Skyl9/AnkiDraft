---
title: MCP Server, External Agents & Workspaces
description: Connect Claude, Cursor, or Antigravity to AnkiDraft's local MCP server, sync your ~/ankiforge_agentique workspace, and review every batch in Safeguard.
---

AnkiDraft includes a built-in local **MCP (Model Context Protocol)** server (`127.0.0.1:8765`, automatically incrementing to a free port if occupied) so you can steer your collection directly from **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf**, or **Antigravity (`agy`)**, with **zero additional API keys**.

To provide your assistant with your active profile context and the live tool list, AnkiDraft also manages a dedicated **agent workspace** (`~/ankiforge_agentique` by default).

## 1. Inside MCP Server & Agents (<kbd>Alt+5</kbd>)

The **MCP Server & Agents** view (<kbd>Alt+5</kbd>) organizes everything across **5 sub-tabs**:

1. **Supervision & Configuration**: start, stop, restart, or ping the local server (Streamable HTTP and SSE transports), rotate the 256-bit Bearer access token (**Rotate token**), and copy ready-to-paste snippets for **Claude**, **Antigravity (agy)**, **Cursor**, or **cURL**.
2. **Safeguard & Validation**: mandatory two-phase human review gate. Individual proposals and multi-step **Staged Bundles** (locked until `commit_staged_bundle`) wait for your explicit approval (**Apply**, **Reject proposal**, **Reject all**).
3. **Tool Catalog**: searchable, domain-filtered inventory of all **93 MCP tools** exposed by the local server (cards, decks, tags, note types, albums, pipelines, agents, documents/knowledge gaps, and workspace drift checks).
4. **Activity**: live log of tool calls executed by your external assistant and their status.
5. **Guides & Workspaces**: manages your local agent workspace (`~/ankiforge_agentique` by default) with a compliance matrix, diff inspector, **Check Drift**, **Resync**, and **Initialize Workspace**.

## 2. The Agent Workspace (`~/ankiforge_agentique`)

Connecting the MCP server alone gives access to the 93 raw tools; **initializing and opening `~/ankiforge_agentique`** in Claude Code, Cursor, or Antigravity also equips your assistant with your active AnkiDraft profile state, safety rules, and synced tool catalog:

- **Root instruction files**: `AGENT.md` (master instructions), `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, and `.gitignore`.
- **Profile & catalog files inside `.agents/`**:
  - `.agents/active-profile.md`: reflects the currently active AnkiDraft profile.
  - `.agents/mcp-catalog.md`: mirrors the exact list of MCP tools available on your server.
  - `.agents/glossary-and-internals.md` and `.agents/rules/ankiforge-conventions.md`: document AnkiDraft internals and two-phase safety constraints.
- **Synced skill templates**: `.agents/skills/general/` (`ask-forge`, `audit-ankiforge`, `code-review`, `domain-modeling`, `doubt-driven-development`, `implement`, `peewee-expert`, `pipeline-dag-ia`, `proposer-commits`, `rag-smart-coverage`, `research`, `tdd`, `ui-pyside6-design`) and `.agents/skills/meta/` (`gouvernance-skills`, `session-retrospective`).

:::note
When updating via **Guides & Workspaces › Resync** (or the `sync_agent_workspace` MCP tool), AnkiDraft runs a non-destructive 3-way sync on system files and **preserves 100%** of your protected user directories **`profiles/`** and **`_shared_models/`**, as well as symbolic links. Drift checks (**Check Drift** / `audit_workspace_drift`) are strictly read-only.
:::

## 3. Safety Safeguard: Two-Phase Human Validation

Neither an external MCP agent nor any tool can modify or delete cards behind your back:
1. The assistant stages proposed changes as intermediate patches or a sequential **Staged Bundle**.
2. Under **MCP Server & Agents** › **Safeguard & Validation**, you inspect a clear before/after diff of every added, edited, split, or deleted card.
3. Click **Apply** or **Reject proposal**: you remain in complete control of your collection.

## 4. Practical Step-by-Step Guides

- **[Zero API Key Workflow: Drive AnkiDraft from Claude or Cursor](/en/workflows/zero-cle-api-agent-mcp/)**: quick setup and ready-to-use prompts for Claude, Cursor, or Antigravity.
- **[Anki Collection Rescue: Duplicates, Leeches, and MCP Hygiene](/en/workflows/sauvetage-et-hygiene-anki-mcp/)**: clean up an imported `.apkg` deck or `.colpkg` collection without losing review progress.
