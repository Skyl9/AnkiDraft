---
title: "Parcours Cours Vidéo YouTube & Audio : Transcription et Cartes"
description: "Transformez un cours magistral vidéo YouTube ou un enregistrement audio en flashcards Anki structurées grâce à la transcription locale et à l'IA."
---

# Parcours Cours Vidéo YouTube & Audio : Transcription et Cartes

Les vidéos de cours (YouTube, conférences enregistrées) et les mémos audio de travaux dirigés sont denses en explications orales difficiles à ficher manuellement. Ce parcours explique comment les convertir en fiches structurées.

## 1. Importer une vidéo YouTube ou un fichier audio local

1. Ouvrez **My Documents** (<kbd>Alt+7</kbd>).
2. Selon votre support ([Importer Vidéo & Audio](/fr/sources/import-youtube-audio/)) :
   - **Vidéo YouTube** : cliquez sur **Importer depuis le Web** et collez l'URL de la vidéo. AnkiDraft récupère automatiquement les sous-titres officiels ou lance la transcription vocale locale.
   - **Enregistrement audio ou cours local** (`.mp3`, `.wav`, `.m4a`, `.mp4`, `.ogg`) : cliquez sur **Importer un fichier** ou glissez-déposez l'enregistrement. Le moteur local **Whisper** transcrit l'audio sans envoyer vos fichiers sur un serveur tiers.

![Vue Documents d'AnkiDraft](assets/screen_documents.png)

## 2. Transformer la transcription brute en chapitres lisibles

Une transcription orale brute contient souvent des hésitations, digressions ou phrases inachevées. Avant de générer vos cartes, structurez le texte :

- **Dans le Studio** : sélectionnez le document transcrit et lancez un [Pipeline de génération](/fr/cards/dag_et_rag/) comportant une étape amont de synthèse Markdown suivie de l'extraction de cartes.
- **Via Agent MCP** : demandez à Claude ou Cursor d'appeler `structure_transcript_for_ai` puis `structure_document_sections` pour transformer le monologue horodaté en sections thématiques claires, sans perdre les repères temporels.

## 3. Découper par séquences et générer vos flashcards

![Studio de Création d'AnkiDraft](assets/screen_creation.png)

1. Ouvrez **Studio de Création** (<kbd>Alt+2</kbd>) ou **Composer le lot…** (*Batch Slice Composer*) pour traiter chaque partie du cours une par une.
2. Ajustez le modèle (*Basique* ou *Texte à trous*) et la persona disciplinaire ([Génération IA](/fr/cards/ai-generation/)).
3. Relisez chaque carte dans la file **Staging** afin de vérifier l'exactitude des formules ou des notions dictées à l'oral.

## 4. Automatiser la synthèse et la génération via MCP

Si vous travaillez sans clé API avec Claude Code, Claude Desktop ou Cursor connecté sur le port `8765`, utilisez cet enchaînement en deux temps :

- **Outils MCP mobilisés** : `structure_transcript_for_ai`, `get_document_outline`, `create_notes_batch`, `begin_staged_bundle`, `commit_staged_bundle`.
- **Prompt type** : *« Prends la transcription brute du document #9, restructure-la avec `structure_transcript_for_ai` (profil didactique en français, horodatages conservés), puis extrais les définitions et mécanismes clés dans un lot `create_notes_batch` vers le paquet `Cours::Neurosciences` pour validation dans le Garde-Fou. »*
