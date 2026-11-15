---
title: Découvrir l'Interface
description: Tour d'horizon des espaces de travail d'AnkiDraft, des 4 dispositions d'écran (IDE, macOS, Dashboard, Glass) et des 12 thèmes visuels intégrés.
---

L'interface d'AnkiDraft est conçue pour rester claire et rapide, que vous travailliez sur un écran portable ou sur un grand moniteur.

## 1. Les espaces de travail principaux

La barre latérale regroupe **11 ateliers** organisés en 4 sections :

### Général
- **Tableau de bord** (<kbd>Alt+1</kbd>) : vue d'ensemble de vos paquets, de votre avancement documentaire et accès rapide aux dernières actions ([Import .apkg / .colpkg](/fr/anki-sync/import-colpkg/) · [Export .apkg](/fr/anki-sync/export-apkg/)).

### Forge & Outils
- **Studio de Création** (<kbd>Alt+2</kbd>) : génération interactive et ciblée sur un extrait de document ou une saisie libre (<kbd>Ctrl+N</kbd>), avec aperçu en direct et relecture carte par carte ([Génération IA](/fr/cards/ai-generation/)).
- **Édition & Navigateur** (<kbd>Alt+3</kbd>) : création manuelle, édition avec aperçu mathématique KaTeX en direct, textes à trous, TTS par champ et gestion de vos cartes ([Éditeur de notes & KaTeX](/fr/cards/editeur_notes_katex/)).
- **Analyse & Audit IA** (<kbd>Alt+4</kbd>) : détection des cartes trop longues, redondantes ou difficiles à mémoriser et suivi de couverture ([Linter Wozniak](/fr/cards/linter_wozniak/)).
- **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) : connexion d'agents externes (Claude Desktop, Cursor, Antigravity) à votre collection locale via MCP avec validation Garde-Fou ([Serveur MCP & Agents](/fr/ai-setup/consultant_mcp/)).
- **Batch Factory** (<kbd>Alt+6</kbd>) : usine de production par lots (file d'attente multi-chapitres via *Composer le lot…* avec <kbd>Ctrl+N</kbd>, reprise sur incident et validation Staging) ([Génération IA](/fr/cards/ai-generation/) · [Délimitation & tranches](/fr/sources/scope-and-slices/)).

### Bibliothèque
- **My Documents** (<kbd>Alt+7</kbd>) : bibliothèque de vos PDF, vidéos YouTube, enregistrements audio, pages web et albums d'images, avec indicateur de couverture par chapitre ([Hub multimodal](/fr/sources/hub_multimodal/)).
- **Types de note** (<kbd>Alt+8</kbd>) : personnalisation des modèles Recto/Verso, Cloze, gabarits Jinja2 et styles CSS ([Types de notes & gabarits](/fr/cards/note-types-and-templates/)).

### Laboratoire IA
- **Éditeur d'Agents** (<kbd>Alt+9</kbd>) : création, prompts Jinja2, outils autorisés et versionnage de vos personas ([Éditeur d'Agents & Tests A/B](/fr/ai-setup/agents-et-tests-ab/)).
- **Pipelines** : création et exécution de chaînes DAG multi-étapes couplées au RAG local ([Pipelines DAG & RAG](/fr/cards/dag_et_rag/)).
- **Tests A/B** : comparaison côte à côte de moteurs, prompts ou pipelines sur vos propres extraits ([Éditeur d'Agents & Tests A/B](/fr/ai-setup/agents-et-tests-ab/)).

## 2. Barre supérieure et pied de barre latérale

Dans la **barre supérieure** de la fenêtre :
- **Repli / dépli de la barre latérale** et **fil d'Ariane** de la vue active.
- **Rechercher / Palette de commandes (<kbd>Ctrl+K</kbd> ou <kbd>⌘K</kbd>)** : tapez quelques lettres pour changer de vue, lancer un [export `.apkg`](/fr/anki-sync/export-apkg/), ouvrir un guide ou modifier un réglage sans quitter le clavier ([Raccourcis clavier](/fr/guides/raccourcis_clavier/)).
- **Compteur de dépenses IA (`Dépenses : 0.00 $ (0 tk)`)** : suivi cumulé des coûts estimés et tokens consommés ([Fournisseurs IA & Budget](/fr/ai-setup/ia_fournisseurs/)).
- **Boutons d'accès rapide** : **Importer un paquet Anki** (<kbd>Ctrl+Shift+I</kbd>), **Exporter des cartes Anki** (<kbd>Ctrl+Alt+E</kbd>), **Notifications** (alertes et diagnostics) et pastille **`✨ Mise à jour`** lorsqu'une nouvelle version est prête.

Tout en bas de la **barre latérale gauche** :
- **Aide & Retours** : accès direct à la documentation, aux guides de dépannage ([FAQ & Dépannage](/fr/guides/faq_depannage/)) et au signalement de bugs.
- **Paramètres (<kbd>Ctrl+,</kbd>)** : configuration de l'apparence, des [Moteurs IA](/fr/ai-setup/ia_fournisseurs/), du serveur [MCP](/fr/ai-setup/consultant_mcp/), d'Anki, du TTS et des raccourcis.
- **Sélecteur de profil (`Profil : <nom>`)** et **indicateur d'état MCP** : basculez d'un espace de travail isolé à un autre en un clic ([Profils & Espaces de travail](/fr/getting-started/profiles-and-workspaces/)).

## 3. Personnaliser la disposition et le thème

Dans **Paramètres** (<kbd>Ctrl+,</kbd>) › **Général** :
- Choisissez parmi **4 dispositions d'interface** (*Concept IDE*, *Concept macOS*, *Concept Dashboard*, *Concept Glassmorphism*) via la grille de miniatures.
- Réglez indépendamment le **Mode d'Apparence** (*Mode Sombre*, *Mode Clair*, *Suivre le thème système*) et votre **Famille de Thèmes** parmi **12 familles bivalentes** (soit **24 thèmes** clairs et sombres intégrés, avec import/export JSON de thèmes tiers).
