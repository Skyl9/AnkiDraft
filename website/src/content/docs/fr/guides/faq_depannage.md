---
title: FAQ et Dépannage
description: Réponses aux questions fréquentes et solutions pas-à-pas pour l'installation d'AnkiDraft, Ollama, l'OCR PDF Marker et l'export vers Anki Desktop.
---

Retrouvez ici les réponses aux questions les plus fréquentes des utilisateurs d'AnkiDraft.

## 1. Questions générales

### AnkiDraft remplace-t-il Anki ?
Non : AnkiDraft et Anki sont complémentaires. **AnkiDraft** est l'atelier de création et d'audit de vos flashcards à partir de vos cours, tandis qu'**Anki** (Desktop, AnkiWeb, AnkiMobile, AnkiDroid) reste l'application dans laquelle vous effectuez vos révisions espacées quotidiennes.

### Puis-je utiliser AnkiDraft gratuitement et sans connexion internet ?
Oui. L'application est gratuite, fonctionne hors ligne, et vous pouvez utiliser des modèles d'IA locaux gratuits grâce à [Ollama](/fr/ai-setup/local-models-ollama/) sans aucune clé API payante.

### Mes cours PDF et mes cartes sont-ils envoyés dans le cloud ?
Non. Vos fichiers PDF, votre base SQLite et vos médias restent stockés localement sur votre ordinateur, isolés par profil (`~/.ankidraft/profiles/<nom_du_profil>/`). Si vous utilisez un fournisseur cloud (OpenAI, Gemini, Claude), seuls les passages sélectionnés pour une génération sont transmis directement à votre compte API.

## 2. Résolution des problèmes courants

### macOS affiche un avertissement à la première ouverture
Assurez-vous d'avoir glissé **AnkiDraft** dans votre dossier **Applications** depuis l'image `.dmg`. Les releases officielles macOS sont notarisées par Apple ; si vous testez une build *nightly* ou non signée et que macOS affiche une alerte Gatekeeper, faites un clic droit sur l'icône d'AnkiDraft > **Ouvrir** (ou autorisez l'application dans **Réglages Système > Confidentialité et sécurité**).

### Ollama n'est pas détecté ou aucun modèle local n'apparaît
Vérifiez qu'**Ollama** est démarré sur votre machine et écoute sur l'adresse locale par défaut (`http://localhost:11434` ; par sécurité anti-SSRF, seules les URL locales/loopback sont acceptées dans **Paramètres** (<kbd>Ctrl+,</kbd>) > **Moteurs IA** > **Ollama Local**). Assurez-vous également d'avoir déjà téléchargé un modèle via `ollama pull <modèle>` avant de cliquer sur le test de connexion.

### Mon PDF scanné reste vide ou les formules LaTeX sont mal extraites
L'extraction automatique rapide (PyMuPDF / pypdf) convient aux PDF numériques dont le texte est sélectionnable. Pour un polycopié scanné ou riche en formules complexes, cliquez sur le bouton **`Marker OCR`** dans la barre d'outils du document ([Import PDF & Documents](/fr/sources/import-pdf/)). Lors du premier lancement, AnkiDraft télécharge PyTorch et les modèles locaux (~5 Go d'espace disque et connexion Internet requis), puis tout fonctionne 100 % hors ligne.

### Comment exporter mes cartes vers Anki Desktop sans perdre mes révisions ?
Utilisez **Exporter des cartes Anki (.apkg)** (<kbd>Ctrl+Alt+E</kbd>) pour générer un paquet à ouvrir dans Anki : AnkiDraft n'altère jamais l'ordonnancement FSRS ou SM-2. Périodiquement, exportez votre collection complète (`.colpkg`) depuis Anki Desktop et réimportez-la dans AnkiDraft (<kbd>Ctrl+Shift+I</kbd>) pour actualiser vos statistiques et purger les cartes supprimées ([Cycle de Vie Distribué](/fr/guides/cycle_de_vie_distribue/)).

### Mes formules mathématiques ne s'affichent pas dans Anki
Vérifiez que vous utilisez bien les délimiteurs compatibles MathJax/KaTeX (`\( ... \)` pour une formule en ligne et `\[ ... \]` pour un bloc centré).

### Comment signaler un bug ou suggérer une amélioration ?
Dans AnkiDraft, ouvrez **Paramètres** (<kbd>Ctrl+,</kbd>) > **Aide & Guides** > **Signaler une idée ou un bug**, cliquez directement sur **Aide & Retours** en bas de la barre latérale, ou ouvrez un ticket sur le [dépôt GitHub officiel](https://github.com/Skyl9/AnkiDraft/issues).
