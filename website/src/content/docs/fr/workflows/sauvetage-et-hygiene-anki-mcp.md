---
title: "Parcours Sauvetage Anki : Doublons, Sangsues et Hygiène MCP"
description: "Assainissez un paquet (.apkg) ou une collection Anki (.colpkg) : repérez doublons et sangsues, lancez une hygiène MCP et scindez vos cartes longues."
---

Vous révisez un vieux paquet Anki (le vôtre ou un paquet partagé) qui accumule des cartes impossibles à retenir, des doublons, des tags désordonnés ou de longs paragraphes ? Ce parcours vous permet de nettoyer un paquet isolé ou toute votre collection sans jamais perdre votre historique ni votre progression de révision dans Anki.

## 1. Importer votre paquet (`.apkg`) ou votre collection (`.colpkg`)

Choisissez le format adapté à ce que vous souhaitez analyser :

- **Option A — Un seul paquet ou un paquet partagé (`.apkg`)** : idéal pour auditer ou nettoyer **un paquet précis** (un deck téléchargé sur AnkiWeb, partagé par un camarade ou exporté individuellement depuis Anki Desktop via **Fichier > Exporter > Paquet d'Anki (`.apkg`)** — cochez *Inclure les informations de planification* si vous voulez aussi importer vos drapeaux et sangsues). L'import `.apkg` **fusionne ce paquet sans toucher aux autres paquets** déjà présents dans votre profil AnkiDraft.
- **Option B — Toute votre collection Anki (`.colpkg`)** : idéal pour nettoyer **tous vos paquets d'un coup** et refléter vos suppressions faites dans Anki : depuis Anki Desktop, exportez **Fichier > Exporter > Collection Anki (`.colpkg`)** en cochant l'inclusion des médias et de la planification. AnkiDraft crée automatiquement une sauvegarde de secours et garde vos documents de cours séparés de vos cartes Anki.

Dans AnkiDraft, appuyez sur <kbd>Ctrl+Shift+I</kbd> et glissez votre fichier `.apkg` ou `.colpkg` ([Importer .apkg ou .colpkg](/fr/anki-sync/import-colpkg/)).

## 2. Repérer les doublons et les cartes trop longues

1. Ouvrez **Analyse & Audit IA** (<kbd>Alt+4</kbd>).
2. Dans l'onglet **Audit & Linter Wozniak**, choisissez un paquet et cliquez sur **Lancer l'audit** : les cartes trop longues, floues ou qui testent plusieurs idées reçoivent des conseils précis ([Améliorer la clarté des cartes](/fr/cards/linter_wozniak/)).
3. Dans l'onglet **Fusions & Doublons**, repérez les cartes quasi-identiques et fusionnez-les proprement.

![Analyse et Linter Wozniak dans AnkiDraft](assets/screen_analysis.png)

## 3. Nettoyer tout un paquet avec Claude ou Cursor (sans clé API)

Pour traiter des centaines de cartes rapidement sur plusieurs paquets, connectez Claude, Cursor ou Antigravity dans **Serveur MCP & Agents** (<kbd>Alt+5</kbd>), ouvrez votre espace de travail (`~/ankiforge_agentique` depuis l'onglet **Guides & Workspaces**) afin de charger les **Skills de nettoyage**, et enchaînez ces quatre étapes :

### Étape A — Traiter les cartes marquées d'un drapeau pendant vos révisions
Pendant vos révisions dans Anki, marquez les cartes pénibles d'un drapeau (Rouge = à découper, Orange = à vérifier), puis réimportez votre `.apkg` (exporté avec la planification incluse) ou votre `.colpkg` dans AnkiDraft :
- **Skills activés** : `refactorisation-cartes`, `chasse-sangsues` (`get_flagged_cards`, `get_note_full_profile_360`, `set_card_flag`).
- **Demande** : *« Récupère toutes mes cartes marquées d'un drapeau rouge et mes sangsues récentes, analyse pourquoi je les rate et propose un découpage en cartes courtes pour chacune. »*

### Étape B — Repérer les notions oubliées et les doublons
- **Skills activés** : `audit-qualite`, `deduplication-consolidation`, `audit-couverture-rag` (`diagnose_domain_knowledge_gaps`, `find_duplicate_cards`).
- **Demande** : *« Analyse le thème Physiologie Rénale sur tous mes paquets : repère les cartes isolées qui parlent du sujet, les doublons à fusionner et les notions manquantes ou trop denses. »*

### Étape C — Nettoyer les tags et supprimer les cartes vides
- **Skill activé** : `hygiene-taxonomie-tags` (`audit_tag_hygiene`, `merge_tag_clusters`, `list_empty_cards`, `delete_empty_cards`).
- **Demande** : *« Audite la cohérence de mes tags, propose la fusion des variantes quasi-identiques et repère les éventuelles cartes au recto vide. »*

### Étape D — Découper et reformuler par lots avec validation
- **Skill activé** : `amelioration-deck` (`begin_staged_bundle`, `propose_card_split`, `propose_card_refactor`, `commit_staged_bundle`).
- **Demande** : *« Prépare un lot groupé pour scinder les 8 cartes dépassant 40 mots en 2 à 3 cartes courtes chacune et reformuler les énoncés flous avant validation. »*

![Supervision & Configuration du Serveur MCP et accès à l'onglet Garde-Fou & Validation](assets/screen_consultant.png)

## 4. Valider et ré-exporter sans perdre votre progression

1. Ouvrez **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) > **Garde-Fou & Validation** et vérifiez visuellement chaque modification Avant / Après.
2. Cliquez sur **Appliquer** pour enregistrer le lot dans AnkiDraft.
3. Exportez le paquet nettoyé via <kbd>Ctrl+Alt+E</kbd> (ou l'outil `export_deck_apkg`) puis importez le `.apkg` dans Anki : grâce aux identifiants stables et à la [fusion intelligente](/fr/anki-sync/synchro_smart_merge/), vos cartes sont mises à jour sans réinitialiser vos intervalles de révision.
