---
title: Importing Web Pages and Online Articles
description: Capture the core educational content of any online article or web documentation page into clean Markdown without ads, menus, or visual clutter.
---

Studying from online encyclopedias, Wikipedia, technical blogs, or web documentation? The AnkiDraft Web Importer extracts only the relevant study content into clean Markdown.

## 1. Single or Batch Web Capture

1. In **My Documents** (`<kbd>Alt+7</kbd>`), click **Import from Web / YouTube** (or paste URLs directly).
2. Enter one or multiple `http://` / `https://` URLs (**one per line**) and choose a target folder if needed.
3. Configure extraction options:
   - **Download images**: locally stores article illustrations so flashcards work offline.
   - **Merge multi-page articles**: automatically follows `rel="next"` pagination links (from **1 to 10 pages**, default **3**).
4. AnkiDraft strips menus, banners, and ads, normalizes Wikipedia pages cleanly, and converts MathML equations into **LaTeX** formulas.

## 2. Dynamic Pages (SPA) and Known Limits

If a site relies on JavaScript to render its content (single-page applications or interactive docs), check **JavaScript rendering for dynamic pages (SPA)** so AnkiDraft loads the DOM via an isolated WebEngine view (with **no persistent cookies**).

:::note[Technical Limits & Access Restrictions]
- Web downloads are capped at **10 MB** per response.
- Pages protected by a paywall, login screen, or anti-bot gate (HTTP **401**, **402**, **403**) cannot be fetched automatically; export or save them as PDF/Markdown locally first.
:::
