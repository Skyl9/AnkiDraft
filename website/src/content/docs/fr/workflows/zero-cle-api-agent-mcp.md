---
title: "Parcours Zéro Clé API : Piloter AnkiDraft avec Claude ou Cursor"
description: "Connectez Claude, Cursor ou Antigravity au serveur MCP d'AnkiDraft, chargez votre espace de Skills et validez vos cartes dans Garde-Fou sans clé API."
---

Vous avez déjà un abonnement **Claude Desktop**, **Claude Code**, **Cursor** ou **Antigravity** ? AnkiDraft intègre un connecteur local et un **espace de travail de Skills** qui vous permettent de créer des cartes, analyser vos cours et nettoyer vos paquets **sans aucune clé API payante**. Chaque modification attend votre validation manuelle avant d'être enregistrée.

![Validation humaine en deux temps dans AnkiDraft](assets/mcp_two_phase_commit.svg)

## 1. Activer le serveur local et l'espace de Skills

1. Ouvrez **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) dans la barre latérale.
2. Dans **Supervision & Configuration**, vérifiez que le serveur est **Actif** sur le port `8765` (sinon cliquez sur **Démarrer**), puis copiez la configuration JSON pour **Claude**, **Antigravity (agy)** ou **Cursor**.
3. Dans l'onglet **Guides & Workspaces**, vérifiez votre dossier agentique (`~/ankiforge_agentique` par défaut) avec **Vérifier le drift** (ou créez-le avec **Amorcer le workspace**).
4. Ouvrez ce dossier dans Claude Code, Cursor ou Antigravity : l'assistant détecte automatiquement votre profil actif et ses **Skills MCP dédiés** ([voir la liste complète des Skills](/fr/ai-setup/consultant_mcp/)).

![Supervision et configuration du Serveur MCP AnkiDraft](assets/screen_consultant.png)

## 2. Cinq demandes types qui déclenchent vos Skills

Une fois votre espace ouvert, parlez simplement à votre assistant en français — il charge lui-même le bon Skill et les bons outils MCP :

### Cas A — Synchroniser le contexte et faire le bilan du profil
- **Skills activés** : `synchronisation-ankiforge`, `exploration-collection`.
- **Demande** : *« Synchronise le workspace avec mon profil AnkiDraft actif et fais-moi un état des lieux 360° de mes paquets, cartes marquées d'un drapeau et documents importés. »*

### Cas B — Créer des cartes à partir d'un cours ou d'un scan OCR
- **Skills activés** : `generation-cours-markdown`, `ingestion-albums-visuels` (sauvegarde préalable, structuration Markdown, insertion groupée et prévisualisation).
- **Demande** : *« À partir du chapitre sur la régulation glycémique dans mon document #3, prépare un lot de 12 cartes courtes en KaTeX dans le paquet `Biochimie::Métabolisme`, vérifie leur rendu et envoie le lot au Garde-Fou. »*

### Cas C — Vérifier les notions oubliées entre cours et paquet
- **Skill activé** : `audit-couverture-rag` (et `diagnose_domain_knowledge_gaps`).
- **Demande** : *« Compare mon cours d'Immunologie avec mon paquet actuel tous sous-paquets confondus, liste les notions manquantes et propose les cartes pour combler les trous. »*

### Cas D — Moderniser vos modèles de cartes et votre mise en page CSS
- **Skills activés** : `audit-pertinence-modele`, `refacto-modeles`.
- **Demande** : *« Vérifie si tous les champs du modèle `Médecine Cloze` sont réellement utilisés, améliore la lisibilité des indices en mode sombre et soumets la refonte du gabarit à ma validation. »*

### Cas E — Nettoyer cartes ratées, doublons et tags
- **Skills activés** : `refactorisation-cartes`, `chasse-sangsues`, `deduplication-consolidation`, `hygiene-taxonomie-tags`.
- **Demande** : *« Récupère mes cartes marquées d'un drapeau rouge et mes sangsues récentes, découpe celles qui sont trop denses, fusionne les doublons évidents et propose un lot prêt à relire. »* (Voir le guide [Sauvetage & Hygiène d'une collection Anki](/fr/workflows/sauvetage-et-hygiene-anki-mcp/)).

:::tip
Pour automatiser une chaîne récurrente sans rester devant l'écran ou combiner plusieurs étapes IA, vous pouvez aussi demander à votre assistant de lancer vos [Pipelines DAG & RAG](/fr/cards/dag_et_rag/) (`list_pipelines`, `trigger_pipeline_run`).
:::

## 3. Relire et valider avant enregistrement

Aucune carte n'est modifiée sans votre accord :
1. Ouvrez l'onglet **Garde-Fou & Validation** dans **Serveur MCP & Agents** (<kbd>Alt+5</kbd>).
2. Vérifiez le comparatif **Avant / Après**, la justification de chaque proposition et l'impact des scissions ou suppressions.
3. Cliquez sur **Appliquer** pour enregistrer le lot dans AnkiDraft, ou sur **Rejeter** pour tout annuler proprement.
