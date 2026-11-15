---
title: "Parcours Zéro Clé API : Piloter AnkiDraft avec Claude ou Cursor"
description: "Connectez Claude, Cursor ou Antigravity au serveur MCP local d'AnkiDraft, synchronisez votre workspace et validez chaque lot dans Garde-Fou sans clé API."
---

Vous avez déjà un abonnement **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf** ou **Antigravity (`agy`)** ? AnkiDraft intègre un serveur MCP local et un **espace de travail agentique** (`~/ankiforge_agentique`) qui vous permettent de créer des cartes, analyser vos cours et nettoyer vos paquets **sans aucune clé API payante**. Chaque modification attend votre validation manuelle avant d'être enregistrée.

![Validation humaine en deux temps dans AnkiDraft](assets/mcp_two_phase_commit.svg)

## 1. Activer le serveur local et le workspace agentique

1. Ouvrez **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) dans la barre latérale.
2. Dans **Supervision & Configuration**, vérifiez que le serveur est actif sur le port `8765` (sinon cliquez sur **Démarrer**), puis copiez la configuration JSON/CLI pour **Claude**, **Antigravity (agy)**, **Cursor** ou **cURL**.
3. Dans l'onglet **Guides & Workspaces**, vérifiez votre dossier agentique (`~/ankiforge_agentique` par défaut) avec **Vérifier le drift** (ou créez-le avec **Amorcer le workspace**).
4. Ouvrez ce dossier dans Claude Code, Cursor ou Antigravity : l'assistant lit `AGENT.md`, `.agents/active-profile.md` et `.agents/mcp-catalog.md` pour connaître votre profil actif et les **93 outils MCP** ([détails du serveur MCP & workspace](/fr/ai-setup/consultant_mcp/)).

![Supervision et configuration du Serveur MCP AnkiDraft](assets/screen_consultant.png)

## 2. Cinq demandes types avec vos outils MCP

Une fois le workspace ouvert, formulez simplement vos demandes en langage naturel : l'assistant sélectionne automatiquement les outils MCP adaptés et soumet les mutations au Garde-Fou :

### Cas A — Synchroniser le contexte et faire le bilan du profil
- **Outils MCP clés** : `sync_agent_workspace`, `audit_workspace_drift`, `list_decks`, `list_documents`, `get_flagged_cards`.
- **Demande** : *« Vérifie et synchronise le workspace avec mon profil AnkiDraft actif, puis fais-moi un bilan de mes paquets, cartes marquées d'un drapeau et documents importés. »*

### Cas B — Créer des cartes à partir d'un cours structuré
- **Outils MCP clés** : `get_document_outline`, `search_document`, `create_notes_batch`, `begin_staged_bundle`, `commit_staged_bundle`.
- **Demande** : *« À partir du chapitre sur la régulation glycémique dans mon document #3, prépare un lot de 12 cartes courtes en KaTeX dans le paquet `Biochimie::Métabolisme` et envoie le lot groupé au Garde-Fou. »*

### Cas C — Repérer les notions oubliées entre cours et paquet
- **Outil MCP clé** : `diagnose_domain_knowledge_gaps`.
- **Demande** : *« Lance `diagnose_domain_knowledge_gaps` sur mon cours d'Immunologie en croisant tous mes paquets, liste les notions manquantes ou non atomiques et propose les cartes pour combler les trous. »*

### Cas D — Moderniser vos modèles de cartes et votre CSS
- **Outils MCP clés** : outils de consultation et de proposition sur les types de notes (`Catalogue d'Outils` › *Types de notes*).
- **Demande** : *« Vérifie les champs du modèle `Médecine Cloze`, améliore la lisibilité des indices en mode sombre et soumets la mise à jour du gabarit à ma validation. »*

### Cas E — Nettoyer cartes ratées, doublons et tags
- **Outils MCP clés** : `get_flagged_cards`, `find_duplicate_cards`, `propose_card_split`, `propose_card_refactor`, `audit_tag_hygiene`.
- **Demande** : *« Récupère mes cartes marquées d'un drapeau rouge, découpe celles qui sont trop denses, repère les doublons et propose un lot prêt à relire. »* (Voir le guide [Sauvetage & Hygiène d'une collection Anki](/fr/workflows/sauvetage-et-hygiene-anki-mcp/)).

:::tip
Pour automatiser une chaîne récurrente sans rester devant l'écran ou combiner plusieurs étapes IA, votre assistant peut aussi déclencher vos [Pipelines DAG & RAG](/fr/cards/dag_et_rag/) via `list_pipelines` et `trigger_pipeline_run`.
:::

## 3. Relire et valider avant enregistrement

Aucune carte n'est modifiée sans votre accord :
1. Ouvrez l'onglet **Garde-Fou & Validation** dans **Serveur MCP & Agents** (<kbd>Alt+5</kbd>).
2. Vérifiez le comparatif **Avant / Après**, la justification de chaque proposition et l'impact des scissions ou suppressions (individuellement ou en **Staged Bundle**).
3. Cliquez sur **Appliquer** pour enregistrer dans AnkiDraft, ou sur **Rejeter la proposition** / **Tout rejeter** pour annuler proprement.
