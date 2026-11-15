---
title: Masquage d'Images Intelligent (Image Occlusion IA)
description: Créez des flashcards Image Occlusion Enhanced sur vos schémas et planches avec tracé manuel, détection Vision IA et modes Hide All ou Hide One.
---

Le **Masquage d'Images Intelligent** (`Image Occlusion IA`) transforme vos schémas d'anatomie, cartes de géographie, organigrammes ou graphiques en flashcards visuelles au standard **`Image Occlusion Enhanced`**, sans quitter AnkiDraft.

## 1. Ouvrir une image dans l'atelier d'occlusion

Plusieurs points d'entrée directs alimentent l'atelier :
- Depuis **My Documents** (<kbd>Alt+7</kbd>) › onglet **Figures** d'un PDF importé : lancez l'occlusion en 1 clic sur n'importe quel schéma extrait.
- Depuis un **Album d'images** : ouvrez directement une planche numérisée dans l'outil d'occlusion ([Albums d'images](/fr/sources/albums-images/)).
- Depuis la fenêtre d'occlusion : utilisez **Changer d'image…** (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.svg`) ou **Coller l'image** directement depuis le presse-papier.

## 2. Masquage manuel ou détection par Vision IA

1. **Détecter avec l'IA** : cliquez sur ce bouton pour laisser un modèle compatible Vision repérer automatiquement toutes les légendes et annotations de votre image et pré-remplir le tableau **Masques & Légendes**.
2. **Tracé et ajustement manuel** : basculez entre l'outil **Mode Sélection / Déplacement** et **Mode Tracé** pour dessiner, redimensionner ou supprimer (<kbd>Suppr</kbd>) des rectangles de masquage.
3. Affinez si besoin les colonnes **`Texte / Réponse`** et **`Indice`** dans le panneau latéral droit, puis ajustez le zoom.

:::note[Prérequis Vision IA]
La détection automatique des légendes nécessite un moteur IA compatible **Vision** (API Gemini/OpenAI/Anthropic ou modèle multimodal local via Ollama) configuré dans **Paramètres** (<kbd>Ctrl+,</kbd>). Le tracé manuel des masques fonctionne intégralement hors-ligne sans aucune clé API.
:::

## 3. Modes d'occlusion et création des notes

Avant de générer vos notes dans le **Paquet cible** de votre choix (avec un titre d'en-tête et vos tags, ex. `image-occlusion`), choisissez la stratégie pédagogique adaptée :
- **`Masquer tout, révéler un (Hide All)`** : idéal quand les autres étiquettes du schéma risquent de vous souffler la réponse. Cochez **`Garder les autres masques fermés au verso`** pour éviter toute fuite d'indice contextuel lors de la vérification.
- **`Masquer un, révéler un (Hide One)`** : laisse le reste du schéma visible pour situer un élément précis dans son contexte global.

Au premier usage, AnkiDraft initialise automatiquement le modèle de note **`Image Occlusion Enhanced`** dans votre collection, compatible avec l'export `.apkg` vers Anki Desktop, AnkiWeb et AnkiMobile.
