---
title: Générer des Flashcards avec l'IA
description: Transformez automatiquement un chapitre de cours en flashcards Questions/Réponses ou textes à trous atomiques avec validation humaine stricte.
---

AnkiDraft vous aide à transformer rapidement un chapitre dense en flashcards atomiques, tout en vous laissant le dernier mot sur chaque carte grâce à la revue humaine.

## 1. Deux ateliers complémentaires : Studio de Création vs Batch Factory

AnkiDraft sépare clairement la création **ciblée** (un extrait, une saisie libre) de la production **par lots** (tout un livre découpé en tâches) :

### Option A — Studio de Création (<kbd>Alt+2</kbd>) : ciblé & interactif
Idéal pour travailler sur **un passage précis**, **une section** ou **une Nouvelle Saisie Libre** (<kbd>Ctrl+N</kbd>) :
1. Ouvrez **Studio de Création** (<kbd>Alt+2</kbd>).
2. Dans l'explorateur à gauche, sélectionnez un document/chapitre (avec sa portée) ou cliquez sur **Nouvelle saisie** (<kbd>Ctrl+N</kbd>).
3. Sous **Cibles Anki** et **Orchestration IA**, sélectionnez le paquet, le type de note, le **Moteur IA** et le **Pipeline d'Agents**, activez si besoin la carte **Vision Multimodale** (badge `ON`/`OFF` selon la compatibilité du moteur) et les **Paramètres Avancés** (*Température*, *Max Tokens*), puis appuyez sur <kbd>Ctrl+Entrée</kbd>.
4. Relisez les propositions avec l'aperçu en direct (<kbd>Espace</kbd> ou <kbd>V</kbd> pour valider, <kbd>Suppr</kbd>, <kbd>Retour</kbd> ou <kbd>R</kbd> pour rejeter, <kbd>E</kbd> pour éditer, <kbd>Alt+Gauche</kbd> / <kbd>Alt+Droite</kbd> pour naviguer, ou **Tout accepter** en 1 clic), puis enregistrez (<kbd>Ctrl+S</kbd>).

### Option B — Batch Factory (<kbd>Alt+6</kbd>) : usine de production par lots
Idéal pour traiter **plusieurs chapitres ou plusieurs documents** en file d'attente :
1. Ouvrez **Batch Factory** (<kbd>Alt+6</kbd>).
2. Cliquez sur **Composer le lot…** (<kbd>Ctrl+N</kbd>) pour découper vos documents ([Cibler les chapitres](/fr/sources/scope-and-slices/)) :
   - **Mode Direct** : chaque section cochée produit une tâche dédiée.
   - **Mode Automatique** : regroupe ou découpe les sections selon leur longueur.
3. Réglez vos cibles et options (**Vision (PDF)**, **Validation auto**, **Document complet par chunks**, *Paramètres Avancés*), puis lancez la file (<kbd>Ctrl+Entrée</kbd>). En cas d'incident sur une tranche, utilisez **Reprendre le Lot** sans tout relancer.
4. Contrôlez les cartes générées dans l'onglet **Revue** en bas de fenêtre (<kbd>Alt+Haut</kbd> / <kbd>Alt+Bas</kbd> pour changer de tranche) avant enregistrement.

## 2. Adapter le comportement de l'IA (Agents & Pipelines)

Le comportement rédactionnel de l'IA dépend du **Pipeline d'Agents** sélectionné dans le Studio ou Batch Factory et configuré dans **Éditeur d'Agents** (<kbd>Alt+9</kbd>). AnkiDraft embarque des modèles spécialisés prêts à cloner et ajuster :
- **Générateur Atomique Wozniak** et **Générateur Auto-Cloze** (textes à trous ciblés) ;
- **Spécialiste Médical & Anatomie** (mécanismes physiopathologiques, clinique, anatomie) ;
- **Formules Scientifiques & KaTeX** (dérivations et notations mathématiques) ;
- **Professeur de Langues & Vocabulaire** (exemples contextualisés, nuances, prononciation) ;
- **Droit, Normes & Jurisprudence** (notions clés, arrêts, distinctions conceptuelles).

:::tip[Directives par type de note]
Vous pouvez également renseigner un **Rôle IA** (ou un tableau sémantique via **Prompt pour l'IA**) directement sur un type de note dans **Types de note** (<kbd>Alt+8</kbd>) pour guider le remplissage exact de chaque champ.
:::

## 3. Revue humaine avant enregistrement (Staging)

Aucune carte générée par l'IA n'est ajoutée aveuglément à votre collection : toutes les propositions arrivent dans la file de revue (**Studio** ou onglet **Revue** du Batch Factory) où vous pouvez les valider, les modifier ou les rejeter avant l'enregistrement final (<kbd>Ctrl+S</kbd>).
