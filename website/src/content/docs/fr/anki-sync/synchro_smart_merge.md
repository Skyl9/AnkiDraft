---
title: Synchronisation, Doublons et Fusion Intelligente (Smart Merge)
description: Résolvez les conflits lors d'un import Anki avec le Smart Merge, préservez votre historique de révision et éliminez les cartes en doublon facilement.
---

Lorsque vous travaillez à plusieurs sur un même paquet ou que vous modifiez une carte à la fois dans Anki et dans AnkiDraft, l'outil de **Fusion Intelligente (Smart Merge)** protège votre travail.

## 1. Déclenchement et fonctionnement de Smart Merge (3 panneaux)

Lors d'un import `.apkg` ou `.txt`, lorsqu'une note entrante partage le même **GUID** qu'une note locale :
- **Si aucune édition manuelle, fusion ou restauration locale n'a été faite sur la note** : l'archive entrante met à jour la note **silencieusement**, sans ouvrir de conflit.
- **Si le contenu diffère et que la note possède des éditions locales** : la fenêtre **Smart Merge** s'ouvre avec un badge de **Similarité (%)** et **3 colonnes** :
  1. À gauche (rouge, lecture seule) : **Base locale AnkiForge** ;
  2. Au centre (bleu, **éditable**) : **Résultat fusionné (interactif)**, avec boutons de transfert champ par champ (`◀` / `▶`) et indicateurs `Différent` / `Identique` ;
  3. À droite (vert, lecture seule) : **Base entrante (`.apkg`)**.

Raccourcis clavier dédiés dans Smart Merge : <kbd>Alt+Gauche</kbd> / <kbd>Alt+Droite</kbd> (conflit précédent / suivant), <kbd>Ctrl+Alt+Gauche</kbd> (**Tout garder Local**), <kbd>Ctrl+Alt+Droite</kbd> (**Tout remplacer par Entrant**) et <kbd>Ctrl+Entrée</kbd> (**Valider la fusion**).

## 2. Doublons, fusions et hygiène des médias

- **Fusions & Doublons** : depuis **Analyse & Audit IA** (<kbd>Alt+4</kbd>) › onglet **Fusions & Doublons**, le scan rapide de **Édition & Navigateur** (<kbd>Alt+3</kbd>) ou votre assistant connecté en [MCP](/fr/ai-setup/consultant_mcp/), repérez les doublons exacts et quasi-doublons (similarité de Levenshtein) pour fusionner sans perte.
- **Médias & stockage** : les médias importés sont dédupliqués par empreinte MD5 et décompressés depuis Zstandard si nécessaire ; vous pouvez purger les médias et le cache audio TTS orphelins dans **Paramètres** (<kbd>Ctrl+,</kbd>) › **Stockage**.
