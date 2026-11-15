---
title: Importer des PDF, Diaporamas et Ebooks
description: Extrayez proprement vos cours PDF, DOCX, PPTX et EPUB avec Marker OCR en préservant les schémas, tableaux et formules mathématiques LaTeX complexes.
---

La vue **My Documents** (<kbd>Alt+7</kbd>) d'AnkiDraft transforme vos supports de cours statiques en chapitres structurés prêts pour la création de flashcards.

## 1. Formats de fichiers pris en charge

Cliquez sur **Importer** ou glissez-déposez un ou plusieurs fichiers directement dans **My Documents** (import multiple avec barre de progression et bouton d'annulation) :
- **Documents PDF (`.pdf`)** : polycopiés de cours, articles scientifiques et livres, avec extraction des tableaux, images et formules mathématiques en syntaxe LaTeX.
- **Documents Word (`.docx`) et Présentations (`.pptx`)** : récupération des titres, listes à puces et notes de diapositives.
- **Livres numériques (`.epub`), Markdown / Texte (`.md`, `.txt`), Notebooks Jupyter (`.ipynb`) et code Python (`.py`)**.

:::tip
Vous avez plutôt des photos de tableau, de fiches manuscrites ou de planches ? Utilisez la vue dédiée [Albums d'Images & OCR Vision](/fr/sources/albums-images/).
:::

## 2. Extraction standard vs Marker OCR (PDF)

À l'import d'un PDF, AnkiDraft adopte automatiquement la meilleure méthode disponible sur votre ordinateur :
- **Extraction standard automatique** (**PyMuPDF** avec repli **pypdf**) : lancée immédiatement si Marker OCR n'est pas installé, idéale pour les PDF numériques dont le texte est déjà sélectionnable.
- **Marker OCR (Deep Learning & LaTeX)** : si vous importez un polycopié scanné, une mise en page multi-colonnes ou un cours riche en formules mathématiques, cliquez ensuite sur le bouton **`Marker OCR`** dans la barre d'outils du document pour relancer l'extraction haute fidélité.

:::note
Lors de la première utilisation de **Marker OCR**, AnkiDraft vous informe avant téléchargement : le moteur installe un environnement Python dédié avec PyTorch et ses modèles locaux, ce qui nécessite environ **5 Go d'espace disque disponible** et une connexion Internet active pour l'installation initiale (tout s'exécute ensuite 100 % hors-ligne).
:::

## 3. Lire, nettoyer et exploiter les schémas

Dans l'espace central de **My Documents**, vous disposez :
- De la bascule de vue **`PDF` / `MD` / `Logs`** (visualiseur PDF natif, éditeur Markdown/KaTeX et console d'extraction).
- Des outils **`Formater`** (correction des césures OCR, KaTeX, tables GFM) et **`Structurer IA`** (réorganisation d'un texte brut en plan clair).
- De l'onglet **Figures** dans l'Inspecteur droit : AnkiDraft filtre automatiquement les petites icônes décoratives et enregistre les vrais schémas et graphiques dans votre bibliothèque média pour les insérer dans une carte ou lancer directement une **occlusion d'image**.
