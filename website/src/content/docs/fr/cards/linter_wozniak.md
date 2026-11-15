---
title: Audit Qualité et les 20 Règles de Wozniak
description: Détectez et scindez les cartes trop longues, floues ou difficiles à mémoriser grâce au Linter des 20 règles de Wozniak pour mieux retenir durablement.
---

Une mauvaise flashcard (trop longue, contenant plusieurs questions à la fois ou dépourvue de contexte) finit par devenir une « sangsue » (*leech*) que vous oubliez sans cesse dans Anki.

AnkiDraft intègre un **Linter pédagogique** inspiré des **20 règles de formulation des connaissances de Piotr Wozniak** (créateur de SuperMemo).

## 1. Audit Wozniak dans Analyse & Audit IA (<kbd>Alt+4</kbd>)

Dans la vue **Analyse & Audit IA** (<kbd>Alt+4</kbd>) › onglet **Audit & Linter Wozniak**, sélectionnez un paquet puis lancez l'analyse (<kbd>Ctrl+Entrée</kbd>). AnkiDraft attribue un score sur 100 et regroupe les anomalies en **4 catégories** (dont les règles peuvent être activées ou ajustées via **Règles**) :
- **Atomicité & Restructuration** : réponses surchargées ou mélangeant plusieurs faits distincts.
- **Cloze & Univoque** : questions vagues ou textes à trous masquant trop d'éléments (avec un interrupteur dédié pour conserver ou convertir les Clozes).
- **Désambiguïsation & Contexte** : cartes trop proches qui créent des interférences mnésiques.
- **Formules & Clarté KaTeX** : expressions mathématiques ambiguës ou mal délimitées.

Un linter rapide est également accessible directement depuis **Édition & Navigateur** (<kbd>Alt+3</kbd>) sur une sélection de notes.

## 2. Scinder les cartes sangsues (Leeches) et fusionner les doublons

- **Scinder en cartes atomiques** : dans **Analyse & Audit IA** (<kbd>Alt+4</kbd>) › onglet **Jetons & SRS** › **Diagnostic des Cartes Sangsues (Leeches)**, repérez vos cartes à fort taux d'échecs et cliquez sur **Scinder** pour générer puis appliquer (avec aperçu *Two-Phase Commit*) leur découpage en 2 ou 3 cartes atomiques.
- **Détection & fusion des doublons** : l'onglet **Fusions & Doublons** (<kbd>Alt+4</kbd>, ainsi que le scan rapide depuis `Édition & Navigateur`) regroupe les quasi-doublons par similarité de Levenshtein afin de fusionner les notes redondantes sans perdre votre historique.
