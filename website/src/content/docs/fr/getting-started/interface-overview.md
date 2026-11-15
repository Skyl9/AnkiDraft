---
title: Découvrir l'Interface
description: Tour d'horizon des espaces de travail d'AnkiDraft, des 4 dispositions d'écran (IDE, macOS, Dashboard, Glass) et des 12 thèmes visuels intégrés.
---

L'interface d'AnkiDraft est conçue pour rester claire et rapide, que vous travailliez sur un écran portable ou sur un grand moniteur.

## 1. Les espaces de travail principaux

La barre latérale regroupe **11 ateliers** organisés en 4 sections :

### Général
- **Tableau de bord** : vue d'ensemble de vos paquets, de votre avancement documentaire et accès rapide aux dernières actions ([Import .apkg / .colpkg](/fr/anki-sync/import-colpkg/) · [Export .apkg](/fr/anki-sync/export-apkg/)).

### Forge & Outils
- **Studio de Création** (<kbd>Alt+2</kbd>) : génération interactive et ciblée sur un extrait de document ou une saisie libre (<kbd>Ctrl+N</kbd>), avec aperçu en direct et relecture carte par carte ([Génération IA](/fr/cards/ai-generation/)).
- **Édition & Navigateur** : création manuelle, édition avec aperçu mathématique KaTeX en direct, textes à trous et gestion de vos cartes ([Éditeur de notes & KaTeX](/fr/cards/editeur_notes_katex/)).
- **Analyse & Audit IA** : détection des cartes trop longues, redondantes ou difficiles à mémoriser et suivi de couverture ([Linter Wozniak](/fr/cards/linter_wozniak/)).
- **Serveur MCP & Agents** : connexion d'agents externes (Claude Desktop, Cursor) à votre collection locale via MCP avec validation Garde-Fou ([Serveur MCP & Agents](/fr/ai-setup/consultant_mcp/)).
- **Batch Factory** (<kbd>Alt+6</kbd>) : usine de production par lots (file d'attente multi-chapitres via *Composer le lot…*, reprise sur incident et validation Staging) ([Génération IA](/fr/cards/ai-generation/) · [Délimitation & tranches](/fr/sources/scope-and-slices/)).

### Bibliothèque
- **My Documents** : bibliothèque de vos PDF, vidéos YouTube, enregistrements audio et pages web, avec indicateur de couverture par chapitre ([Hub multimodal](/fr/sources/hub_multimodal/)).
- **Types de note** : personnalisation des modèles Recto/Verso, Cloze, gabarits Jinja2 et styles CSS ([Types de notes & gabarits](/fr/cards/note-types-and-templates/)).

### Laboratoire IA
- **Éditeur d'Agents** : configuration et surcharge locale des prompts et personas IA ([Fournisseurs IA & Budget](/fr/ai-setup/ia_fournisseurs/) · [Modèles locaux Ollama](/fr/ai-setup/local-models-ollama/)).
- **Pipelines** : création et exécution de chaînes DAG multi-étapes couplées au RAG local ([Pipelines DAG & RAG](/fr/cards/dag_et_rag/)).
- **Tests A/B** : comparaison de prompts et de modèles IA côte à côte sur vos propres extraits de cours.

## 2. Barre supérieure et menus principaux

Directement accessibles en permanence depuis la barre supérieure de la fenêtre :

- **Sélecteur de profil** : basculez d'un espace de travail isolé à un autre en un clic ([Profils & Espaces de travail](/fr/getting-started/profiles-and-workspaces/)).
- **Compteur de dépenses IA (`0.00 $`)** : suivi en temps réel du coût cumulé de vos appels aux fournisseurs IA ([Fournisseurs IA & Budget](/fr/ai-setup/ia_fournisseurs/)).
- **Rechercher / Palette de commandes (<kbd>Ctrl+K</kbd>)** : tapez quelques lettres pour changer de vue, lancer un [export `.apkg`](/fr/anki-sync/export-apkg/), ouvrir un guide d'aide ou modifier un réglage sans quitter le clavier. Consultez aussi la [référence des raccourcis clavier](/fr/guides/raccourcis_clavier/).
- **Aide & Retours** : accès direct à la documentation, aux guides de dépannage ([FAQ & Dépannage](/fr/guides/faq_depannage/)) et au signalement de bugs.
- **Paramètres (<kbd>Ctrl+,</kbd>)** : configuration des fournisseurs IA, des modèles locaux [Ollama](/fr/ai-setup/local-models-ollama/), du serveur [MCP](/fr/ai-setup/consultant_mcp/) et de l'apparence.

## 3. Personnaliser la disposition et le thème

Dans **Paramètres** (<kbd>Ctrl+,</kbd>) > **Apparence** :
- Choisissez parmi **4 dispositions d'interface** (*IDE Studio*, *macOS Natif*, *Tableau de bord*, *Glassmorphism*) grâce aux miniatures d'aperçu.
- Sélectionnez votre thème parmi **12 palettes de couleurs** (claires et sombres) adaptées aux longues sessions de révision.
