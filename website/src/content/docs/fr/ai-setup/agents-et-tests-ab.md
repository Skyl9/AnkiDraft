---
title: Éditeur d'Agents (Alt+9) et Tests A/B
description: Créez et versionnez vos personas dans Éditeur d'Agents (Alt+9), personnalisez les prompts Jinja2 et comparez moteurs ou pipelines dans Tests A/B.
---

La section **Laboratoire IA** de la barre latérale réunit l'**Éditeur d'Agents** (<kbd>Alt+9</kbd>), les [Pipelines DAG](/fr/cards/dag_et_rag/) et le laboratoire **Tests A/B** pour adapter finement le comportement rédactionnel de l'IA à vos matières.

## 1. Configurer vos personas dans l'Éditeur d'Agents (<kbd>Alt+9</kbd>)

Ouvrez **Laboratoire IA › Éditeur d'Agents** (<kbd>Alt+9</kbd>) pour créer, organiser par dossiers et personnaliser vos agents :

- **Portée et format de sortie** :
  - **Portée / Usage** : `Pipeline de Forge (DAG)`, `Consultant IA (Serveur MCP)` ou `Universel (Forge & MCP)` (avec filtres rapides **Tous**, **Pipeline**, **MCP**, **Universel** dans l'arborescence).
  - **Format de sortie** : `json`, `cloze`, `markdown` ou `text`.
- **Moteur IA dédié (optionnel)** : assignez un modèle précis à l'agent (par ex. un modèle rapide ou compatible Vision), ou conservez l'héritage pour suivre automatiquement le **modèle IA global par défaut** défini dans **Paramètres** (<kbd>Ctrl+,</kbd>).
- **Instructions & Prompt Jinja2** :
  - Démarrez vite avec **Canevas...** (structures prêtes à l'emploi Cloze, Wozniak, Langues…).
  - Insérez au curseur les variables dynamiques (`{{ text_source }}`, `{{ last_output }}`, `{{ fields }}`, `{{ retrieved_chunks }}`, `{{ item }}`, `{{ initial_prompt }}`, `{{ state.variables.xxx }}`), consultez l'aide **Variables** et vérifiez le rendu réel avec **Aperçu**.
- **Outils & Presets par rôle** : cochez manuellement les outils accessibles à l'agent ou appliquez un preset (*Auditeur Wozniak*, *Architecte Modèles & CSS*, *Analyste SRS & Sangsues*, *Chercheur RAG & Documents*, *Administrateur BDD & Scripts*, *Consultant Universel (Tout)*).
- **Test unitaire & Historique des versions** :
  - Cliquez sur **Tester** (<kbd>Ctrl+Entrée</kbd>) pour exécuter l'agent seul sur un court extrait avant de l'intégrer dans un pipeline.
  - Utilisez **Historique** (Machine à Remonter le Temps) pour comparer les révisions successives de vos prompts via un diff visuel, et dupliquez un agent existant pour expérimenter sans risque.

## 2. Comparer deux approches dans Tests A/B

Ouvrez **Laboratoire IA › Tests A/B** pour trancher objectivement entre deux configurations sur un même document (ou extrait) et un même type de note cible :

- **3 modes de comparaison** :
  1. **Comparer deux Moteurs IA** (ex. `Gemini 3.5 Flash Lite` vs un modèle local Ollama ou OpenRouter gratuit).
  2. **Comparer deux Prompts / Personas** sur un moteur commun.
  3. **Comparer deux Pipelines DAG** complets.
- **Réglages d'inférence** : testez à paramètres identiques ou cochez **Réglages indépendants A/B** pour varier Température et Max Tokens entre la branche A et la branche B, puis lancez avec **Lancer le Test A/B** (<kbd>Ctrl+Entrée</kbd>).
- **4 vues comparatives côte à côte** :
  - **Rendu Visuel** (Recto/Verso interactif avec modes **Bureau 100%**, **Tablette 768px** et **Mobile 375px**, plus **Synchronisation Navigation A ↔ B**).
  - **Tableau des Champs** (inspection structurée champ par champ).
  - **JSON Brut** (sortie brute des modèles).
  - **Diff A↔B** (mise en évidence directe des écarts textuels), avec suivi du nombre de cartes, des tokens, de la latence et du coût USD estimé pour chaque branche.
