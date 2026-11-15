---
title: Importer un Paquet (.apkg) ou une Collection (.colpkg)
description: Chargez vos paquets Anki .apkg ou .colpkg existants dans AnkiDraft pour les enrichir, auditer leur qualité et suivre votre couverture de cours.
---

Vous utilisez déjà Anki depuis des mois ou des années ? Vous pouvez importer vos cartes existantes dans AnkiDraft à tout moment.

## 1. Ouvrir l'assistant d'importation (<kbd>Ctrl+Shift+I</kbd>)

Appuyez sur <kbd>Ctrl+Shift+I</kbd> (ou cliquez sur **Importer un paquet Anki (.apkg)** dans **Édition & Navigateur**) et glissez votre fichier : AnkiDraft prend en charge les archives **`.apkg`**, **`.colpkg`** (y compris Anki 23.10+ compressé en **Zstandard** `collection.anki21b` / `media.zstd`) ainsi que les exports texte tabulés **`.txt`** (avec colonne `#guid`).

## 2. `.apkg` / `.txt` vs `.colpkg`

- **Paquet `.apkg` ou export `.txt` (ajout ou fusion ciblée)** : vous choisissez entre **Conserver la hiérarchie d'origine des paquets** ou **Fusionner dans le paquet** cible. Les notes inconnues sont créées et les notes modifiées localement déclenchent [Smart Merge](/fr/anki-sync/synchro_smart_merge/) en cas de conflit.
- **Archive `.colpkg` (`Remplacement intégral de la collection Anki`)** : remplace **atomiquement** tout le *Périmètre Anki* (paquets, notes, types de notes, cartes et statistiques) par l'archive entrante, tout en **sanctuarisant strictement** vos documents sources, fragments RAG, agents IA, personas et pipelines, et en créant **automatiquement une sauvegarde SQLite** avant remplacement.

:::note[Plafonds de sécurité anti-zip-bomb]
Par sécurité, l'import applique par défaut un plafond de décompression de **1 Gio** pour les archives `.apkg` et de **5 Gio** pour les collections `.colpkg`.
:::

Pour visualiser en détail l'articulation entre AnkiDraft et Anki, consultez le [Guide Visuel du Cycle de Vie Distribué](/fr/guides/cycle_de_vie_distribue/).
