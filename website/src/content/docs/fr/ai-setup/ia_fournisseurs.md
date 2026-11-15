---
title: Configurer vos Fournisseurs d'IA (OpenAI, Gemini, Claude)
description: Connectez vos clés API OpenAI, Anthropic, Gemini, Groq, OpenCode ou OpenRouter en toute sécurité et maîtrisez les plafonds de tokens IA et Consultant.
---

AnkiDraft est **agnostique vis-à-vis des fournisseurs** : vous choisissez librement le service d'IA adapté à votre budget ou basculez de modèle selon la tâche.

## 1. Fournisseurs et passerelles compatibles

Dans **Paramètres** (<kbd>Ctrl+,</kbd>) › **Moteurs IA**, vous pouvez configurer :

- **Clés API Cloud dédiées (`CLÉS API DES FOURNISSEURS CLOUD`)** :
  - **OpenAI** (`GPT-4o`, `GPT-4o-mini`, `o3-mini`, `o1`, `o1-mini`)
  - **Anthropic** (`Claude 3.7 Sonnet`, `Claude 3.5 Sonnet`, `Claude 3.5 Haiku`)
  - **Google Gemini** (`Gemini 3.5 Flash Lite`, `Gemini 2.0 Flash`, `Gemini 1.5 Pro`)
  - **Groq** (`Llama 3.3 70B`, `DeepSeek-R1 70B` sur matériel LPU)
  - **OpenCode** (`DeepSeek V4 Flash`, `Gemini 3.5 Flash Lite`, `GPT-5.4 Mini`, `Qwen 3.8 Flash`)
  - **OpenRouter** (modèles `:free` dont `Qwen 3.8 27B`, `Gemma 4 31B`, `Nemotron 3.5 Lightning`, plus des centaines de modèles payants)
- **Passerelles configurables (`SERVEURS LOCAUX & PASSERELLES D'ACCÈS`)** :
  - **Ollama Local** (`http://localhost:11434` par défaut) — voir [Utiliser un Modèle Local avec Ollama](/fr/ai-setup/local-models-ollama/)
  - **Passerelle OpenCode** (`https://opencode.ai/zen/v1` par défaut)
  - **API OpenRouter** (`https://openrouter.ai/api/v1` par défaut)
- **Modèles personnalisés (`Ajouter un modèle ▾` › `Modèle personnalisé...`)** : ajoutez n'importe quel identifiant de modèle ou fournisseur compatible OpenAI et ajustez sa **Limite Contexte**, son **Plafond Génération (max tokens)**, sa **Température par défaut** et ses capacités (**Vision multimodale**, **Raisonnement approfondi (Thinking / CoT)**, **Sorties structurées JSON**, **Modèle gratuit / inclus / local**).

## 2. Obtenir une clé API gratuite (spécial étudiants)

