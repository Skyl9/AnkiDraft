---
title: Exporter vos Paquets vers Anki (.apkg)
description: Générez un fichier .apkg propre et prêt à réviser pour Anki Desktop, AnkiWeb et AnkiMobile avec IDs stables et sans perdre votre historique.
---

Une fois vos cartes créées et relues dans AnkiDraft, vous pouvez les transférer vers Anki en quelques secondes grâce à l'export `.apkg`.

## 1. Exporter un paquet ou une sélection (.apkg)

1. Appuyez sur <kbd>Ctrl+Alt+E</kbd> (globalement, hors vue **Types de note**) ou cliquez sur **Exporter des cartes Anki (.apkg)** dans **Édition & Navigateur** (<kbd>Alt+3</kbd>).
2. Sélectionnez un paquet précis (et ses sous-paquets `Matière::Chapitre`) ou **Tous les paquets (Collection entière)**.
3. Choisissez la portée (**Toutes les cartes du paquet** ou **Nouvelles cartes uniquement (statut `new`)**) et laissez cochées selon votre besoin :
   - **Inclure tous les médias associés (images et sons)** ;
   - **Synchroniser drapeaux et suspensions sous forme de tags (`flag::couleur`, `is::suspended`)**.
4. Cliquez sur **Exporter le Paquet** pour générer l'archive `.apkg`.

:::tip[Drapeaux & cartes suspendues natifs dans Anki Desktop]
AnkiDraft exporte le GUID stable de chaque note ainsi que les drapeaux et suspensions natifs. Pour que Anki Desktop restaure ces états natifs lors de l'import, cochez **« Importer la planification »** côté Anki Desktop ; à défaut, les tags `flag::...` et `is::suspended` restent immédiatement filtrables.
:::

## 2. Mettre à jour dans Anki sans écraser votre FSRS / SM-2

AnkiDraft n'injecte **pas** d'historique ni d'ordonnancement FSRS / SM-2 dans le `.apkg`. Grâce à l'identifiant stable (**GUID**) conservé sur chaque note, réimporter un `.apkg` mis à jour dans Anki Desktop actualise le texte et les médias de vos cartes **tout en laissant intacts votre historique et vos intervalles FSRS/SM-2 déjà présents dans Anki**.

## 3. Export rapide multi-formats (JSON, JSONL, Texte, Markdown)

Depuis **Édition & Navigateur** (<kbd>Alt+3</kbd>), le bouton **Exporter en texte ou JSON (analyse rapide)** permet aussi d'exporter votre sélection, le filtre actif ou toute la collection vers **`.json`**, **`.jsonl`**, **`.txt` (TSV importable Anki)** ou **`.md`**, en fichier unique ou un fichier par carte (avec ou sans `id`, `guid` et `chunk_id`).
