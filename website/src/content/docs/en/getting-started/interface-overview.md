---
title: Interface Overview
description: Take a guided tour of AnkiDraft workspaces, 4 switchable window layouts (IDE, macOS, Dashboard, Glass), and 12 built-in visual themes for study.
---

AnkiDraft is designed to stay clean and responsive whether you work on a laptop screen or an ultrawide monitor.

## 1. Main Workspaces

The sidebar organizes **11 workspaces** into 4 sections:

### General
- **Dashboard**: overview of your decks, document coverage progress, and recent activity ([Import .apkg / .colpkg](/en/anki-sync/import-colpkg/) · [Export .apkg](/en/anki-sync/export-apkg/)).

### Forge & Tools
- **Creation Studio** (<kbd>Alt+2</kbd>): interactive, focused card crafting from an excerpt or free-form input (<kbd>Ctrl+N</kbd>) with live preview and card-by-card review ([AI Generation](/en/cards/ai-generation/)).
- **Editor & Browser**: manual creation, editing with live KaTeX math preview, cloze deletions, and card management ([Note Editor & KaTeX](/en/cards/editeur_notes_katex/)).
- **Analysis & AI Audit**: detection of overloaded, vague, or hard-to-memorize flashcards and coverage tracking ([Wozniak Linter](/en/cards/linter_wozniak/)).
- **MCP Server & Agents**: connect external agents (Claude Desktop, Cursor) to your local collection via MCP with Safeguard review ([MCP Server & Agents](/en/ai-setup/consultant_mcp/)).
- **Batch Factory** (<kbd>Alt+6</kbd>): batch production queue for whole books or multiple chapters (*Batch Slice Composer*, resumable jobs, and Staging review) ([AI Generation](/en/cards/ai-generation/) · [Scope & Slices](/en/sources/scope-and-slices/)).

### Library
- **My Documents**: library of your PDFs, YouTube videos, audio recordings, and web articles with per-chapter coverage bars ([Multimodal Hub](/en/sources/hub_multimodal/)).
- **Note Types**: customize Front/Back and Cloze note types, Jinja2 templates, and CSS styling ([Note Types & Templates](/en/cards/note-types-and-templates/)).

### AI Lab
- **Agent Editor**: configure and customize AI prompts and personas ([AI Providers & Budget](/en/ai-setup/ia_fournisseurs/) · [Local Models with Ollama](/en/ai-setup/local-models-ollama/)).
- **Pipelines**: build and run multi-step DAG workflows powered by local RAG ([DAG & RAG Pipelines](/en/cards/dag_et_rag/)).
- **A/B Tests**: compare AI prompts and models side-by-side on your own course excerpts.

## 2. Top Bar & Main Menus

Always visible directly in the top bar of the window:

- **Profile Switcher**: switch between isolated study workspaces in one click ([Profiles & Workspaces](/en/getting-started/profiles-and-workspaces/)).
- **AI Cost Counter (`$0.00`)**: real-time tracking of cumulative token spending across your AI providers ([AI Providers & Budget](/en/ai-setup/ia_fournisseurs/)).
- **Search / Command Palette (<kbd>Ctrl+K</kbd>)**: type a few letters to jump to a view, trigger an [`.apkg` export](/en/anki-sync/export-apkg/), open a user guide, or change a setting without leaving the keyboard. See also the [keyboard shortcuts reference](/en/guides/raccourcis_clavier/).
- **Help & Feedback**: quick access to documentation, troubleshooting ([FAQ & Troubleshooting](/en/guides/faq_depannage/)), and issue reporting.
- **Settings (<kbd>Ctrl+,</kbd>)**: configure AI providers, local [Ollama](/en/ai-setup/local-models-ollama/) models, [MCP](/en/ai-setup/consultant_mcp/) server, and appearance.

## 3. Customizing Layouts and Themes

In **Settings** (<kbd>Ctrl+,</kbd>) > **Appearance**:
- Pick from **4 interchangeable layouts** (*IDE Studio*, *macOS Native*, *Dashboard*, *Glassmorphism*) using high-resolution preview cards.
- Choose from **12 color themes** (light and dark) crafted for long study sessions.
