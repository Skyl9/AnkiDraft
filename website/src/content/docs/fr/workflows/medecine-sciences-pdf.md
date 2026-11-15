---
title: "Parcours Médecine & Sciences : PDF, Formules et Schémas"
description: "Guide pas-à-pas pour transformer un cours PDF dense de médecine ou de sciences en flashcards Anki atomiques avec formules KaTeX, schémas et MCP."
---

Ce parcours montre comment transformer un polycopié universitaire dense (médecine, droit, physique, mathématiques) en cartes courtes et précises, avec formules mathématiques et schémas annotés.

## 1. Importer le polycopié PDF avec extraction des figures et formules

1. Ouvrez **My Documents** (<kbd>Alt+7</kbd>) et cliquez sur **Importer un fichier** (ou glissez-déposez votre `.pdf`).
2. Choisissez la méthode adaptée :
   - **Extraction rapide** pour un PDF numérique propre sans formules complexes.
   - **Reconnaissance avancée (OCR Marker)** pour les scans, polycopiés à deux colonnes, tableaux et équations mathématiques.
3. AnkiDraft extrait automatiquement les schémas et figures dans votre bibliothèque média. Consultez [Importer des PDF](/fr/sources/import-pdf/) pour les réglages détaillés.

![Vue Documents d'AnkiDraft](assets/screen_documents.png)

## 2. Écarter les pages inutiles sans rien supprimer

Un polycopié de 200 pages contient souvent un avant-propos, un sommaire et une bibliographie qui fausseraient la génération et votre suivi d'avancement.

Dans le sélecteur de portée ([Cibler les chapitres](/fr/sources/scope-and-slices/)) :
- **Écarter** les annexes, remerciements et bibliographies : l'IA ignore ces pages, mais elles restent lisibles dans votre document.
- **Neutraliser** le sommaire ou les pages de garde : ils sont retirés du calcul de votre jauge de couverture pour refléter votre avancement réel.

## 3. Générer des cartes précises et éditer équations ou schémas

![Studio de Création d'AnkiDraft](assets/screen_creation.png)

1. Pour travailler sur un chapitre ou un extrait ciblé avec aperçu direct, ouvrez **Studio de Création** (<kbd>Alt+2</kbd>). Pour traiter plusieurs chapitres ou tout un polycopié à la chaîne, ouvrez **Batch Factory** (<kbd>Alt+6</kbd>) et cliquez sur **Composer le lot…** (<kbd>Ctrl+N</kbd>).
2. Choisissez un modèle adapté (*Basique*, *Texte à trous* ou *Image Occlusion*) et le paquet de destination (ex. `Médecine::Cardiologie`).
3. Dans **Édition & Navigateur** (<kbd>Alt+3</kbd>), vérifiez le rendu mathématique en direct et créez des textes à trous sur les mots-clés avec <kbd>Ctrl+Shift+C</kbd> (<kbd>Cmd+Shift+C</kbd> sur macOS) ou masquez les légendes d'un schéma ([Éditeur de Notes & KaTeX](/fr/cards/editeur_notes_katex/)).

![Éditeur de Notes et rendu KaTeX](assets/screen_edition.png)

## 4. Vérifier la clarté des cartes avant l'export

Ouvrez **Analyse & Audit IA** (<kbd>Alt+4</kbd>) pour lancer la [vérification de clarté](/fr/cards/linter_wozniak/) : toute carte trop longue ou qui mélange plusieurs notions à la fois est signalée pour être découpée en un clic, puis exportée via <kbd>Ctrl+Alt+E</kbd> ([Exporter un paquet .apkg](/fr/anki-sync/export-apkg/)).

## 5. Piloter ce parcours avec Claude ou Cursor (sans clé API)

Vous préférez préparer votre examen depuis Claude Desktop, Claude Code ou Cursor ? Activez la connexion locale dans **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) et utilisez ces exemples :

- **Nettoyer les pages inutiles avant génération** :
  - Outils utilisés : `get_document_outline`, `exclude_document_region`, `neutralize_document_region`.
  - Prompt type : *« Lis le plan du document #4, neutralise le sommaire et écarte la bibliographie, puis vérifie les chapitres restants. »*
- **Repérer les notions oubliées dans vos paquets et générer le complément** :
  - Outils utilisés : `diagnose_domain_knowledge_gaps`, `search_document`, `create_notes_batch`.
  - Prompt type : *« Lance `diagnose_domain_knowledge_gaps` sur le chapitre Potentiel d'Action de mon cours de Physiologie en croisant tous mes paquets, identifie les notions manquantes et crée des cartes courtes avec formules KaTeX `\( ... \)` soumises à ma validation. »*

> Toutes les propositions de Claude ou Cursor attendent obligatoirement votre clic sur **Appliquer** avant d'entrer dans votre collection.
