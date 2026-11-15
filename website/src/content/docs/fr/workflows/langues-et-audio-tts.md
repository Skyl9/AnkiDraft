---
title: "Parcours Langues & Audio : Vocabulaire et Prononciation TTS"
description: "Apprenez une langue avec AnkiDraft : générez des cartes de vocabulaire illustrées d'un audio naturel hors-ligne (Kokoro ou Piper) en Studio ou MCP."
---

Ce parcours montre comment créer des paquets de langues (anglais, japonais, espagnol, allemand, mandarin...) avec des exemples en contexte et une prononciation audio générée 100 % hors-ligne.

## 1. Préparer votre liste ou importer un support

Vous pouvez démarrer depuis trois types d'entrées :
- Un **document source** (fiche de grammaire, liste de vocabulaire, article ou sous-titres importés dans **My Documents**).
- Un **paquet Anki existant** importé via <kbd>Ctrl+Shift+I</kbd> ([Importer .apkg / .colpkg](/fr/anki-sync/import-colpkg/)).
- Une **saisie directe** dans **Édition & Navigateur** (<kbd>Alt+3</kbd>).

Pour mieux retenir, privilégiez toujours une **phrase d'exemple courte** sur le recto avec le mot ciblé plutôt qu'une traduction brute isolée.

## 2. Télécharger les modules vocaux puis ajouter la prononciation audio

Par défaut, pour garder l'installeur léger, les moteurs neuronaux hors-ligne (**Piper** et **Kokoro**) ne sont pas préinstallés : vous les téléchargez à la demande en quelques clics ([Synthèse Vocale TTS](/fr/cards/audio-tts/)).

### Étape A — Installer les voix hors-ligne (Piper ou Kokoro)

1. Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) › **Audio & TTS**.
2. Choisissez votre mode de fonctionnement :
   - **Piper TTS (recommandé hors-ligne)** : dépliez la section **MOTEUR LOCAL PIPER**, cliquez sur **Télécharger Piper CLI (1-Clic)**, puis dans **Voix additionnelles**, sélectionnez la voix de votre langue et cliquez sur **Télécharger**.
   - **Kokoro-82M (optionnel, haute fidélité hors-ligne)** : dépliez **MOTEUR LOCAL KOKORO-82M (OPTIONNEL)** et cliquez sur **Installer Kokoro (1-Clic)** (puis **Télécharger les modèles Kokoro** si demandé).
   - **Sans téléchargement préalable** : utilisez **Edge-TTS (Voix Neuronales Cloud Gratuit)** (nécessite Internet, sans clé API) ou le **Moteur Système OS** (voix natives de votre ordinateur).
3. Dans **Moteur de synthèse**, sélectionnez le moteur installé (**Piper TTS**, **Kokoro-82M**, **Edge-TTS** ou **Moteur Système OS**), choisissez la voix par défaut et cliquez sur **Tester la voix sélectionnée**.

:::note
Les modules téléchargés sont stockés localement dans le dossier outils d'AnkiDraft (`tools/tts/piper` et `tools/tts/kokoro`) : une fois installés, la génération audio fonctionne **100 % hors-ligne**.
:::

### Étape B — Générer l'audio sur vos cartes

1. **Sur une seule carte** : dans **Édition & Navigateur** (<kbd>Alt+3</kbd>), cliquez dans le champ de la phrase cible puis sur l'icône **TTS / haut-parleur** pour créer et écouter le fichier `[sound:tts_xxx.mp3]` immédiatement.
2. **Sur tout un paquet** : sélectionnez plusieurs notes dans le navigateur et lancez la **Génération TTS par lot** pour sonoriser toutes les cartes manquantes en arrière-plan.

![Navigateur et Éditeur de cartes AnkiDraft](assets/screen_edition.png)

## 3. Enrichir et corriger vos cartes avec Claude ou Cursor (sans clé API)

Un défaut fréquent dans les paquets de langues est de mélanger deux langues dans le même énoncé ou de coller des traductions mot à mot sans contexte. Votre assistant connecté en [mode sans clé API](/fr/workflows/zero-cle-api-agent-mcp/) peut nettoyer tout un paquet :

- **Sonoriser toutes les cartes sans audio d'un paquet** :
  - Outils utilisés : `get_cards_by_deck_or_tag`, `generate_card_audio`, `generate_cards_batch_audio`.
  - Prompt type : *« Liste les notes du paquet `Langues::Japonais` (avec `recursive=True`) qui n'ont pas encore de balise `[sound:...]` et lance `generate_cards_batch_audio` sur le champ Expression avec une voix japonaise. »*
- **Corriger les mélanges de langues et ajouter des phrases d'exemple** :
  - Outils utilisés : `diagnose_domain_knowledge_gaps`, `propose_card_refactor`.
  - Prompt type : *« Audite le paquet `Langues::Espagnol` avec `diagnose_domain_knowledge_gaps`, repère les cartes qui mélangent deux langues ou accumulent trop de synonymes, et propose via `propose_card_refactor` des cartes courtes avec une phrase naturelle. »*

## 4. Exporter avec vos fichiers audio

Appuyez sur <kbd>Ctrl+Alt+E</kbd> pour générer votre `.apkg` : AnkiDraft embarque automatiquement les fichiers audio sans doublons afin qu'ils fonctionnent immédiatement sur Anki Desktop, AnkiWeb et AnkiMobile.
