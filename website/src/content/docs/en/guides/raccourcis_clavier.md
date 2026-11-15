---
title: Keyboard Shortcuts Reference
description: Official reference of all keyboard shortcuts in AnkiDraft by category and scope to navigate workspaces, edit cards, and run AI pipelines fast.
---

<!-- ⚠️ TRANSLATED FROM THE AUTO-GENERATED SHORTCUTS CATALOG (src/ankidraft/ui/shortcuts/catalog.py) -->

This page is the **official and complete reference** for all AnkiDraft keyboard shortcuts from the central declarative registry (`src/ankidraft/ui/shortcuts/`).

:::note
All shortcuts listed below can be viewed, searched, and customized in the app under **Settings (Ctrl+,) > Keyboard**. On macOS, <kbd>Ctrl</kbd> maps automatically to <kbd>Cmd ⌘</kbd>.
:::

---

## 🏛️ Architecture & Keyboard Rules

1. **Strict 4-tier scope hierarchy**:
    - **Dialog**: highest priority when a modal dialog is open.
    - **Widget**: active only when a specific widget (table, list, canvas) holds focus.
    - **View**: active within the currently displayed main workspace view.
    - **Application**: global across the entire application (command palette, navigation, settings).
2. **Text-input priority**: whenever a text field (`QLineEdit`, `QTextEdit`, KaTeX) has focus, single-key and card-level shortcuts never trigger unintended card actions.
3. **Protected sequences**: essential system shortcuts (`Ctrl+C`, `Ctrl+V`, `Ctrl+Z`, `Ctrl+A`, `Ctrl+W`, `Ctrl+Q`) cannot be reassigned to prevent ergonomic conflicts.

---

## 📋 Shortcut Inventory (98 actions)

### Application

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Command Palette** | <kbd>Ctrl+K</kbd> | `Application` | Open the global command palette omnibox | `app.command_palette` |
| **Settings** | <kbd>Ctrl+,</kbd> | `Application` | Open the Settings dialog | `app.settings` |
| **Save** | <kbd>Ctrl+S</kbd> | `Application` | Unified save router for the active view | `app.save` |
| **Primary View Action** | <kbd>Ctrl+Return</kbd> | `Application` | Trigger the main action in the active view (generation, run) | `app.run_primary` |
| **Find** | <kbd>Ctrl+F</kbd> | `Application` | Focus the search field in the active view | `app.find` |
| **Import Anki Package (.apkg)** | <kbd>Ctrl+Shift+I</kbd> | `Application` | Open the collection or deck import wizard | `app.import` |
| **Export Anki Cards (.apkg)** | <kbd>Ctrl+Alt+E</kbd> | `Application` | Open the card export dialog | `app.export` |
| **AnkiDraft Guided Tour** | <kbd>F1</kbd> | `Application` | Launch the interactive feature tour | `app.tour` |
| **Version History** | <kbd>Ctrl+H</kbd> | `View` | Display the timeline and previous card versions | `view.history` |

### Navigation

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Go to View 1** | <kbd>Alt+1</kbd> | `Application` | — | `nav.view_1` |
| **Go to View 2** | <kbd>Alt+2</kbd> | `Application` | — | `nav.view_2` |
| **Go to View 3** | <kbd>Alt+3</kbd> | `Application` | — | `nav.view_3` |
| **Go to View 4** | <kbd>Alt+4</kbd> | `Application` | — | `nav.view_4` |
| **Go to View 5** | <kbd>Alt+5</kbd> | `Application` | — | `nav.view_5` |
| **Go to View 6** | <kbd>Alt+6</kbd> | `Application` | — | `nav.view_6` |
| **Go to View 7** | <kbd>Alt+7</kbd> | `Application` | — | `nav.view_7` |
| **Go to View 8** | <kbd>Alt+8</kbd> | `Application` | — | `nav.view_8` |
| **Go to View 9** | <kbd>Alt+9</kbd> | `Application` | — | `nav.view_9` |
| **Next View** | <kbd>Ctrl+Tab</kbd> | `Application` | — | `nav.next_view` |
| **Previous View** | <kbd>Ctrl+Shift+Tab</kbd> | `Application` | — | `nav.prev_view` |

