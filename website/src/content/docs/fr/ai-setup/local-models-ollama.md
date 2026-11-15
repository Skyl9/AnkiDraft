---
title: Utiliser un Modèle Local Gratuit avec Ollama
description: Générez vos flashcards Anki 100 % hors-ligne et gratuitement sur votre ordinateur avec Ollama grâce à l'auto-détection locale, sans aucune clé API cloud.
---

Vous ne souhaitez pas utiliser d'API payante ou vous révisez des documents confidentiels sans connexion Internet ? AnkiDraft s'intègre nativement avec **Ollama**.

## 1. Installer Ollama en 2 minutes

1. Téléchargez et installez Ollama depuis [ollama.com](https://ollama.com).
2. Ouvrez votre terminal et téléchargez un modèle adapté à la mémoire vive (RAM) de votre ordinateur :
   - **8 Go de RAM** : `ollama pull llama3.2:3b` ou `ollama pull qwen2.5:3b`
   - **16 Go+ de RAM (ex. Apple Silicon M1/M2/M3/M4)** : `ollama pull qwen2.5:7b` ou `ollama pull mistral`

## 2. Connecter et scanner Ollama dans AnkiDraft

1. Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) › **Moteurs IA**.
2. Sous **SERVEURS LOCAUX & PASSERELLES D'ACCÈS**, repérez la ligne **Ollama Local :** (`http://localhost:11434` par défaut ; seules les URL locales/loopback sont acceptées par sécurité anti-SSRF).
3. Cliquez sur **Scanner les modèles** : AnkiDraft interroge Ollama (`/api/tags`), détecte automatiquement les capacités de chaque modèle (Vision, Thinking/CoT, JSON, fenêtre de contexte) et les importe dans votre catalogue avec l'indicateur **Modèle gratuit / inclus / local**.
4. Vous pouvez également ajouter manuellement un modèle via **Ajouter un modèle ▾** › **Presets rapides populaires** › **`Ollama Local (llama3)`** ou **Modèle personnalisé...** (pratique pour ajuster la **Limite Contexte**, activer **Vision multimodale** sur un modèle vision local ou ajuster la **Température**).

:::tip
Si votre ordinateur génère lentement sur CPU ou GPU modeste, augmentez le **Délai max. de génération** et le **Délai de requête par défaut** dans **Paramètres** (<kbd>Ctrl+,</kbd>) › **Moteurs IA** afin d'éviter un arrêt prématuré sur les longs chapitres.
:::
