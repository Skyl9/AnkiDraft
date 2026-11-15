---
title: Configurer vos Fournisseurs d'IA (OpenAI, Gemini, Claude)
description: Connectez vos clés API OpenAI, Anthropic ou Gemini en toute sécurité, configurez vos modèles locaux et maîtrisez votre budget de tokens IA global.
---

AnkiDraft est **agnostique du fournisseur d'IA** : vous êtes libre d'utiliser le service de votre choix ou d'alterner selon vos besoins.

## 1. Fournisseurs compatibles

Dans **Paramètres** (<kbd>Ctrl+,</kbd>) > **Moteurs IA**, vous pouvez configurer :
- **Google Gemini** (`Gemini 3.5 Flash Lite`, `Gemini 2.0 Flash`, `Gemini 1.5 Pro`)
- **OpenRouter** (modèles gratuits `:free` dont `Qwen 3.8 27B`, `Gemma 4 31B`, `Nemotron 3.5 Lightning`, et centaines de modèles)
- **Groq** (`Llama 3.3 70B`, `DeepSeek-R1 70B` sur puces LPU)
- **OpenAI** (`GPT-4o`, `GPT-4o-mini`, `o3-mini`) et **Anthropic Claude** (`Claude Sonnet`, `Claude Haiku`)
- **OpenCode** et **tout serveur compatible OpenAI** (Mistral, serveur universitaire local)
- **Ollama (100 % gratuit et hors ligne)** : voir le guide [Utiliser un Modèle Local avec Ollama](/fr/ai-setup/local-models-ollama/).

## 2. Obtenir une clé API gratuite (spécial étudiants)

| Source gratuite | Carte bancaire | Comment l'obtenir | Modèle conseillé dans AnkiDraft | Limites à connaître |
| :--- | :--- | :--- | :--- | :--- |
| **Google AI Studio** | Non | Compte Google sur [aistudio.google.com](https://aistudio.google.com/) → *Create API key* (`AIzaSy...`) | `Google Gemini 3.5 Flash Lite` (vision + PDF) | Quotas/min et /jour ; données utilisables par Google en palier gratuit |
| **OpenRouter (`:free`)** | Non | Compte sur [openrouter.ai](https://openrouter.ai/) → *Keys* (`sk-or-...`) | `OpenRouter Gratuit (Qwen 3.8 27B)` | ~20 req/min et ~50 req/jour (ou 1 000/j après 10 $ de crédit non expirant) |
| **Groq Console** | Non | Compte sur [console.groq.com](https://console.groq.com/) → *API Keys* (`gsk_...`) | `Llama 3.3 70B` / `DeepSeek-R1 70B` | Plafond de jetons/min strict sur les gros chapitres |
| **Mistral / GitHub / Campus** | Non | Palier gratuit [Mistral](https://console.mistral.ai/), **GitHub Student Pack** (`models.github.ai`), crédits **Google AI étudiants** ou passerelle fac | **Modèle personnalisé…** (URL OpenAI-compatible) | Dépend de la vérification étudiante ou des quotas campus |

**Comment l'activer en 30 secondes dans AnkiDraft :**
1. Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) > **Moteurs IA** et collez la clé face au fournisseur correspondant, puis cliquez sur **Tester**.
2. Dans la section des moteurs en dessous, cliquez sur **Ajouter un modèle** > **Presets rapides populaires** (ex. `Google Gemini 3.5 Flash Lite` ou `OpenRouter Gratuit (Qwen 3.8 27B)`), ou passez par **Explorer le catalogue & comparateur...**.
3. Vérifiez que la case **Modèle gratuit / inclus / local** est cochée : le compteur de coûts de la barre supérieure restera à `0.00 $`.

:::note
Pour des documents médicaux confidentiels ou pour travailler sans aucune limite de quota en période d'examens, préférez [Ollama en local](/fr/ai-setup/local-models-ollama/) ou votre assistant via [Serveur MCP (<kbd>Alt+5</kbd>)](/fr/workflows/zero-cle-api-agent-mcp/).
:::

## 3. Sécurité de vos clés API

- Vos clés API sont enregistrées dans le **trousseau sécurisé de votre système d'exploitation** (macOS Keychain, Windows Credential Manager, Secret Service Linux).
- Elles ne transitent par aucun serveur intermédiaire : AnkiDraft communique directement depuis votre ordinateur vers l'API du fournisseur sélectionné.
- Les journaux techniques masquent automatiquement toute clé (`sk-*`, `AIza*`).

## 4. Contrôle du budget

Avant de lancer une génération importante sur un livre entier, AnkiDraft estime le nombre de jetons (*tokens*) nécessaires et vous permet de fixer un plafond par exécution pour éviter toute surprise de facturation.
