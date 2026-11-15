---
title: Prise en Main Rapide
description: "Créez, vérifiez et exportez votre premier paquet de flashcards Anki en 5 minutes avec AnkiDraft et choisissez le parcours adapté à votre discipline."
---

Ce guide vous permet de produire votre premier paquet de flashcards Anki en quelques minutes et de choisir le parcours exact correspondant à votre matière et à votre équipement IA.

## Quel parcours choisir selon votre besoin ?

![Arbre de décision des parcours AnkiDraft](assets/arbre_decision_workflow.svg)

Choisissez directement le guide qui correspond à votre situation :

1. **[Cours écrits & Sciences : PDF, formules et schémas](/fr/workflows/medecine-sciences-pdf/)** — sélectionnez les chapitres utiles d'un polycopié, récupérez équations et schémas, puis vérifiez la clarté de vos cartes.
2. **[Langues & Prononciation : vocabulaire et audio hors-ligne](/fr/workflows/langues-et-audio-tts/)** — ajoutez une prononciation audio naturelle hors-ligne sur vos cartes de vocabulaire et corrigez les cartes floues.
3. **[Vidéo & Audio : cours YouTube et enregistrements](/fr/workflows/cours-video-youtube-audio/)** — transcrivez un cours filmé ou enregistré et transformez les passages clés en flashcards.
4. **[Nettoyage & Hygiène d'un paquet ou d'une collection Anki](/fr/workflows/sauvetage-et-hygiene-anki-mcp/)** — importez un paquet `.apkg` ou votre collection `.colpkg`, supprimez les doublons, simplifiez les cartes trop longues et ré-exportez sans perdre votre progression.
5. **[Combler les lacunes par rapport à un cours](/fr/cards/dag_et_rag/)** — reliez vos cartes existantes aux chapitres du cours pour repérer immédiatement les notions oubliées.

- **[Mode transversal — Travailler sans clé API avec Claude ou Cursor](/fr/workflows/zero-cle-api-agent-mcp/)** — applicable à tous les parcours ci-dessus si vous préférez piloter AnkiDraft depuis votre abonnement IA habituel.

## Deux façons de travailler avec l'IA

AnkiDraft fonctionne aussi bien de manière autonome qu'avec votre assistant IA habituel (Claude, Cursor).

| Critère | Studio intégré (dans l'application) | Avec votre assistant IA (Claude, Cursor) |
| :--- | :--- | :--- |
| **Ce qu'il vous faut** | Un modèle gratuit hors-ligne ([Ollama](/fr/ai-setup/local-models-ollama/)) ou une [clé API](/fr/ai-setup/ia_fournisseurs/) | Votre abonnement habituel (Claude Desktop/Code, Cursor) — **sans clé API** |
| **Comment ça marche** | Boutons guidés, sélection des chapitres et génération par lots | Vous discutez normalement avec votre assistant connecté à AnkiDraft |
| **Idéal pour** | Extraire des chapitres de PDF, ajouter de l'audio, éditer des formules | Repérer les oublis dans plusieurs paquets, nettoyer ou reformuler en série |
| **Votre contrôle** | Vous relisez chaque carte avant de l'enregistrer | **Validation obligatoire** : rien n'est modifié sans votre clic sur **Appliquer** |

## Démarrer en 4 étapes simples

### Étape 1 : Choisir ou créer votre profil

Au premier lancement, AnkiDraft ouvre le profil `default`. Pour éviter de mélanger vos cours volumineux et vos fiches personnelles, créez un profil séparé depuis le sélecteur en haut de l'écran ([Gérer vos profils](/fr/getting-started/profiles-and-workspaces/)).

### Étape 2 : Choisir votre moteur d'IA (optionnel)

Ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>), puis l'onglet **Moteurs IA** :
- **Gratuit et 100 % hors-ligne** : installez [Ollama](/fr/ai-setup/local-models-ollama/) sur votre ordinateur et choisissez un modèle local.
- **Avec une clé API** : renseignez votre clé OpenAI, Google Gemini ou Anthropic Claude (chiffrée sur votre appareil).
- **Sans clé API** : activez la connexion locale dans **Serveur MCP & Agents** (<kbd>Alt+5</kbd>) pour utiliser votre abonnement [Claude ou Cursor](/fr/workflows/zero-cle-api-agent-mcp/).

### Étape 3 : Importer votre premier cours

1. Ouvrez **My Documents** (<kbd>Alt+7</kbd>) dans la barre latérale.
2. Glissez-déposez un fichier PDF, Word, PowerPoint, EPUB, ou collez le lien d'une vidéo YouTube.
3. Pour un chapitre précis ou une saisie libre, passez dans **Studio de Création** (<kbd>Alt+2</kbd>) ; pour découper et traiter tout un livre par lots, ouvrez **Batch Factory** (<kbd>Alt+6</kbd>) › **Composer le lot…**.

### Étape 4 : Relire, améliorer et exporter vers Anki

Relisez les cartes proposées, lancez une vérification dans **Analyse & Audit IA** (<kbd>Alt+4</kbd>) pour repérer les cartes trop longues ou floues, puis appuyez sur <kbd>Ctrl+Alt+E</kbd> (**Exporter des cartes Anki (.apkg)**). Double-cliquez sur le fichier `.apkg` généré pour l'ajouter directement dans Anki.

> Pour des exemples concrets Avant / Après et la définition simple de chaque terme, consultez le [Glossaire Utilisateur](/fr/guides/glossaire/).
