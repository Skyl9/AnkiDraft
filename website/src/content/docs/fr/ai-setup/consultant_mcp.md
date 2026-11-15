---
title: Serveur MCP, Agents Externes et Skills
description: "Connectez Claude, Cursor ou Antigravity à AnkiDraft via MCP, utilisez les Skills dédiés dans votre espace agentique et validez chaque lot via Garde-Fou."
---

AnkiDraft intègre un **serveur MCP (Model Context Protocol)** local (`127.0.0.1:8765`) qui vous permet de piloter votre collection directement depuis **Claude Desktop**, **Claude Code**, **Cursor**, **Antigravity** ou **Gemini CLI**, sans aucune clé API supplémentaire.

Pour rendre votre assistant immédiatement fiable sur Anki, AnkiDraft s'appuie sur un **espace de travail agentique dédié** (`~/ankiforge_agentique`) contenant des **Skills MCP prêts à l'emploi**.

## 1. Les 5 onglets de Serveur MCP & Agents (<kbd>Alt+5</kbd>)

La vue **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) centralise toute la connexion et le contrôle :

1. **Supervision & Configuration** : démarrez ou arrêtez le serveur local, régénérez le jeton d'accès et copiez en un clic la configuration pour **Claude**, **Antigravity (agy)**, **Cursor** ou **cURL**.
2. **Garde-Fou & Validation** : sas obligatoire de relecture humaine en deux temps où chaque création, retouche, scission ou suppression attend votre feu vert (**Appliquer** ou **Rejeter**).
3. **Catalogue d'Outils** : inventaire interactif des outils MCP exposés par le serveur local.
4. **Activité** : journal en direct des requêtes exécutées par votre assistant et de leur résultat.
5. **Guides & Workspaces** : gestionnaire de votre dossier agentique (`~/ankiforge_agentique` par défaut) avec matrice de conformité, détection de dérive (**Vérifier le drift**), mise à jour (**Resynchroniser**) et création initiale (**Amorcer le workspace**).

## 2. L'espace de travail agentique et vos Skills MCP

Connecter le serveur MCP seul donne accès aux outils bruts ; **ouvrir votre espace agentique (`~/ankiforge_agentique`)** dans Claude Code, Cursor ou Antigravity donne en plus à l'assistant une méthode complète, vos règles de profil et des **Skills spécialisés** dans `.agents/skills/` :

### Compétences générales (`.agents/skills/general/`)

| Objectif utilisateur | Skill activé | Rôle concret |
| :--- | :--- | :--- |
| **Démarrer une session** | `synchronisation-ankiforge` | Vérifie le profil actif, les outils MCP disponibles et rafraîchit les compteurs du profil |
| **Faire un bilan global** | `exploration-collection` | Dresse un panorama 360° des paquets, drapeaux et priorités de travail |
| **Contrôler la clarté** | `audit-qualite` | Repère les cartes trop longues, floues, redondantes ou multi-notions |
| **Vérifier un modèle de note** | `audit-pertinence-modele` | Mesure l'utilité réelle de chaque champ et détecte les modèles redondants |
| **Corriger les cartes ratées** | `chasse-sangsues` | Analyse les cartes *sangsues* (échecs répétés) et propose découpages ou indices |
| **Enrichir un paquet** | `amelioration-deck` | Propose des reformulations, corrections, indices et découpages en cartes courtes |
| **Traiter les drapeaux** | `refactorisation-cartes` | Récupère les cartes marquées d'un drapeau pendant vos révisions et prépare un lot de correction |
| **Nettoyer les gabarits** | `refacto-modeles` | Modernise la mise en page HTML/CSS et corrige les modèles de cartes défectueux |
| **Organiser les tags** | `hygiene-taxonomie-tags` | Repère et fusionne les variantes de tags proches ou incohérentes |
| **Fusionner les doublons** | `deduplication-consolidation` | Détecte les cartes en doublon et conserve celle ayant le meilleur historique Anki |
| **Repérer les oublis de cours** | `audit-couverture-rag` | Compare un document importé avec votre paquet pour créer les cartes manquantes |
| **Créer depuis un cours** | `generation-cours-markdown` | Structure un cours Markdown, sauvegarde la base et génère des cartes courtes avec prévisualisation |
| **Extraire un scan / album** | `ingestion-albums-visuels` | Exploite l'OCR des livres scannés et planches d'images pour produire des cartes reliées aux pages |

### Compétences métier partagées, profils et méta-skills

- **Règles par profil et modèles partagés (sanctuarisés)** : `.agents/profiles/<profil>/profile-context.md` décrit vos paquets et objectifs du profil actif, tandis que `.agents/rules/_shared_models/` et `.agents/skills/_shared_domain/` (par exemple `extraction-japonais`) conservent vos consignes par matière.
- **Amélioration continue (`meta/`)** : `evolution-skills` permet d'ajuster un skill après une session de travail, et `feedback-dev-ankiforge` recense d'éventuelles limites techniques rencontrées.

:::note
Lors d'une mise à jour via **Guides & Workspaces > Resynchroniser**, AnkiDraft actualise les guides système (`AGENT.md`, `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.agents/active-profile.md`, `.agents/mcp-catalog.md`) **sans jamais écraser** vos fichiers de profil (`profiles/`), vos règles de modèles (`_shared_models/`) ni vos skills personnalisés (`_shared_domain/`).
:::

## 3. Garde-fou de sécurité : validation humaine en deux temps

Ni un agent externe connecté via MCP ni aucun de ses skills ne peut modifier ou supprimer vos cartes sans votre accord :
1. L'assistant prépare ses propositions dans un **lot en attente (Staged Bundle)**.
2. Dans **Serveur MCP & Agents** > **Garde-Fou & Validation**, vous inspectez l'avant/après de chaque carte ajoutée, modifiée, scindée ou supprimée.
3. Vous cliquez sur **Appliquer** ou **Rejeter** : vous gardez toujours le contrôle absolu sur votre collection.

## 4. Passer à la pratique

- **[Parcours Zéro Clé API : Piloter AnkiDraft avec Claude ou Cursor](/fr/workflows/zero-cle-api-agent-mcp/)** : configuration rapide et exemples de demandes déclenchant les Skills.
- **[Parcours Sauvetage Anki : Doublons, Sangsues et Hygiène MCP](/fr/workflows/sauvetage-et-hygiene-anki-mcp/)** : nettoyer un paquet `.apkg` ou une collection `.colpkg` existante sans perdre votre historique.
