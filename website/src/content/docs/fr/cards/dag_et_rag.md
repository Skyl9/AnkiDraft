---
title: Pipelines de Génération et Couverture Intelligente
description: Automatisez la création de cartes par étapes avec les pipelines DAG et comblez les lacunes de vos cours grâce au RAG local et Smart Coverage.
---

Pour les cours volumineux, AnkiDraft combine l'éditeur de **Pipelines DAG** (workflows en graphe dirigé acyclique) et la **Couverture intelligente** (RAG local & Smart Coverage).

## 1. Enchaîner jusqu'à 6 types d'étapes dans un Pipeline DAG

Dans la vue **Pipelines**, chaque workflow combine des étapes réutilisables et inspectables avec garde-fou anti-cycles et branchements conditionnels (`↳ étape`) :
- **`RAG_RETRIEVAL` (Recherche RAG Vectorielle)** : extrait les passages pertinents d'un document indexé (`top_k`).
- **`LLM_PROMPT` (Agent IA)** : génère ou audite des cartes avec un agent (et possibilité de **surcharge locale de prompt** propre à cette étape sans modifier l'agent global).
- **`MAP_REDUCE` (Génération Parallèle par Lots)** : découpe et traite de longs contenus par tranches parallèles.
- **`HUMAN_VALIDATION` (Pause Copilote)** : interrompt le pipeline pour vous faire valider ou ajuster un plan intermédiaire avant de forger les cartes.
- **`PYTHON_TOOL` (Outil Python Déterministe)** : exécute un traitement sans LLM (ex. `clean_html_latex`, `validate_json_schema`, `deduplicate_cards_levenshtein`).
- **`AUDIO_TTS` (Génération Audio TTS)** : ajoute automatiquement la prononciation audio `[sound:...]` sur chaque carte générée.

Trois modèles prêts à l'emploi (*Pipeline Standard Cours*, *Pipeline Copilote avec Validation Humaine*, *Pipeline Haute Précision Map-Reduce & RAG*) sont proposés via **Modèles Prédéfinis…**, avec **simulation pas-à-pas** (<kbd>Ctrl+Entrée</kbd>) et import/export JSON ou inter-profils.

## 2. Détecter les chapitres oubliés (Smart Coverage)

Grâce à l'indexation sémantique locale de vos documents et aux liens de provenance (`NoteChunkLinkModel`), AnkiDraft compare vos cartes existantes à l'intégralité de votre cours :
- Dans **My Documents** (<kbd>Alt+7</kbd>) › onglet **Couverture** ou dans **Analyse & Audit IA** (<kbd>Alt+4</kbd>) › **Documents**, il met en évidence les sections orphelines sans aucune flashcard.
- Cliquez sur **Forger la section** (ou <kbd>Ctrl+Alt+F</kbd>) pour générer uniquement les cartes manquantes sur ces passages sans créer de doublons.