| Option gratuite | Carte bancaire | Comment obtenir la clé | Preset conseillé dans AnkiDraft | Limites à connaître |
| :--- | :--- | :--- | :--- | :--- |
| **Google AI Studio** | Non | Compte Google sur [aistudio.google.com](https://aistudio.google.com/) → *Create API key* (`AIzaSy...`) | `Google Gemini 3.5 Flash Lite` (vision + PDF) | Plafonds par minute/jour ; sur le palier gratuit, Google peut examiner les requêtes pour améliorer ses produits |
| **OpenRouter (`:free`)** | Non | Compte sur [openrouter.ai](https://openrouter.ai/) → *Keys* (`sk-or-...`) | `OpenRouter Gratuit (Qwen 3.8 27B)` | ~20 req/min et ~50 req/jour (ou 1 000/jour après un dépôt ponctuel de 10 $) |
| **Groq Console** | Non | Compte sur [console.groq.com](https://console.groq.com/) → *API Keys* (`gsk_...`) | `Llama 3.3 70B` / `DeepSeek-R1 70B` | Quotas serrés de tokens/minute sur les très longs chapitres |
| **GitHub / Campus / OpenCode** | Non | **GitHub Student Pack** (`models.github.ai`), passerelle **OpenCode** ou endpoint universitaire | **Modèle personnalisé…** / **Passerelle OpenCode** | Dépend de la vérification étudiante ou des quotas de votre passerelle |

**Activer votre clé en 30 secondes dans AnkiDraft :**
1. Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) › **Moteurs IA**, collez la clé face au fournisseur correspondant, puis cliquez sur **Tester**.
2. Sous le **CATALOGUE DES MOTEURS & MODÈLES**, cliquez sur **Ajouter un modèle ▾** › **Presets rapides populaires** (par ex. `Google Gemini 3.5 Flash Lite` ou `OpenRouter Gratuit (Qwen 3.8 27B)`), ou cliquez sur **Explorer le catalogue & comparateur...**.
3. Cochez **Modèle gratuit / inclus / local** dans les propriétés du modèle si vous souhaitez que le compteur de coûts de la barre supérieure reste à `$0.00`.

:::note
Pour des documents médicaux confidentiels ou pour travailler sans aucune limite de quota en période d'examens, préférez [Ollama en local](/fr/ai-setup/local-models-ollama/) ou votre assistant via [Serveur MCP (<kbd>Alt+5</kbd>)](/fr/workflows/zero-cle-api-agent-mcp/).
:::

## 3. Sécurité des clés API et du serveur MCP

- **Trousseau OS chiffré obligatoire** : vos clés API sont conservées dans le **trousseau sécurisé de votre système** (service `AnkiForge` : macOS Keychain, Gestionnaire d'identification Windows, Secret Service Linux). Si aucun trousseau système n'est disponible, la clé n'est jamais écrite en clair sur le disque.
- **Connexion directe sans intermédiaire** : aucune clé ne transite par un serveur tiers AnkiDraft ; votre ordinateur dialogue directement avec le fournisseur choisi.
- **Masquage automatique dans les logs** : le pipeline de journalisation filtre automatiquement les clés d'API (`sk-*`, `AIza*`) et jetons `Bearer` avant toute écriture disque.
- **Serveur MCP local (`SERVEUR MCP LOCAL`)** : depuis le même onglet **Moteurs IA**, activez ou désactivez le serveur en arrière-plan, choisissez le **Port d'écoute** (`8765` par défaut) sous **Avancé MCP & diagnostic**, régénérez le jeton Bearer 256 bits (**Renouveler le jeton**) et définissez l'onglet et la cible des demandes contextuelles.

## 4. Préférences IA globales, RAG & contrôle des plafonds

- **Modèle IA par défaut global** : sélectionnez le moteur utilisé lorsqu'un [Agent](/fr/ai-setup/agents-et-tests-ab/) ou une étape hérite du modèle global.
- **Bascules globales** : activez ou désactivez **Streaming des réponses**, **Capacités Vision activées**, **Validation automatique des cartes** et **Audit Linter automatique**.
- **Plafonds de tokens, réflexion & délais** :
  - Sous **Options avancées de génération & RAG** : réglez la **Température**, le **Plafond Max Tokens** (`4 096` à `128 000`, `16 384` par défaut), le **Budget Réflexion (CoT)** (`0` à `32 768` tokens), le **Délai max. de génération** par requête, ainsi que les réglages de recherche sémantique (**Chunks RAG (Top-K)** de `1` à `20` et **Seuil similarité min** de `40 %` à `95 %`).
  - Sous **PARAMÈTRES DE GÉNÉRATION PAR DÉFAUT** : ajustez la **Température par défaut** (`0.30`), le **Budget max tokens par défaut** (`4 000`) et le **Délai de requête par défaut** (`60 s`).
- **Protection budget du Consultant (`Budget Tokens Consultant` & `Budget Coût Consultant (USD)`)** : fixez un plafond dédié aux sessions du Consultant (jusqu'à `200 000 tokens` et `5.00 $`, défaut `50 000 tokens` / `0.50 $`), avec **arrêt préventif à 80 % du quota**.
- **Suivi des estimations et coûts** : lors de la sélection d'un document ou du découpage en tranches, AnkiDraft affiche une estimation du volume en tokens (`~X tokens`) ; les pipelines DAG acceptent un plafond par étape ; la vue **Tests A/B** estime le coût USD avant comparaison ; et le compteur de la barre supérieure suit le volume cumulé consommé.
