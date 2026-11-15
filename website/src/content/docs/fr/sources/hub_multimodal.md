---
title: Hub Documentaire et Formats Multimodaux
description: "Vue d'ensemble des sources dans AnkiDraft : PDF, Web, YouTube, audio, DOCX, PPTX, EPUB, notebooks, code et Albums d'images avec traçabilité complète."
---

La vue **My Documents** (<kbd>Alt+7</kbd>) centralise tous vos supports d'étude au même endroit, organisés en **dossiers** (avec glisser-déposer et **import depuis un autre profil**), et conserve le lien entre chaque flashcard et le passage exact dont elle est issue.

## 1. Tous vos supports au même endroit

| Type de support | Formats | Ce qu'AnkiDraft extrait |
| :--- | :--- | :--- |
| **Cours et livres PDF** | `.pdf` | Plan des chapitres, texte, tableaux, figures et formules LaTeX |
| **Albums d'images** | Images groupées (`.png`, `.jpg`, `.webp`…) | Classement par planches, rotation/recadrage, transcription OCR par IA vision et RAG visuel ([Albums d'Images](/fr/sources/albums-images/)) |
| **Vidéos en ligne** | Liens YouTube (`youtube.com`, `youtu.be`) | Sous-titres horodatés ou transcription vocale (via `yt-dlp` + Whisper) |
| **Enregistrements audio** | `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac` (`.wma`, `.webm`) | Transcription segmentée par paragraphes + lecteur audio intégré |
| **Pages web & Wikipédia** | URLs `http://` / `https://` | Corps de l'article épuré, formules MathML → LaTeX et images en option |
| **Bureautique, Ebooks & Code** | `.docx`, `.pptx`, `.epub`, `.md`, `.txt`, `.ipynb`, `.py` | Structure hiérarchique des titres, listes, cellules de notebooks et code Python |

## 2. Retrouver la source d'une carte en un clic

Lorsque vous relisez ou modifiez une carte dans **Édition & Navigateur** (<kbd>Alt+3</kbd>), le bandeau de traçabilité affiche le document et le fil d'Ariane : cliquez sur **`Voir le cours ➔`** pour revenir immédiatement au passage correspondant dans **My Documents**.

À l'inverse, dans l'Inspecteur droit de **My Documents** (onglet **Couverture**), le bouton **Synchroniser les cartes** permet de rattacher a posteriori vos fiches existantes portant des tags `source:`, `section:` ou `page:`.