### Editing & Browser

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Move to Deck…** | <kbd>Ctrl+D</kbd> | `View` | Move selected cards or notes to another deck | `edition.move_to_deck` |
| **New Deck…** | <kbd>Ctrl+N</kbd> | `View` | Create a new flashcard deck | `edition.new_deck` |
| **Deselect All** | <kbd>Ctrl+Shift+A</kbd> | `View` | Uncheck and deselect all cards in the view | `edition.deselect_all` |
| **Edit Focused Note** | <kbd>Ctrl+E</kbd> | `View` | Focus the field editor for the selected note | `edition.edit_note` |
| **Edit Focused Note (Quick Key)** | <kbd>E</kbd> *(single key)* | `Widget` | Open the editor directly from the card table | `edition.edit_note_bare` |
| **Change Note Type…** | <kbd>Ctrl+Shift+M</kbd> | `View` | Change the note type of the selected cards | `edition.change_model` |
| **Toggle Cards / Notes** | <kbd>Ctrl+Alt+T</kbd> | `View` | Switch table display between individual cards and parent notes | `edition.toggle_display_mode` |
| **Targeted Find & Replace…** | <kbd>Ctrl+Alt+F</kbd> | `View` | Open Group Edit pre-configured on Find and Replace | `edition.find_replace` |
| **Delete Selection** | <kbd>Ctrl+Delete</kbd> | `View` | Permanently delete selected cards or notes | `edition.delete` |
| **Suspend / Unsuspend** | <kbd>Ctrl+J</kbd> | `View` | Toggle suspended state on selected cards or notes | `edition.suspend` |
| **Suspend / Unsuspend (Table)** | <kbd>!</kbd> *(single key)* | `Widget` | Toggle suspended state from the focused table | `edition.suspend_bare` |
| **Group Edit…** | <kbd>Ctrl+Shift+E</kbd> | `View` | Open the batch Group Edit dialog | `edition.group_edit` |
| **Show / Hide Preview** | <kbd>Ctrl+P</kbd> | `View` | Toggle the card preview side panel | `edition.toggle_preview` |
| **Collapse / Expand Card List** | <kbd>Ctrl+Shift+T</kbd> | `View` | Collapse or expand the card table panel | `edition.toggle_table` |
| **Previous Card** | <kbd>Alt+Up</kbd> | `View` | Select the previous card in the table | `edition.prev_card` |
| **Next Card** | <kbd>Alt+Down</kbd> | `View` | Select the next card in the table | `edition.next_card` |
| **No Flag** | <kbd>Ctrl+0</kbd> | `View` | Remove any flag from selected cards | `edition.flag_0` |
| **Flag 1 (Red)** | <kbd>Ctrl+1</kbd> | `View` | — | `edition.flag_1` |
| **Flag 2 (Orange)** | <kbd>Ctrl+2</kbd> | `View` | — | `edition.flag_2` |
| **Flag 3 (Green)** | <kbd>Ctrl+3</kbd> | `View` | — | `edition.flag_3` |
| **Flag 4 (Blue)** | <kbd>Ctrl+4</kbd> | `View` | — | `edition.flag_4` |
| **Flag 5 (Pink)** | <kbd>Ctrl+5</kbd> | `View` | — | `edition.flag_5` |
| **Flag 6 (Turquoise)** | <kbd>Ctrl+6</kbd> | `View` | — | `edition.flag_6` |
| **Flag 7 (Purple)** | <kbd>Ctrl+7</kbd> | `View` | — | `edition.flag_7` |
| **Bold** | <kbd>Ctrl+B</kbd> | `View` | Apply bold formatting to selected text | `edition.format_bold` |
| **Italic** | <kbd>Ctrl+I</kbd> | `View` | Apply italic formatting to selected text | `edition.format_italic` |
| **Underline** | <kbd>Ctrl+U</kbd> | `View` | Apply underline formatting to selected text | `edition.format_underline` |
| **Cloze Deletion** | <kbd>Ctrl+Shift+C</kbd> | `View` | Insert an Anki cloze deletion (`{{c1::...}}`) | `edition.format_cloze` |
| **KaTeX Formula** | <kbd>Ctrl+M</kbd> | `View` | Insert a KaTeX math inline or block formula | `edition.format_math` |
| **Inline Code** | <kbd>Ctrl+K</kbd> | `View` | Wrap selected text in code tags | `edition.format_code` |

