---
title: Interface Overview
description: Take a guided tour of AnkiDraft workspaces, 4 switchable window layouts (IDE, macOS, Dashboard, Glass), and 12 built-in visual themes for study.
---

AnkiDraft is designed to stay clean and responsive whether you work on a laptop screen or an ultrawide monitor.

## 1. Main Workspaces

The sidebar organizes **11 workspaces** into 4 sections:

### General
- **Dashboard** (<kbd>Alt+1</kbd>): overview of your decks, document coverage progress, and recent activity ([Import .apkg / .colpkg](/en/anki-sync/import-colpkg/) · [Export .apkg](/en/anki-sync/export-apkg/)).

### Forge & Tools
- **Creation Studio** (<kbd>Alt+2</kbd>): interactive, focused card crafting from an excerpt or free-form input (<kbd>Ctrl+N</kbd>) with live preview and card-by-card review ([AI Generation](/en/cards/ai-generation/)).
- **Editor & Browser** (<kbd>Alt+3</kbd>): manual creation, editing with live KaTeX math preview, cloze deletions, per-field TTS, and card management ([Note Editor & KaTeX](/en/cards/editeur_notes_katex/)).
- **Analysis & AI Audit** (<kbd>Alt+4</kbd>): detection of overloaded, vague, or hard-to-memorize flashcards and coverage tracking ([Wozniak Linter](/en/cards/linter_wozniak/)).
- **MCP Server & Agents** (<kbd>Alt+5</kbd>): connect external agents (Claude Desktop, Cursor, Antigravity) to your local collection via MCP with Safeguard review ([MCP Server & Agents](/en/ai-setup/consultant_mcp/)).
- **Batch Factory** (<kbd>Alt+6</kbd>): batch production queue for whole books or multiple chapters (*Batch Slice Composer* with <kbd>Ctrl+N</kbd>, resumable jobs, and Staging review) ([AI Generation](/en/cards/ai-generation/) · [Scope & Slices](/en/sources/scope-and-slices/)).

### Library
- **My Documents** (<kbd>Alt+7</kbd>): library of your PDFs, YouTube videos, audio recordings, web articles, and image albums with per-chapter coverage bars ([Multimodal Hub](/en/sources/hub_multimodal/)).
- **Note Types** (<kbd>Alt+8</kbd>): customize Front/Back and Cloze note types, Jinja2 templates, and CSS styling ([Note Types & Templates](/en/cards/note-types-and-templates/)).

### AI Lab
- **Agent Editor** (<kbd>Alt+9</kbd>): create, prompt with Jinja2, assign tools, and version custom personas ([Agent Editor & A/B Testing](/en/ai-setup/agents-et-tests-ab/)).
- **Pipelines**: build and run multi-step DAG workflows powered by local RAG ([DAG & RAG Pipelines](/en/cards/dag_et_rag/)).
- **A/B Tests**: compare engines, prompts, or pipelines side-by-side on your own course excerpts ([Agent Editor & A/B Testing](/en/ai-setup/agents-et-tests-ab/)).

## 2. Top Bar & Sidebar Footer

In the **top bar** of the window:
- **Sidebar collapse toggle** and active view **breadcrumb**.
- **Search / Command Palette (<kbd>Ctrl+K</kbd> or <kbd>⌘K</kbd>)**: type a few letters to jump to a view, trigger an [`.apkg` export](/en/anki-sync/export-apkg/), open a guide, or change a setting without leaving the keyboard ([Keyboard Shortcuts](/en/guides/raccourcis_clavier/)).
- **AI Cost Counter (`Dépenses : 0.00 $ (0 tk)`)**: real-time cumulative spend and token usage across AI requests ([AI Providers & Budget](/en/ai-setup/ia_fournisseurs/)).
- **Quick Action Buttons**: **Import Anki Package** (<kbd>Ctrl+Shift+I</kbd>), **Export Anki Cards** (<kbd>Ctrl+Alt+E</kbd>), **Notifications** (alerts & diagnostics), and the **`✨ Mise à jour`** badge when an update is ready.

At the bottom of the **left sidebar**:
- **Help & Feedback**: quick access to documentation, troubleshooting ([FAQ & Troubleshooting](/en/guides/faq_depannage/)), and issue reporting.
- **Settings (<kbd>Ctrl+,</kbd>)**: configure appearance, [AI Engines](/en/ai-setup/ia_fournisseurs/), [MCP](/en/ai-setup/consultant_mcp/) server, Anki, TTS, and shortcuts.
- **Profile Switcher (`Profil : <name>`)** and **MCP status indicator**: switch between isolated study workspaces in one click ([Profiles & Workspaces](/en/getting-started/profiles-and-workspaces/)).

## 3. Customizing Layouts and Themes

In **Settings** (<kbd>Ctrl+,</kbd>) › **General**:
- Pick from **4 interchangeable layouts** (*Concept IDE*, *Concept macOS*, *Concept Dashboard*, *Concept Glassmorphism*) using the thumbnail grid.
- Choose **Appearance Mode** (*Dark*, *Light*, *Follow system theme*) independently from **12 bivalent Theme Families** (**24 built-in light/dark palettes**, plus JSON theme import/export).
