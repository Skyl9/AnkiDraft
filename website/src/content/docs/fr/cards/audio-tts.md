---
title: Synthèse Vocale (TTS) et Cartes Audio
description: Générez automatiquement une prononciation audio naturelle hors-ligne pour vos cartes de langues et terminologies avec les voix Kokoro ou Piper.
---

Pour l'apprentissage des langues étrangères, de la médecine ou de la musique, associer un extrait sonore à une flashcard renforce considérablement la mémorisation.

## 1. Installer les moteurs audio et voix hors-ligne

Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) › **Audio & TTS** avant votre première utilisation hors-ligne :

- **Piper TTS (local et rapide)** : dépliez **MOTEUR LOCAL PIPER**, cliquez sur **Télécharger Piper CLI (1-Clic)**, puis sélectionnez et téléchargez la ou les voix souhaitées dans **Voix additionnelles** (français, anglais, japonais, espagnol, allemand, etc.).
- **Kokoro-82M (optionnel, haute fidélité locale)** : dépliez **MOTEUR LOCAL KOKORO-82M (OPTIONNEL)** et cliquez sur **Installer Kokoro (1-Clic)** pour récupérer le runner local et ses modèles ONNX.
- **Options sans téléchargement** : **Edge-TTS** fonctionne directement via Internet (gratuit, sans clé API), et le **Moteur Système OS** utilise les voix déjà installées sur votre système.

Testez le rendu avec **Tester la voix sélectionnée** avant de lancer un traitement par lot.

## 2. Générer et écouter la prononciation d'un champ en un clic

1. Dans **Édition & Navigateur** (<kbd>Alt+3</kbd>), ouvrez une note et cliquez sur le bouton **Générer la prononciation audio (TTS)** (icône haut-parleur dans l'en-tête du champ concerné). Si vous avez surligné une portion de texte, seule la sélection est synthétisée ; sinon, tout le champ est lu (les balises Cloze `{{c1::mot}}` sont développées proprement avant synthèse).
2. Le fichier audio est généré avec le moteur et la voix configurés dans **Paramètres** (<kbd>Ctrl+,</kbd>) › **Audio & TTS**, mis en cache dans vos médias et attaché au champ sous la forme d'une balise Anki compatible avec Anki Desktop, AnkiWeb et AnkiMobile :
   - **Edge-TTS** : produit un fichier **`.mp3`** (`[sound:tts_xxx.mp3]`) ;
   - **Piper TTS** et **Kokoro-82M** : produisent un fichier **`.wav`** (`[sound:tts_xxx.wav]`) ;
   - **Moteur Système OS** : produit un fichier **`.wav`** (ou **`.m4a`** sous macOS).
3. Dès qu'une balise `[sound:...]` est présente dans un champ, un bouton **Lecture / Stop** apparaît dans son en-tête pour réécouter immédiatement l'extrait.

## 3. Génération audio en lot via un Pipeline DAG

Pour sonoriser automatiquement tout un lot de cartes lors de leur création, ajoutez une étape **`Génération Audio (TTS)`** (`AUDIO_TTS`) à la suite de votre pipeline dans **Pipelines** (voir [Pipelines de génération](/fr/cards/dag_et_rag/)). Vous pouvez y préciser le champ source, le champ cible (ajout en fin de champ ou remplacement), le moteur et la voix souhaités.
