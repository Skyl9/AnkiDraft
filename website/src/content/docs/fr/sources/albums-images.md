---
title: Albums d'Images, Scans Photo et OCR Vision
description: "Rassemblez photos de tableaux, scans et schémas dans un Album d'Images, transcrivez-les en Markdown par IA vision, indexez en RAG et créez vos cartes."
---

Vous avez pris en photo le tableau de l’amphithéâtre, photographié des fiches manuscrites ou récupéré des planches d’anatomie en vrac ? Dans **My Documents** (<kbd>Alt+7</kbd>), les **Albums d’images** regroupent vos visuels page par page pour les organiser, les transcrire par IA vision et en tirer des flashcards.

## 1. Créer et organiser un Album d'images

1. Ouvrez **My Documents** (<kbd>Alt+7</kbd>) et cliquez sur l’icône **Créer un Album d’images** (ou **Créer un album** dans l’état vide).
2. Donnez un titre, choisissez le dossier de classement et l’ordre de tri initial :
   - **Tri alphanumérique naturel** (`page_1`, `page_2`…)
   - **Date de prise de vue EXIF** (ordre chronologique de votre appareil photo)
   - **Ordre d’importation brut**
3. Une fois l’album ouvert, chaque planche dispose d’actions rapides : déplacer à gauche/droite, **tourner de 90°**, **inspecter / recadrer**, supprimer ou ajouter de nouvelles images (**Ajouter des images**).

## 2. Transcrire l'album en Markdown par IA vision

1. Cliquez sur **Transcrire l’album…** dans la barre d’outils de l’album.
2. Choisissez un moteur compatible **Vision multimodale** (ex. `Google Gemini 3.5 Flash Lite` ou un modèle local vision sous Ollama ; AnkiDraft bloque et signale les modèles texte seuls).
3. Ciblez précisément les planches à traiter :
   - **Tout l’album**
   - **Planches non transcrites uniquement**
   - **Planches périmées** (modifiées ou pivotées depuis la dernière transcription)
   - **Intervalle personnalisé** (ex. `1-5, 8, 12-15`)
4. Précisez le **Type de donnée d’image** (type de planches/documents) et vos consignes. Si certaines pages échouent (quota ou réseau), cliquez simplement sur **Relancer les échecs**.

## 3. Exploiter vos planches : RAG visuel, PDF et Flashcards

- **RAG Visuel** : indexe les planches et schémas dans FAISS pour interroger l’album via la recherche sémantique.
- **Compiler en PDF** : assemble toutes les pages (avec leurs rotations et recadrages) en un document PDF de lecture unique.
- **Forger des cartes** : envoie l’album directement vers le Studio de Création (<kbd>Alt+2</kbd>) ou lancez une **occlusion d’image** depuis l’inspecteur pour masquer des légendes de schémas.

:::tip
Vous travaillez sans clé API avec Claude Code, Cursor ou Antigravity ? Le Skill `ingestion-albums-visuels` de votre espace `~/ankiforge_agentique` sait inspecter et structurer vos planches avant de les soumettre au **Garde-Fou & Validation** (<kbd>Alt+5</kbd>).
:::
