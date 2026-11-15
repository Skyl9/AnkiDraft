---
title: Modèles de Cartes, Gabarits et Styles CSS
description: Personnalisez vos types de notes, gabarits HTML/Mustache, directives Rôle IA, préambules LaTeX et styles CSS pour Anki Desktop, AnkiWeb et Mobile.
---

La vue **Types de note** (<kbd>Alt+8</kbd>) permet de concevoir, styliser et partager des modèles de cartes 100 % compatibles avec l'écosystème Anki.

## 1. Modèle initial, Starter Pack et Image Occlusion

- **À la création d'un profil vierge** : AnkiDraft n'injecte volontairement qu'un unique modèle **`Basique`** (`Recto` / `Verso`) afin d'éviter tout conflit lors d'un premier import `.apkg`.
- **Starter Pack à la demande** : ouvrez le **Starter Pack** dans **Types de note** (<kbd>Alt+8</kbd>) pour installer **`Texte à trous (Cloze)`** (`{{cloze:Texte}}`) et d'autres modèles communautaires prêts à l'emploi.
- **`Image Occlusion Enhanced`** : créé automatiquement dès votre première session dans le [Masquage d'Images Intelligent](/fr/cards/image-occlusion/).

## 2. Gabarits HTML/Mustache, CSS, LaTeX et Snippets

Chaque type de note dispose de **4 sous-onglets** (*Style CSS*, *HTML Recto*, *HTML Verso*, et **LaTeX** pour les préambules/fins de compilation) accompagnés d'un aperçu en direct (bascule **mode clair / mode sombre** sur données d'exemple automatiques ou sur une note témoin réelle) :
- Utilisez la syntaxe **Mustache d'Anki** (`{{Recto}}`, `{{FrontSide}}`, `{{cloze:Texte}}`) et le panneau **Aides d'insertion** (champs, Cloze, classes CSS, structure).
- Piochez dans l'onglet **Snippets** (encadrés *Info*, *Attention*, *Erreur*, *Astuce*, *Théorème*, badges de difficulté/examen, grilles QCM, blocs de code, cadres KaTeX) avec détection automatique des conflits CSS.
- Renseignez le **Rôle IA** (ou le tableau guidé **Prompt pour l'IA**) pour indiquer aux agents comment remplir chaque champ lors de la génération.

## 3. Import, Export et Réconciliation intelligente

- Importez ou exportez vos modèles au format `.afmodel` / `.json` (<kbd>Ctrl+Alt+O</kbd> / <kbd>Ctrl+Alt+E</kbd>) ou importez un type de note depuis un autre profil AnkiDraft.
- Lors de l'import d'un paquet `.apkg`, AnkiDraft adopte ou réconcilie intelligemment les types de notes existants pour éviter de multiplier les doublons (`Basique-12345`).
