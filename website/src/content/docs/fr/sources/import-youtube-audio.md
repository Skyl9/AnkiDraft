---
title: Importer des Vidéos YouTube et Cours Audio
description: Transformez une conférence YouTube, un podcast ou un enregistrement vocal en transcription horodatée et en flashcards Anki atomiques locales.
---

AnkiDraft vous permet de créer des flashcards directement à partir de cours vidéo en ligne ou d'enregistrements d'amphithéâtre.

## 1. Importer une vidéo YouTube

1. Ouvrez **My Documents** (<kbd>Alt+7</kbd>) et cliquez sur **Importer depuis le Web / YouTube**.
2. Collez le lien de la vidéo YouTube (`youtube.com/watch...` ou `youtu.be/...`).
3. Si la vidéo possède des sous-titres (manuels ou automatiques), AnkiDraft les récupère immédiatement et reconstitue un texte fluide découpé par thématiques avec ses repères temporels.
4. **Si la vidéo n'a aucun sous-titre**, AnkiDraft peut télécharger la piste audio via **`yt-dlp`** et la transcrire avec **Whisper** (voir prérequis ci-dessous).

## 2. Transcrire un fichier audio (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`…)

Vous avez enregistré un cours magistral ou un mémo vocal ?
1. Glissez votre fichier audio dans **My Documents** (formats acceptés : `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.wma`, `.webm`).
2. La transcription automatique découpe l'enregistrement en paragraphes horodatés, et un **lecteur audio intégré** s'affiche au-dessus de l'éditeur pour réécouter les passages.
3. Au besoin, cliquez sur **Structurer IA** pour transformer la retranscription brute en véritable plan de cours hiérarchisé avant de générer vos cartes.

:::note
**Prérequis pour la transcription vocale (audio ou YouTube sans sous-titres) :**
La récupération des sous-titres YouTube fonctionne sans outil externe. En revanche, pour transcrire un flux audio (fichier audio local ou vidéo sans sous-titres nécessitant `yt-dlp`), AnkiDraft utilise **soit** un binaire **Whisper local** installé sur votre poste (`whisper` ou `whisper-cli`), **soit** une clé API **OpenAI** ou **Groq** (même gratuite) renseignée dans **Paramètres (<kbd>Ctrl+,</kbd>) > Moteurs IA**.
:::
