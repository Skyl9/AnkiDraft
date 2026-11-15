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

## 2. Générer la prononciation d'un champ en un clic

1. Dans **Édition & Navigateur** (<kbd>Alt+3</kbd>), placez votre curseur dans le champ contenant le mot ou la phrase à prononcer.
2. Cliquez sur l'icône **Synthèse vocale (TTS)** dans la barre d'outils.
3. Choisissez la langue et la voix naturelle souhaitée parmi les voix installées ou disponibles.
4. Le fichier audio est généré, normalisé et attaché automatiquement à votre carte sous la forme `[sound:fichier.mp3]` compatible avec Anki Desktop, AnkiWeb et AnkiMobile.

## 3. Génération audio en lot

Vous avez un paquet entier de vocabulaire sans audio ? Sélectionnez plusieurs cartes dans la table d'édition et lancez la **Génération TTS par lot** : AnkiDraft sonorise toutes les cartes sélectionnées en arrière-plan.