### Studio & Batch

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **New Input Tab** | <kbd>Ctrl+N</kbd> | `View` | Open a new free-form input tab in Creation Studio | `creation.new_input` |
| **Compose Batch…** | <kbd>Ctrl+N</kbd> | `View` | Open the Batch Slice Composer dialog | `batch.compose` |
| **Validate Card (Space)** | <kbd>Space</kbd> *(single key)* | `Widget` | Mark the focused card as approved | `review.validate_space` |
| **Validate Card (V)** | <kbd>V</kbd> *(single key)* | `Widget` | Mark the focused card as approved | `review.validate_v` |
| **Reject Card (Delete)** | <kbd>Delete</kbd> *(single key)* | `Widget` | Reject the focused card | `review.reject_delete` |
| **Reject Card (Backspace)** | <kbd>Backspace</kbd> *(single key)* | `Widget` | Reject the focused card | `review.reject_backspace` |
| **Reject Card (R)** | <kbd>R</kbd> *(single key)* | `Widget` | Reject the focused card | `review.reject_r` |
| **Edit Card** | <kbd>E</kbd> *(single key)* | `Widget` | Enable inline editing for the focused card | `review.edit` |
| **Previous Card** | <kbd>Alt+Left</kbd> | `Widget` | Select the previous card in the review table | `review.prev_card` |
| **Next Card** | <kbd>Alt+Right</kbd> | `Widget` | Select the next card in the review table | `review.next_card` |
| **Previous Slice** | <kbd>Alt+Up</kbd> | `Widget` | Switch to the previous task or slice in batch review | `review.prev_task` |
| **Next Slice** | <kbd>Alt+Down</kbd> | `Widget` | Switch to the next task or slice in batch review | `review.next_task` |

### Documents

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Import Document** | <kbd>Ctrl+O</kbd> | `View` | Open the file picker to import a document or course | `documents.import_file` |
| **New Album…** | <kbd>Ctrl+N</kbd> | `View` | Create a new image document album | `documents.new_album` |
| **Delimit Scope…** | <kbd>Ctrl+Alt+P</kbd> | `View` | Open the document scope & exclusion dialog | `documents.delimit_scope` |
| **Vectorize in RAG** | <kbd>Ctrl+Alt+R</kbd> | `View` | Start vector indexing of the active document for semantic search | `documents.vectorize` |
| **Show / Hide Coverage** | <kbd>Ctrl+Alt+C</kbd> | `View` | Toggle the coverage and structure inspection panel | `documents.toggle_coverage` |

### Analysis & Audit

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Reindex Sources** | <kbd>Ctrl+Alt+R</kbd> | `View` | Reindex the selected topic or document in Analysis | `analysis.reindex` |
| **Align Sources** | <kbd>Ctrl+Alt+A</kbd> | `View` | Synchronize and align Anki cards with source sections | `analysis.align_sources` |
| **Forge Focused Fragment** | <kbd>Ctrl+Alt+F</kbd> | `View` | Open Creation Studio on the selected orphan section | `analysis.forge_fragment` |

### Note Types

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **New Note Type** | <kbd>Ctrl+N</kbd> | `View` | Create a new card note type | `models.new_type` |
| **Duplicate Note Type** | <kbd>Ctrl+Shift+D</kbd> | `View` | Duplicate the currently selected note type | `models.duplicate` |
| **Import Note Type (JSON)…** | <kbd>Ctrl+Alt+O</kbd> | `View` | Import a note type definition from a JSON file | `models.import_json` |
| **Export Note Type (JSON)…** | <kbd>Ctrl+Alt+E</kbd> | `View` | Export the selected note type to JSON | `models.export_json` |
| **Format Code** | <kbd>Ctrl+Alt+L</kbd> | `Widget` | Re-indent and clean HTML or CSS code in the editor | `code.format` |

