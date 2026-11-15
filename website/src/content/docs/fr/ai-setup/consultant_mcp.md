---
title: Serveur MCP, Agents Externes et Workspaces
description: Connectez Claude, Cursor ou Antigravity au serveur MCP local d'AnkiDraft, synchronisez votre workspace ~/ankiforge_agentique et validez via Garde-Fou.
---

AnkiDraft intègre un **serveur MCP (Model Context Protocol)** local (`127.0.0.1:8765`, avec repli automatique sur un port libre si occupé) qui vous permet de piloter votre collection directement depuis **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf** ou **Antigravity (`agy`)**, sans aucune clé API supplémentaire.

Pour donner à votre assistant le contexte de votre profil actif et le catalogue des outils disponibles, AnkiDraft gère également un **espace de travail agentique** dédié (`~/ankiforge_agentique` par défaut).

## 1. Les 5 onglets de Serveur MCP & Agents (<kbd>Alt+5</kbd>)

La vue **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) centralise toute la connexion et le contrôle :

1. **Supervision & Configuration** : démarrer, arrêter, redémarrer ou tester (**Ping**) le serveur local (transports HTTP Streamable et SSE), renouveler le jeton **Bearer 256 bits** (**Renouveler le jeton**) et copier la configuration JSON/CLI prête à l'emploi pour **Claude**, **Antigravity (agy)**, **Cursor** ou **cURL**.
2. **Garde-Fou & Validation** : sas humain obligatoire en deux phases (*Two-Phase Commit*). Chaque proposition individuelle ou lot multi-étapes (**Staged Bundle** verrouillé jusqu'à finalisation `commit_staged_bundle`) attend votre validation explicite (**Appliquer**, **Rejeter la proposition**, **Tout rejeter**).
3. **Catalogue d'Outils** : inventaire interactif et filtrable par domaine des **93 outils MCP** exposés par le serveur local (consultation, création/édition de cartes, paquets, tags, types de notes, albums, pipelines, agents, documents/lacunes et audit de workspace).
4. **Activité** : journal en temps réel des appels d'outils exécutés par votre assistant externe et de leur statut.
5. **Guides & Workspaces** : gestion de votre workspace agentique local (`~/ankiforge_agentique` par défaut) avec matrice de conformité, inspecteur diff, **Vérifier le drift**, **Resynchroniser** et **Amorcer le workspace**.

## 2. L'espace de travail agentique (`~/ankiforge_agentique`)

Connecter le serveur MCP seul donne accès aux 93 outils bruts ; **initialiser puis ouvrir `~/ankiforge_agentique`** dans Claude Code, Cursor ou Antigravity fournit en plus à l'assistant le contexte du profil AnkiDraft actif, les garde-fous et le catalogue synchronisé :

- **Fichiers système générés à la racine** : `AGENT.md` (instructions maîtres), shims `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md` et `.gitignore`.
- **Contexte & conventions dans `.agents/`** :
  - `.agents/active-profile.md` : indique le profil AnkiDraft actif pour la session.
  - `.agents/mcp-catalog.md` : reflète la liste exacte des outils MCP disponibles sur votre serveur.
  - `.agents/glossary-and-internals.md` et `.agents/rules/ankiforge-conventions.md` : rappellent le fonctionnement interne et les garde-fous d'AnkiDraft.
- **Gabarits de skills synchronisés** : `.agents/skills/general/` (`ask-forge`, `audit-ankiforge`, `code-review`, `domain-modeling`, `doubt-driven-development`, `implement`, `peewee-expert`, `pipeline-dag-ia`, `proposer-commits`, `rag-smart-coverage`, `research`, `tdd`, `ui-pyside6-design`) et `.agents/skills/meta/` (`gouvernance-skills`, `session-retrospective`).

:::note
Lors d'une mise à jour via **Guides & Workspaces › Resynchroniser** (ou via l'outil MCP `sync_agent_workspace`), AnkiDraft effectue une synchronisation 3 voies non destructive des fichiers système et **préserve 100 %** de vos répertoires utilisateur sanctuarisés **`profiles/`** et **`_shared_models/`** ainsi que vos liens symboliques. L'audit (**Vérifier le drift** / `audit_workspace_drift`) est strictement en lecture seule.
:::

## 3. Le Garde-Fou : validation humaine en deux temps

Ni un agent externe connecté via MCP ni aucun outil ne peut modifier ou supprimer vos cartes sans votre accord :
1. L'assistant prépare ses modifications dans des patchs intermédiaires ou un **Staged Bundle** (lot séquentiel).
2. Dans **Serveur MCP & Agents** › **Garde-Fou & Validation**, vous inspectez le comparatif Avant / Après de chaque carte ajoutée, modifiée, scindée ou supprimée.
3. Cliquez sur **Appliquer** ou **Rejeter la proposition** : vous gardez un contrôle absolu sur votre collection.

## 4. Parcours pratiques étape par étape

- **[Parcours Zéro Clé API : Piloter AnkiDraft avec Claude ou Cursor](/fr/workflows/zero-cle-api-agent-mcp/)** : configuration rapide et exemples de demandes avec Claude, Cursor ou Antigravity.
- **[Parcours Sauvetage Anki : Doublons, Sangsues et Hygiène MCP](/fr/workflows/sauvetage-et-hygiene-anki-mcp/)** : nettoyer un paquet `.apkg` ou une collection `.colpkg` existante sans perdre votre historique.