### Pipelines & Agents

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **New Agent** | <kbd>Ctrl+N</kbd> | `View` | Create a new AI agent in the workshop | `agents.new` |
| **Duplicate Agent** | <kbd>Ctrl+Shift+D</kbd> | `View` | Clone the selected AI agent | `agents.duplicate` |
| **New Pipeline** | <kbd>Ctrl+N</kbd> | `View` | Create a new DAG pipeline | `pipelines.new` |
| **Move Step Up** | <kbd>Ctrl+Up</kbd> | `View` | Move the selected step earlier in the DAG | `pipelines.move_step_up` |
| **Move Step Down** | <kbd>Ctrl+Down</kbd> | `View` | Move the selected step later in the DAG | `pipelines.move_step_down` |
| **Delete Focused Step** | <kbd>Delete</kbd> *(single key)* | `Widget` | Delete the currently selected step in the workflow | `pipelines.delete_step` |

### A/B Lab

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Previous Sample A** | <kbd>Alt+Up</kbd> | `View` | Show the previous card generated by Branch A | `ab.sample_a_prev` |
| **Next Sample A** | <kbd>Alt+Down</kbd> | `View` | Show the next card generated by Branch A | `ab.sample_a_next` |
| **Previous Sample B** | <kbd>Alt+Left</kbd> | `View` | Show the previous card generated by Branch B | `ab.sample_b_prev` |
| **Next Sample B** | <kbd>Alt+Right</kbd> | `View` | Show the next card generated by Branch B | `ab.sample_b_next` |

### Smart Merge

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Previous Conflict** | <kbd>Alt+Left</kbd> | `Dialog` | Navigate to the previous import conflict | `merge.prev_conflict` |
| **Next Conflict** | <kbd>Alt+Right</kbd> | `Dialog` | Navigate to the next import conflict | `merge.next_conflict` |
| **Keep All Local** | <kbd>Ctrl+Alt+Left</kbd> | `Dialog` | Keep all local field values for the conflicting card | `merge.keep_all_local` |
| **Keep All Incoming** | <kbd>Ctrl+Alt+Right</kbd> | `Dialog` | Replace all field values with the incoming version | `merge.keep_all_incoming` |
| **Confirm Merge** | <kbd>Ctrl+Return</kbd> | `Dialog` | Confirm conflict resolutions and apply the merge | `merge.confirm` |

### Tooling & Debug

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Debug Screenshot** | <kbd>Ctrl+F12</kbd> | `Application` | Save a UI snapshot for diagnostic purposes | `app.debug_screenshot` |
| **Dialog Gallery (Dev)** | <kbd>Ctrl+Alt+D</kbd> | `Application` | Open the dialog showcase in development mode | `app.debug_gallery` |

### Dialogs

| Action | Default Sequence | Scope | Description | Identifier |
| :--- | :--- | :--- | :--- | :--- |
| **Close Dialog** | <kbd>Escape</kbd> | `Dialog` | Close the active dialog without confirming | `dialog.close` |
| **Confirm Dialog** | <kbd>Return</kbd> | `Dialog` | Confirm and accept the dialog selection | `dialog.confirm` |
| **Apply Changes** | <kbd>Ctrl+Return</kbd> | `Dialog` | Validate or apply changes without closing the dialog | `dialog.apply` |
| **New Deck** | <kbd>Ctrl+N</kbd> | `Dialogue` | Open new deck creation inside the deck picker | `dialog.new_deck` |
| **Previous Item** | <kbd>Up</kbd> *(single key)* | `Widget` | Select the previous item in the dialog list | `dialog.prev_item` |
| **Next Item** | <kbd>Down</kbd> *(single key)* | `Widget` | Select the next item in the dialog list | `dialog.next_item` |
